"""THE PRICE - produkcija epizode (16:9 YouTube i 9:16 Shorts).
Montaza (push-in), kolor (hladno=muka, toplo=nagrada), letterbox, zrno, titlovi sinhronizovani sa naracijom,
sopstvena dark-trap muzika + SFX (boom, whoosh, riser, impact), ducking muzike ispod glasa.

Upotreba: python3 produce.py ep1 [16x9|9x16]
"""
import os, sys, math, random, subprocess, wave
import numpy as np
import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "motivacija"))
import design2 as D

SRC = os.path.join(HERE, "src")
TMP = os.path.join(HERE, "out"); os.makedirs(TMP, exist_ok=True)
OUTDIR = os.path.join(HERE, "..", "videos", "the_price"); os.makedirs(OUTDIR, exist_ok=True)
FPS, SR = 30, 48000

EPISODES = {
    "ep1": {
        "title": "THE PRICE", "subtitle": "EPISODE 1", "next": "SHARE  •  LIKE  •  COMMENT FOR MORE",
        "voice": "voiceover_ep1.wav",
        "title_len": 1.5, "end_len": 2.5,
        # (izvor, trajanje, tip) - grind = hladno, reward = toplo
        "shots": [("01_alarm", 2.0, "g"), ("02_wake", 2.0, "g"), ("03_midnight", 2.0, "g"), ("04_runner", 2.0, "g"),
                  ("05_rain", 2.0, "g"), ("06_bandage", 2.0, "g"), ("07_boxer", 2.0, "g"), ("08_bag", 2.0, "g"),
                  ("09_typing", 2.0, "g"), ("10_overtime", 2.0, "g"), ("11_exhausted", 2.0, "g"), ("12_sunrise", 2.0, "g"),
                  ("13_watch_on", 2.6, "r"), ("14_watch_close", 2.6, "r"), ("15_dashboard", 2.6, "r"), ("16_red_car", 2.6, "r"),
                  ("17_ferrari", 2.6, "r"), ("18_blue_car", 2.6, "r"), ("19_jet", 2.6, "r"), ("20_burj", 2.6, "r"),
                  ("21_yacht", 2.6, "r"), ("22_champagne", 2.6, "r")],
        "captions": [(1.6, 3.8, "Everyone wants the *car*."), (3.8, 5.7, "Nobody wants *5 A.M.*"),
                     (5.7, 6.6, "Nobody wants"), (6.6, 7.9, "the cold mornings."), (7.9, 9.2, "The empty streets."),
                     (9.2, 9.9, "The *rain*."), (11.8, 13.2, "Nobody wants"), (13.2, 14.2, "the *pain*."),
                     (17.6, 18.8, "The nights alone,"), (18.8, 20.1, "while everyone else"), (20.1, 20.8, "is asleep."),
                     (20.8, 21.6, "No applause."), (21.6, 22.3, "Just *work*."), (22.7, 23.9, "Day after day."),
                     (23.9, 25.7, "Until one *morning*..."), (26.0, 27.2, "you don't wake up"),
                     (27.2, 28.8, "for the *alarm* anymore."), (28.9, 29.8, "You wake up"), (29.8, 30.7, "for the *life*"),
                     (30.7, 31.5, "you built."), (41.2, 42.5, "Everyone wants"), (42.5, 43.6, "the *result*."),
                     (48.4, 49.7, "Few are willing"), (49.7, 51.1, "to pay the *price*.")],
        "whoosh": [5.5, 9.5, 13.5, 17.5, 21.5],
        "reveal": 25.5,
    },
}

COLD = "eq=contrast=1.18:saturation=0.45:brightness=-0.06:gamma=0.95,colorbalance=rs=-0.08:gs=-0.02:bs=0.12:rm=-0.04:bm=0.06"
WARM = "eq=contrast=1.12:saturation=1.05:brightness=0.0,colorbalance=rs=0.05:gs=0.01:bs=-0.06:rh=0.06:gh=0.03:bh=-0.07"


