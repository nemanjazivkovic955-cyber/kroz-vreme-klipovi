"""STOIC RULES — dugi YouTube video (16:9) sa naracijom, titlovima i muzikom.
Ulaz: stoic/long_epNN.py (SECTIONS: kartica pravila + pasusi (kadar, start, tekst)).
Glas: Kokoro TTS (stoic/youtube.py: tts(), VOICE). Muzika: sopstvena generisana podloga (youtube.piano), stišava se ispod glasa.
Izlaz: videos/stoic_long/<ep>.mp4 + <ep>_opis.txt (naslov, opis sa poglavljima, tagovi) + <ep>_thumb.jpg
Upotreba: python3 stoic/longform.py long_ep01
"""
import os, sys, re, math, json, wave, importlib, subprocess
import numpy as np, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make as M
import youtube as YT

W, H, FPS = 1920, 1080, 30
TSR = 24000  # TTS sample rate
GAP, PARA_GAP, CARD_LEAD = 0.38, 0.30, 0.9
GRADE = M.GRADE
OUTD = os.path.join(ROOT, "videos", "stoic_long")


def sentences(text):
    return [s.strip() for s in re.findall(r"[^.?!]+[.?!]+", text) if s.strip()]


def ffdur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def vsize(p):
    w, h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", p],
                          capture_output=True, text=True).stdout.strip().split(",")[:2]
    return int(w), int(h)


