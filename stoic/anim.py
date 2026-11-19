"""STOIC ANIMACIJA — sopstveni crtani stil za naše stoičke priče (odluka korisnika 19.11.: "držimo se naših priča, ali animirano").
Stil (NAŠ, nije kopija tuđeg kanala): ravne boje, debela tamnoplava kontura, prigušena noćna paleta sa toplim akcentom,
lik "Stoik" (ogrtač sa kapuljačom, kratka brada, oštre obrve), paralaksa pozadina, čestice (sneg, prašina), blago zrno.
Zvuk: samo glas (George), tekst preko ekrana kao u Shorts šablonu, kraj "Share, like & comment".
Upotreba: python3 stoic/anim.py <ime_epizode>   (epizode su u ANIM dole)
"""
import os, sys, math, random, subprocess, wave
import numpy as np, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make as M
import youtube as YT

W, H, FPS = 1080, 1920, 30
INK = (0.09, 0.11, 0.17)
OUT = os.path.join(ROOT, "videos", "stoic_anim")


def hexc(h, a=1.0):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)


def fill(c, h, a=1.0): c.set_source_rgba(*hexc(h, a))


def ink(c, lw=7):
    c.set_source_rgba(*INK, 1); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)


def shape(c, h, lw=7, a=1.0):
    fill(c, h, a); c.fill_preserve(); ink(c, lw); c.stroke()


def grad(c, y0, y1, stops):
    g = cairo.LinearGradient(0, y0, 0, y1)
    for s, h in stops: g.add_color_stop_rgba(s, *hexc(h))
    return g


def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()


# ---------------- lik: STOIK ----------------
CLOAK, CLOAK2, SKIN, BEARD, BOOT = "#3d4f63", "#2c3a4a", "#e2b38f", "#4a3426", "#2a2320"


def limb(c, x0, y0, ang, l1, ang2, l2, w, color):
    x1, y1 = x0 + math.sin(ang) * l1, y0 + math.cos(ang) * l1
    x2, y2 = x1 + math.sin(ang + ang2) * l2, y1 + math.cos(ang + ang2) * l2
    for lw, col in ((w + 12, None), (w, color)):
        c.move_to(x0, y0); c.line_to(x1, y1); c.line_to(x2, y2)
        if col is None: c.set_source_rgba(*INK, 1)
        else: fill(c, col)
        c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    return x2, y2