# ----------------------------------------------------------------- VIDEO
def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def cut(i, name, d, kind, W, H):
    src = os.path.join(SRC, name + ".mp4"); L = dur(src)
    st = max(0.0, min(L * 0.35, L - d - 0.05))
    grade = COLD if kind == "g" else WARM
    z = 0.07 if kind == "r" else 0.05
    out = os.path.join(TMP, f"seg_{W}_{i:02d}.mp4")
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
          f"scale=w='{W}*(1+{z}*t/{d})':h=-2:eval=frame,crop={W}:{H},setsar=1,{grade},vignette=PI/4.5,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{st:.2f}", "-t", str(d), "-i", src,
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", out], check=True)
    return out


def card_clip(path, d, W, H, big, small, fade_in=True):
    out = path
    frames = int(d * FPS)
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "16",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(frames):
        t = f / FPS
        c = cairo.Context(s); c.set_source_rgb(0.01, 0.01, 0.012); c.paint()
        a = D.ease(t / 0.6) if fade_in else 1.0
        a *= 1 - D.ease((t - (d - 0.35)) / 0.35)
        sc = 1.0 + 0.04 * t / d
        c.translate(W / 2, H / 2); c.scale(sc, sc); c.translate(-W / 2, -H / 2)
        g = cairo.RadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.5)
        g.add_color_stop_rgba(0, 0.85, 0.62, 0.18, 0.18 * a); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
        size = min(W * 0.13, 190)
        c.select_font_face("Anton"); c.set_font_size(size)
        spaced = "  ".join(big.split(" ")); txt = " ".join(spaced)
        e = c.text_extents(txt)
        if e.x_advance > W * 0.86:  # uklopi u sirinu (npr. uspravni format)
            size *= W * 0.86 / e.x_advance; c.set_font_size(size); e = c.text_extents(txt)
        x = W / 2 - e.x_advance / 2; y = H / 2 + size * 0.32
        c.move_to(x, y); c.text_path(txt); c.set_source(D._gold_grad(y - size * 0.75, y)); c.fill()
        c.set_source_rgba(1, 0.82, 0.35, 0.9 * a); c.set_line_width(2)
        lw = e.x_advance * 0.55 * D.ease(t / 1.0)
        for yy in (y - size * 0.95, y + size * 0.35):
            c.move_to(W / 2 - lw / 2, yy); c.line_to(W / 2 + lw / 2, yy); c.stroke()
        c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size * 0.2)
        st = " ".join(small); e2 = c.text_extents(st)
        c.move_to(W / 2 - e2.x_advance / 2, y + size * 0.62); c.set_source_rgba(1, 0.82, 0.35, a); c.show_text(st)
        # fade preko svega
        c.identity_matrix(); c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, 1 - a); c.fill()
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()
    return out


def caption_overlay(ep, total, W, H, out):
    """Providni overlay: letterbox (16:9), titlovi."""
    vertical = H > W
    bar = 0 if vertical else int((H - W / 2.39) / 2)
    size = 104 if vertical else 94
    base_y = H * 0.70 if vertical else H - bar - 48
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    caps = ep["captions"]
    for f in range(int(total * FPS)):
        t = f / FPS
        c = cairo.Context(s); c.set_operator(cairo.OPERATOR_CLEAR); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
        if bar:
            c.rectangle(0, 0, W, bar); c.rectangle(0, H - bar, W, bar); c.set_source_rgb(0, 0, 0); c.fill()
        for a0, b0, txt in caps:
            if not (a0 <= t < b0): continue
            pop = D.ease((t - a0) / 0.14)
            al = pop * (1 - D.ease((t - (b0 - 0.08)) / 0.08))
            sc = 0.86 + 0.14 * pop
            D._face(c, D.QUOTE_FONT, size)
            lines, sp = D._balanced(c, D._tokens(txt), W * 0.82)
            lh = size * 1.08
            c.save(); c.translate(W / 2, base_y); c.scale(sc, sc); c.translate(-W / 2, -base_y)
            for li, (words, lw) in enumerate(lines):
                y = base_y - (len(lines) - 1 - li) * lh
                x = W / 2 - lw / 2 - sum(12 for (_, h, _) in words if h)
                for (w, hl, ww) in words:
                    if hl:
                        x += 12
                        D._rrect(c, x - 12, y - size * 0.86, ww + 24, size * 1.02, 10)
                        c.set_source(D._gold_grad(y - size * 0.86, y + size * 0.16, al)); c.fill()
                        c.move_to(x, y); c.set_source_rgba(0.04, 0.03, 0.02, al); c.show_text(w)
                    else:
                        D._shadow_text(c, x, y, w, D.GOLD, al, outline=6)
                    x += ww + sp + (12 if hl else 0)
            c.restore()
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()