def render_para(out, name, start, d, zin):
    src = M.src(name); sd = ffdur(src); sw, sh = vsize(src)
    avail = max(1.0, sd - start - 0.1)
    slow = max(1.0, d / avail)  # prekratak izvor -> usporeno
    if slow > 1.0 and sd - 0.2 > avail: start = 0.1; avail = sd - 0.2; slow = max(1.0, d / avail)
    z0, z1 = (1.0, 1.07) if zin else (1.07, 1.0)
    zoom = f"scale=w='{W}*({z0}+({z1}-{z0})*t/{d:.3f})':h=-2:eval=frame:flags=bicubic,crop={W}:{H},setsar=1"
    pre = f"setpts={slow:.4f}*(PTS-STARTPTS),"
    if sw >= sh:
        vf = f"{pre}scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},{GRADE},{zoom},vignette=PI/5,format=yuv420p"
        fc = ["-vf", vf]
    else:  # uspravni izvor: zamućena pozadina + kadar u sredini
        fc = ["-filter_complex",
              f"[0:v]{pre}fps={FPS},split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=40,eq=brightness=-0.12[bg];"
              f"[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0,{GRADE},{zoom},vignette=PI/5,format=yuv420p"]
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-i", src] + fc +
                   ["-an", "-t", f"{d:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "17", out], check=True)


def face(c, size, bold=True):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def shadow(c, x, y, s, a=1.0, rgb=(1, 1, 1)):
    for dx, dy, al in ((0, 4, 0.6), (0, 2, 0.6), (3, 3, 0.35), (-3, 3, 0.35)):
        c.move_to(x + dx, y + dy); c.set_source_rgba(0, 0, 0, al * a); c.show_text(s)
    c.move_to(x, y); c.set_source_rgba(*rgb, a); c.show_text(s)


def wrap2(c, text, maxw):
    words = text.split()
    if c.text_extents(text).x_advance <= maxw: return [text]
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        m = max(c.text_extents(a).x_advance, c.text_extents(b).x_advance)
        if best is None or m < best[0]: best = (m, [a, b])
    return best[1]


def sub_png(path, text, card=None, tag=None):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    # titl: donja trećina, 2 reda max, tamna traka
    face(c, 50); size = 50
    while True:
        lines = wrap2(c, text, 1500)
        if all(c.text_extents(l).x_advance <= 1560 for l in lines) or size <= 38: break
        size -= 2; face(c, size)
    lh = size * 1.25; y0 = H - 120 - (len(lines) - 1) * lh
    g = cairo.LinearGradient(0, y0 - 110, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(0.5, 0, 0, 0, 0.45); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.rectangle(0, y0 - 110, W, H - y0 + 110); c.set_source(g); c.fill()
    for i, l in enumerate(lines):
        shadow(c, W / 2 - c.text_extents(l).x_advance / 2, y0 + i * lh, l)
    if card:  # kartica pravila: "RULE 3" + naslov, centrirano
        big, small = card
        g = cairo.RadialGradient(W / 2, H * 0.42, 0, W / 2, H * 0.42, W * 0.45)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
        face(c, 44); sp = "  ".join(big.upper())
        shadow(c, W / 2 - c.text_extents(sp).x_advance / 2, H * 0.36, sp, 0.9)
        c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(3)
        c.move_to(W / 2 - 60, H * 0.36 + 30); c.line_to(W / 2 + 60, H * 0.36 + 30); c.stroke()
        face(c, 92); sm = small.upper()
        while c.text_extents(sm).x_advance > 1600: face(c, c.get_font_matrix().xx - 4)
        shadow(c, W / 2 - c.text_extents(sm).x_advance / 2, H * 0.36 + 140, sm)
    if tag:
        face(c, 30); shadow(c, 70, 90, tag, 0.75)
    s.write_to_png(path)


def long_music(path, total, n_sections):
    """Duga podloga: akordi 2 s (120 BPM), druga progresija za svaki deo, blagi pad + retke note."""
    N = int(total * 44100); out = np.zeros(N + 44100 * 4)
    beat = 0.5; bar = 2.0
    rng = np.random.default_rng(7)
    b = 0; t0 = 0.0
    while t0 < total:
        prog = YT.PROGS[(b // 16) % len(YT.PROGS)]
        ch = YT.CHORDS[prog[b % 4]]
        tt = np.arange(int(bar * 1.7 * 44100)) / 44100
        env = np.minimum(1, tt / 0.8) * np.exp(-tt * 0.45)
        pad = sum(np.sin(2 * np.pi * YT.hz(m) * tt) * g for m, g in ((ch[0] - 12, 0.18), (ch[0], 0.09), (ch[1], 0.06), (ch[3], 0.03))) * env
        i0 = int(t0 * 44100); out[i0:i0 + len(pad)] += pad
        for k, pos in enumerate((0.0, 2.0) if b % 2 else (0.0, 1.5, 3.0)):
            m = ch[2 + (k + int(rng.integers(0, 2))) % 3] + 12
            nt = YT.piano(YT.hz(m), 2.4, 0.08 if k == 0 else 0.05)
            j = int((t0 + pos * beat) * 44100); out[j:j + len(nt)] += nt[:len(out) - j]
        b += 1; t0 += bar
    dry = out.copy()
    for d, g in ((0.09, 0.30), (0.19, 0.22), (0.31, 0.16), (0.47, 0.11), (0.71, 0.07)):
        k = int(d * 44100); out[k:] += dry[:-k] * g
    out = out[:N]
    f = int(2.0 * 44100); out[:f] *= np.linspace(0, 1, f); f = int(4.0 * 44100); out[-f:] *= np.linspace(1, 0, f)
    out = np.tanh(out * 1.3); out = out / (np.abs(out).max() + 1e-9) * 0.8
    st = np.stack([out, np.roll(out, 240)], 1)
    with wave.open(path, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100); w.writeframes((st * 32767).astype(np.int16).tobytes())


def fmt(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def build(ep):
    E = importlib.import_module(ep)
    tmp = os.path.join(M.TMP, ep); os.makedirs(tmp, exist_ok=True); os.makedirs(OUTD, exist_ok=True)
    k = YT.tts()
    # 1) TTS + vremenska linija
    timeline, voice, t, chapters = [], [], 0.0, []
    for si, sec in enumerate(E.SECTIONS):
        chapters.append((t, sec["chapter"]))
        for pi, (shot, st, text) in enumerate(sec["paras"]):
            sents = []
            lead = CARD_LEAD if (sec["card"] and pi == 0) else 0.0
            p0 = t; t += lead
            for s_ in sentences(text):
                f = os.path.join(tmp, f"tts_{si:02d}_{pi:02d}_{len(sents):02d}.wav")
                if not os.path.exists(f):
                    a, sr = k.create(s_, voice=YT.VOICE, speed=YT.SPEED, lang="en-us")
                    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 240): nz[-1] + 1200]
                    np.save(f + ".npy", a); os.replace(f + ".npy", f)
                a = np.load(f)
                sents.append((t, t + len(a) / TSR + GAP, s_, sec["card"] if pi == 0 and not sents else None))
                voice.append((t, a)); t += len(a) / TSR + GAP
            t += PARA_GAP
            timeline.append({"shot": shot, "start": st, "t0": p0, "t1": t, "sents": sents, "card": sec["card"] if pi == 0 else None})
    total = t + 2.0
    timeline[-1]["t1"] = total
    print(f"{ep}: {len(timeline)} kadrova, trajanje {fmt(total)}")
    # 2) kadrovi + titlovi
    parts = []
    for i, p in enumerate(timeline):
        d = p["t1"] - p["t0"]; raw = os.path.join(tmp, f"p{i:03d}_raw.mp4"); out = os.path.join(tmp, f"p{i:03d}.mp4")
        render_para(raw, p["shot"], p["start"], d, i % 2 == 0)
        ins, fl = ["-i", raw], ""; cur = "0:v"
        for j, (s0, s1, txt, card) in enumerate(p["sents"]):
            png = os.path.join(tmp, f"p{i:03d}_{j}.png"); sub_png(png, txt, card)
            a, b = s0 - p["t0"], (s1 - p["t0"]) if j < len(p["sents"]) - 1 else d
            ins += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]
            fl += f"[{j + 1}:v]format=rgba,fade=t=in:st={max(0, a - 0.05):.2f}:d=0.15:alpha=1[s{j}];[{cur}][s{j}]overlay=enable='between(t,{a:.3f},{b:.3f})'[o{j}];"
            cur = f"o{j}"
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y"] + ins + ["-filter_complex", fl.rstrip(";"), "-map", f"[{cur}]",
                        "-t", f"{d:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", out], check=True)
        parts.append(out)
        print(f"  kadar {i + 1}/{len(timeline)} {p['shot']} {d:.1f}s", flush=True)
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{q}'\n" for q in parts))
    base = os.path.join(tmp, "base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], check=True)
    # 3) zvuk: glas + muzika (stišana ispod glasa)
    vt = np.zeros(int(total * TSR) + TSR)
    for s0, a in voice:
        i0 = int(s0 * TSR); vt[i0:i0 + len(a)] += a
    vw = os.path.join(tmp, "voice.wav")
    with wave.open(vw, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(TSR)
        w.writeframes((vt / (np.abs(vt).max() + 1e-9) * 0.9 * 32767).astype(np.int16).tobytes())
    mw = os.path.join(tmp, "music.wav"); long_music(mw, total, len(E.SECTIONS))
    out = os.path.join(OUTD, f"{ep}.mp4")
    fc = ("[2:a]aresample=44100,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
          "aecho=0.8:0.5:40|75:0.10|0.06,asplit[v1][v2];"
          "[1:a]volume=0.32[m];[m][v1]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=400[md];"
          "[md][v2]amix=inputs=2:weights='1 1.7':normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", mw, "-i", vw, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "8M", "-bufsize", "16M",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.3f}",
                    "-movflags", "+faststart", out], check=True)
    # 4) opis sa poglavljima
    chap = "\n".join(f"{fmt(a)} {b}" for a, b in chapters)
    desc = (f"Ten stoic rules to help you stay calm, disciplined and in control, no matter what life throws at you.\n\n"
            f"CHAPTERS\n{chap}\n\n"
            f"Which rule do you need most right now? Tell me in the comments.\n"
            f"Subscribe for a new stoic rule every day and a video like this every week.\n\n"
            f"#stoicism #stoic #selfimprovement\n")
    open(os.path.join(OUTD, f"{ep}_opis.txt"), "w").write(
        f"NASLOV: {E.TITLE}\n\nOPIS:\n{desc}\nTAGOVI: {', '.join(E.TAGS)}\n\nTRAJANJE: {fmt(total)}\n")
    json.dump({"total": total, "chapters": chapters, "shots": [p["shot"] for p in timeline]},
              open(os.path.join(OUTD, f"{ep}_plan.json"), "w"), indent=1)
    print(out, fmt(total))
    return out


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "long_ep01")
