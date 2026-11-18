"""Inspirativni govor "BE LIKE WATER": vodopadi, meki prelazi, prava muzika (Mixkit, gudaci), studijski obradjen glas.
Upotreba: python3 water.py [16x9|9x16]
"""
import os, sys, json, re, subprocess
import produce as P

HERE = P.HERE
SRC, TMP, OUTDIR = P.SRC, P.TMP, P.OUTDIR
TALK = json.load(open(os.path.join(SRC, "talk_water.json")))
VOICE = os.path.join(SRC, "talk_water.wav")
MUSIC = os.path.join(HERE, "music", "mixkit_871.mp3")
XF = 0.7
TOTAL = TALK["total"]

# (izvor, trajanje) - zbir minus prelazi ~= TOTAL - kraj
SHOTS = [("wf_slowmo", 5.0), ("wf_crash", 4.6), ("wf_rocks", 4.4), ("wf_riverslow", 4.6), ("wf_rocky", 4.2),
         ("p_nature_13878296", 4.6), ("wf_iguazu", 4.6), ("wf_niagara", 4.6), ("wf_valley", 4.6),
         ("p_snow_6650177", 4.4), ("wf_hiker", 4.6), ("p_nature_38840179", 4.6), ("p_travel_33545687", 4.4),
         ("wf_rainbow", 4.4), ("p_nature_28951859", 4.0), ("p_travel_8970213", 5.0)]
END_LEN = 6.6
# skaliraj kadrove: zavrsna kartica pocinje tacno pre "Be like water" (63.6 s)
_card_start = TALK["segments"][-1][0] - 0.3
_k = (_card_start + XF * (len(SHOTS) - 1)) / sum(d for _, d in SHOTS)
SHOTS = [(n, round(d * _k, 2)) for n, d in SHOTS]
KEY = {"water", "rock", "quit", "way", "one", "mountains", "never", "wall", "flowing", "pushing", "try", "talent", "truth", "you"}
GRADE = ("eq=contrast=1.12:saturation=1.08:brightness=-0.02,"
         "colorbalance=rs=-0.05:gs=0.0:bs=0.06:rh=0.05:gh=0.02:bh=-0.05")


def chunks(seg_list):
    out = []
    for a, b, txt in seg_list:
        parts = [p.strip() for p in re.split(r"(?<=[.,])\s+", txt) if p.strip()]
        pieces = []
        for p in parts:
            w = p.split()
            while len(w) > 4:
                pieces.append(" ".join(w[:3])); w = w[3:]
            pieces.append(" ".join(w))
        tot = sum(len(p) for p in pieces); x = a
        for p in pieces:
            d = (b - a) * len(p) / tot
            marked = " ".join(f"*{w}*" if re.sub(r"[^a-z]", "", w.lower()) in KEY else w for w in p.split())
            out.append((round(x, 2), round(x + d, 2), marked)); x += d
    return out


def seg(i, name, d, W, H):
    src = os.path.join(SRC, name + ".mp4"); L = P.dur(src)
    st = max(0.0, min(L * 0.3, L - d - 0.1))
    out = os.path.join(TMP, f"w_{W}_{i:02d}.mp4")
    if os.path.exists(out) and os.environ.get("REUSE"): return out
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={P.FPS},"
          f"scale=w='{W}*(1+0.06*t/{d})':h=-2:eval=frame,crop={W}:{H},setsar=1,{GRADE},vignette=PI/5,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{st:.2f}", "-t", str(d), "-i", src,
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", out], check=True)
    return out