# ----------------------------------------------------------------- AUDIO
def env_exp(n, k):
    return np.exp(-np.arange(n) / SR * k)


def add(buf, t, sig, g=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    e = min(len(buf), i + len(sig)); buf[i:e] += sig[:e - i] * g


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def kick808(note=36, d=0.9):
    n = int(d * SR); tt = np.arange(n) / SR
    f = hz(note) * (1 + 2.5 * np.exp(-tt * 30))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(1.6 * np.sin(ph) * env_exp(n, 3.2))


def snare(d=0.35):
    n = int(d * SR); rnd = np.random.RandomState(4)
    noise = rnd.randn(n); noise = np.convolve(noise, np.ones(6) / 6, "same") - np.convolve(noise, np.ones(40) / 40, "same")
    tone = np.sin(2 * np.pi * 190 * np.arange(n) / SR) * env_exp(n, 30)
    return (noise * 1.6 * env_exp(n, 14) + tone * 0.5) * 0.7


def hat(d=0.06, seed=1):
    n = int(d * SR); x = np.random.RandomState(seed).randn(n)
    x = x - np.convolve(x, np.ones(8) / 8, "same")
    return x * env_exp(n, 70) * 0.35


def pad(chord, d, bright=0.0):
    n = int(d * SR); tt = np.arange(n) / SR; out = np.zeros(n)
    for m in chord:
        for det in (-0.12, 0.0, 0.12):
            f = hz(m + det)
            out += np.sin(2 * np.pi * f * tt) * 0.5 + bright * np.sin(4 * np.pi * f * tt) * 0.15
    a = np.minimum(1, tt / 1.2) * np.minimum(1, (d - tt) / 1.0)
    return out / (len(chord) * 3) * a * (0.8 + 0.2 * np.sin(2 * np.pi * 0.2 * tt))


def whoosh(d=0.7, seed=3):
    n = int(d * SR); x = np.random.RandomState(seed).randn(n); tt = np.arange(n) / SR
    out = np.zeros(n); k = 30
    for i in range(0, n, 512):  # pomeranje filtra
        w = int(4 + 60 * (1 - abs(2 * tt[i] / d - 1)))
        seg = x[max(0, i - 200):i + 712]
        y = np.convolve(seg, np.ones(w) / w, "same")[200 if i >= 200 else 0:][:512]
        out[i:i + len(y)] = y
    return out * np.sin(np.pi * tt / d) ** 2 * 1.4


def riser(d=2.2):
    n = int(d * SR); tt = np.arange(n) / SR; x = np.random.RandomState(9).randn(n)
    hp = x - np.convolve(x, np.ones(12) / 12, "same")
    f = 200 * (1 + 6 * (tt / d) ** 2); tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (hp * 0.5 + tone * 0.25) * (tt / d) ** 2.2


def impact(d=2.5):
    n = int(d * SR); tt = np.arange(n) / SR
    f = 70 * np.exp(-tt * 1.5) + 28
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 1.8)
    x = np.random.RandomState(5).randn(n); crack = np.convolve(x, np.ones(3) / 3, "same") * env_exp(n, 9)
    return np.tanh(1.8 * sub) + crack * 0.5


