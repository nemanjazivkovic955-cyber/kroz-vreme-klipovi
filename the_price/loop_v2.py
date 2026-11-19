"""TikTok LOOP v2 generator (Ciklus 1 studija) — vidi motivacija/tiktok_loops_v2.py i studio/lessons.md.
- svaka rečenica ima SVOJ kadar (ili 2 brza reza na vrhuncu), kadriranje po x-centru subjekta
- paleta po kadru + automatska korekcija ekspozicije (cilj prosečne osvetljenosti >= 0.30)
- "udarac" na rezu: kratki zoom-out (vizuelni akcenat jer je klip bez zvuka), pa lagani push-in
- loop: prvi i poslednji kadar su uzastopni delovi istog snimka, zoom se nastavlja bez skoka
Upotreba: python3 loop_v2.py m045 [m046 ...]
"""
import os, sys, json, math, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "motivacija")]
import shortloop as S
from tiktok_loops_v2 import LOOPS_V2

W, H, FPS, PER = S.W, S.H, S.FPS, 2.0
TMP = os.path.join(HERE, "out", "v2"); os.makedirs(TMP, exist_ok=True)
OUTDIR = os.path.join(HERE, "..", "videos", "tiktok_loops")
GRADE = {
    "gold": "colorbalance=rs=.05:gs=.01:bs=-.06:rm=.03:bm=-.04,eq=saturation=1.08:contrast=1.04",
    "warm": "colorbalance=rm=.04:bm=-.03,eq=saturation=1.05:contrast=1.04",
    "cool": "colorbalance=rs=-.02:bs=.04:bm=.03,eq=saturation=0.92:contrast=1.04",
    "steel": "colorbalance=bs=.03:bm=.02,eq=saturation=0.85:contrast=1.08",
    "mono": "hue=s=0,eq=contrast=1.1",
    "night": "eq=saturation=1.12:contrast=1.06",
    "teal": "colorbalance=rs=-.03:bs=.03:rh=.03,eq=saturation=1.1:contrast=1.04",
    "neutral": "eq=saturation=1.05:contrast=1.04",
}
TARGET = 0.43


def src(name): return os.path.join(HERE, "src", name + ".mp4")


def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                        capture_output=True, text=True).stdout)


def frame_gray(path, t, vf_pre="", w=108, h=192):
    vf = (vf_pre + "," if vf_pre else "") + f"scale={w}:{h},format=gray"
    seek = ["-sseof", f"{t:.3f}"] if t < 0 else ["-ss", f"{t:.3f}"]
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error"] + seek + ["-i", path, "-frames:v", "1",
                          "-vf", vf, "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w) / 255.0


def frame_cut(xc):
    return f"scale=-2:{H}:flags=lanczos,crop={W}:{H}:x='(iw-{W})*{xc}':y=0"


