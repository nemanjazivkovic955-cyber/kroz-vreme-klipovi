"""VIDEO INSPECTION & QC ENGINE — pregleda STVARNI renderovani MP4 (ne scenario, ne plan).

Upotreba:
  python3 studio/qc_inspect.py videos/tiktok_loops/m045.mp4 [--id m045] [--expect-silent]
  python3 studio/qc_inspect.py --review m045 review.json     # upis vizuelnog pregleda (vision model nad kadrovima)
  python3 studio/qc_inspect.py --status m045                  # stanje odobrenja

Šta meri (svaki frejm se dekodira; analiza na umanjenim frejmovima):
  1 metapodaci (rezolucija, odnos, fps, trajanje, kodek, broj audio/video zapisa)
  2 kontakt-listovi: vremensko uzorkovanje svakih 0.5 s + listovi oko SVAKOG reza (-2f, -1f, rez, +1f)
  3 rezovi i kadrovi (razlika frejmova + histogram), ključni kadar po kadru
  4 ponavljanje: dHash kadrova (bez trake teksta) unutar videa i prema SVIM ranije pregledanim videima
  5 kontinuitet na rezovima (skok osvetljenosti/boje), loop spoj kraj->početak
  6 crni frejmovi, zamrznuti delovi, preeksponirano, mutno (Laplacian), kratki "flash" kadrovi
  7 zvuk: glasnoća EBU R128, true peak, klipovanje, tišine; transkript (faster-whisper) vs scenario (WER)
  8 tekst/titlovi: trenuci smene teksta (zlatna maska u traci teksta) vs planirana mreža
  9 slabe scene + preporuke; odobrenje SAMO ako tehničke provere prođu + postoji vizuelni pregled + kreativna ocena >= 90
Izlaz: studio/inspections/<id>.json, <id>.md, <id>/sheet_*.jpg; indeks heševa studio/frame_hashes.json
"""
import os, sys, json, math, subprocess, difflib, re, datetime
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")  # preuzimanje preko LFS CDN-a (xet host nije dozvoljen)
import numpy as np
import cv2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INS = os.path.join(ROOT, "studio", "inspections"); os.makedirs(INS, exist_ok=True)
HASHES = os.path.join(ROOT, "studio", "frame_hashes.json")
sys.path[:0] = [os.path.join(ROOT, "motivacija"), os.path.join(ROOT, "the_price")]
FONT = cv2.FONT_HERSHEY_SIMPLEX


# ---------- pomoćno ----------
def probe(path):
    r = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                                  capture_output=True, text=True).stdout)
    v = [s for s in r["streams"] if s["codec_type"] == "video"]
    a = [s for s in r["streams"] if s["codec_type"] == "audio"]
    vs = v[0]; num, den = map(int, vs["avg_frame_rate"].split("/"))
    return {"width": vs["width"], "height": vs["height"], "fps": round(num / den, 3) if den else 0,
            "duration": round(float(r["format"]["duration"]), 3), "vcodec": vs["codec_name"], "pix_fmt": vs.get("pix_fmt"),
            "video_streams": len(v), "audio_streams": len(a), "acodec": a[0]["codec_name"] if a else None,
            "bitrate_kbps": round(int(r["format"].get("bit_rate", 0)) / 1000)}


def dhash(img, n=16):  # 256 bita - 64 bita davalo lažna poklapanja (gradijent nebo/tlo)
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    s = cv2.resize(g, (n + 1, n), interpolation=cv2.INTER_AREA)
    return int("".join("1" if b else "0" for b in (s[:, 1:] > s[:, :-1]).flatten()), 2)


def ham(a, b): return bin(a ^ b).count("1")


def no_band(img):  # ukloni traku teksta (25%-62% visine) da tekst ne utiče na poređenje slike
    h = img.shape[0]
    return np.vstack([img[: int(h * 0.25)], img[int(h * 0.62):]])