def stoic(c, x, y, s, t, pose="stand", walk=0.0, lean=0.0, look=0.0, hood=True, glow=None, wind=0.0, blink_seed=1,
          beard=BEARD, cloak=None, laurel=False, hair=None, arms=None):
    """x,y = tačka između stopala. pose: stand | walk | sit | lie | climb"""
    c.save(); c.translate(x, y); c.scale(s, s)
    if pose == "lie":
        c.rotate(-math.pi / 2); c.translate(-40, 0)
    c.rotate(lean)
    ph = t * 2 * math.pi * (1.4 if pose != "climb" else 1.0)
    sw = math.sin(ph) * walk
    hip_y = -230
    # noge
    if pose in ("stand", "walk", "climb", "lie"):
        a1, a2 = 0.45 * sw + (0.09 if walk == 0 else 0), -0.45 * sw - (0.09 if walk == 0 else 0)  # stav: noge malo raširene
        k1, k2 = max(0, -sw) * 0.6, max(0, sw) * 0.6
        if pose == "climb": a1, a2, k1, k2 = 0.5 + 0.35 * math.sin(ph), -0.2 - 0.35 * math.sin(ph), -0.5, -0.5
        for a, k in ((a2, k2), (a1, k1)):
            fx, fy = limb(c, 0, hip_y, a, 120, -k, 115, 34, "#30343c")
            c.save(); c.translate(fx, fy); c.rotate(-(a - k) * 0.5)
            rrect(c, -18, -14, 56, 30, 12); shape(c, BOOT, 6); c.restore()
    elif pose == "sit":
        for dx in (-18, 18):
            limb(c, dx, hip_y + 10, -1.45, 120, 1.45, 110, 34, "#30343c")
    # ogrtač (trup)
    flap = math.sin(t * 5.0) * 10 * wind + wind * 25
    c.move_to(-70, -470); c.curve_to(-95, -380, -100, -280, -92 - flap * 0.5, hip_y + 40)
    c.line_to(92 - flap, hip_y + 40 + flap * 0.3); c.curve_to(100, -280, 95, -380, 70, -470); c.close_path()
    c1, c2 = cloak or (CLOAK, CLOAK2)
    g = cairo.LinearGradient(-90, 0, 90, 0); g.add_color_stop_rgb(0, *hexc(c1)[:3]); g.add_color_stop_rgb(1, *hexc(c2)[:3])
    c.set_source(g); c.fill_preserve(); ink(c, 8); c.stroke()
    # pojas
    c.move_to(-88, -300); c.line_to(88, -300); ink(c, 10); c.stroke()
    # ruke
    if pose == "climb":
        arm = [(-1.9 + 0.4 * math.sin(ph), -0.4), (-2.6 - 0.4 * math.sin(ph), 0.3)]
    elif pose == "sit":
        arm = [(0.6, -1.2), (-0.6, 1.2)]
    elif pose == "lie":
        arm = [(0.2, 0.1), (-0.2, -0.1)]
    else:
        arm = [(-0.35 * sw + 0.1, -0.3), (0.35 * sw - 0.1, 0.3)]
    if arms: arm = arms(t) if callable(arms) else arms
    for side, (a, b) in zip((-1, 1), arm):
        hx, hy = limb(c, side * 72, -440, a * side if pose != "climb" else a, 105, b, 95, 30, (cloak or (CLOAK,))[0])
        c.arc(hx, hy, 17, 0, 2 * math.pi); shape(c, SKIN, 6)
    # glava
    hx, hy = 0, -535
    c.arc(hx, hy, 72, 0, 2 * math.pi); shape(c, SKIN, 8)
    if hair:  # kosa (kad nema kapuljače)
        c.move_to(hx - 72, hy - 5); c.curve_to(hx - 80, hy - 95, hx + 80, hy - 95, hx + 72, hy - 5)
        c.curve_to(hx + 50, hy - 50, hx - 50, hy - 50, hx - 72, hy - 5); shape(c, hair, 6)
    if beard:  # brada
        c.move_to(hx - 62, hy + 5); c.curve_to(hx - 55, hy + 85, hx + 55, hy + 85, hx + 62, hy + 5)
        c.curve_to(hx + 35, hy + 30, hx - 35, hy + 30, hx - 62, hy + 5); shape(c, beard, 6)
    # oči (treptanje)
    rnd = random.Random(blink_seed); bl = (t * 0.6 + rnd.random()) % 3.2 < 0.12
    ex = look * 10
    for dx in (-26, 26):
        if bl:
            c.move_to(hx + dx - 9 + ex, hy - 12); c.line_to(hx + dx + 9 + ex, hy - 12); ink(c, 6); c.stroke()
        else:
            c.arc(hx + dx + ex, hy - 12, 8, 0, 2 * math.pi); c.set_source_rgba(*INK, 1); c.fill()
        # obrve (oštre)
        c.move_to(hx + dx - 16 + ex, hy - 34 + (4 if dx < 0 else 0)); c.line_to(hx + dx + 14 + ex, hy - 34 + (0 if dx < 0 else 4)); ink(c, 7); c.stroke()
    # kapuljača
    if hood:
        c.move_to(hx - 92, hy + 40); c.curve_to(hx - 110, hy - 70, hx - 50, hy - 118, hx, hy - 118)
        c.curve_to(hx + 50, hy - 118, hx + 110, hy - 70, hx + 92, hy + 40)
        c.curve_to(hx + 80, hy - 40, hx + 55, hy - 88, hx, hy - 90)
        c.curve_to(hx - 55, hy - 88, hx - 80, hy - 40, hx - 92, hy + 40); c.close_path(); shape(c, CLOAK2, 8)
    if laurel:  # lovorov venac (car)
        for side in (-1, 1):
            for k in range(6):
                ang = math.pi * (0.95 + side * 0.0) + side * (0.25 + k * 0.17)
                lx, ly = hx + math.cos(ang) * 74 * side * -1, hy - 30 + math.sin(ang) * -40 - k * 6
                c.save(); c.translate(hx + side * (40 + k * 7), hy - 58 + k * 9); c.rotate(side * (0.9 - k * 0.12))
                c.scale(1, 0.45); c.arc(0, 0, 17, 0, 2 * math.pi); c.restore(); shape(c, "#7a9a3a", 4)
    if glow:  # plavi sjaj ekrana na licu
        g = cairo.RadialGradient(hx, hy + 40, 10, hx, hy + 40, 160); g.add_color_stop_rgba(0, *hexc(glow, 0.45)); g.add_color_stop_rgba(1, *hexc(glow, 0))
        c.arc(hx, hy, 150, 0, 2 * math.pi); c.set_source(g); c.fill()
    c.restore()