def music_and_sfx(ep, total):
    m = np.zeros(int(total * SR) + SR); fx = np.zeros_like(m)
    bpm = 72.0; beat = 60 / bpm; bar = beat * 4
    rev = ep["reveal"]; t0 = ep["title_len"]
    cm = [48, 55, 63]; ab = [44, 51, 60]; fm = [41, 48, 56]; gm = [43, 50, 59]
    prog = [cm, ab, fm, gm]
    # pad kroz ceo film
    t, k = 0.0, 0
    while t < total:
        add(m, t, pad(prog[k % 4], bar + 1.0, bright=0.6 if t >= rev else 0.0), 0.55 if t < rev else 0.7); t += bar; k += 1
    # muka: otkucaji sata (hat) + srce (meki kick)
    t = t0
    while t < rev - 2.2:
        for b in range(4):
            add(m, t + b * beat, hat(0.04, b), 0.5)
            add(m, t + b * beat + beat / 2, hat(0.03, b + 7), 0.25)
        add(m, t, kick808(31, 0.5), 0.35); add(m, t + beat * 0.5, kick808(31, 0.4), 0.22)
        t += bar
    # nagrada: puni trap ritam (half-time)
    t = rev; rnd = random.Random(2)
    while t < total - ep["end_len"] + 0.5:
        for b in range(4):
            tb = t + b * beat
            for s16 in range(4):
                add(m, tb + s16 * beat / 4, hat(0.05, s16 + b), 0.32 if s16 % 2 == 0 else 0.18)
            if b == 2: add(m, tb, snare(), 0.55)
        for off, nt in ((0, 36), (beat * 1.5, 36), (beat * 2.75, 39), (beat * 3.25, 34)):
            add(m, t + off, kick808(nt, 0.85), 0.75)
        t += bar
    # SFX
    add(fx, 0.05, impact(1.8), 0.55)
    for w in ep["whoosh"]: add(fx, w - 0.35, whoosh(0.7, int(w * 10)), 0.35)
    add(fx, rev - 2.2, riser(2.2), 0.45)
    add(fx, rev, impact(2.6), 0.9)
    add(fx, total - ep["end_len"], impact(2.0), 0.4)
    # fade
    fo = int(2.0 * SR); m[int(total * SR) - fo:int(total * SR)] *= np.linspace(1, 0, fo)
    m = m[:int(total * SR)]; fx = fx[:int(total * SR)]
    return m / (np.abs(m).max() + 1e-9) * 0.8, fx / (np.abs(fx).max() + 1e-9) * 0.9


def write_wav(path, x):
    x = np.clip(x, -1, 1); d = (np.stack([x, x], 1) * 32767).astype(np.int16)
    with wave.open(path, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())


# ----------------------------------------------------------------- MAIN
def produce(epname, fmt="16x9"):
    ep = EPISODES[epname]
    W, H = (1920, 1080) if fmt == "16x9" else (1080, 1920)
    segs = [card_clip(os.path.join(TMP, f"title_{W}.mp4"), ep["title_len"], W, H, ep["title"], ep["subtitle"])]
    for i, (n, d, k) in enumerate(ep["shots"]):
        segs.append(cut(i, n, d, k, W, H))
    segs.append(card_clip(os.path.join(TMP, f"end_{W}.mp4"), ep["end_len"], W, H, ep["title"], ep["next"]))
    total = ep["title_len"] + sum(d for _, d, _ in ep["shots"]) + ep["end_len"]
    lst = os.path.join(TMP, f"list_{W}.txt")
    with open(lst, "w") as f:
        for s in segs: f.write(f"file '{s}'\n")
    base = os.path.join(TMP, f"base_{W}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", base], check=True)
    ov = os.path.join(TMP, f"captions_{W}.mov"); caption_overlay(ep, total, W, H, ov)
    mus, fx = music_and_sfx(ep, total)
    mw, fw = os.path.join(TMP, f"music_{W}.wav"), os.path.join(TMP, f"sfx_{W}.wav")
    write_wav(mw, mus); write_wav(fw, fx)
    voice = os.path.join(SRC, ep["voice"])
    out = os.path.join(OUTDIR, f"{epname}_the_price_{fmt}.mp4")
    fc = (f"[0:v][1:v]overlay=format=auto,noise=alls=7:allf=t,format=yuv420p[v];"
          f"[2:a]aresample={SR},apad,atrim=0:{total},volume=1.0,asplit=2[vo][sc];"
          f"[3:a]volume=0.55[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[duck];"
          f"[4:a]volume=0.8[fx];[vo][duck][fx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.2[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov, "-i", voice, "-i", mw, "-i", fw,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "14M", "-bufsize", "28M",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    print("OK", os.path.abspath(out), total, "s")


if __name__ == "__main__":
    produce(sys.argv[1] if len(sys.argv) > 1 else "ep1", sys.argv[2] if len(sys.argv) > 2 else "16x9")
