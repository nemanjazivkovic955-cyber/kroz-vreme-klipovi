"""STOIC ANIMACIJA — dugi video 16:9 (1920x1080) po naraciji (stoic/narrate.py -> timing.json).
Isti sopstveni crtani stil kao stoic/anim.py (lik Stoik, debela kontura, noćna paleta sa toplim akcentom).
Svaki pasus naracije = jedna scena (lista SHOTS po poglavljima), kamera se polako kreće, titlovi dole, kartica poglavlja.
Zvuk: samo glas (George). Upotreba: python3 stoic/anim_long.py ep02
"""
import os, sys, math, random, json, subprocess
import numpy as np, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import anim as A
from anim import fill, ink, shape, grad, ease, rrect, stoic, hexc, SKIN

W, H, FPS = 1920, 1080, 30
A.W, A.H = W, H   # pomoćne funkcije iz anim.py crtaju u 16:9
EMP = dict(hood=False, laurel=True, hair="#4a3426", cloak=("#7a2b2b", "#5c1f22"))       # car Marko (purpurni ogrtač)
EMP_OLD = dict(hood=False, laurel=True, hair="#9a9a9a", beard="#b9b9b9", cloak=("#7a2b2b", "#5c1f22"))
BOY = dict(hood=False, beard=None, hair="#4a3426", cloak=("#b8a27a", "#9c8862"))
HADRIAN = dict(hood=False, laurel=True, hair="#d9d9d9", beard="#e6e6e6", cloak=("#6b3f7a", "#4f2d5c"))
ANTONINUS = dict(hood=False, laurel=False, hair="#8c8c8c", beard="#9e9e9e", cloak=("#4e6a8a", "#3b5270"))
SOLDIER = dict(hood=False, beard="#3a2a20", hair="#3a2a20", cloak=("#8a3a2a", "#6a2a20"))
MODERN = dict(hood=True, beard=None, cloak=("#2f3a48", "#232c38"))


def R(seed): return random.Random(seed)


# ---------------- pozadinski elementi ----------------
def sky(c, stops): c.rectangle(-200, -200, W + 400, H + 400); c.set_source(grad(c, 0, H, stops)); c.fill()


def stars(c, t, n=120, seed=3, bottom=600):
    r = R(seed)
    for i in range(n):
        x, y = r.uniform(0, W), r.uniform(0, bottom); a = 0.3 + 0.7 * abs(math.sin(t * 1.1 + i))
        c.arc(x, y, r.uniform(1.2, 3.0), 0, 2 * math.pi); c.set_source_rgba(1, 1, 0.92, a * 0.8); c.fill()


def ground(c, y, color, wave=18, seed=1):
    r = R(seed); c.move_to(-200, H + 200); c.line_to(-200, y)
    for i in range(13): c.line_to(i * 170, y + r.uniform(-wave, wave))
    c.line_to(W + 200, y); c.line_to(W + 200, H + 200); c.close_path(); shape(c, color, 7)


def tent(c, x, y, s, color="#b39a72", glow=0.0, door=True):
    c.move_to(x - 160 * s, y); c.line_to(x, y - 190 * s); c.line_to(x + 160 * s, y); c.close_path(); shape(c, color, 7)
    if door:
        c.move_to(x - 45 * s, y); c.line_to(x, y - 120 * s); c.line_to(x + 45 * s, y); c.close_path()
        shape(c, "#ffcf7a" if glow > 0 else "#3a2f24", 5, 1.0)
    if glow:
        g = cairo.RadialGradient(x, y - 60 * s, 5, x, y - 60 * s, 260 * s); g.add_color_stop_rgba(0, 1, 0.8, 0.45, 0.45 * glow); g.add_color_stop_rgba(1, 1, 0.8, 0.45, 0)
        c.arc(x, y - 60 * s, 260 * s, 0, 2 * math.pi); c.set_source(g); c.fill()


