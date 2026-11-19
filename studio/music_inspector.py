"""MUZIČKI INSPEKTOR — bira muziku u skladu sa scenama i temom.

1. Scena: za svaki segment (t0, t1, tekst) meri sliku (osvetljenost, zasićenost, toplina, pokret) i
   raspoloženje teksta (rečnik: napetost, nada, mir, odlučnost, epika).
2. Muzika: besplatne Mixkit numere (studio/music_catalog.json, oznake raspoloženja sa mixkit.co).
   Prvo filter po oznakama, pa se TOP kandidati preuzmu i analiziraju (energija, svetlina zvuka, tempo, dinamika).
3. Izbor: ukupna ocena = poklapanje oznaka sa scenom + poklapanje zvučnih osobina + kazna za ponavljanje
   (studio/music_history.json) + kazna za glasnu/bubnjarsku numeru ispod naracije.
4. Isečak: bira se deo numere čija kriva energije najbolje prati krivu scene (bez tihog uvoda).
Izveštaj sa razlozima: studio/music_reports/<id>.md

Upotreba iz koda: choose(prod_id, segments, video=None, voice=True) -> dict
Ručno: python3 studio/music_inspector.py <video.mp4> [--voice]   (ceo video kao jedan segment)
"""
import os, sys, re, json, subprocess, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CAT = os.path.join(HERE, "music_catalog.json")
HIST = os.path.join(HERE, "music_history.json")
REPORTS = os.path.join(HERE, "music_reports")
CACHE = os.path.join(ROOT, "stoic", "music")  # mp3 (u .gitignore)
FEAT = os.path.join(HERE, "music_features.json")
URL = "https://assets.mixkit.co/music/{i}/{i}.mp3"
OFFGENRE = r"party|dance|club|trap|funk|disco|christmas|xmas|wedding|love|romantic|game|cheer|happy|fun|kids|cartoon|reggae|hip ?hop|type beat|floka|jazz|country|beach|summer|tropical|cat\b"

DIMS = ["energy", "tension", "hope", "calm", "drive"]
TAGV = {  # raspoloženje Mixkit oznake -> vektor (energija, napetost, nada, mir, odlučnost)
    "dark": (0.4, 0.9, 0.0, 0.2, 0.2), "dramatic": (0.7, 0.7, 0.2, 0.0, 0.5), "epic": (0.9, 0.5, 0.4, 0.0, 0.7),
    "melancholic": (0.2, 0.5, 0.2, 0.6, 0.0), "sad": (0.2, 0.6, 0.1, 0.5, 0.0), "hopeful": (0.4, 0.0, 0.9, 0.4, 0.3),
    "calm": (0.1, 0.0, 0.4, 0.9, 0.0), "determined": (0.7, 0.3, 0.4, 0.0, 0.9), "mysterious": (0.3, 0.7, 0.1, 0.4, 0.1),
    "emotional": (0.4, 0.4, 0.5, 0.3, 0.2), "atmospheric": (0.2, 0.4, 0.2, 0.7, 0.0), "meditative": (0.1, 0.1, 0.3, 1.0, 0.0),
    "motivating": (0.7, 0.1, 0.7, 0.0, 0.8), "heroic": (0.8, 0.3, 0.6, 0.0, 0.8), "majestic": (0.6, 0.2, 0.6, 0.2, 0.5),
    "lonely": (0.2, 0.6, 0.1, 0.6, 0.0), "inspiring": (0.6, 0.0, 0.8, 0.2, 0.6), "tense": (0.6, 0.9, 0.0, 0.0, 0.3),
}
LEX = {  # reči u tekstu -> dimenzija
    "tension": "storm broke broken hurt hurts anger angry furious fight fighting war die dies death afraid fear worst hard cold pain "
               "lose lost lying wasting stolen argue misunderstood grudges dark chain chains victim",
    "hope": "win wins ends sunrise free freeing freedom love forgive survive survived grow grows path peace fine helped happy "
            "obvious proof respond eventually",
    "calm": "silence silent quiet quietly calm wait simple little still patience let breathe sleep slowly",
    "drive": "discipline train trained training work muscle resistance step standing endure endurance control power decision "
             "shows show hard pushups build start rule strongest focus",
    "energy": "every day now today stop never most thousand empire",
}
LEXW = {d: set(w.split()) for d, w in LEX.items()}


def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, check=True, **kw)


# ---------- scena ----------
def text_mood(text):
    words = re.findall(r"[a-z']+", text.lower())
    v = np.zeros(len(DIMS))
    for w in words:
        for d, ws in LEXW.items():
            if w in ws: v[DIMS.index(d)] += 1
    return v / max(1.0, np.abs(v).sum()) if v.any() else v