# ---------------- pozadine ----------------
def stars(c, t, n=90, seed=2, top=0, bottom=900):
    r = random.Random(seed)
    for i in range(n):
        x, y = r.uniform(0, W), r.uniform(top, bottom); a = 0.3 + 0.7 * abs(math.sin(t * 1.3 + i))
        c.arc(x, y, r.uniform(1.5, 3.5), 0, 2 * math.pi); c.set_source_rgba(1, 1, 0.92, a * 0.8); c.fill()


def mountains(c, base, color, seed, amp, n=7, snow=False, xoff=0.0):
    r = random.Random(seed); pts = []
    step = W / (n - 1)
    for i in range(-1, n + 2):
        pts.append((i * step + xoff % step - step, base - r.uniform(0.35, 1.0) * amp))
    c.move_to(-200, H + 50)
    for i, (x, y) in enumerate(pts):
        c.line_to(x, y)
        if i < len(pts) - 1: c.line_to((x + pts[i + 1][0]) / 2, base - amp * 0.15)
    c.line_to(W + 200, H + 50); c.close_path(); fill(c, color); c.fill_preserve(); ink(c, 6); c.stroke()
    if snow:
        for x, y in pts:
            c.move_to(x - 55, y + 60); c.line_to(x, y); c.line_to(x + 55, y + 60)
            c.line_to(x + 25, y + 48); c.line_to(x, y + 70); c.line_to(x - 25, y + 48); c.close_path(); fill(c, "#e8eef5"); c.fill()


def snowfall(c, t, n=160, wind=2.0, seed=5, speed=260):
    r = random.Random(seed)
    for i in range(n):
        x0, y0, z = r.uniform(-200, W + 200), r.uniform(0, H), r.uniform(0.4, 1.4)
        y = (y0 + t * speed * z) % (H + 40) - 20; x = (x0 + t * speed * wind * 0.45 * z + math.sin(t * 2 + i) * 12) % (W + 400) - 200
        c.arc(x, y, 3 + 4 * z, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 0.55 + 0.3 * (z - 0.4)); c.fill()