def fire(c, x, y, s, t):
    for i, (dx, h, col) in enumerate(((-18, 70, "#e8562a"), (16, 60, "#f08a2c"), (0, 95, "#ffb43a"), (0, 50, "#ffe27a"))):
        f = 1 + 0.15 * math.sin(t * 9 + i * 2)
        c.move_to(x + (dx - 26) * s, y); c.curve_to(x + (dx - 30) * s, y - h * 0.6 * s * f, x + dx * s, y - h * 0.8 * s * f, x + dx * s, y - h * s * f)
        c.curve_to(x + dx * s, y - h * 0.8 * s * f, x + (dx + 30) * s, y - h * 0.6 * s * f, x + (dx + 26) * s, y); c.close_path(); fill(c, col); c.fill()
    g = cairo.RadialGradient(x, y - 40 * s, 5, x, y - 40 * s, 300 * s); g.add_color_stop_rgba(0, 1, 0.6, 0.25, 0.35); g.add_color_stop_rgba(1, 1, 0.6, 0.25, 0)
    c.arc(x, y - 40 * s, 300 * s, 0, 2 * math.pi); c.set_source(g); c.fill()
    for k in range(3):
        c.move_to(x - 40 * s, y + 4 * s - k * 6 * s); c.line_to(x + 40 * s, y - 8 * s + k * 6 * s); ink(c, 14 * s); c.stroke()


def column(c, x, y, h, w=70, col="#e8dcc4"):
    rrect(c, x - w / 2, y - h, w, h, 6); shape(c, col, 6)
    for k in (-0.25, 0, 0.25):
        c.move_to(x + k * w, y - h + 20); c.line_to(x + k * w, y - 10); c.set_source_rgba(0, 0, 0, 0.15); c.set_line_width(4); c.stroke()
    rrect(c, x - w / 2 - 14, y - h - 22, w + 28, 26, 4); shape(c, col, 6)
    rrect(c, x - w / 2 - 10, y - 18, w + 20, 18, 3); shape(c, col, 6)


def temple(c, x, y, s, col="#e8dcc4", n=6):
    w = 120 * s * (n - 1)
    for i in range(n): column(c, x - w / 2 + i * 120 * s, y, 300 * s, 54 * s, col)
    rrect(c, x - w / 2 - 70 * s, y - 330 * s, w + 140 * s, 30 * s, 4); shape(c, col, 6)
    c.move_to(x - w / 2 - 80 * s, y - 330 * s); c.line_to(x, y - 450 * s); c.line_to(x + w / 2 + 80 * s, y - 330 * s); c.close_path(); shape(c, col, 6)


