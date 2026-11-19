"""STOIC RULES generator — jedan dosledan stil serije.
Vreme (10 s, 120 BPM = 0.5 s udarac):
  0.0-2.0  HOOK (pun od 1. frejma)            kadar A (loop izvor, glava)
  2.0-4.5  rečenica 1, reč po reč (1/8 = 0.25 s)  kadar B
  4.5-7.0  rečenica 2                           kadar C
  7.0-9.0  rečenica 3                           kadar D
  9.0-10.0 "Follow for rule #N+1"               kadar A (rep, teče pravo u početak)
Stil: tamno-hladni filmski kolor, zrno, vinjeta, blagi zoom; beli Poppins Bold sa mekom senkom; "Stoic rule #N" gore levo.
Tekst samo u sigurnoj zoni (ne u donjih 20% ni desnih 15%). Bez zvuka.
Upotreba: python3 stoic/make.py 1 [2 3 ...]
"""
import os, sys, math, json, subprocess
import cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from rules import RULES

W, H, FPS = 1080, 1920, 30
SAFE_R, SAFE_B = int(W * 0.85), int(H * 0.80)
CX = (70 + SAFE_R) / 2; MAXW = SAFE_R - 70 - 50
TMP = os.path.join(HERE, "out"); OUT = os.path.join(ROOT, "videos", "stoic")
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
CTA = "Follow for rule #{n}"  # youtube.py menja u "Subscribe for rule #{n}"
SEG = [(0.0, 2.0), (2.0, 4.5), (4.5, 7.0), (7.0, 9.0), (9.0, 10.0)]
TOTAL = 10.0; WORD = 0.25
FONT = "Poppins"
GRADE = ("colortemperature=temperature=7800:pl=0.5,eq=saturation=0.68:contrast=1.12:brightness=-0.02,"
         "colorbalance=rs=-0.05:gs=0.0:bs=0.09:rm=-0.03:bm=0.04:rh=0.02:bh=-0.01,"
         "curves=all='0/0.04 0.5/0.47 1/0.96'")


def src(n): return os.path.join(HERE, "src", n + ".mp4")


def render_shot(out, name, start, d, xc, z0, z1, extra=""):
    vf = (f"scale=-2:{H}:flags=lanczos,crop={W}:{H}:x='(iw-{W})*{xc}':y=0,fps={FPS},{GRADE}" + ("," + extra if extra else "") + ","
          f"scale=w='{W}*({z0}+({z1}-{z0})*t/{d})':h=-2:eval=frame:flags=bicubic,crop={W}:{H},setsar=1,"
          f"vignette=PI/4.5,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{d:.3f}", "-i", src(name),
                    "-vf", vf, "-an", "-r", str(FPS), "-frames:v", str(int(round(d * FPS))), "-c:v", "libx264", "-preset", "fast", "-crf", "14", out], check=True)


def cut(src_, out, ss, d):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", src_, "-ss", f"{ss}", "-frames:v", str(int(round(d * FPS))), "-an",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "14", out], check=True)


def face(c, size, weight=cairo.FONT_WEIGHT_BOLD):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, weight); c.set_font_size(size)


def wrap(c, words, maxw):
    W_ = lambda ws: c.text_extents(" ".join(ws)).x_advance
    if W_(words) <= maxw: return [words]
    best = None
    for i in range(1, len(words)):  # 2 reda: minimizuj širi red
        a, b = words[:i], words[i:]
        if max(W_(a), W_(b)) <= maxw and (best is None or max(W_(a), W_(b)) < best[0]): best = (max(W_(a), W_(b)), [a, b])
    if best: return best[1]
    return wrap_greedy(c, words, maxw)


def balance3(c, words, maxw):  # 3 reda bez siročeta: minimizuj najširi red
    W_ = lambda ws: c.text_extents(" ".join(ws)).x_advance
    best = None
    for i in range(1, len(words) - 1):
        for j in range(i + 1, len(words)):
            ls = [words[:i], words[i:j], words[j:]]
            m = max(W_(x) for x in ls)
            if best is None or m < best[0]: best = (m, ls)
    return best[1]


def wrap_greedy(c, words, maxw):
    lines, cur = [], []
    for w in words:
        t = " ".join(cur + [w])
        if cur and c.text_extents(t).x_advance > maxw: lines.append(cur); cur = [w]
        else: cur.append(w)
    if cur: lines.append(cur)
    # izbalansiraj 2 reda (izbegni jednu reč u drugom redu)
    if len(lines) == 2 and len(lines[1]) == 1 and len(lines[0]) > 2:
        lines = [lines[0][:-1], [lines[0][-1]] + lines[1]]
    return lines


def shadow_text(c, x, y, s, a):
    for dx, dy, al in ((0, 4, 0.55), (0, 2, 0.6), (2, 3, 0.35), (-2, 3, 0.35)):  # meka senka
        c.move_to(x + dx, y + dy); c.set_source_rgba(0, 0, 0, al * a); c.show_text(s)
    c.move_to(x, y); c.set_source_rgba(1, 1, 1, a); c.show_text(s)


BOXES = []