def shot(out, name, start, d, xc, pal, z0, z1, hit, at=None):
    cut = frame_cut(xc)
    m = float(frame_gray(src(name), start + d / 2 if at is None else at, cut + "," + GRADE[pal]).mean())
    gamma = 1.0 if m >= 0.40 else min(2.1, max(1.0, math.log(max(m, 0.02)) / math.log(TARGET)))
    zexpr = f"({z0}+({z1}-{z0})*t/{d})" + (f"+0.07*max(0\\,1-t/0.22)" if hit else "")
    vf = (f"{cut},fps={FPS},{GRADE[pal]},eq=gamma={gamma:.3f},"
          f"scale=w='{W}*({zexpr})':h=-2:eval=frame:flags=bicubic,crop={W}:{H},setsar=1,vignette=PI/6,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{d:.3f}", "-i", src(name),
                    "-vf", vf, "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "14", out], check=True)
    return {"src": name, "start": round(start, 2), "d": d, "palette": pal, "src_luma": round(m, 3), "gamma": round(gamma, 2)}


def make(cid):
    v = LOOPS_V2[cid]; n = len(v["texts"]); total = n * PER
    lname, lx, a = v["loop"]
    plan = []  # (name, start, d, x, pal, z0, z1, hit)
    used = {}
    for i, sl in enumerate(v["shots"]):
        if i == 0:
            plan.append((lname, a, PER, lx, v["palette"], 1.04, 1.08, False)); continue
        if i == n - 1:
            plan.append((lname, a - PER, PER, lx, v["palette"], 1.00, 1.04, False)); continue
        d = PER / len(sl)
        for j, (nm, xc, pal) in enumerate(sl):
            L = dur(src(nm)); k = used.get(nm, 0); used[nm] = k + 1
            st = min(L * (0.30 + 0.35 * k), L - d - 0.1)
            plan.append((nm, st, d, xc, pal, 1.0, 1.05, True))
    parts, info = [], []
    # loop snimak: JEDAN kontinualan render [a-PER, a+PER] (isti zoom/gamma), pa se deli -> spoj bez skoka
    full = os.path.join(TMP, f"{cid}_loopfull.mp4")
    li = shot(full, lname, a - PER, 2 * PER, lx, v["palette"], 1.00, 1.08, False, at=a)
    head, tail = os.path.join(TMP, f"{cid}_head.mp4"), os.path.join(TMP, f"{cid}_tail.mp4")
    for o, ss in ((head, PER), (tail, 0.0)):
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", full, "-ss", f"{ss}", "-t", f"{PER}",
                        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14", o], check=True)
    for k, (nm, st, d, xc, pal, z0, z1, hit) in enumerate(plan):
        if k == 0: parts.append(head); info.append(dict(li, start=a, d=PER)); continue
        if k == len(plan) - 1: parts.append(tail); info.append(dict(li, start=a - PER, d=PER)); continue
        o = os.path.join(TMP, f"{cid}_{k:02d}.mp4"); parts.append(o)
        info.append(shot(o, nm, st, d, xc, pal, z0, z1, hit))
    lst = os.path.join(TMP, f"{cid}_list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    base = os.path.join(TMP, f"{cid}_base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], check=True)
    ov = os.path.join(TMP, f"{cid}_ov.mov"); S.overlay(v["texts"], total, ov)
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, f"{cid}.mp4"); part = out.replace(".mp4", ".part.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov,
                    "-filter_complex", "[0:v][1:v]overlay=format=auto,noise=alls=4:allf=t,format=yuv420p[v]",
                    "-map", "[v]", "-an", "-t", f"{total}", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", part], check=True)
    os.replace(part, out)
    open(out.replace(".mp4", "_opis.txt"), "w").write(v["caption"] + "\n\n" + v["tags"] + "\n")
    json.dump(info, open(os.path.join(TMP, f"{cid}_plan.json"), "w"), indent=1)
    return check(cid, info)


def check(cid, info=None):
    v = LOOPS_V2[cid]; n = len(v["texts"]); total = n * PER
    out = os.path.join(OUTDIR, f"{cid}.mp4")
    info = info or json.load(open(os.path.join(TMP, f"{cid}_plan.json")))
    if not S.REPORT.get("boxes"):  # bez rendera: izracunaj okvire teksta ponovo (samo 1 frejm po tekstu)
        S.overlay(v["texts"], total, os.path.join(TMP, f"{cid}_ov_check.mov"))
    r = S.verify(out, v)
    # dodatne provere v2
    lum = [round(float(frame_gray(out, PER * i + 1.0).mean()), 3) for i in range(n)]
    f0 = frame_gray(out, 0.0, w=216, h=384); fl = frame_gray(out, -0.05, w=216, h=384)
    srcs = sorted({x["src"] for x in info})
    r.update({"osvetljenost_po_tekstu": lum, "min_osvetljenost": min(lum), "prosek_osvetljenosti": round(sum(lum) / n, 3),
              "loop_spoj_razlika_255": round(float(np.abs(f0 - fl).mean() * 255), 2), "izvora": len(srcs), "izvori": srcs,
              "kadrova": len(info), "plan": info})
    r["sve_ok_v2"] = bool(r["sve_ok"] and r["izvora"] >= 5 and r["prosek_osvetljenosti"] >= 0.30)
    json.dump(r, open(out.replace(".mp4", "_provera.json"), "w"), indent=1, ensure_ascii=False)
    print(cid, "OK" if r["sve_ok_v2"] else "PROBLEM", r["trajanje_s"], "s, izvora", r["izvora"], "luma", lum, "spoj", r["loop_spoj_razlika_255"])
    return r


if __name__ == "__main__":
    args = sys.argv[1:]
    fn = make
    if args and args[0] == "--check": fn = check; args = args[1:]
    for c in args or list(LOOPS_V2):
        fn(c)