# ---------------- scene epizode "comfort" (Short #4) ----------------
def sc_couch(c, t, d):
    """Hook: čovek tone u ogroman mekan kauč, plavi sjaj telefona, kamera se primiče."""
    c.save(); z = 1.0 + 0.10 * ease(t / d); c.translate(W / 2, H * 0.62); c.scale(z, z); c.translate(-W / 2, -H * 0.62)
    c.rectangle(-100, -100, W + 200, H + 200); c.set_source(grad(c, 0, H, [(0, "#1b2233"), (1, "#0e121c")])); c.fill()
    # prozor sa noćnim gradom
    rrect(c, 640, 330, 320, 420, 18); shape(c, "#1e2a44", 8)
    for i in range(14):
        r = random.Random(i); bx = 660 + r.uniform(0, 270); bh = r.uniform(80, 300)
        c.rectangle(bx, 750 - bh, r.uniform(26, 50), bh); fill(c, "#141c2e"); c.fill()
        for k in range(4):
            if (i + k) % 3 == 0: c.rectangle(bx + 8, 760 - bh + 20 + k * 40, 8, 12); fill(c, "#f2c66d", 0.8); c.fill()
    c.move_to(800, 330); c.line_to(800, 750); c.move_to(640, 540); c.line_to(960, 540); ink(c, 8); c.stroke()
    # pod
    c.rectangle(-100, 1420, W + 200, 700); fill(c, "#202634"); c.fill()
    sink = 60 * ease(t / d)
    # kauč (ogroman, mekan)
    rrect(c, 90, 980, 900, 360, 120); shape(c, "#6b4a8a", 9)            # naslon
    stoic(c, 520, 1430 + sink, 1.0, t, pose="sit", glow="#5ec8ff", look=0.6)
    rrect(c, 60, 1180 + sink * 0.4, 960, 300, 110); shape(c, "#7d58a0", 9)  # sedište preko nogu
    for x in (60, 870): rrect(c, x, 1080, 150, 380, 75); shape(c, "#6b4a8a", 9)  # naslon za ruke
    # telefon u ruci
    c.save(); c.translate(620, 1010 + sink); c.rotate(-0.25); rrect(c, -34, -60, 68, 120, 12); shape(c, "#11151d", 6)
    rrect(c, -26, -50, 52, 100, 8); fill(c, "#5ec8ff", 0.9 + 0.1 * math.sin(t * 9)); c.fill(); c.restore()
    c.restore()


def sc_days(c, t, d):
    """Lagani dani: sat se vrti, sunce i mesec se smenjuju u prozoru, čovek leži u krevetu."""
    cyc = (t * 1.6) % 1.0; day = math.sin(cyc * math.pi)
    top = tuple(np.array(hexc("#14203a")[:3]) * (1 - day) + np.array(hexc("#7fb2e5")[:3]) * day)
    c.rectangle(0, 0, W, H); fill(c, "#262c3b"); c.fill()
    rrect(c, 120, 300, 840, 520, 22); c.set_source_rgb(*top); c.fill_preserve(); ink(c, 9); c.stroke()
    ang = cyc * math.pi; sx, sy = 540 - math.cos(ang) * 330, 760 - math.sin(ang) * 360
    c.arc(sx, sy, 55, 0, 2 * math.pi); fill(c, "#ffd25e" if day > 0.25 else "#e9edf5"); c.fill()
    c.move_to(540, 300); c.line_to(540, 820); ink(c, 9); c.stroke()
    # sat na zidu
    cx, cy = 540, 1000
    c.arc(cx, cy, 95, 0, 2 * math.pi); shape(c, "#efe6d2", 8)
    for k, (l, sp) in enumerate(((60, 12.0), (80, 70.0))):
        a = t * sp * (1 + k); c.move_to(cx, cy); c.line_to(cx + math.sin(a) * l, cy - math.cos(a) * l); ink(c, 9 - 3 * k); c.stroke()
    # krevet + čovek
    rrect(c, 80, 1360, 920, 200, 30); shape(c, "#5a6b80", 9)
    rrect(c, 110, 1250, 230, 130, 50); shape(c, "#e6e9ef", 7)     # jastuk
    # glava na jastuku (lik leži; telo pod pokrivačem)
    hx, hy = 230, 1255
    c.arc(hx, hy, 66, 0, 2 * math.pi); shape(c, SKIN, 8)
    c.move_to(hx - 55, hy + 10); c.curve_to(hx - 45, hy + 80, hx + 45, hy + 80, hx + 55, hy + 10); c.curve_to(hx + 30, hy + 30, hx - 30, hy + 30, hx - 55, hy + 10); shape(c, BEARD, 6)
    for dx in (-24, 24):  # zatvorene oči (spava)
        c.move_to(hx + dx - 10, hy - 10); c.curve_to(hx + dx - 4, hy - 2, hx + dx + 4, hy - 2, hx + dx + 10, hy - 10); ink(c, 6); c.stroke()
    c.move_to(hx + 70, hy - 90); c.show_text("")
    for k in range(3):  # "z z z"
        zz = (t * 0.8 + k * 0.33) % 1.0
        M.face(c, 40 + k * 10); c.move_to(hx + 70 + zz * 90, hy - 80 - zz * 160 - k * 10); c.set_source_rgba(0.9, 0.92, 1, 1 - zz); c.show_text("z")
    rrect(c, 290, 1270, 710, 150, 60); shape(c, "#9aa9bd", 9)  # pokrivač
    # kalendar listovi lete
    for i in range(5):
        p = (t * 0.9 + i * 0.2) % 1.0
        x, y = 870 + p * 220, 1130 - p * 520 + math.sin(p * 9 + i) * 30
        c.save(); c.translate(x, y); c.rotate(p * 4 + i); rrect(c, -40, -48, 80, 96, 8); shape(c, "#f4efe4", 5, 1 - p)
        c.restore()