def gold_mask(img):  # zlatni tekst u traci
    h = img.shape[0]
    band = img[int(h * 0.25): int(h * 0.70)]
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 0] >= 12) & (hsv[..., 0] <= 32) & (hsv[..., 1] >= 110) & (hsv[..., 2] >= 150)) | ((hsv[..., 1] <= 40) & (hsv[..., 2] >= 225))
    # tekst ima oštre ivice (crni obrub) - zadrži samo zlatne piksele uz jaku ivicu, da zlatna pozadina (zalazak) ne smeta
    g = cv2.cvtColor(band, cv2.COLOR_BGR2GRAY)
    e = cv2.dilate((cv2.Canny(g, 80, 200) > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    return (m & e)


def expected_for(vid):
    """Scenario/plan iz izvora produkcije: tekstovi + planirana vremena smene + naracija."""
    try:
        from tiktok_loops_v2 import LOOPS_V2
        if vid in LOOPS_V2:
            t = [x.replace("*", "") for x in LOOPS_V2[vid]["texts"]]
            return {"texts": t, "text_changes": [2.0 * i for i in range(1, len(t))], "silent": True, "loop": True,
                    "kind": "tiktok_loop_v2"}
    except Exception:
        pass
    m_ = re.match(r"stoic_rule_(\d+)$", vid)
    if m_:
        sys.path.insert(0, os.path.join(ROOT, "stoic"))
        from rules import RULES
        r = RULES[int(m_.group(1))]
        return {"texts": [r["hook"]] + r["rule"] + [f"Follow for rule #{int(m_.group(1)) + 1}"],
                "text_changes": [2.0, 4.5, 7.0, 9.0], "silent": True, "loop": True, "kind": "stoic", "dur": (9, 11), "min_luma": 0.07}
    m_ = re.match(r"stoic_edit_(\d+)$", vid)
    if m_:
        return {"texts": [], "text_changes": [4.0], "silent": True, "loop": True, "kind": "stoic_edit", "dur": (7, 11),
                "min_luma": 0.07, "min_shot": 0.45}
    try:
        import talks
        k = vid.replace("talk_", "")
        if k in talks.TALKS:
            return {"narration": " ".join(s for s, _ in talks.TALKS[k]["script"]), "silent": False, "loop": False, "kind": "talk"}
    except Exception:
        pass
    return {"silent": None, "loop": False, "kind": "unknown"}


# ---------- glavna inspekcija ----------
def inspect(path, vid=None, expect_silent=None):
    vid = vid or os.path.splitext(os.path.basename(path))[0]
    out_dir = os.path.join(INS, vid); os.makedirs(out_dir, exist_ok=True)
    meta = probe(path); exp = expected_for(vid)
    if expect_silent is not None: exp["silent"] = expect_silent
    cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS) or meta["fps"]
    small, lum, sd, sharp, over, gm, hue, hist, full_keep = [], [], [], [], [], [], [], [], {}
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        sm = cv2.resize(fr, (180, 320), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        small.append(g.astype(np.float32)); lum.append(float(g.mean() / 255)); sd.append(float(g.std() / 255))
        over.append(float((g > 250).mean()))
        med = cv2.resize(fr, (540, 960), interpolation=cv2.INTER_AREA)
        sharp.append(float(cv2.Laplacian(cv2.cvtColor(no_band(med), cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()))
        gm.append(gold_mask(cv2.resize(fr, (360, 640), interpolation=cv2.INTER_AREA)))  # 360x640: tanka slova vidljiva
        hsv = cv2.cvtColor(no_band(sm), cv2.COLOR_BGR2HSV); hue.append(float(hsv[..., 0].mean()))
        hh = cv2.calcHist([hsv], [0, 1, 2], None, [12, 6, 6], [0, 180, 0, 256, 0, 256]); cv2.normalize(hh, hh); hist.append(hh)
        full_keep[i] = cv2.resize(fr, (270, 480), interpolation=cv2.INTER_AREA)
        i += 1
    cap.release()
    n = len(small); T = lambda k: round(k / fps, 3)
    diff = [0.0] + [float(np.abs(small[k] - small[k - 1]).mean()) for k in range(1, n)]
    # rezovi: razlika van trake teksta
    nb = [no_band(s) for s in small]
    dnb = [0.0] + [float(np.abs(nb[k] - nb[k - 1]).mean()) for k in range(1, n)]
    medd = float(np.median(dnb[1:])) if n > 1 else 0
    hc = [1.0] + [float(cv2.compareHist(hist[k - 1], hist[k], cv2.HISTCMP_CORREL)) for k in range(1, n)]
    # rez = velika promena slike I promena palete (timelapse svetla i munje menjaju sliku, ali ne celu paletu)
    cuts = [k for k in range(1, n) if (dnb[k] > max(18.0, 6 * medd) and hc[k] < 0.75) or (dnb[k] > max(10.0, 4 * medd) and hc[k] < 0.3)]  # 2. uslov: rez između dva tamna kadra
    # treperenje: >=4 "reza" u 1 s = nestabilna ekspozicija izvora (timelapse flicker), ne pravi rezovi
    flick = set()
    for k in cuts:
        grp = [c for c in cuts if 0 <= c - k <= fps]
        if len(grp) >= 4: flick.update(grp)
    flicker_ranges = []
    for k in sorted(flick):
        if flicker_ranges and k - flicker_ranges[-1][1] <= fps * 0.4: flicker_ranges[-1][1] = k
        else: flicker_ranges.append([k, k])
    cuts = [c for c in cuts if c not in flick]
    # munja/blic: 2 "reza" na <=0.2 s koji se vrate na istu sliku -> jedan dogadjaj, ne rez
    flashes = [c for c in cuts if any(0 < d - c <= fps * 0.2 for d in cuts)]
    for c in flashes:
        nxt = min(d for d in cuts if d > c)
        if ham(dhash(no_band(full_keep[max(0, c - 1)])), dhash(no_band(full_keep[min(n - 1, nxt)]))) <= 40:
            cuts = [x for x in cuts if x not in (c, nxt)]
    hard = list(cuts)
    L = int(fps / 3)
    d10 = [0.0] * n
    for k in range(L, n): d10[k] = float(np.abs(nb[k] - nb[k - L]).mean())
    m10 = float(np.median(d10[L:])) if n > L else 0
    for k in range(L, n - 1):
        w0, w1 = max(L, k - int(fps * 0.6)), min(n, k + int(fps * 0.6))
        if d10[k] > max(22.0, 4 * m10) and d10[k] == max(d10[w0:w1]) and cv2.compareHist(hist[k - L], hist[k], cv2.HISTCMP_CORREL) < 0.6 and all(abs(k - L // 2 - c) > fps * 0.6 for c in cuts):
            cuts.append(k - L // 2)  # sredina pretapanja
    cuts = sorted(set(cuts))
    dissolves = [c for c in cuts if c not in hard]
    bounds = [0] + cuts + [n]
    shots = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        mid = (a + b) // 2
        key = full_keep[mid]
        shots.append({"index": len(shots), "start": T(a), "end": T(b), "dur": round((b - a) / fps, 3),
                      "luma": round(float(np.mean(lum[a:b])), 3), "sharpness": round(float(np.median(sharp[a:b])), 1),
                      "overexposed_frac": round(float(np.mean(over[a:b])), 3), "hue": round(float(np.mean(hue[a:b])), 1),
                      "hash": dhash(no_band(key)), "key_frame": mid})
    issues = []
    def issue(sev, kind, t, msg): issues.append({"severity": sev, "type": kind, "t": t, "msg": msg})
    for a_, b_ in flicker_ranges:
        issue("major", "flicker", T(a_), f"treperenje osvetljenosti {T(a_)}-{T(b_)} s (nestabilan izvor) - zameniti kadar")
    # 1 tehnički
    tech = {"resolution_ok": (meta["width"], meta["height"]) == (1080, 1920),
            "aspect": f'{meta["width"]}:{meta["height"]}', "fps_ok": abs(meta["fps"] - 30) < 0.1,
            "duration_ok": (exp["dur"][0] <= meta["duration"] <= exp["dur"][1]) if exp.get("dur") else
                           (7 <= meta["duration"] <= 15 if exp["kind"] == "tiktok_loop_v2" else meta["duration"] > 0),
            "audio_rule_ok": (meta["audio_streams"] == 0) if exp.get("silent") else (meta["audio_streams"] >= 1 if exp.get("silent") is False else True),
            "frames_decoded": n, "frames_expected": int(round(meta["duration"] * meta["fps"]))}
    for k, v in tech.items():
        if k.endswith("_ok") and not v: issue("critical", "technical", 0, f"{k} = False ({meta})")
    if abs(n - tech["frames_expected"]) > 2: issue("major", "technical", 0, f"dekodirano {n} frejmova, očekivano {tech['frames_expected']}")
    # 2 crni / zamrznuti / preeksponirani / mutni / flash
    blk = [k for k in range(n) if lum[k] < 0.04 and sd[k] < 0.02]
    if blk: issue("critical", "black_frames", T(blk[0]), f"{len(blk)} crnih frejmova (prvi {T(blk[0])} s)")
    run = 0
    for k in range(1, n):
        run = run + 1 if diff[k] < 0.35 else 0
        if run == int(fps * 0.6): issue("major", "frozen", T(k - run), f"zamrznuta slika >= 0.6 s od {T(k - run)} s")
    for s in shots:
        if s["overexposed_frac"] > 0.35: issue("minor", "overexposed", s["start"], f"kadar {s['index']}: {s['overexposed_frac']:.0%} piksela izgoreno")
        if s["luma"] < exp.get("min_luma", 0.22): issue("major", "underexposed", s["start"], f"kadar {s['index']}: osvetljenost {s['luma']}")
        if s["sharpness"] < 25: issue("minor", "soft", s["start"], f"kadar {s['index']}: mutno (Laplacian {s['sharpness']})")
        if s["dur"] < exp.get("min_shot", 0.3) - 0.05: issue("major", "flash_shot", s["start"], f"kadar {s['index']} traje samo {s['dur']} s")
    # 3 ponavljanje unutar videa
    reps = []
    for x in range(len(shots)):
        for y in range(x + 1, len(shots)):
            d = ham(shots[x]["hash"], shots[y]["hash"])
            loop_pair = exp.get("loop") and x == 0 and y == len(shots) - 1
            if d <= 40 and not loop_pair:
                reps.append((x, y, d)); issue("major", "repeat_in_video", shots[y]["start"], f"kadar {y} skoro isti kao kadar {x} (dHash {d})")
    # 4 ponavljanje prema ranijim videima
    db = json.load(open(HASHES)) if os.path.exists(HASHES) else {}
    cross = []
    for other, hs in db.items():
        if other == vid: continue
        for s in shots:
            for h in hs:
                if ham(s["hash"], int(h)) <= 32:
                    cross.append({"shot": s["index"], "other": other}); break
    for c in cross: issue("major", "repeat_across_videos", shots[c["shot"]]["start"], f"kadar {c['shot']} skoro isti kao kadar u {c['other']}")
    db[vid] = [str(s["hash"]) for s in shots]; json.dump(db, open(HASHES, "w"), indent=0)
    # 5 kontinuitet na rezovima + loop spoj
    cont = []
    for c in cuts:
        a0, b0 = max(0, c - 3), min(n, c + 3)
        dl = abs(np.mean(lum[c:b0]) - np.mean(lum[a0:c])); dh = abs(np.mean(hue[c:b0]) - np.mean(hue[a0:c]))
        cont.append({"t": T(c), "luma_jump": round(float(dl), 3), "hue_jump": round(float(dh), 1)})
        if dl > 0.25: issue("minor", "continuity", T(c), f"nagli skok osvetljenosti na rezu ({dl:.2f})")
    seam = None
    if exp.get("loop") and n > 2:
        seam = round(float(np.abs(small[0] - small[-1]).mean()), 2)
        nbm = round(float(np.median(diff[1:])), 2)
        seam = {"seam_diff": seam, "median_neighbor_diff": nbm, "ok": seam <= max(4.0, 2.5 * nbm) or seam < 15}
        # tekst se menja na spoju (hook != kraj) pa meri i bez trake
        sb = round(float(np.abs(nb[0] - nb[-1]).mean()), 2); seam["seam_diff_no_text"] = sb
        seam["ok"] = sb <= max(6.0, 3 * nbm)
        if not seam["ok"]: issue("major", "loop_seam", meta["duration"], f"loop spoj vidljiv (bez teksta {sb} vs susedni {nbm})")
    # 6 smena teksta vs plan
    def _chg(a, b):
        u = (a | b).sum()
        gone = (a.sum() >= 8 and b.sum() < 0.3 * a.sum()) or (b.sum() >= 8 and a.sum() < 0.3 * b.sum())  # tanak tekst nestaje/pojavljuje se
        return (u >= 20 and (a ^ b).sum() / u > 0.45) or gone
    tc = [k for k in range(1, n) if _chg(gm[k], gm[k - 1])]
    # spoji bliske detekcije (animacija pop traje nekoliko frejmova)
    merged = []
    for k in tc:
        if not merged or k - merged[-1] > fps * 0.4: merged.append(k)
    text_times = [T(k) for k in merged]
    timing = {"detected": text_times}
    if exp.get("text_changes"):
        errs = []
        for e in exp["text_changes"]:
            raw_t = [T(k) for k in tc]
            near = min(raw_t, key=lambda x: abs(x - e)) if raw_t else None
            errs.append(None if near is None else round(near - e, 3))
            if near is None or abs(near - e) > 2.5 / fps:
                issue("major", "text_timing", e, f"smena teksta planirana u {e} s, detektovana {near}")
        timing.update({"expected": exp["text_changes"], "offset_s": errs,
                       "on_beat_120bpm": all(x is not None and abs(x) <= 2.5 / fps for x in errs)})
    # 7 zvuk
    audio = {"streams": meta["audio_streams"]}
    if meta["audio_streams"]:
        r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", path, "-af", "ebur128=peak=true,silencedetect=n=-45dB:d=0.8,astats",
                            "-f", "null", "-"], capture_output=True, text=True).stderr
        I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
        audio.update({"integrated_lufs": float(I[-1]) if I else None, "true_peak_dbfs": float(TP[-1]) if TP else None,
                      "silences": len(re.findall("silence_start", r))})
        if audio["true_peak_dbfs"] is not None and audio["true_peak_dbfs"] > -0.5: issue("major", "audio_clip", 0, f"true peak {audio['true_peak_dbfs']} dBFS (klipovanje)")
        if audio["integrated_lufs"] is not None and not (-18 <= audio["integrated_lufs"] <= -10): issue("minor", "audio_loudness", 0, f"glasnoća {audio['integrated_lufs']} LUFS (cilj -14)")
        if exp.get("narration"):
            audio.update(transcribe(path, exp["narration"]))
            ws = audio.get("words") or []
            starts = [ws[0]["t"]] + [ws[i]["t"] for i in range(1, len(ws)) if re.search(r"[.!?,]$", ws[i - 1]["w"])] if ws else []
            if starts and text_times:
                offs = [round(min(text_times, key=lambda x: abs(x - st)) - st, 2) for st in starts[1:]]
                bad = [(st, o) for st, o in zip(starts[1:], offs) if abs(o) > 0.5]
                timing["subtitle_vs_speech"] = {"sentence_starts": starts, "nearest_caption_change_offset_s": offs, "out_of_sync": bad}
                for st, o in bad: issue("minor", "subtitle_sync", st, f"rečenica počinje u {st} s, titl se menja {o:+} s od toga")
            for op, a_, b_ in audio.get("diff", []):
                issue("minor", "pronunciation", 0, f"scenario '{a_}' -> čuje se '{b_}'")
            if audio.get("wer") is not None and audio["wer"] > 0.15: issue("major", "narration_mismatch", 0, f"WER {audio['wer']} prema scenariju")
    else:
        audio["note"] = "bez zvučnog zapisa" + (" — po pravilu korisnika (muziku dodaje u TikTok-u)" if exp.get("silent") else "")
        if exp.get("silent") is False: issue("critical", "audio_missing", 0, "očekivan glas/muzika, a nema zvuka")
    # 8 kontakt-listovi
    sheets = make_sheets(full_keep, n, fps, cuts, out_dir, vid)
    rep = {"id": vid, "file": os.path.relpath(path, ROOT), "inspected_at": datetime.datetime.now().isoformat(timespec="seconds"),
           "method": "Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + "
                     "frejmovi oko svakog reza), NE gledanjem videa u pokretu.",
           "meta": meta, "expected": {k: v for k, v in exp.items() if k != "narration"}, "technical": tech,
           "shots": [{k: v for k, v in s.items() if k not in ("hash", "key_frame")} for s in shots],
           "cuts": [T(c) for c in cuts], "dissolves": [T(c) for c in dissolves], "continuity": cont, "loop_seam": seam, "text_timing": timing, "audio": audio,
           "repetition": {"in_video": reps, "across_videos": cross}, "issues": issues, "sheets": sheets}
    prev = os.path.join(INS, f"{vid}.json")
    if os.path.exists(prev):  # zadrži raniji vizuelni pregled samo ako je za ISTI fajl (isti broj kadrova i rezova)
        old = json.load(open(prev))
        if old.get("vision_review") and old.get("cuts") == rep["cuts"]: rep["vision_review"] = old["vision_review"]
        rep["history"] = old.get("history", []) + [{"at": old.get("inspected_at"), "approved": old.get("approval", {}).get("approved"),
                                                     "issues": len(old.get("issues", []))}]
    finalize(rep)
    return rep


def transcribe(path, script):
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel("base.en", device="cpu", compute_type="int8")
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                             capture_output=True).stdout  # sopstveno dekodiranje (PyAV verzija nije kompatibilna)
        segs, _ = m.transcribe(np.frombuffer(raw, np.float32), word_timestamps=True)
        segs = list(segs)
        txt = " ".join(s.text.strip() for s in segs)
    except Exception as e:
        return {"transcript": None, "wer": None, "transcribe_error": str(e)[:200]}
    norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower()).split()
    a, b = norm(script), norm(txt)
    sm = difflib.SequenceMatcher(None, a, b)
    errors = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
    words = [{"w": w.word.strip(), "t": round(w.start, 2)} for s_ in segs for w in (s_.words or [])]
    return {"transcript": txt, "wer": round(errors / max(1, len(a)), 3), "words": words,
            "diff": [(op, " ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"][:20]}


def label(img, s):
    img = img.copy(); cv2.rectangle(img, (0, 0), (img.shape[1], 24), (0, 0, 0), -1)
    cv2.putText(img, s, (4, 17), FONT, 0.5, (0, 215, 255), 1, cv2.LINE_AA); return img


def make_sheets(frames, n, fps, cuts, out_dir, vid):
    res = []
    idx = list(range(0, n, max(1, int(round(fps * 0.5))))) + [n - 1]
    tiles = [label(frames[k], f"{k / fps:.2f}s") for k in idx]
    cols = 8; rows = math.ceil(len(tiles) / cols); th, tw = tiles[0].shape[:2]
    sheet = np.zeros((rows * th, cols * tw, 3), np.uint8)
    for i, t in enumerate(tiles): sheet[(i // cols) * th:(i // cols + 1) * th, (i % cols) * tw:(i % cols + 1) * tw] = t
    p = os.path.join(out_dir, "sheet_time.jpg"); cv2.imwrite(p, sheet, [cv2.IMWRITE_JPEG_QUALITY, 82]); res.append(os.path.relpath(p, ROOT))
    if cuts:
        rows_ = []
        for c in cuts + ([n - 1] if True else []):
            ks = [max(0, c - 2), max(0, c - 1), c, min(n - 1, c + 1)] if c != n - 1 else [n - 2, n - 1, 0, 1]
            tag = "LOOP" if c == n - 1 else "REZ"
            rows_.append(np.hstack([label(cv2.resize(frames[k], (180, 320)), f"{tag} {k / fps:.2f}s") for k in ks]))
        # po 3 reza u redu
        per = 3; blank = np.zeros_like(rows_[0]); grid = []
        for i in range(0, len(rows_), per):
            chunk = rows_[i:i + per] + [blank] * (per - len(rows_[i:i + per]))
            grid.append(np.hstack(chunk))
        p = os.path.join(out_dir, "sheet_cuts.jpg"); cv2.imwrite(p, np.vstack(grid), [cv2.IMWRITE_JPEG_QUALITY, 82]); res.append(os.path.relpath(p, ROOT))
    return res


def finalize(rep):
    crit = [i for i in rep["issues"] if i["severity"] == "critical"]
    major = [i for i in rep["issues"] if i["severity"] == "major"]
    vr = rep.get("vision_review")
    vr_major = [s for s in (vr or {}).get("scenes", []) if s.get("verdict") == "weak"]
    score = (vr or {}).get("creative_score")
    rep["approval"] = {
        "technical_pass": not crit and not major,
        "vision_reviewed": bool(vr),
        "weak_scenes": len(vr_major),
        "creative_score": score,
        "approved": bool(not crit and not major and vr and not vr_major and score is not None and score >= 90),
    }
    a = rep["approval"]
    a["blocking"] = ([f"{len(crit)} kritičnih" ] if crit else []) + ([f"{len(major)} većih problema"] if major else []) + \
                    ([] if vr else ["nema vizuelnog pregleda"]) + ([f"{len(vr_major)} slabih scena"] if vr_major else []) + \
                    ([f"kreativna ocena {score} < 90"] if score is not None and score < 90 else [])
    json.dump(rep, open(os.path.join(INS, f"{rep['id']}.json"), "w"), indent=1, ensure_ascii=False)
    write_md(rep)
    print(f"{rep['id']}: {'ODOBRENO' if a['approved'] else 'NIJE ODOBRENO'} | tehnički {'OK' if a['technical_pass'] else 'PAD'} | "
          f"vizuelni pregled {'da' if a['vision_reviewed'] else 'NE'} | ocena {score} | {'; '.join(a['blocking'])}")
    for i in rep["issues"]: print(f"   [{i['severity']}] {i['type']} @{i['t']}s: {i['msg']}")


def write_md(rep):
    a = rep["approval"]; m = rep["meta"]
    L = [f"# Inspekcija {rep['id']} — {'ODOBRENO' if a['approved'] else 'NIJE ODOBRENO'}", "",
         f"Fajl: `{rep['file']}` · {rep['inspected_at']}", "", f"_Metod:_ {rep['method']}", "",
         "## Tehnički", f"{m['width']}x{m['height']} · {m['fps']} fps · {m['duration']} s · {m['vcodec']} · audio zapisa: {m['audio_streams']} · "
         f"dekodirano {rep['technical']['frames_decoded']}/{rep['technical']['frames_expected']} frejmova", "",
         "## Scene (merenja)", "| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |", "|---|---|---|---|---|---|"]
    vs = {s["index"]: s for s in (rep.get("vision_review") or {}).get("scenes", [])}
    for s in rep["shots"]:
        v = vs.get(s["index"], {})
        L.append(f"| {s['index']} | {s['start']}–{s['end']} | {s['luma']} | {s['sharpness']} | {v.get('verdict', '—')} | {v.get('note', '')} |")
    L += ["", "## Kontinuitet i loop", f"Rezovi: {rep['cuts']}", f"Loop spoj: {rep['loop_seam']}", "",
          "## Tekst / titlovi", f"{rep['text_timing']}", "", "## Zvuk", f"{rep['audio']}", "",
          "## Ponavljanje", f"{rep['repetition']}", "", "## Problemi"]
    L += [f"- [{i['severity']}] {i['type']} @{i['t']} s — {i['msg']}" for i in rep["issues"]] or ["- nema automatski otkrivenih"]
    vr = rep.get("vision_review")
    if vr:
        L += ["", f"## Vizuelni pregled ({vr.get('reviewer')})", vr.get("summary", ""), "", f"Storytelling: {vr.get('storytelling', '')}", "",
              f"Kreativna ocena: **{vr.get('creative_score')}** {vr.get('breakdown', '')}", "", "### Preporučene ispravke"]
        L += [f"- {r}" for r in vr.get("recommendations", [])]
    L += ["", "## Odobrenje", f"{a}", "", "Kontakt-listovi: " + ", ".join(f"`{s}`" for s in rep["sheets"])]
    open(os.path.join(INS, f"{rep['id']}.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--review":
        vid, f = args[1], args[2]
        rep = json.load(open(os.path.join(INS, f"{vid}.json")))
        rep["vision_review"] = json.load(open(f)); finalize(rep)
    elif args and args[0] == "--status":
        print(json.dumps(json.load(open(os.path.join(INS, f"{args[1]}.json")))["approval"], ensure_ascii=False))
    else:
        vid = None; es = None; files = []
        it = iter(args)
        for x in it:
            if x == "--id": vid = next(it)
            elif x == "--expect-silent": es = True
            else: files.append(x)
        for p in files: inspect(os.path.abspath(p), vid if len(files) == 1 else None, es)
