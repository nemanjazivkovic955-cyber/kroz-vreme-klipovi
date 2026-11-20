"""Dugi video #2 — verzija 2 (viši nivo): AI ilustracija + 2.5D kamera po mapi dubine (stoic/sd/parallax.py),
meka pretapanja između scena (0.5 s), čestice, oznake, titlovi, kartice poglavlja; glas Fable (stoic/narrate2.py, bez prekida).
Upotreba: python3 stoic/anim_ep02_v2.py [ep02v2]"""
import os, sys, json, subprocess
import numpy as np, cairo, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path[:0] = [HERE, os.path.join(HERE, "sd")]
import anim_ep02 as E
import anim_long as L
import anim_ep02_sd as SD
import parallax as PX
from anim_long import W, H, FPS, ease

IMG = os.path.join(HERE, "sd", "ep02")
XF = 0.5   # trajanje pretapanja (s)


class ShotRender:
    def __init__(self): self.cache = {}

    def base(self, sh, lt, d):
        """BGRA numpy frejm scene (bez titlova/oznaka)."""
        name = sh["scene"].__name__; i = sh["i"]; src = os.path.join(IMG, f"shot_{i:03d}.png")
        if name in SD.INFO or not os.path.exists(src):
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); c.set_line_join(cairo.LINE_JOIN_ROUND)
            sh["scene"](c, lt, d, sh["v"]); s.flush()
            return np.ndarray((H, W, 4), np.uint8, s.get_data()).copy()
        if i not in self.cache:
            if len(self.cache) > 2: self.cache.pop(next(iter(self.cache)))
            self.cache[i] = PX.prepare(src)
        big, dep = self.cache[i]
        bgr = PX.frame(big, dep, min(1.0, lt / d), mode=i % 4)
        fr = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
        kind = SD.PART.get(name)
        if kind == "snow?": kind = "snow" if (sh["v"] or {}).get("snow") else "dust"
        if kind:  # čestice preko slike
            s = cairo.ImageSurface.create_for_data(fr, cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
            SD.particles(c, kind, lt, i); s.flush()
        return fr


def build(ep="ep02v2"):
    tm = json.load(open(os.path.join(HERE, "out", ep, "timing.json")))
    shots, labels, sents = E.shots_from_timing(tm)
    total = tm["total"]
    out = os.path.join(ROOT, "videos", "stoic_long", "marcus_aurelius_v2.mp4")
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", os.path.join(HERE, "out", ep, "voice.wav"),
                          "-filter_complex", "[0:v]noise=alls=3:allf=t,vignette=PI/6,format=yuv420p[v];"
                          "[1:a]aresample=48000,highpass=f=60,acompressor=threshold=-24dB:ratio=2:attack=15:release=250,"
                          "pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
                          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M",
                          "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    R = ShotRender(); si = 0; last = {}
    for f in range(int(round(total * FPS))):
        t = f / FPS
        while si < len(shots) - 1 and t >= shots[si + 1]["t0"]: si += 1
        sh = shots[si]; lt = t - sh["t0"]; d = max(0.5, sh["t1"] - sh["t0"])
        fr = R.base(sh, lt, d)
        if si > 0 and lt < XF:  # meko pretapanje iz prethodne scene
            pv = shots[si - 1]
            if si - 1 not in last: last[si - 1] = R.base(pv, pv["t1"] - pv["t0"], max(0.5, pv["t1"] - pv["t0"]))
            a = ease(lt / XF); fr = cv2.addWeighted(fr, a, last[si - 1], 1 - a, 0)
        last = {k: v for k, v in last.items() if k >= si - 1}
        fr = np.ascontiguousarray(fr)
        s = cairo.ImageSurface.create_for_data(fr, cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        for (a0, b0, txt) in labels:
            if a0 <= t < b0: E.label(c, txt, min(1, (t - a0) / 0.25) * min(1, (b0 - t) / 0.3))
        cur = next((x for x in sents if x["t0"] - 0.05 <= t < x["t1"] + 0.2), None)
        if cur: L.sub_text(c, cur["text"])
        if sh["card"] and lt < 2.6: L.chapter_card(c, sh["card"], min(1, lt / 0.4) * min(1, (2.6 - lt) / 0.5))
        s.flush(); p.stdin.write(fr.tobytes())
        if f % (FPS * 30) == 0: print(f"{int(t // 60)}:{int(t % 60):02d} / {int(total // 60)}:{int(total % 60):02d}", flush=True)
    p.stdin.close(); p.wait(); print("GOTOVO", out)


if __name__ == "__main__":
    build(*(sys.argv[1:2] or []))