def sc_snow_road(c, t, d):
    """Hladan, težak put: čovek hoda uz vetar po snežnom putu, paralaksa planina."""
    c.rectangle(0, 0, W, H); c.set_source(grad(c, 0, H, [(0, "#5d7391"), (0.6, "#a9bccf"), (1, "#dfe7ee")])); c.fill()
    mountains(c, 1050, "#7b8fa8", 11, 420, xoff=-t * 20, snow=True)
    mountains(c, 1250, "#5f7390", 12, 300, n=6, xoff=-t * 55, snow=True)
    # put (nagnut)
    c.move_to(-50, 1700); c.line_to(1150, 1380); c.line_to(1150, H + 50); c.line_to(-50, H + 50); c.close_path(); shape(c, "#e9eff5", 8)
    for i in range(8):  # tragovi
        x = (i * 160 - t * 160) % 1300 - 100; y = 1700 - (x + 50) * 0.267 + 40
        c.save(); c.translate(x, y); c.scale(1, 0.4); c.arc(0, 0, 18, 0, 2 * math.pi); fill(c, "#c3cfda"); c.fill(); c.restore()
    stoic(c, 520, 1585, 0.95, t, pose="walk", walk=0.9, lean=0.12, wind=1.0, look=0.3)
    snowfall(c, t, wind=-2.2)


def sc_climb(c, t, d):
    """Nastavi kad boli: strma litica, čovek se penje, sunce izlazi iza vrha."""
    rise = ease(t / d)
    c.rectangle(0, 0, W, H); c.set_source(grad(c, 0, H, [(0, "#2a3557"), (0.45, "#e0846b"), (0.75, "#f5c48a"), (1, "#f5c48a")])); c.fill()
    c.arc(700, 760 - 180 * rise, 150, 0, 2 * math.pi); fill(c, "#ffe2a3", 0.95); c.fill()
    mountains(c, 1000, "#56506e", 21, 300, snow=True)
    # litica
    c.move_to(-50, H + 50); c.line_to(-50, 900); c.line_to(260, 760); c.line_to(560, 980); c.line_to(820, 1400); c.line_to(1150, 1650); c.line_to(1150, H + 50)
    c.close_path(); shape(c, "#3b3550", 9)
    p = 0.15 + 0.55 * ease(t / d)   # stopala na ivici litice (820,1400) -> (560,980) -> (260,760)
    pts = [(820, 1400), (560, 980), (260, 760)]; q = p * 2; k = min(1, int(q)); f = q - k
    x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f; y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f
    stoic(c, x + 10, y + 8, 0.7, t, pose="climb", lean=-0.45, look=-0.4)
    snowfall(c, t, n=60, wind=-1.2, speed=180)