def draw_block(c, text, t_rel, size, reveal, cy=H * 0.43):
    words = text.split()
    for sz in range(size, int(size * 0.84) - 1, -2):  # najveći font koji staje u <=2 reda
        face(c, sz); lines = wrap(c, words, MAXW)
        if len(lines) <= 2: break
    size = sz
    if len(lines) > 2: lines = balance3(c, words, MAXW)
    sp = c.text_extents(" ").x_advance; lh = size * 1.18
    k = 0
    for li, ln in enumerate(lines):
        lw = c.text_extents(" ".join(ln)).x_advance
        x = CX - lw / 2; y = cy + (li - (len(lines) - 1) / 2) * lh + size * 0.35
        BOXES.append((x, y - size * 0.8, x + lw, y + size * 0.25))
        for w in ln:
            if reveal:
                p = max(0.0, min(1.0, (t_rel - k * WORD) / 0.14))
                a = p; dy = 10 * (1 - p)
            else:
                a, dy = 1.0, 0
            if a > 0: shadow_text(c, x, y + dy, w, a)
            x += c.text_extents(w).x_advance + sp; k += 1


def overlay(r, n, path):
    # jedinstvena veličina za sve 3 rečenice pravila (dosledan raspored serije) = najveća koja svakoj daje <=2 reda
    tmp = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)); rs = 84
    while rs > 64:
        face(tmp, rs)
        if all(len(wrap(tmp, x.split(), MAXW)) <= 2 for x in r["rule"]): break
        rs -= 2
    texts = [(r["hook"], False, 104)] + [(s, True, rs) for s in r["rule"]] + [(CTA.format(n=n + 1), False, 74)]
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "qtrle", path], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(int(TOTAL * FPS)):
        t = f / FPS
        i = next(k for k, (a, b) in enumerate(SEG) if a <= t < b or k == len(SEG) - 1)
        c = cairo.Context(s); c.set_operator(cairo.OPERATOR_CLEAR); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
        # blaga tamna traka iza teksta (čitljivost na svetlim kadrovima)
        g = cairo.LinearGradient(0, H * 0.27, 0, H * 0.60)
        for st, al in ((0, 0), (0.35, 0.32), (0.65, 0.32), (1, 0)): g.add_color_stop_rgba(st, 0, 0, 0, al)
        c.rectangle(0, H * 0.27, W, H * 0.33); c.set_source(g); c.fill()
        txt, rev, size = texts[i]
        draw_block(c, txt, t - SEG[i][0], size, rev)
        # oznaka serije gore levo
        face(c, 34, cairo.FONT_WEIGHT_BOLD); tag = f"STOIC RULE #{n}"
        c.move_to(64, 262); c.set_source_rgba(0, 0, 0, 0.5); c.show_text(tag)
        c.move_to(62, 260); c.set_source_rgba(1, 1, 1, 0.82); c.show_text(tag)
        if f == 0: BOXES.append((62, 228, 62 + c.text_extents(tag).x_advance, 268))
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()


def make(n):
    r = RULES[n]; BOXES.clear()
    lname, lx, a = r["loop"]
    full = os.path.join(TMP, f"r{n}_loop.mp4")
    render_shot(full, lname, a - 1.0, 3.0, lx, 1.00, 1.06, r.get("loop_extra", ""))            # kontinualno [a-1, a+2]
    head, tail = os.path.join(TMP, f"r{n}_head.mp4"), os.path.join(TMP, f"r{n}_tail.mp4")
    cut(full, head, 1.0, 2.0); cut(full, tail, 0.0, 1.0)
    parts = [head]
    for k, sh in enumerate(r["shots"], 1):
        nm, xc, st = sh[:3]; extra = sh[3] if len(sh) > 3 else ""
        d = SEG[k][1] - SEG[k][0]; o = os.path.join(TMP, f"r{n}_{k}.mp4")
        render_shot(o, nm, st, d, xc, 1.00, 1.05, extra); parts.append(o)
    parts.append(tail)
    lst = os.path.join(TMP, f"r{n}_list.txt"); open(lst, "w").write("".join(f"file '{q}'\n" for q in parts))
    base = os.path.join(TMP, f"r{n}_base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], check=True)
    ov = os.path.join(TMP, f"r{n}_ov.mov"); overlay(r, n, ov)
    out = os.path.join(OUT, f"stoic_rule_{n:02d}.mp4"); part = out.replace(".mp4", ".part.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov, "-filter_complex",
                    "[0:v][1:v]overlay=format=auto,noise=alls=7:allf=t,format=yuv420p[v]", "-map", "[v]", "-an", "-tune", "grain", "-maxrate", "22M", "-bufsize", "44M",
                    "-t", f"{TOTAL}", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", part], check=True)
    os.replace(part, out)
    open(out.replace(".mp4", "_opis.txt"), "w").write(
        f"{r['caption']} \U0001F447\n\n{r['tags']}\n\nZvuk (dodaješ u TikTok-u): {r['sound']}\n")
    safe = all(x0 >= 0 and y0 >= 0 and x1 <= SAFE_R and y1 <= SAFE_B for x0, y0, x1, y1 in BOXES)
    words = max(len(s.split()) for s in r["rule"])
    chk = {"tekst_u_sigurnoj_zoni": safe, "max_reci_u_recenici": words, "recenica": len(r["rule"])}
    json.dump(chk, open(out.replace(".mp4", "_plan_provera.json"), "w"), indent=1)
    print(out, chk)
    return out


if __name__ == "__main__":
    for x in sys.argv[1:] or ["1"]:
        make(int(x))