def elegant_overlay(caps, total, W, H, out):
    """Elegantni titlovi: ukosen serif (DM Serif Display Italic), bledo zlatno + kljucne reci jarko zlatne sa
    tankom linijom; mek ulaz (fade + blago podizanje). Letterbox samo za 16:9."""
    import cairo
    D = P.D
    vertical = H > W
    bar = 0 if vertical else int((H - W / 2.39) / 2)
    size = 96 if vertical else 76
    cy = H * 0.64 if vertical else H - bar - 70
    PALE, RICH = (0.96, 0.89, 0.72), (1.0, 0.78, 0.28)
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{W}x{H}", "-r", str(P.FPS), "-i", "-", "-c:v", "qtrle", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(int(total * P.FPS)):
        t = f / P.FPS
        c = cairo.Context(s); c.set_operator(cairo.OPERATOR_CLEAR); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
        if bar:
            c.rectangle(0, 0, W, bar); c.rectangle(0, H - bar, W, bar); c.set_source_rgb(0, 0, 0); c.fill()
        # meka tamna traka iza titlova (citljivost preko belih vodopada)
        band = cairo.LinearGradient(0, cy - size * 2.2, 0, cy + size * 1.6)
        for st_, a_ in ((0, 0), (0.35, 0.42), (0.65, 0.42), (1, 0)):
            band.add_color_stop_rgba(st_, 0, 0, 0, a_)
        c.rectangle(0, cy - size * 2.2, W, size * 3.8); c.set_source(band); c.fill()
        for a0, b0, txt in caps:
            if not (a0 <= t < b0 + 0.25): continue
            al = D.ease((t - a0) / 0.3) * (1 - D.ease((t - b0) / 0.25))
            dy = 18 * (1 - D.ease((t - a0) / 0.4))
            c.select_font_face("DM Serif Display", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
            c.set_font_size(size)
            toks = [(w.replace("*", ""), "*" in w) for w in txt.split()]
            lines, sp = D._balanced(c, toks, W * 0.8)
            lh = size * 1.18
            for li, (words, lw) in enumerate(lines):
                y = cy + dy + (li - (len(lines) - 1) / 2) * lh
                x = W / 2 - lw / 2
                for (w, hl, ww) in words:
                    col = RICH if hl else PALE
                    for r, aa in ((8, 0.10), (4, 0.18), (2, 0.30)):
                        for ox, oy in ((r, r), (-r, r), (0, r), (r, 0)):
                            c.move_to(x + ox * 0.5 + 1, y + oy * 0.5 + 3); c.text_path(w)
                        c.set_source_rgba(0, 0, 0, aa * al); c.fill()
                    c.move_to(x, y); c.set_source_rgba(*col, al); c.show_text(w)
                    if hl:
                        c.move_to(x + 4, y + size * 0.16); c.line_to(x + ww - 4, y + size * 0.16)
                        c.set_source_rgba(*RICH, 0.85 * al); c.set_line_width(3); c.stroke()
                    x += ww + sp
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()


def main(fmt="16x9"):
    W, H = (1920, 1080) if fmt == "16x9" else (1080, 1920)
    parts = [seg(i, n, d, W, H) for i, (n, d) in enumerate(SHOTS)]
    parts.append(P.card_clip(os.path.join(TMP, f"w_end_{W}.mp4"), END_LEN, W, H, "BE LIKE WATER", "FOLLOW FOR MORE"))
    durs = [d for _, d in SHOTS] + [END_LEN]
    # meki prelazi (xfade lanac)
    inputs = sum([["-i", p] for p in parts], []); fc = ""; last = "0:v"; t = durs[0]
    for i in range(1, len(parts)):
        off = t - XF
        fc += f"[{last}][{i}:v]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}];"
        last = f"x{i}"; t = off + durs[i]
    base = os.path.join(TMP, f"w_base_{W}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y"] + inputs + ["-filter_complex", fc.rstrip(";"),
                    "-map", f"[{last}]", "-c:v", "libx264", "-preset", "fast", "-crf", "16", base], check=True)
    total = round(t, 2)
    ep = {"captions": chunks(TALK["segments"])}
    ov = os.path.join(TMP, f"w_cap_{W}.mov"); elegant_overlay(ep["captions"], total, W, H, ov)
    final = os.path.join(OUTDIR, f"be_like_water_{fmt}.mp4"); out = final + ".part.mp4"
    # zvuk: glas (toplina + jasnoca + prostor) + gudaci (ducking) + fade
    fc = (f"[0:v][1:v]overlay=format=auto,noise=alls=5:allf=t,format=yuv420p[v];"
          f"[2:a]aresample=48000,highpass=f=70,equalizer=f=180:t=q:w=1:g=3,equalizer=f=3200:t=q:w=1.2:g=2.5,"
          f"equalizer=f=7500:t=q:w=1:g=-2,acompressor=threshold=-22dB:ratio=3.5:attack=8:release=160:makeup=3,"
          f"aecho=0.85:0.55:45|90|160:0.18|0.12|0.07,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{total},asplit=2[vo][sc];"
          f"[3:a]aresample=48000,atrim=0:{total},asetpts=PTS-STARTPTS,volume=0.9,"
          f"afade=t=in:d=2,afade=t=out:st={total - 4.5}:d=4.5[mu];"
          f"[mu][sc]sidechaincompress=threshold=0.04:ratio=4:attack=40:release=700:makeup=1[duck];"
          f"[vo][duck]amix=inputs=2:weights='1 0.85':normalize=0,loudnorm=I=-14:TP=-1.2:LRA=9[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov, "-i", VOICE, "-i", MUSIC,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "9M", "-bufsize", "18M",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    os.replace(out, final)
    print("OK", os.path.abspath(final), total)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "16x9")