def video_feats(video, t0, t1, fps=3):
    """Prosek po segmentu: osvetljenost, zasićenost, toplina (R-B), pokret (razlika frejmova)."""
    raw = _run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{t0:.2f}", "-t", f"{max(0.4, t1 - t0):.2f}", "-i", video,
                "-vf", f"fps={fps},scale=64:36", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 36, 64, 3).astype(np.float32) / 255
    if len(a) == 0: return dict(luma=0.3, sat=0.3, warm=0.0, motion=0.0)
    mx, mn = a.max(-1), a.min(-1)
    luma = (a @ np.array([0.299, 0.587, 0.114], np.float32)).mean()
    sat = ((mx - mn) / (mx + 1e-6)).mean()
    warm = (a[..., 0] - a[..., 2]).mean()
    motion = float(np.abs(np.diff(a, axis=0)).mean()) if len(a) > 1 else 0.0
    return dict(luma=float(luma), sat=float(sat), warm=float(warm), motion=motion)


def scene_vector(vf, text):
    """Ciljni vektor raspoloženja segmenta (slika 50% + tekst 50%)."""
    vis = np.array([
        min(1, vf["motion"] * 12 + vf["sat"] * 0.4),     # energija: pokret + zasićenost
        min(1, max(0, 0.55 - vf["luma"]) * 2.2),         # napetost: mrak
        min(1, max(0, vf["warm"]) * 6 + vf["luma"] * 0.5),  # nada: toplo, svetlo
        min(1, max(0, 0.05 - vf["motion"]) * 20),        # mir: statičan kadar
        min(1, vf["motion"] * 15),                        # odlučnost: pokret
    ])
    tm = text_mood(text)
    v = 0.5 * vis + 0.5 * (tm / (tm.max() + 1e-9) if tm.any() else vis)
    return v


# ---------- muzika ----------
def catalog():
    return json.load(open(CAT))


TAGMEAN = np.mean(list(TAGV.values()), 0)


def tag_vector(moods):
    vs = [TAGV[m] for m in moods if m in TAGV]
    return np.mean(vs, 0) if vs else TAGMEAN.copy()


def ccos(a, b):  # kosinus oko proseka -> razlikuje "tužno" od "herojsko" (bez centriranja sve je ~0.95)
    return cos(a - TAGMEAN, b - TAGMEAN)


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def fetch(i):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f"mixkit_{i}.mp3")
    if not os.path.exists(p):
        _run(["curl", "-sSfLo", p, URL.format(i=i)])
    return p


def audio_feats(i):
    feats = json.load(open(FEAT)) if os.path.exists(FEAT) else {}
    if str(i) in feats: return feats[str(i)]
    p = fetch(i); sr = 11025
    raw = _run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]).stdout
    x = np.frombuffer(raw, np.float32)
    hop = sr // 2  # 0.5 s
    fr = x[: len(x) // hop * hop].reshape(-1, hop)
    rms = np.sqrt((fr ** 2).mean(1) + 1e-12)
    spec = np.abs(np.fft.rfft(fr * np.hanning(hop), axis=1))
    freqs = np.fft.rfftfreq(hop, 1 / sr)
    cent = (spec * freqs).sum(1) / (spec.sum(1) + 1e-9)
    # tempo: autokorelacija anvelope udara (23 ms prozori)
    h2 = 256; f2 = x[: len(x) // h2 * h2].reshape(-1, h2)
    env = np.sqrt((f2 ** 2).mean(1)); on = np.maximum(0, np.diff(env))
    on = on - on.mean(); ac = np.correlate(on, on, "full")[len(on) - 1:]
    lags = np.arange(len(ac)) * h2 / sr; ok = (lags > 0.33) & (lags < 1.0)
    bpm = float(60 / lags[ok][np.argmax(ac[ok])]) if ok.any() else 0.0
    perc = float(np.percentile(on, 95) / (env.mean() + 1e-9))
    f = dict(dur=len(x) / sr, rms=rms.round(4).tolist(), loud=float(np.median(rms)), dyn=float(rms.std() / (rms.mean() + 1e-9)),
             bright=float(np.median(cent)), bpm=round(bpm, 1), perc=round(perc, 3))
    feats[str(i)] = f; json.dump(feats, open(FEAT, "w"))
    return f


def best_offset(f, need, target_curve):
    """Deo numere (korak 0.5 s) čija energija najbolje prati krivu scene; preskače tihi uvod i rep."""
    rms = np.array(f["rms"]); n = int(math.ceil(need / 0.5))
    if len(rms) <= n + 2: return 0.0, 0.0
    tc = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(target_curve)), target_curve)
    best = (-9, 0)
    for s in range(0, len(rms) - n):
        w = rms[s:s + n]
        if w[:4].mean() < 0.25 * np.median(rms): continue  # ne počinji u tišini
        c = np.corrcoef(w, tc)[0, 1] if tc.std() > 1e-6 and w.std() > 1e-6 else 0
        c += 0.15 * (w.mean() / (rms.max() + 1e-9))  # radije puniji deo
        if c > best[0]: best = (c, s)
    return best[1] * 0.5, float(best[0])