def sc_summit(c, t, d):
    """Kraj: čovek stoji na vrhu, izlazak sunca, ogrtač se vijori."""
    c.rectangle(0, 0, W, H); c.set_source(grad(c, 0, H, [(0, "#3b4f7a"), (0.5, "#f0a77c"), (1, "#ffd9a0")])); c.fill()
    c.arc(540, 880, 230, 0, 2 * math.pi); fill(c, "#fff0c2", 0.9); c.fill()
    for k in range(12):
        a = k * math.pi / 6 + t * 0.2; c.move_to(540 + math.cos(a) * 260, 880 + math.sin(a) * 260); c.line_to(540 + math.cos(a) * 420, 880 + math.sin(a) * 420)
        c.set_source_rgba(1, 0.95, 0.8, 0.35); c.set_line_width(14); c.stroke()
    mountains(c, 1350, "#6e5d7e", 31, 250, snow=True)
    c.move_to(-50, H + 50); c.line_to(300, 1330); c.line_to(540, 1250); c.line_to(780, 1330); c.line_to(1130, H + 50); c.close_path(); shape(c, "#3b3550", 9)
    stoic(c, 540, 1265, 0.75, t, pose="stand", wind=1.2)


ANIM = {
    "comfort": {"rule": 4, "scenes": [sc_couch, sc_days, sc_snow_road, sc_climb, sc_summit]},
}


def build(name):
    ep = ANIM[name]; r = dict(YT.RULES[ep["rule"]]); r.update(YT.YT_FOOTAGE.get(ep["rule"], {}))
    os.makedirs(OUT, exist_ok=True)
    # glas -> segmenti (isti šablon kao Shorts)
    clips = YT.voice_lines(r, ep["rule"])
    segs, t = [], 0.0
    for i, a in enumerate(clips):
        d = max(2.0 if i == 0 else 1.25, math.ceil((YT.LEAD + len(a) / 24000 + YT.PAD) / YT.BEAT) * YT.BEAT)
        segs.append((t, t + d)); t += d
    M.SEG, M.TOTAL, M.WORD = segs, t, 0.22
    texts = [r["hook"]] + r["rule"] + ["Share, like & comment"]
    vt = np.zeros(int(t * 24000) + 24000)
    for (s0, _), a in zip(segs, clips):
        i0 = int((s0 + YT.LEAD) * 24000); vt[i0:i0 + len(a)] += a
    vw = os.path.join(M.TMP, f"anim_{name}_voice.wav")
    with wave.open(vw, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
        w.writeframes((vt[:int(t * 24000)] / (np.abs(vt).max() + 1e-9) * 0.9 * 32767).astype(np.int16).tobytes())
    out = os.path.join(OUT, f"{name}.mp4")
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-i", vw,
                          "-filter_complex", "[0:v]noise=alls=5:allf=t,vignette=PI/5,format=yuv420p[v];"
                          "[1:a]aresample=48000,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
                          "aecho=0.8:0.5:40|75:0.12|0.07,pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=7[a]",
                          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                          "-c:a", "aac", "-b:a", "192k", "-t", f"{t:.3f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(int(round(t * FPS))):
        tt = f / FPS
        i = next(k for k, (a, b) in enumerate(segs) if a <= tt < b or k == len(segs) - 1)
        c = cairo.Context(s)
        ep["scenes"][i](c, tt - segs[i][0], segs[i][1] - segs[i][0])
        # tekst gore (lik je u donjoj polovini)
        g = cairo.LinearGradient(0, H * 0.13, 0, H * 0.36)
        for st, al in ((0, 0), (0.3, 0.35), (0.7, 0.35), (1, 0)): g.add_color_stop_rgba(st, 0, 0, 0, al)
        c.rectangle(0, H * 0.13, W, H * 0.23); c.set_source(g); c.fill()
        size = 100 if i == 0 else (74 if i == len(segs) - 1 else 80)
        M.draw_block(c, texts[i], tt - segs[i][0], size, 0 < i < len(segs) - 1, cy=H * 0.245)
        # pretapanje između scena (kratko, 4 frejma)
        for (a, b) in segs[1:]:
            if 0 <= tt - a < 0.13:
                c.rectangle(0, 0, W, H); c.set_source_rgba(0.05, 0.06, 0.1, 1 - (tt - a) / 0.13); c.fill()
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()
    print(out, f"{t:.2f}s")
    return out


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "comfort")
