"""Motivacioni klipovi: pozadinski snimak + beli tekst koji se smenjuje + mirna muzika.

Upotreba:
    python3 make.py <id>          # renderuje klip iz quotes.py u videos/motivacija/
    python3 make.py <id> preview  # samo PNG kadrovi za proveru
"""
import os, sys, math, random, subprocess, wave
import cairo
import numpy as np
from quotes import QUOTES

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "..", "videos", "motivacija")
TMP = os.path.join(HERE, "out")
W, H = 1080, 1920
FONT = "Poppins"
TEXT_Y = 0.36  # vertikalni polozaj teksta (deo visine)


def wrap(ctx, text, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if ctx.text_extents(t).x_advance > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    if cur: lines.append(cur)
    return lines


def _shadowed(ctx, x, y, ln, rgb=(1, 1, 1)):
    for r, a in ((10, 0.10), (6, 0.16), (3, 0.28)):
        for dx, dy in ((r, r), (-r, r), (r, -r), (-r, -r), (0, r), (r, 0)):
            ctx.move_to(x + dx * 0.4 + 2, y + dy * 0.4 + 3); ctx.text_path(ln)
        ctx.set_source_rgba(0, 0, 0, a); ctx.fill()
    ctx.move_to(x, y); ctx.text_path(ln)
    ctx.set_source_rgba(0, 0, 0, 0.55); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(x, y); ctx.set_source_rgb(*rgb); ctx.show_text(ln)


def header_png(path, text="QUOTE OF THE DAY"):
    """Stalni natpis gore: razmaknuta slova + zlatne linije."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(40)
    spaced = " ".join(text.upper())
    e = ctx.text_extents(spaced)
    y = H * 0.17
    _shadowed(ctx, W / 2 - e.x_advance / 2, y, spaced)
    for sx in (-1, 1):
        x0 = W / 2 + sx * (e.x_advance / 2 + 24)
        ctx.move_to(x0, y - 13); ctx.line_to(x0 + sx * 70, y - 13)
        ctx.set_source_rgba(0, 0, 0, 0.4); ctx.set_line_width(7); ctx.stroke()
        ctx.move_to(x0, y - 13); ctx.line_to(x0 + sx * 70, y - 13)
        ctx.set_source_rgb(1.0, 0.83, 0.23); ctx.set_line_width(4); ctx.stroke()
    surf.write_to_png(path)


def text_png(path, text, size=64, label=None):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    text = text.upper()
    maxw = W * 0.78
    n = len(wrap(ctx, text, maxw))
    while maxw > 200 and len(wrap(ctx, text, maxw - 10)) == n:  # ravnomerni redovi
        maxw -= 10
    lines = wrap(ctx, text, maxw)
    lh = size * 1.22
    y0 = H * TEXT_Y - (len(lines) - 1) * lh / 2
    for i, ln in enumerate(lines):
        e = ctx.text_extents(ln)
        _shadowed(ctx, W / 2 - e.x_advance / 2, y0 + i * lh, ln)
    if label:  # npr. "TODAY'S LESSON" iznad teksta, zlatno
        ctx.set_font_size(42)
        lt = " ".join(label.upper())
        e = ctx.text_extents(lt)
        _shadowed(ctx, W / 2 - e.x_advance / 2, y0 - size - 34, lt, (1.0, 0.83, 0.23))
        ctx.set_font_size(size)
    surf.write_to_png(path)


def ambient(path, dur, seed=7):
    """Mirna klavirska podloga (generisana, bez autorskih prava)."""
    sr = 44100
    n = int(dur * sr)
    out = np.zeros(n)
    rnd = random.Random(seed)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [55, 59, 62, 67]]  # Am F C G
    bar = 60 / 70 * 4
    t = 0.0; b = 0
    while t < dur:
        ch = prog[b % 4]
        # pad
        tt = np.arange(int(min(bar * 1.3, dur - t) * sr)) / sr
        env = np.minimum(1, tt / 1.2) * np.exp(-tt * 0.5)
        pad = sum(np.sin(2 * np.pi * hz(m - 12) * tt) * 0.05 for m in ch[:3]) * env
        st = int(t * sr); out[st:st + len(pad)] += pad[:n - st]
        # klavirske note (arpeggio)
        for k in range(6):
            m = ch[(k * 2 + rnd.randint(0, 1)) % 4] + (12 if k % 3 == 2 else 0)
            nt = t + k * bar / 6
            if nt >= dur: break
            tt = np.arange(int(1.8 * sr)) / sr
            f = hz(m)
            note = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) + 0.1 * np.sin(6 * np.pi * f * tt))
            note *= np.minimum(1, tt / 0.005) * np.exp(-tt * 2.2) * 0.09
            st = int(nt * sr); e = min(n, st + len(note)); out[st:e] += note[:e - st]
        t += bar; b += 1
    # jednostavan reverb (eho)
    for d, g in ((0.11, 0.35), (0.23, 0.25), (0.37, 0.18), (0.53, 0.12)):
        k = int(d * sr); out[k:] += out[:-k] * g
    fade = int(2.5 * sr)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[:int(1.0 * sr)] *= np.linspace(0, 1, int(1.0 * sr))
    out = out / (np.abs(out).max() + 1e-9) * 0.45
    data = (np.stack([out, out], 1) * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(data.tobytes())


def build(qid, preview=False):
    q = QUOTES[qid]
    os.makedirs(TMP, exist_ok=True); os.makedirs(OUTDIR, exist_ok=True)
    lines = list(q["lines"]) + ([q["lesson"]] if q.get("lesson") else [])
    per = q.get("per_line", 5.2)
    dur = per * len(lines) + 0.8
    pngs = []
    for i, ln in enumerate(lines):
        lab = "Today's lesson" if (q.get("lesson") and i == len(lines) - 1) else None
        p = os.path.join(TMP, f"{qid}_{i}.png"); text_png(p, ln, q.get("size", 64), lab); pngs.append(p)
    hdr = None
    if q.get("header", True if q.get("lesson") else False):
        hdr = os.path.join(TMP, f"{qid}_hdr.png"); header_png(hdr, q.get("header_text", "Quote of the day"))
    bg = os.path.join(HERE, "broll", q["broll"])
    out = os.path.join(OUTDIR, f"{qid}.mp4")
    if preview:
        for i in range(len(lines)):
            t = 0.4 + i * per + per / 2
            extra = ["-i", hdr] if hdr else []
            post = ";[o][2:v]overlay" if hdr else ""
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t % 14), "-i", bg, "-i", pngs[i]] + extra +
                           ["-filter_complex", "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                            + ("hflip," if q.get("flip") else "") +
                            "eq=saturation=0.8:brightness=-0.04[b];[b][1:v]overlay" + ("[o]" + post if hdr else ""), "-frames:v", "1",
                            os.path.join(TMP, f"{qid}_prev{i}.png")], check=True)
        return
    music = os.path.join(TMP, f"{qid}.wav")
    track = os.path.join(HERE, "music", q.get("music", "cinematic_piano.mp3"))
    if os.path.exists(track):  # deo prave numere, sa fade in/out
        start = q.get("music_start", 0)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-t", f"{dur:.2f}", "-i", track,
                        "-af", f"afade=t=in:d=0.8,afade=t=out:st={dur - 2.5:.2f}:d=2.5,loudnorm=I=-16:TP=-1.5",
                        "-ar", "44100", "-ac", "2", music], check=True)
    else:
        ambient(music, dur, seed=hash(qid) % 1000)
    inputs = ["-stream_loop", "-1", "-ss", str(q.get("broll_start", 0)), "-i", bg]
    for p in pngs: inputs += ["-loop", "1", "-t", str(dur), "-i", p]
    if hdr: inputs += ["-loop", "1", "-t", str(dur), "-i", hdr]
    music_idx = len(pngs) + 1 + (1 if hdr else 0)
    inputs += ["-i", music]
    fc = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,"
          + ("hflip," if q.get("flip") else "") +
          "eq=saturation=0.8:brightness=-0.04,trim=0:%.2f,setpts=PTS-STARTPTS[v0];" % dur)
    for i in range(len(lines)):
        a = 0.4 + i * per; b = a + per - 0.15
        fc += (f"[{i + 1}:v]format=rgba,fade=t=in:st={a:.2f}:d=0.35:alpha=1,fade=t=out:st={b - 0.3:.2f}:d=0.3:alpha=1[t{i}];"
               f"[v{i}][t{i}]overlay=enable='between(t,{a:.2f},{b:.2f})'[v{i + 1}];")
    last = f"v{len(lines)}"
    if hdr:
        fc += (f"[{len(pngs) + 1}:v]format=rgba,fade=t=in:st=0.2:d=0.5:alpha=1[hd];"
               f"[{last}][hd]overlay[vh];")
        last = "vh"
    fc = fc.rstrip(";")
    cmd = ["ffmpeg", "-loglevel", "error", "-y"] + inputs + [
        "-filter_complex", fc, "-map", f"[{last}]", "-map", f"{music_idx}:a",
        "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    silent_dir = os.path.join(OUTDIR, "bez_muzike"); os.makedirs(silent_dir, exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out, "-an", "-c:v", "copy", "-movflags", "+faststart",
                    os.path.join(silent_dir, f"{qid}.mp4")], check=True)
    with open(os.path.join(silent_dir, "opisi.txt"), "w") as f:
        for k, qq in QUOTES.items():
            f.write(f"{k}.mp4\n{qq['caption']}\n\n")
    print("OK", os.path.abspath(out))


if __name__ == "__main__":
    build(sys.argv[1], preview=len(sys.argv) > 2 and sys.argv[2] == "preview")