def choose(prod_id, segments, video=None, voice=True, top=8, avoid_last=6, exclude=(), record=True):
    """segments: [(t0, t1, text)]. Vraća izbor + piše izveštaj."""
    rows, curve = [], []
    for t0, t1, text in segments:
        vf = video_feats(video, t0, t1) if video else dict(luma=0.3, sat=0.3, warm=0.0, motion=0.02)
        sv = scene_vector(vf, text); rows.append((t0, t1, text, vf, sv)); curve.append(sv[0] * 0.6 + sv[4] * 0.4)
    durs = np.array([r[1] - r[0] for r in rows])
    target = (np.array([r[4] for r in rows]) * durs[:, None]).sum(0) / durs.sum()
    need = float(rows[-1][1] - rows[0][0])
    hist = json.load(open(HIST)) if os.path.exists(HIST) else []
    recent = {h["track"] for h in hist[-avoid_last:]}
    cands = []
    for t in catalog():
        if t["id"] in exclude: continue
        cands.append((ccos(target, tag_vector(t["moods"])) - (0.25 if t["id"] in recent else 0), t))
    cands.sort(key=lambda x: -x[0])
    scored = []
    for ts, t in cands[:top]:
        try:
            f = audio_feats(t["id"])
        except Exception as e:  # numera nedostupna
            continue
        if f["dur"] < min(need, 60) * 0.5: continue
        # zvučne osobine -> energija/svetlina; ispod glasa: kazna za glasne udaraljke
        aen = min(1, f["loud"] * 6 + f["perc"] * 0.05)
        a_match = 1 - abs(aen - target[0]) - 0.3 * abs(min(1, f["bright"] / 2500) - (0.3 + 0.4 * target[2]))
        pen = (0.15 * max(0, f["perc"] - 6) / 6 + 0.1 * max(0, aen - 0.7)) if voice else 0
        # žanr koji ne pristaje ozbiljnoj stoičkoj naraciji (po nazivu numere)
        if re.search(OFFGENRE, t["title"].lower()): pen += 0.25
        # prebrzo ispod glasa (miran govor ~120 BPM i sporije)
        if voice and f["bpm"] > 135: pen += 0.08 * min(1, (f["bpm"] - 135) / 30)
        # samo jedna oznaka raspoloženja = slabiji dokaz
        if len(t["moods"]) == 1: pen += 0.04
        off, fit = best_offset(f, need, np.array(curve))
        score = 0.55 * (ts + 1) / 2 + 0.30 * a_match + 0.15 * fit - pen
        scored.append(dict(id=t["id"], title=t["title"], moods=t["moods"], tag=round(ts, 3), audio=round(a_match, 3),
                           fit=round(fit, 3), pen=round(pen, 3), score=round(score, 3), offset=off, bpm=f["bpm"], dur=round(f["dur"], 1)))
    if not scored: return None
    scored.sort(key=lambda x: -x["score"])
    pick = scored[0]; pick["path"] = fetch(pick["id"]); pick["target"] = dict(zip(DIMS, np.round(target, 2).tolist()))
    # izveštaj
    os.makedirs(REPORTS, exist_ok=True)
    L = [f"# Muzika za {prod_id}", "", f"Cilj (energija, napetost, nada, mir, odlučnost): {pick['target']}", "",
         "| segment | osvetlj. | toplina | pokret | tekst |", "|---|---|---|---|---|"]
    for t0, t1, text, vf, sv in rows:
        L.append(f"| {t0:.1f}-{t1:.1f}s | {vf['luma']:.2f} | {vf['warm']:+.2f} | {vf['motion']:.3f} | {text[:60]} |")
    L += ["", "| # | numera | oznake | tagovi | zvuk | prati scenu | kazna | ukupno | BPM | od |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, s in enumerate(scored[:6], 1):
        L.append(f"| {k} | {s['title']} (mixkit {s['id']}) | {', '.join(s['moods'])} | {s['tag']} | {s['audio']} | {s['fit']} | {s['pen']} | **{s['score']}** | {s['bpm']} | {s['offset']:.1f}s |")
    L += ["", f"**Izbor: {pick['title']} (mixkit {pick['id']}), od {pick['offset']:.1f} s.** Licenca: Mixkit Free License (besplatno, i za monetizovane videe)."]
    open(os.path.join(REPORTS, f"{prod_id}.md"), "w").write("\n".join(L) + "\n")
    if record:
        hist.append({"prod": prod_id, "track": pick["id"], "title": pick["title"]}); json.dump(hist, open(HIST, "w"), indent=1)
    pick["all"] = scored
    return pick


def cut(pick, out_wav, dur, fade_in=0.4, fade_out=1.2, offset=None):
    off = pick["offset"] if offset is None else offset
    _run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{off:.2f}", "-t", f"{dur:.3f}", "-i", pick["path"],
          "-af", f"afade=t=in:d={fade_in},afade=t=out:st={max(0, dur - fade_out):.2f}:d={fade_out}", "-ar", "44100", "-ac", "2", out_wav])


if __name__ == "__main__":
    v = sys.argv[1]
    d = float(_run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v]).stdout)
    print(json.dumps(choose(os.path.basename(v), [(0, d, "")], v, voice="--voice" in sys.argv), indent=1))