def house(c, x, y, w, h, col, roof="#a0522d", windows=True):
    rrect(c, x, y - h, w, h, 4); shape(c, col, 6)
    c.move_to(x - 15, y - h); c.line_to(x + w / 2, y - h - 60); c.line_to(x + w + 15, y - h); c.close_path(); shape(c, roof, 6)
    if windows:
        for k in range(int(w // 70)):
            rrect(c, x + 22 + k * 70, y - h + 40, 30, 45, 4); shape(c, "#3a2f24", 4)


def crowd(c, y, t, n=26, seed=4, col="#2a2230", scale=1.0):
    r = R(seed)
    for i in range(n):
        x = r.uniform(-50, W + 50); s = r.uniform(0.7, 1.1) * scale; b = math.sin(t * 2 + i) * 6
        c.arc(x, y - 150 * s + b, 34 * s, 0, 2 * math.pi); fill(c, col); c.fill()
        rrect(c, x - 45 * s, y - 120 * s + b, 90 * s, 140 * s, 30 * s); fill(c, col); c.fill()


def scroll_paper(c, x, y, w, h, t=0.0, lines=6):
    rrect(c, x, y, w, h, 8); shape(c, "#efe2c2", 6)
    for k in range(lines):
        c.move_to(x + 25, y + 30 + k * (h - 50) / lines); c.line_to(x + w - 25 - (k % 3) * 30, y + 30 + k * (h - 50) / lines)
        c.set_source_rgba(0.3, 0.25, 0.2, 0.6); c.set_line_width(4); c.stroke()


def lamp(c, x, y, t, r=420):
    g = cairo.RadialGradient(x, y, 5, x, y, r); g.add_color_stop_rgba(0, 1, 0.82, 0.5, 0.55); g.add_color_stop_rgba(1, 1, 0.82, 0.5, 0)
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source(g); c.fill()
    c.move_to(x - 30, y + 30); c.curve_to(x - 30, y + 5, x + 30, y + 5, x + 30, y + 30); c.close_path(); shape(c, "#b8863a", 5)
    f = 1 + 0.1 * math.sin(t * 11)
    c.move_to(x - 8, y + 8); c.curve_to(x - 10, y - 15 * f, x, y - 30 * f, x, y - 34 * f); c.curve_to(x, y - 30 * f, x + 10, y - 15 * f, x + 8, y + 8); fill(c, "#ffd36b"); c.fill()


def write_arms(t):  # ruka koja piše
    return [(0.9 + 0.12 * math.sin(t * 7), -1.3), (-0.5, 1.1)]


# ---------------- scene (c, t, d, v) ----------------
def camp_ext(c, t, d, v=None):
    sky(c, [(0, "#0b1022"), (0.6, "#1d2a4a"), (1, "#3a4a6a")]); stars(c, t)
    A.mountains(c, 640, "#2a3552", 9, 260, n=9, snow=True)
    ground(c, 760, "#d9e2ec", 10)
    for i, (x, s) in enumerate(((260, 0.8), (620, 0.95), (1350, 0.85), (1700, 0.7))):
        tent(c, x, 800 + s * 40, s, "#8f7c5c")
    tent(c, 980, 880, 1.25, "#b39a72", glow=1.0)
    fire(c, 470, 900, 0.7, t); fire(c, 1520, 880, 0.6, t + 1)
    A.snowfall(c, t, n=120, wind=0.6, speed=90)


def tent_write(c, t, d, v=None):
    sky(c, [(0, "#2a1f18"), (1, "#3d2c20")])
    for k in range(7):  # platno šatora
        c.move_to(k * 320 - 100, 0); c.line_to(960, -300); c.set_source_rgba(0, 0, 0, 0.18); c.set_line_width(5); c.stroke()
    rrect(c, -100, 820, W + 200, 400, 0); shape(c, "#2a2018", 6)
    lamp(c, 1220, 640, t)
    rrect(c, 760, 700, 620, 40, 8); shape(c, "#6b4a2e", 7)          # sto
    for x in (800, 1330): rrect(c, x, 735, 26, 160, 6); shape(c, "#6b4a2e", 6)
    scroll_paper(c, 960, 640, 220, 70, t, 3)
    stoic(c, 830, 900, 0.95, t, pose="sit", arms=write_arms, look=0.5, **(v or EMP))
    c.save(); c.translate(1010 + 8 * math.sin(t * 7), 630); c.rotate(-0.6); c.move_to(0, 0); c.line_to(0, -70); ink(c, 6); c.stroke(); c.restore()


def rome_street(c, t, d, v=None):
    sky(c, [(0, "#7fb2e5"), (1, "#d7e8f6")])
    A.mountains(c, 640, "#9db7a0", 3, 120, n=6)
    for i, (x, w, h, col) in enumerate(((60, 300, 330, "#e6c9a0"), (420, 260, 420, "#e0b98e"), (1180, 320, 360, "#ebd3b0"), (1560, 300, 300, "#dcb790"))):
        house(c, x, 780, w, h, col)
    temple(c, 960, 780, 0.75)
    ground(c, 770, "#cdb38c", 4)
    x = 300 + (t / d) * 1200
    stoic(c, x, 1000, 0.62, t, pose="walk", walk=0.8, **(v or ANTONINUS))
    stoic(c, x + 150, 1000, 0.42, t + 0.3, pose="walk", walk=0.9, **BOY)


def boy_mat(c, t, d, v=None):
    sky(c, [(0, "#3b3040"), (1, "#2a2230")])
    rrect(c, 760, 220, 400, 300, 10); c.set_source(grad(c, 220, 520, [(0, "#1d2a4a"), (1, "#3a4a6a")])); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(1050, 300, 30, 0, 2 * math.pi); fill(c, "#f0f0e6"); c.fill()
    rrect(c, 520, 860, 900, 70, 20); shape(c, "#8a7a5a", 7)        # prostirka
    hx, hy = 640, 850
    c.arc(hx, hy, 50, 0, 2 * math.pi); shape(c, SKIN, 7)
    c.move_to(hx - 52, hy - 5); c.curve_to(hx - 58, hy - 70, hx + 58, hy - 70, hx + 52, hy - 5); c.curve_to(hx + 35, hy - 35, hx - 35, hy - 35, hx - 52, hy - 5); shape(c, "#4a3426", 5)
    for dx in (-18, 18):
        c.move_to(hx + dx - 8, hy + 2); c.curve_to(hx + dx - 3, hy + 8, hx + dx + 3, hy + 8, hx + dx + 8, hy + 2); ink(c, 5); c.stroke()
    rrect(c, 690, 815, 680, 70, 30); shape(c, "#b8a27a", 7)
    lamp(c, 1500, 760, t, 300)


def palace(c, t, d, v=None):
    sky(c, [(0, "#3a2a3a"), (1, "#5a3a3a")])
    for x in range(-40, W + 200, 260): column(c, x, 900, 760, 90, "#d8cbb0")
    rrect(c, 640, 120, 640, 780, 10); c.set_source(grad(c, 120, 900, [(0, "#8a2a2a"), (1, "#5a1a1a")])); c.fill()   # zavesa
    for k in range(8):
        c.move_to(660 + k * 80, 130); c.line_to(660 + k * 80, 890); c.set_source_rgba(0, 0, 0, 0.2); c.set_line_width(8); c.stroke()
    rrect(c, -100, 900, W + 200, 300, 0); shape(c, "#bfae8c", 6)
    who = v or {}
    stoic(c, 760, 960, 0.85, t, pose="stand", look=0.6, arms=[(-0.35, -0.3), (1.5, 0.2)], **(who.get("a", HADRIAN)))
    stoic(c, 1200, 960, 0.72, t, pose="stand", look=-0.6, **(who.get("b", BOY)))


def study(c, t, d, v=None):
    sky(c, [(0, "#2e2620"), (1, "#3d3228")])
    for row in range(4):  # police sa svicima
        rrect(c, 120, 180 + row * 170, 700, 20, 4); shape(c, "#6b4a2e", 5)
        for k in range(9):
            c.arc(170 + k * 75, 160 + row * 170, 26, 0, 2 * math.pi); shape(c, "#efe2c2", 4)
    lamp(c, 1600, 560, t, 380)
    rrect(c, -100, 900, W + 200, 300, 0); shape(c, "#2a2018", 6)
    stoic(c, 1100, 960, 0.85, t, pose="sit", arms=[(0.8, -1.4), (-0.8, 1.4)], look=0.2, **(v or dict(EMP, laurel=False)))
    scroll_paper(c, 1020, 560 + 4 * math.sin(t * 2), 200, 140, t, 5)


def thrones(c, t, d, v=None):
    sky(c, [(0, "#2a1f2f"), (1, "#4a2a2a")])
    for x in range(100, W, 430): column(c, x, 880, 700, 80, "#cdbf9f")
    rrect(c, -100, 880, W + 200, 300, 0); shape(c, "#9c8a6a", 6)
    for x in (720, 1200):
        rrect(c, x - 110, 520, 220, 300, 30); shape(c, "#b8862a", 8); rrect(c, x - 140, 760, 280, 120, 20); shape(c, "#c8962a", 8)
    stoic(c, 720, 930, 0.7, t, pose="stand", **EMP)
    stoic(c, 1200, 930, 0.7, t + 0.5, pose="stand", **dict(EMP, hair="#2a1e16", cloak=("#2b4a7a", "#1f3a5c")))


def plague_map(c, t, d, v=None):
    sky(c, [(0, "#d9c8a0"), (1, "#c4b080")])
    r = R(7)  # stilizovana mapa carstva
    c.move_to(260, 520)
    for k in range(40):
        a = k / 40 * 2 * math.pi; rr = 1 + 0.18 * math.sin(a * 5) + 0.1 * math.sin(a * 11)
        c.line_to(960 + math.cos(a) * 660 * rr, 520 + math.sin(a) * 300 * rr)
    c.close_path(); shape(c, "#a89060", 8)
    c.arc(960, 540, 180, 0, 2 * math.pi); fill(c, "#7aa0c0", 0.9); c.fill()         # more
    n = int(5 + 60 * ease(t / d))
    for i in range(n):
        x, y = r.uniform(380, 1540), r.uniform(300, 760)
        if math.hypot(x - 960, y - 540) < 200: continue
        rad = 10 + 8 * math.sin(t * 3 + i)
        c.arc(x, y, abs(rad), 0, 2 * math.pi); c.set_source_rgba(0.7, 0.1, 0.1, 0.75); c.fill()
    c.rectangle(-100, -100, W + 200, H + 200); c.set_source_rgba(0.1, 0.05, 0.05, 0.35 * ease(t / d)); c.fill()


def forum_auction(c, t, d, v=None):
    sky(c, [(0, "#8ab4dc"), (1, "#e8dcc0")])
    temple(c, 960, 640, 0.9)
    ground(c, 640, "#d8c8a4", 3)
    for x in (380, 960, 1540):  # stolovi sa blagom
        rrect(c, x - 200, 700, 400, 30, 6); shape(c, "#7a5a3a", 6)
        for k, col in enumerate(("#e2b23a", "#d4d4e0", "#c04040", "#e2b23a")):
            cx = x - 140 + k * 90
            if k % 2 == 0:
                c.move_to(cx - 25, 700); c.line_to(cx - 32, 640); c.line_to(cx + 32, 640); c.line_to(cx + 25, 700); c.close_path(); shape(c, col, 5)
            else:
                rrect(c, cx - 30, 610, 60, 90, 10); shape(c, col, 5)
    crowd(c, 1120, t, 30, 5, "#3a3040", 1.1)
    stoic(c, 1700, 1000, 0.55, t, pose="stand", **EMP)


def danube(c, t, d, v=None):
    sky(c, [(0, "#3e4f6e"), (0.6, "#8fa3bd"), (1, "#c8d4e0")])
    A.mountains(c, 520, "#5f7190", 13, 180, n=8, snow=True)
    c.rectangle(-100, 520, W + 200, 140); fill(c, "#cfe0ee"); c.fill()                # zaleđena reka
    for k in range(10):
        c.move_to(k * 220 - 60, 560 + (k % 3) * 25); c.line_to(k * 220 + 70, 590 + (k % 2) * 20); c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(4); c.stroke()
    ground(c, 660, "#e9eff5", 8)
    for x in (300, 1650): tent(c, x, 760, 0.8, "#8f7c5c")
    fire(c, 960, 930, 0.9, t)
    stoic(c, 700, 1040, 0.6, t, pose="stand", look=0.6, **EMP)
    for i, x in enumerate((1180, 1330)): stoic(c, x, 1040, 0.55, t + i, pose="stand", look=-0.5, **SOLDIER)
    A.snowfall(c, t, n=140, wind=-1.0, speed=150)


def general(c, t, d, v=None):
    sky(c, [(0, "#e0a050"), (1, "#f4d090")])
    c.arc(1500, 300, 120, 0, 2 * math.pi); fill(c, "#fff0b0"); c.fill()
    ground(c, 760, "#c89a5a", 25, 3)
    crowd(c, 1000, t, 34, 9, "#5a3020", 0.9)
    up = ease(t / 1.2)
    stoic(c, 960, 880, 0.8, t, pose="stand", arms=[(-0.4, -0.3), (2.6 * up + 0.2, 0.1)], **dict(SOLDIER, cloak=("#5a2a5a", "#3a1a3a")))
    c.save(); c.translate(960 + 80, 880 - 470 * 0.8 - 150 * up); c.rotate(-0.2); rrect(c, -8, -170, 16, 170, 4); shape(c, "#d8d8e0", 5); c.restore()


def letters_burn(c, t, d, v=None):
    sky(c, [(0, "#14100e"), (1, "#2a1c14")])
    rrect(c, -100, 880, W + 200, 300, 0); shape(c, "#1e1610", 6)
    rrect(c, 900, 720, 220, 120, 20); shape(c, "#4a4a52", 7)              # mangal
    fire(c, 1010, 730, 1.1, t)
    r = R(11)
    for i in range(6):  # pisma padaju u vatru i gore
        p = (t * 0.35 + i / 6) % 1.0
        x = 1010 + (r.uniform(-1, 1)) * 60 * (1 - p); y = 380 + p * 360
        c.save(); c.translate(x, y); c.rotate(p * 3 + i); rrect(c, -40, -30, 80, 60, 6); shape(c, "#efe2c2", 4, max(0, 1 - p * 1.2)); c.restore()
    for i in range(30):
        p = (t * 0.6 + i / 30) % 1.0; c.arc(1010 + math.sin(i * 7 + t) * 80, 700 - p * 500, 4, 0, 2 * math.pi); c.set_source_rgba(1, 0.6, 0.2, 1 - p); c.fill()
    stoic(c, 640, 960, 0.85, t, pose="stand", look=0.7, arms=[(-0.3, -0.3), (1.3, 0.3)], **EMP_OLD)


def deathbed(c, t, d, v=None):
    k = ease(t / d)
    sky(c, [(0, "#2a1f3a"), (0.5, "#c06040"), (1, "#f0a060")])
    c.arc(1480, 700 + 140 * k, 140, 0, 2 * math.pi); fill(c, "#ffd080"); c.fill()
    ground(c, 760, "#3a2a2a", 10)
    rrect(c, 380, 640, 1000, 360, 30); shape(c, "#5a4030", 8)          # unutrašnjost šatora
    rrect(c, 460, 820, 640, 90, 20); shape(c, "#8a7a6a", 7)            # postelja
    hx, hy = 540, 800
    c.arc(hx, hy, 52, 0, 2 * math.pi); shape(c, SKIN, 7)
    c.move_to(hx - 50, hy + 8); c.curve_to(hx - 45, hy + 70, hx + 45, hy + 70, hx + 50, hy + 8); c.curve_to(hx + 30, hy + 25, hx - 30, hy + 25, hx - 50, hy + 8); shape(c, "#b9b9b9", 5)
    rrect(c, 580, 790, 500, 70, 30); shape(c, "#7a2b2b", 7)
    stoic(c, 1240, 1000, 0.6, t, pose="stand", look=-0.7, **SOLDIER)
    c.rectangle(-100, -100, W + 200, H + 200); c.set_source_rgba(0.05, 0.03, 0.08, 0.45 * k); c.fill()


def modern(c, t, d, v=None):
    sky(c, [(0, "#0e1424"), (1, "#1a2236")])
    rrect(c, 1180, 160, 560, 420, 14); shape(c, "#162038", 8)
    for i in range(16):
        r = R(i); bx = 1200 + r.uniform(0, 500); bh = r.uniform(80, 330)
        c.rectangle(bx, 580 - bh, r.uniform(30, 60), bh); fill(c, "#0f1626"); c.fill()
        for k in range(4):
            if (i + k) % 3 == 0: c.rectangle(bx + 8, 590 - bh + 20 + k * 45, 9, 14); fill(c, "#f2c66d", 0.8); c.fill()
    rrect(c, 200, 760, 1100, 160, 30); shape(c, "#4a5a70", 8)
    book = (v or {}).get("book", False)
    stoic(c, 700, 860, 0.85, t, pose="sit", glow=None if book else "#5ec8ff", look=0.4, arms=[(0.8, -1.4), (-0.8, 1.4)], **MODERN)
    if book:
        lamp(c, 380, 560, t, 380); scroll_paper(c, 620, 470, 180, 120, t, 5)
    else:
        rrect(c, 640, 470, 60, 100, 10); shape(c, "#11151d", 5); rrect(c, 646, 478, 48, 84, 6); fill(c, "#5ec8ff"); c.fill()


SCENES = dict(camp=camp_ext, tent=tent_write, street=rome_street, mat=boy_mat, palace=palace, study=study, thrones=thrones,
              plague=plague_map, forum=forum_auction, danube=danube, general=general, letters=letters_burn,
              deathbed=deathbed, modern=modern)
HAD_ANT = {"a": HADRIAN, "b": ANTONINUS}
ANT_YOUNG = {"a": ANTONINUS, "b": dict(EMP, laurel=False)}
SHOTS = {  # po poglavlju: jedna scena po pasusu (naziv, varijanta)
    0: [("camp",), ("tent",), ("camp",), ("tent",), ("camp",)],
    1: [("street",), ("street",), ("mat",), ("palace", {"a": HADRIAN, "b": BOY}), ("palace", {"a": HADRIAN, "b": BOY})],
    2: [("palace", HAD_ANT), ("palace", HAD_ANT), ("palace", {"a": HADRIAN, "b": BOY}), ("study",), ("study",), ("study",),
        ("study",), ("mat",), ("street",), ("study",)],
    3: [("palace", ANT_YOUNG), ("palace", ANT_YOUNG), ("palace", ANT_YOUNG), ("palace", ANT_YOUNG), ("thrones",),
        ("thrones",), ("plague",), ("plague",), ("plague",), ("tent",)],
    4: [("danube",), ("forum",), ("forum",), ("forum",), ("forum",), ("forum",)],
    5: [("danube",), ("danube",), ("danube",), ("tent",), ("tent",), ("tent",), ("tent",), ("tent",)],
    6: [("general",), ("general",), ("danube",), ("tent", EMP_OLD), ("general",), ("letters",), ("letters",), ("letters",)],
    7: [("deathbed",), ("danube",), ("deathbed",), ("deathbed",), ("deathbed",), ("deathbed",), ("camp",)],
    8: [("modern", {"book": True}), ("modern",), ("modern",), ("modern",), ("letters",), ("danube",), ("deathbed",),
        ("palace", {"a": HADRIAN, "b": dict(EMP, laurel=False)}), ("camp",), ("modern", {"book": True})],
    9: [("tent",), ("camp",)],
}


def sub_text(c, text, a=1.0):
    A.M.face(c, 44)
    words = text.split(); lines = [words]
    if c.text_extents(text).x_advance > 1500:
        best = None
        for i in range(1, len(words)):
            m = max(c.text_extents(" ".join(words[:i])).x_advance, c.text_extents(" ".join(words[i:])).x_advance)
            if best is None or m < best[0]: best = (m, [words[:i], words[i:]])
        lines = best[1]
    y0 = H - 95 - (len(lines) - 1) * 56
    g = cairo.LinearGradient(0, y0 - 90, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(0.6, 0, 0, 0, 0.5 * a); g.add_color_stop_rgba(1, 0, 0, 0, 0.6 * a)
    c.rectangle(0, y0 - 90, W, H - y0 + 90); c.set_source(g); c.fill()
    for i, ln in enumerate(lines):
        s = " ".join(ln); x = W / 2 - c.text_extents(s).x_advance / 2
        A.M.shadow_text(c, x, y0 + i * 56, s, a)


def chapter_card(c, title, a):
    if " — " in title: title = title.split(" — ")[-1]
    parts = title.split(": ", 1)
    c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, 0.45 * a); c.fill()
    if len(parts) == 2:
        A.M.face(c, 40); sp = "  ".join(parts[0].replace("POGLAVLJE", "CHAPTER")); A.M.shadow_text(c, W / 2 - c.text_extents(sp).x_advance / 2, 430, sp, a * 0.9)
        title = parts[1]
    A.M.face(c, 86); A.M.shadow_text(c, W / 2 - c.text_extents(title.upper()).x_advance / 2, 560, title.upper(), a)


def build(ep):
    tm = json.load(open(os.path.join(HERE, "out", ep, "timing.json")))
    shots = []
    for ci, ch in enumerate(tm["chapters"]):
        for pi, p in enumerate(ch["paras"]):
            spec = SHOTS[ci][pi] if pi < len(SHOTS[ci]) else SHOTS[ci][-1]
            t1 = ch["paras"][pi + 1]["t0"] if pi + 1 < len(ch["paras"]) else (tm["chapters"][ci + 1]["t0"] if ci + 1 < len(tm["chapters"]) else tm["total"])
            shots.append({"t0": p["t0"] if pi else ch["t0"], "t1": t1, "scene": SCENES[spec[0]], "v": spec[1] if len(spec) > 1 else None,
                          "sents": p["sentences"], "card": ch["chapter"] if pi == 0 and ci not in (0, 9) else None, "i": len(shots)})
    shots[0]["t0"] = 0.0
    total = tm["total"]
    out = os.path.join(ROOT, "videos", "stoic_long", f"anim_{ep}.mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", os.path.join(HERE, "out", ep, "voice.wav"),
                          "-filter_complex", "[0:v]noise=alls=4:allf=t,vignette=PI/6,format=yuv420p[v];"
                          "[1:a]aresample=48000,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
                          "aecho=0.8:0.5:40|75:0.10|0.06,pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
                          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "6M", "-bufsize", "12M",
                          "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); si = 0
    nf = int(round(total * FPS))
    for f in range(nf):
        t = f / FPS
        while si < len(shots) - 1 and t >= shots[si + 1]["t0"]: si += 1
        sh = shots[si]; lt = t - sh["t0"]; d = max(0.5, sh["t1"] - sh["t0"])
        c = cairo.Context(s); c.set_line_join(cairo.LINE_JOIN_ROUND)
        # kamera: blago zumiranje / pomeranje, smer zavisi od kadra
        z = 1.0 + 0.06 * ease(lt / d) if sh["i"] % 2 == 0 else 1.06 - 0.06 * ease(lt / d)
        px = (sh["i"] % 3 - 1) * 30 * ease(lt / d)
        c.save(); c.translate(W / 2 + px, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        sh["scene"](c, lt, d, sh["v"]); c.restore()
        cur = next((x for x in sh["sents"] if x["t0"] - 0.05 <= t < x["t1"] + 0.3), None)
        if cur: sub_text(c, cur["text"])
        if sh["card"] and lt < 2.6:
            chapter_card(c, sh["card"], min(1, lt / 0.3) * min(1, (2.6 - lt) / 0.4))
        if lt < 0.12 and si > 0:
            c.rectangle(0, 0, W, H); c.set_source_rgba(0.04, 0.04, 0.07, 1 - lt / 0.12); c.fill()
        s.flush(); p.stdin.write(bytes(s.get_data()))
        if f % (FPS * 30) == 0: print(f"{int(t // 60)}:{int(t % 60):02d} / {int(total // 60)}:{int(total % 60):02d}", flush=True)
    p.stdin.close(); p.wait(); print("GOTOVO", out)


def preview(names, out):
    fs = []
    for k, n in enumerate(names):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); SCENES[n](c, 1.5, 4.0, None)
        f = out + f"_{k}.png"; s.write_to_png(f); fs.append(f)
    return fs


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        print(preview(sys.argv[3:], sys.argv[2]))
    else:
        build(sys.argv[1])
