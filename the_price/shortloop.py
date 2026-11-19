"""Kratki TikTok LOOP klip (7-15 s), quote stil, BEZ ZVUKA.
Pravila: hook od 0. sekunde, tekst <= 8 reci/kadru, smena teksta na 2 s (4 udarca @120 BPM), rez slike na 1 s,
tekst samo u sigurnoj zoni (ne u donjih 20% i desnih 15%), crno-zlatno, SHARE • LIKE • COMMENT FOR MORE ispod
zavrsne poruke, kraj se nadovezuje na pocetak (isti snimak, uzastopni delovi).
Upotreba: python3 shortloop.py <ime>
"""
import os, sys, subprocess
import cairo
import produce as P

D = P.D
W, H, FPS = 1080, 1920, 30
BEAT = 0.5  # 120 BPM
SAFE_R = int(W * 0.85)        # desnih 15% zabranjeno
SAFE_B = int(H * 0.80)        # donjih 20% zabranjeno
CX = (60 + SAFE_R) / 2        # centar sigurne zone
MAXW = SAFE_R - 60 - 40

LOOPS = {
    "discipline": {
        "texts": ["Nobody tells you this about *discipline*…",
                  "It's not about feeling *motivated*.",
                  "It's doing it *anyway*.",
                  "Tired. Bored. *Unseen*.",
                  "Do it *anyway*.",
                  "That's what nobody tells you about *discipline*."],
        # 12 kadara po 1 s; prvi i poslednji iz istog snimka (uzastopno) radi besprekornog loopa
        "loop_src": "01_alarm", "loop_at": 3.0,
        "shots": ["02_wake", "04_runner", "06_bandage", "07_boxer", "09_typing", "08_bag",
                  "11_exhausted", "04_runner", "07_boxer", "12_sunrise"],
        "caption": "Which part hit you the hardest? \U0001F447",
        "tags": "#motivation #discipline #mindset #selfimprovement #nevergiveup",
    },
}
COLD = P.COLD


def shot(i, name, start, d):
    src = os.path.join(P.SRC, name + ".mp4")
    out = os.path.join(P.TMP, f"sl_{i:02d}.mp4")
    z = 0.10 if i % 2 == 0 else 0.06  # punch-in razlicit po kadru
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
          f"scale=w='{W}*(1.04+{z}*t/{d})':h=-2:eval=frame,crop={W}:{H},setsar=1,{COLD},vignette=PI/4,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{start:.2f}", "-t", f"{d:.2f}", "-i", src,
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "15", out], check=True)
    return out


def overlay(texts, total, out):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    per = total / len(texts)
    size = 112
    for f in range(int(round(total * FPS))):
        t = f / FPS
        idx = min(len(texts) - 1, int(t // per)); t0 = idx * per
        c = cairo.Context(s); c.set_operator(cairo.OPERATOR_CLEAR); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
        # tamni sloj iza teksta (citljivost)
        g = cairo.LinearGradient(0, H * 0.25, 0, H * 0.62)
        for st_, a_ in ((0, 0), (0.3, 0.45), (0.7, 0.45), (1, 0)): g.add_color_stop_rgba(st_, 0, 0, 0, a_)
        c.rectangle(0, H * 0.25, W, H * 0.37); c.set_source(g); c.fill()
        # hook je pun od prvog kadra (bez fade-a); ostali: brz pop na udarac
        pop = 1.0 if idx == 0 else D.ease((t - t0) / 0.12)
        sc = 0.9 + 0.1 * pop
        D._face(c, D.QUOTE_FONT, size)
        lines, sp = D._balanced(c, D._tokens(texts[idx]), MAXW)
        lh = size * 1.1; cy = H * 0.43
        c.save(); c.translate(CX, cy); c.scale(sc, sc); c.translate(-CX, -cy)
        for li, (words, lw) in enumerate(lines):
            y = cy + (li - (len(lines) - 1) / 2) * lh + size * 0.35
            x = CX - lw / 2 - sum(12 for (_, h, _) in words if h)
            for (w, hl, ww) in words:
                if hl:
                    x += 12
                    D._rrect(c, x - 12, y - size * 0.86, ww + 24, size * 1.02, 10)
                    c.set_source(D._gold_grad(y - size * 0.86, y + size * 0.16, pop)); c.fill()
                    c.move_to(x, y); c.set_source_rgba(0.04, 0.03, 0.02, pop); c.show_text(w)
                else:
                    D._shadow_text(c, x, y, w, D.GOLD, pop, outline=7)
                x += ww + sp + (12 if hl else 0)
        c.restore()
        if idx == len(texts) - 1:  # stalno pravilo: CTA ispod zavrsne poruke
            ca = D.ease((t - t0 - 0.2) / 0.3)
            D._face(c, D.SANS, 40, bold=True)
            cta = "SHARE  •  LIKE  •  COMMENT FOR MORE"; e = c.text_extents(cta)
            D._shadow_text(c, CX - e.x_advance / 2, cy + len(lines) * lh / 2 + 110, cta, D.GOLD, ca, outline=5)
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()


def make(name):
    v = LOOPS[name]
    n_txt = len(v["texts"]); total = n_txt * 4 * BEAT       # 4 udarca po tekstu
    n_shots = int(round(total / (2 * BEAT)))                 # rez na 2 udarca
    d = total / n_shots
    a = v["loop_at"]
    parts = [shot(0, v["loop_src"], a, d)]                   # pocetak: [a, a+d]
    for i, nm in enumerate(v["shots"][:n_shots - 2], 1):
        L = P.dur(os.path.join(P.SRC, nm + ".mp4"))
        parts.append(shot(i, nm, max(0.2, min(L * (0.25 + 0.07 * i), L - d - 0.1)), d))
    parts.append(shot(n_shots - 1, v["loop_src"], a - d, d))  # kraj: [a-d, a] -> tece pravo u pocetak
    lst = os.path.join(P.TMP, "sl_list.txt")
    with open(lst, "w") as f:
        for q in parts: f.write(f"file '{q}'\n")
    base = os.path.join(P.TMP, "sl_base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", base], check=True)
    ov = os.path.join(P.TMP, "sl_ov.mov"); overlay(v["texts"], total, ov)
    outdir = os.path.join(P.OUTDIR, "..", "tiktok_loops"); os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f"loop_{name}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov,
                    "-filter_complex", "[0:v][1:v]overlay=format=auto,noise=alls=5:allf=t,format=yuv420p[v]",
                    "-map", "[v]", "-an", "-t", f"{total}", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    with open(out.replace(".mp4", "_opis.txt"), "w") as f:
        f.write(v["caption"] + "\n\n" + v["tags"] + "\n")
    print("OK", os.path.abspath(out), total, "s,", n_shots, "kadrova,", n_txt, "tekstova")


if __name__ == "__main__":
    make(sys.argv[1] if len(sys.argv) > 1 else "discipline")
