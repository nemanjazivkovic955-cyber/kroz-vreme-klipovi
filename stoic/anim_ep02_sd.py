"""Dugi video #2 sa AI ilustracijama (stoic/sd/ep02/shot_NNN.png): ilustracija + spora kamera (Ken Burns) + čestice
(sneg/kiša/varnice/sjaj vatre) + oznake + titlovi + kartice poglavlja + glas George. Infografike (mapa, porodično stablo,
lista zahvalnosti, pet careva, lekcije) ostaju nacrtane kodom jer nose imena i brojeve.
Upotreba: python3 stoic/anim_ep02_sd.py"""
import os, sys, math, json, random, subprocess
import cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import anim_ep02 as E
import anim_long as L
from anim_long import W, H, FPS, A, ease

IMG = os.path.join(HERE, "sd", "ep02")
INFO = {"family_tree", "danube_map", "thanks_list", "five_emperors", "lesson", "half_empire"}
PART = {"camp_ext": "snow", "danube": "snow", "march": "snow?", "tribes": "snow", "forgive": "snow", "grave": "rain",
        "letters_burn": "embers", "general": "dust", "tent_write": "glow", "sick_emperor": "glow", "handed_letters": "glow",
        "argue": "glow", "lamp_out": "glow", "book": "glow", "deathbed": "dust"}
_cache = {}


def surface(i):
    if i not in _cache:
        src = os.path.join(IMG, f"shot_{i:03d}.png"); up = os.path.join(IMG, f"up_{i:03d}.png")
        if not os.path.exists(up):
            subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", src, "-vf",
                            "scale=2112:-2:flags=lanczos,unsharp=5:5:0.6,format=bgra", up], check=True)
        _cache.clear(); _cache[i] = cairo.ImageSurface.create_from_png(up)
    return _cache[i]


def particles(c, kind, t, seed):
    r = random.Random(seed)
    if kind == "snow":
        A.snowfall(c, t, n=110, wind=-0.6, speed=110, seed=seed)
    elif kind == "rain":
        for i in range(70):
            x = (r.uniform(0, W) + t * 120) % W; y = (r.uniform(0, H) + t * 1100) % H
            c.move_to(x, y); c.line_to(x - 10, y + 46); c.set_source_rgba(0.85, 0.9, 1, 0.3); c.set_line_width(3); c.stroke()
    elif kind == "embers":
        for i in range(50):
            p = (t * 0.4 + r.random()) % 1.0; x = r.uniform(300, 1600) + math.sin(t * 2 + i) * 40; y = H - p * H
            c.arc(x, y, 3 + 3 * r.random(), 0, 2 * math.pi); c.set_source_rgba(1, 0.6 + 0.3 * r.random(), 0.2, 1 - p); c.fill()
    elif kind == "dust":
        for i in range(40):
            x = (r.uniform(0, W) + t * 25 * (0.5 + r.random())) % W; y = r.uniform(0, H) + math.sin(t + i) * 15
            c.arc(x, y, 2 + 2 * r.random(), 0, 2 * math.pi); c.set_source_rgba(1, 0.9, 0.7, 0.25); c.fill()
    elif kind == "glow":
        a = 0.06 + 0.04 * math.sin(t * 7) + 0.02 * math.sin(t * 13)
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 0.75, 0.4, a); c.fill()


def draw_shot(c, sh, lt, d):
    name = sh["scene"].__name__
    if name in INFO or not os.path.exists(os.path.join(IMG, f"shot_{sh['i']:03d}.png")):
        sh["scene"](c, lt, d, sh["v"]); return
    s = surface(sh["i"]); sw, shh = s.get_width(), s.get_height()
    base = max(W / sw, H / shh)
    k = ease(lt / d); mode = sh["i"] % 4
    z = base * ((1.0 + 0.10 * k) if mode in (0, 2) else (1.10 - 0.10 * k))
    dx = (k - 0.5) * 60 * (1 if mode in (1, 2) else -1)
    c.save(); c.translate(W / 2 + dx, H / 2); c.scale(z, z); c.translate(-sw / 2, -shh / 2)
    c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()
    kind = PART.get(name)
    if kind == "snow?": kind = "snow" if (sh["v"] or {}).get("snow") else "dust"
    if kind: particles(c, kind, lt, sh["i"])


def build(ep="ep02"):
    tm = json.load(open(os.path.join(HERE, "out", ep, "timing.json")))
    shots, labels, sents = E.shots_from_timing(tm)
    total = tm["total"]
    out = os.path.join(ROOT, "videos", "stoic_long", f"anim_{ep}_ai.mp4")
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", os.path.join(HERE, "out", ep, "voice.wav"),
                          "-filter_complex", "[0:v]noise=alls=3:allf=t,vignette=PI/6,format=yuv420p[v];"
                          "[1:a]aresample=48000,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
                          "aecho=0.8:0.5:40|75:0.10|0.06,pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
                          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M",
                          "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); si = 0
    for f in range(int(round(total * FPS))):
        t = f / FPS
        while si < len(shots) - 1 and t >= shots[si + 1]["t0"]: si += 1
        sh = shots[si]; lt = t - sh["t0"]; d = max(0.5, sh["t1"] - sh["t0"])
        c = cairo.Context(s); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.set_source_rgb(0, 0, 0); c.paint()
        draw_shot(c, sh, lt, d)
        for (a, b, txt) in labels:
            if a <= t < b: E.label(c, txt, min(1, (t - a) / 0.2) * min(1, (b - t) / 0.25))
        cur = next((x for x in sents if x["t0"] - 0.05 <= t < x["t1"] + 0.3), None)
        if cur: L.sub_text(c, cur["text"])
        if sh["card"] and lt < 2.4: L.chapter_card(c, sh["card"], min(1, lt / 0.3) * min(1, (2.4 - lt) / 0.4))
        if lt < 0.12 and si > 0: c.rectangle(0, 0, W, H); c.set_source_rgba(0.03, 0.03, 0.05, 1 - lt / 0.12); c.fill()
        s.flush(); p.stdin.write(bytes(s.get_data()))
        if f % (FPS * 30) == 0: print(f"{int(t // 60)}:{int(t % 60):02d} / {int(total // 60)}:{int(total % 60):02d}", flush=True)
    p.stdin.close(); p.wait(); print("GOTOVO", out)


if __name__ == "__main__":
    build()
