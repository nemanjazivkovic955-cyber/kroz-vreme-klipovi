"""Dugi animirani video #2 — "The ENTIRE Life of Marcus Aurelius": slika PRATI TEKST rečenicu po rečenicu
(kao kanali tipa istorija brenda: šta narator kaže, to se vidi; godine i ključne reči kao velike oznake).
Scene iz stoic/anim_long.py + nove ovde. SENT: jedna stavka po rečenici naracije (stoic/out/ep02/timing.json):
  (scena, varijanta, oznaka) | None = ista scena se nastavlja (bez reza).
Upotreba: python3 stoic/anim_ep02.py  [preview <i0> <i1> ...]
"""
import os, sys, math, json, subprocess, random
import numpy as np, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import anim_long as L
from anim_long import (W, H, FPS, A, fill, ink, shape, grad, ease, rrect, stoic, SKIN, sky, stars, ground, tent, fire,
                       column, temple, house, crowd, scroll_paper, lamp, EMP, EMP_OLD, BOY, HADRIAN, ANTONINUS, SOLDIER, MODERN)

MOTHER = dict(hood=True, beard=None, cloak=("#5a6a4a", "#46543a"))
GRANDPA = dict(hood=False, hair="#cfcfcf", beard="#dedede", cloak=("#e8e2d2", "#cfc8b4"))
RICHKID = dict(hood=False, beard=None, hair="#c9a24a", cloak=("#c8962a", "#a87a1a"))
EPICTETUS = dict(hood=False, hair="#5a4a3a", beard="#6a5a4a", cloak=("#8a7a62", "#6e6050"))
RUSTICUS = dict(hood=False, hair="#7a7a7a", beard="#8a8a8a", cloak=("#3e5a4a", "#2e4638"))
POOR = dict(hood=True, beard="#5a4030", cloak=("#7a6a52", "#5e5140"))
SENATOR = dict(hood=False, hair="#6a6a6a", beard=None, cloak=("#f0ece0", "#d8d2c0"))
LUCIUS = dict(EMP, hair="#2a1e16", cloak=("#2b4a7a", "#1f3a5c"))
TRIBE = dict(hood=False, hair="#c8a060", beard="#b08850", cloak=("#4a5a3a", "#3a4a2e"))
CASSIUS = dict(SOLDIER, cloak=("#5a2a5a", "#3a1a3a"))


def stx(c, x, y, s, a=1.0, rgb=(1, 1, 1)):
    for dx, dy, al in ((0, 4, 0.6), (0, 2, 0.6), (3, 3, 0.35), (-3, 3, 0.35)):
        c.move_to(x + dx, y + dy); c.set_source_rgba(0, 0, 0, al * a); c.show_text(s)
    c.move_to(x, y); c.set_source_rgba(*rgb, a); c.show_text(s)


def label(c, text, a, y=200, size=110, color=(1.0, 0.82, 0.3)):
    """Velika oznaka (godina, broj, ključna reč) — zlatna, sa senkom."""
    A.M.face(c, size); e = c.text_extents(text)
    while e.x_advance > W - 160 and size > 40: size -= 6; A.M.face(c, size); e = c.text_extents(text)
    stx(c, W / 2 - e.x_advance / 2, y, text, a, color)


# ---------------- nove scene ----------------
def birth(c, t, d, v=None):
    L.rome_street(c, 0.0, d, v)
    c.rectangle(0, 0, W, H); c.set_source_rgba(1, 0.95, 0.8, 0.12); c.fill()
    for k in range(10):  # sunčevi zraci
        a = k * 0.6 + t * 0.15; c.move_to(1700, 120); c.line_to(1700 + math.cos(a) * 900, 120 + math.sin(a) * 900); c.set_source_rgba(1, 0.95, 0.7, 0.12); c.set_line_width(40); c.stroke()


def grave(c, t, d, v=None):
    v = v or {}
    sky(c, [(0, "#5a6478"), (1, "#9aa4b4")]); ground(c, 780, "#5a6a4a", 10)
    for x in v.get("stones", [960]):
        rrect(c, x - 90, 560, 180, 240, 70); shape(c, "#9a9a9a", 7)
        c.move_to(x - 40, 640); c.line_to(x + 40, 640); ink(c, 6); c.stroke()
    for i, (who, x, s) in enumerate(v.get("people", [(MOTHER, 560, 0.7), (BOY, 700, 0.42), (GRANDPA, 1380, 0.7)])):
        stoic(c, x, 1000, s, t + i, pose="stand", look=0.3 if x < 960 else -0.3, **who)
    for i in range(40):  # kiša
        r = random.Random(i); x = (r.uniform(0, W) + t * 80) % W; y = (r.uniform(0, H) + t * 900) % H
        c.move_to(x, y); c.line_to(x - 8, y + 40); c.set_source_rgba(0.85, 0.9, 1, 0.35); c.set_line_width(3); c.stroke()


def quiet_boy(c, t, d, v=None):
    sky(c, [(0, "#d8c8a8"), (1, "#c0a888")])
    for x in (200, 1720): column(c, x, 900, 650, 90, "#e6dcc6")
    rrect(c, -100, 900, W + 200, 300, 0); shape(c, "#b8a07a", 6)
    rrect(c, 760, 760, 400, 60, 10); shape(c, "#8a7050", 7)  # klupa
    stoic(c, 960, 960, 0.6, t, pose="sit", look=0.0, arms=[(0.7, -1.3), (-0.7, 1.3)], **BOY)
    scroll_paper(c, 905, 640, 110, 70, t, 3)


def split_rich(c, t, d, v=None):
    c.rectangle(0, 0, W / 2, H); c.set_source(grad(c, 0, H, [(0, "#f2d38a"), (1, "#d8a84a")])); c.fill()
    c.rectangle(W / 2, 0, W / 2, H); c.set_source(grad(c, 0, H, [(0, "#3a3040"), (1, "#2a2230")])); c.fill()
    for i in range(14):  # zlato i igračke
        r = random.Random(i); x, y = r.uniform(80, 880), r.uniform(700, 960)
        c.arc(x, y, r.uniform(18, 34), 0, 2 * math.pi); shape(c, "#ffd34a", 5)
    stoic(c, 480, 960, 0.55, t, pose="stand", arms=[(-1.8, -0.3), (1.8, 0.3)], **RICHKID)
    rrect(c, 1180, 880, 560, 50, 18); shape(c, "#8a7a5a", 6)
    stoic(c, 1460, 930, 0.5, t, pose="sit", **BOY)
    c.move_to(W / 2, 0); c.line_to(W / 2, H); ink(c, 10); c.stroke()


def truth(c, t, d, v=None):
    quiet_boy(c, t, d)
    k = ease(t / 0.6)
    rrect(c, 1080, 360 - 30 * k, 420, 170, 40); shape(c, "#ffffff", 7, k)
    c.move_to(1110, 520 - 30 * k); c.line_to(1060, 580); c.line_to(1170, 525 - 30 * k); fill(c, "#ffffff", k); c.fill()
    c.move_to(1210, 450 - 30 * k); c.line_to(1260, 500 - 30 * k); c.line_to(1370, 400 - 30 * k); c.set_source_rgba(0.2, 0.6, 0.3, k); c.set_line_width(22); c.stroke()


def hadrian_sick(c, t, d, v=None):
    sky(c, [(0, "#2a2030"), (1, "#3a2a3a")])
    lamp(c, 1500, 560, t, 380)
    rrect(c, 420, 760, 1000, 140, 30); shape(c, "#6a3a7a", 8)
    hx, hy = 520, 730
    c.arc(hx, hy, 60, 0, 2 * math.pi); shape(c, SKIN, 7)
    c.move_to(hx - 56, hy + 8); c.curve_to(hx - 50, hy + 80, hx + 50, hy + 80, hx + 56, hy + 8); c.curve_to(hx + 30, hy + 28, hx - 30, hy + 28, hx - 56, hy + 8); shape(c, "#e6e6e6", 5)
    rrect(c, 580, 730, 820, 90, 40); shape(c, "#8a5a9a", 7)


def family_tree(c, t, d, v=None):
    sky(c, [(0, "#e8dcc0"), (1, "#d4c4a0")])
    rrect(c, 160, 120, 1600, 840, 30); shape(c, "#efe2c2", 8)
    pts = [(560, 520, HADRIAN, "HADRIAN"), (960, 520, ANTONINUS, "ANTONINUS"), (1360, 520, dict(EMP, laurel=False), "MARCUS")]
    for i, (x, y, who, name) in enumerate(pts):
        k = ease((t - i * 0.7) / 0.5)
        if k <= 0: continue
        c.arc(x, y - 60, 150, 0, 2 * math.pi); shape(c, "#d8c8a0", 7, k)
        c.save(); c.translate(x, y + 330); c.scale(0.55, 0.55); c.translate(-x, -(y + 330))
        stoic(c, x, y + 330, 1.0, t, pose="stand", **who); c.restore()
        A.M.face(c, 46); e = c.text_extents(name); stx(c, x - e.x_advance / 2, y + 200, name, k)
        if i:
            c.move_to(pts[i - 1][0] + 160, y - 60); c.line_to(x - 160, y - 60); c.set_source_rgba(0.5, 0.2, 0.1, k); c.set_line_width(12); c.stroke()
            c.move_to(x - 185, y - 85); c.line_to(x - 160, y - 60); c.line_to(x - 185, y - 35); c.stroke()


def afraid(c, t, d, v=None):
    L.palace(c, t, d, {"a": HADRIAN, "b": dict(EMP, laurel=False)})
    for i in range(3):  # kapljice znoja
        p = (t * 0.8 + i * 0.33) % 1.0
        c.arc(1265 + i * 18, 470 + p * 70, 9, 0, 2 * math.pi); c.set_source_rgba(0.6, 0.85, 1, 1 - p); c.fill()


def power_shadow(c, t, d, v=None):
    sky(c, [(0, "#100c14"), (1, "#22161e")])
    rrect(c, 830, 380, 260, 380, 40); shape(c, "#8a6a1a", 8)
    c.move_to(960, 380); c.line_to(960 - 600, 1080); c.line_to(960 + 600, 1080); c.close_path(); c.set_source_rgba(0, 0, 0, 0.45); c.fill()
    crowd(c, 1100, t, 22, 6, "#0a0a10", 1.0)


def teacher(c, t, d, v=None):
    L.study(c, t, d, dict(EMP, laurel=False))
    stoic(c, 1480, 960, 0.85, t, pose="stand", look=-0.6, arms=[(-0.3, -0.3), (-1.4, -0.2)], **RUSTICUS)


def epictetus(c, t, d, v=None):
    sky(c, [(0, "#4a3a2a"), (1, "#2e241a")])
    ground(c, 880, "#5a4a36", 6)
    stoic(c, 960, 960, 0.9, t, pose="stand", arms=[(-0.4, -0.3), (1.2, 0.4)], **EPICTETUS)
    for side in (-1, 1):  # pokidani lanci
        for k in range(5):
            c.save(); c.translate(960 + side * (120 + k * 40), 760 + k * 22); c.scale(1, 0.6); c.arc(0, 0, 18, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0.7, 0.7, 0.75, 1); c.set_line_width(8); c.stroke()
    A.M.face(c, 40); s = "EPICTETUS"; stx(c, W / 2 - c.text_extents(s).x_advance / 2, 1000, s, 0.9)


def thanks_list(c, t, d, v=None):
    sky(c, [(0, "#2a2018"), (1, "#3a2c20")])
    rrect(c, 560, 90, 800, 900, 20); shape(c, "#efe2c2", 8)
    items = (v or {}).get("items", ["GRANDFATHER", "MOTHER", "TEACHERS", "ANTONINUS"])
    hi = (v or {}).get("hi", -1)
    for i, it in enumerate(items):
        k = ease((t - i * 0.35) / 0.4)
        if k <= 0: continue
        y = 260 + i * 170
        A.M.face(c, 56); c.move_to(700, y); c.set_source_rgba(0.25, 0.18, 0.12, k * (1 if hi in (-1, i) else 0.35)); c.show_text("thank you, " + it.lower())
        if hi == i:
            c.move_to(680, y + 20); c.line_to(700 + c.text_extents("thank you, " + it.lower()).x_advance + 20, y + 20); c.set_source_rgba(0.75, 0.3, 0.1, 0.9); c.set_line_width(8); c.stroke()


def antoninus_work(c, t, d, v=None):
    cyc = (t * 0.5) % 1.0; day = math.sin(cyc * math.pi)
    top = tuple(np.array(A.hexc("#14203a")[:3]) * (1 - day) + np.array(A.hexc("#8ab4dc")[:3]) * day)
    c.rectangle(0, 0, W, H); c.set_source_rgb(*top); c.fill()
    ang = cyc * math.pi; c.arc(960 - math.cos(ang) * 800, 700 - math.sin(ang) * 560, 70, 0, 2 * math.pi); fill(c, "#ffd25e" if day > 0.3 else "#e9edf5"); c.fill()
    ground(c, 820, "#8a7a5a", 4)
    rrect(c, 700, 760, 520, 40, 8); shape(c, "#6b4a2e", 7)
    stoic(c, 860, 960, 0.8, t, pose="sit", arms=lambda tt: [(0.9 + 0.12 * math.sin(tt * 7), -1.3), (-0.5, 1.1)], **ANTONINUS)
    scroll_paper(c, 980, 700, 200, 60, t, 3)


def respect(c, t, d, v=None):
    sky(c, [(0, "#e8d6b0"), (1, "#c8b088")])
    for x in (150, 1770): column(c, x, 900, 700, 90, "#efe6d2")
    rrect(c, -100, 900, W + 200, 300, 0); shape(c, "#b8a07a", 6)
    stoic(c, 520, 960, 0.75, t, pose="stand", look=0.5, **POOR)
    stoic(c, 960, 960, 0.8, t, pose="stand", arms=[(-1.3, 0.2), (1.3, -0.2)], **ANTONINUS)
    stoic(c, 1400, 960, 0.75, t, pose="stand", look=-0.5, **SENATOR)


def senate(c, t, d, v=None):
    L.thrones(c, t, d)
    c.rectangle(0, 0, W, H); fill(c, "#2a1f2f", 0.6); c.fill()
    rrect(c, 840, 520, 240, 320, 30); shape(c, "#c8962a", 8)
    crowd(c, 1120, t, 20, 3, "#d8d2c0", 1.0)


def march(c, t, d, v=None):
    v = v or {}
    sky(c, v.get("sky", [(0, "#c89a5a"), (1, "#f0d090")]))
    A.mountains(c, 640, v.get("mtn", "#a07850"), 5, 160, n=8, snow=v.get("snow", False))
    ground(c, 760, v.get("ground", "#c8a070"), 8)
    for i in range(7):
        x = (i * 260 + t * 120) % (W + 300) - 150
        stoic(c, x, 1000 - (i % 2) * 40, 0.5, t + i * 0.2, pose="walk", walk=0.8, **(v.get("lead") if i == 3 and v.get("lead") else SOLDIER))
    if v.get("snow"): A.snowfall(c, t, n=100, wind=-1.0, speed=140)


def tribes(c, t, d, v=None):
    L.danube(c, 0.0, d)
    for i in range(9):
        x = 200 + i * 190 + (t * 30) % 60; y = 600 + (i % 3) * 30
        stoic(c, x, y + 60, 0.35, t + i, pose="walk", walk=0.7, **TRIBE)


def treasury(c, t, d, v=None):
    sky(c, [(0, "#1c160f"), (1, "#2c2216")])
    lamp(c, 960, 300, t, 500)
    rrect(c, 700, 600, 520, 300, 20); shape(c, "#7a4a22", 9)               # škrinja otvorena i prazna
    c.move_to(700, 600); c.line_to(760, 420); c.line_to(1280, 420); c.line_to(1220, 600); c.close_path(); shape(c, "#8a5a2a", 9)
    rrect(c, 730, 620, 460, 60, 10); fill(c, "#120c06"); c.fill()
    for i in range(3):
        p = (t * 0.7 + i / 3) % 1.0
        c.arc(1000 + i * 30, 640 + p * 30, 14, 0, 2 * math.pi); c.set_source_rgba(1, 0.8, 0.2, 1 - p); c.fill()


def taxes(c, t, d, v=None):
    sky(c, [(0, "#9ab0c8"), (1, "#d8d0c0")]); ground(c, 820, "#b8a07a", 4)
    crowd(c, 1100, t, 18, 12, "#5a5060", 1.0)
    stoic(c, 960, 900, 0.75, t, pose="stand", arms=[(-0.4, -0.3), (1.6, 0.1)], **dict(SOLDIER, cloak=("#4a4a5a", "#3a3a48")))
    c.arc(1140, 430, 60, 0, 2 * math.pi); shape(c, "#c8a050", 7)
    A.M.face(c, 60); c.move_to(1118, 452); c.set_source_rgba(0.3, 0.2, 0.1, 1); c.show_text("$")


def sick_emperor(c, t, d, v=None):
    L.tent_write(c, t, d, EMP_OLD)
    k = abs(math.sin(t * 3))  # kašalj
    c.rectangle(0, 0, W, H); c.set_source_rgba(0.2, 0.25, 0.3, 0.12 * k); c.fill()


def danube_map(c, t, d, v=None):
    sky(c, [(0, "#d9c8a0"), (1, "#c4b080")])
    rrect(c, 120, 80, 1680, 920, 30); shape(c, "#e2d4ae", 8)
    c.move_to(160, 420)
    for k in range(30): c.line_to(160 + k * 56, 420 + 90 * math.sin(k * 0.45) + k * 9)
    c.set_source_rgba(0.35, 0.55, 0.8, 1); c.set_line_width(22); c.stroke()
    A.M.face(c, 40); c.move_to(720, 340); c.set_source_rgba(0.3, 0.4, 0.6, 1); c.show_text("DANUBE")
    for i, (x, y, n1, n2) in enumerate(((620, 470, "VINDOBONA", "today: VIENNA"), (1380, 760, "SIRMIUM", "today: SREMSKA MITROVICA"))):
        k = ease((t - 0.3 - i * 1.2) / 0.5)
        if k <= 0: continue
        c.arc(x, y, 26, 0, 2 * math.pi); c.set_source_rgba(0.75, 0.15, 0.1, k); c.fill()
        A.M.face(c, 46); stx(c, x - c.text_extents(n1).x_advance / 2, y - 50, n1, k)
        A.M.face(c, 32); stx(c, x - c.text_extents(n2).x_advance / 2, y + 80, n2, k, (1.0, 0.85, 0.4))


def book(c, t, d, v=None):
    v = v or {}
    sky(c, [(0, "#1a1410"), (1, "#2a2016")])
    lamp(c, 1500, 380, t, 420)
    c.save(); c.translate(960, 560); c.rotate(-0.05 + 0.02 * math.sin(t)); rrect(c, -260, -340, 520, 680, 18); shape(c, v.get("cover", "#5a1f22"), 9)
    rrect(c, -210, -290, 420, 580, 10); c.set_source_rgba(1, 0.85, 0.4, 0.8); c.set_line_width(5); c.stroke()
    A.M.face(c, 54); s = v.get("title", "MEDITATIONS"); c.move_to(-c.text_extents(s).x_advance / 2, -40); c.set_source_rgba(1, 0.85, 0.4, 1); c.show_text(s)
    A.M.face(c, 30); s2 = v.get("sub", "MARCUS AURELIUS"); c.move_to(-c.text_extents(s2).x_advance / 2, 40); c.show_text(s2)
    c.restore()


def argue(c, t, d, v=None):
    L.tent_write(c, 0.0, d, EMP_OLD)
    c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
    stoic(c, 640, 960, 0.85, t, pose="stand", look=0.8, arms=[(-0.3, -0.3), (1.5 + 0.3 * math.sin(t * 4), 0.2)], **EMP_OLD)
    stoic(c, 1280, 960, 0.85, t + 1, pose="stand", look=-0.8, arms=[(-1.5 - 0.3 * math.sin(t * 4 + 1), -0.2), (0.3, 0.3)], **dict(EMP_OLD, cloak=("#4a4a5a", "#3a3a48")))


def mirror(c, t, d, v=None):
    sky(c, [(0, "#c8d4d8"), (1, "#aab8bc")])
    for i in range(10):
        for j in range(6): rrect(c, i * 200 - 20, j * 200 - 20, 196, 196, 6); c.set_source_rgba(1, 1, 1, 0.25); c.fill()
    rrect(c, 560, 140, 800, 620, 30); shape(c, "#dfe8ea", 9)
    c.save(); c.translate(1150, 330); c.rotate(0.06); rrect(c, -120, -90, 240, 180, 6); shape(c, "#ffe27a", 5)
    A.M.face(c, 30); c.move_to(-95, -20); c.set_source_rgba(0.2, 0.15, 0.1, 1); c.show_text("be kind."); c.move_to(-95, 30); c.show_text("do your duty."); c.restore()
    stoic(c, 820, 1100, 0.75, t, pose="stand", look=0.5, **MODERN)


def rumor(c, t, d, v=None):
    L.forum_auction(c, t, d)
    c.rectangle(0, 0, W, H); fill(c, "#1a1020", 0.35); c.fill()
    for i in range(6):
        x = 300 + i * 260; y = 820 + 40 * math.sin(t * 2 + i)
        rrect(c, x, y - 120, 150, 80, 30); shape(c, "#ffffff", 5, 0.8)
        A.M.face(c, 34); c.move_to(x + 30, y - 68); c.set_source_rgba(0.2, 0.2, 0.2, 0.9); c.show_text("dead?")


def half_empire(c, t, d, v=None):
    L.plague_map(c, 0.0, d)
    c.rectangle(0, 0, W, H); c.set_source_rgba(0.85, 0.82, 0.7, 1); c.fill()
    c.move_to(260, 520)
    for k in range(40):
        a = k / 40 * 2 * math.pi; rr = 1 + 0.18 * math.sin(a * 5) + 0.1 * math.sin(a * 11)
        c.line_to(960 + math.cos(a) * 660 * rr, 520 + math.sin(a) * 300 * rr)
    c.close_path(); shape(c, "#a89060", 8)
    c.rectangle(960, 0, W, H); c.clip()
    c.move_to(260, 520)
    for k in range(40):
        a = k / 40 * 2 * math.pi; rr = 1 + 0.18 * math.sin(a * 5) + 0.1 * math.sin(a * 11)
        c.line_to(960 + math.cos(a) * 660 * rr, 520 + math.sin(a) * 300 * rr)
    c.close_path(); fill(c, "#7a3a6a", 0.6 + 0.2 * math.sin(t * 3)); c.fill(); c.reset_clip()
    c.move_to(960, 150); c.line_to(960, 900); ink(c, 8); c.stroke()


def forgive(c, t, d, v=None):
    L.danube(c, t, d)
    c.rectangle(0, 0, W, H); fill(c, "#ffffff", 0.08); c.fill()


def cassius_falls(c, t, d, v=None):
    L.general(c, 3.0, d)
    c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.0, 0.05, 0.5 * ease(t / 1.5)); c.fill()


def handed_letters(c, t, d, v=None):
    sky(c, [(0, "#1a1410"), (1, "#2a2016")]); lamp(c, 960, 380, t, 480)
    rrect(c, -100, 880, W + 200, 300, 0); shape(c, "#1e1610", 6)
    stoic(c, 640, 960, 0.85, t, pose="stand", look=0.6, **EMP_OLD)
    stoic(c, 1280, 960, 0.8, t, pose="stand", look=-0.6, arms=[(-1.4, -0.2), (-1.4, 0.2)], **SOLDIER)
    rrect(c, 980, 520, 200, 120, 12); shape(c, "#7a4a22", 7)
    for k in range(4): rrect(c, 1000 + k * 40, 480 - k * 6, 60, 70, 4); shape(c, "#efe2c2", 4)


def sunrise_set(c, t, d, v=None):
    k = ease(t / d)
    sky(c, [(0, "#2a2a5a"), (0.5, "#e07a50"), (1, "#f8c080")])
    c.arc(960, 640 + 200 * k, 200, 0, 2 * math.pi); fill(c, "#ffe0a0"); c.fill()
    A.mountains(c, 780, "#4a3a5a", 31, 220, n=8, snow=True)


def lamp_out(c, t, d, v=None):
    L.tent_write(c, t, d, EMP_OLD)
    c.rectangle(0, 0, W, H); c.set_source_rgba(0.02, 0.02, 0.04, min(0.9, ease(t / d) * 0.95)); c.fill()


def five_emperors(c, t, d, v=None):
    sky(c, [(0, "#2a1f2f"), (1, "#4a3a3a")])
    rrect(c, -100, 820, W + 200, 300, 0); shape(c, "#6a5a4a", 6)
    names = ["NERVA", "TRAJAN", "HADRIAN", "ANTONINUS", "MARCUS"]
    for i, n in enumerate(names):
        x = 260 + i * 350; k = ease((t - i * 0.35) / 0.4)
        if k <= 0: continue
        rrect(c, x - 110, 640, 220, 180, 10); shape(c, "#cfc4ae", 7, k)
        c.arc(x, 520, 85, 0, 2 * math.pi); shape(c, "#e6dcc6" if i < 4 else "#ffd36b", 7, k)
        A.M.face(c, 36); stx(c, x - c.text_extents(n).x_advance / 2, 760, n, k)


def bookstore(c, t, d, v=None):
    sky(c, [(0, "#3a2c20"), (1, "#2a2016")])
    cols = ["#5a1f22", "#2b4a7a", "#3e5a4a", "#8a6a1a", "#5a1f22", "#4a4a5a"]
    for row in range(5):
        rrect(c, 80, 180 + row * 170, 1760, 18, 4); shape(c, "#6b4a2e", 5)
        for k in range(26):
            col = "#5a1f22" if (k + row) % 5 == 0 else cols[(k * 3 + row) % len(cols)]
            rrect(c, 100 + k * 66, 50 + row * 170, 56, 130, 4); shape(c, col, 4)
    lamp(c, 960, 120, t, 600)


def lesson(c, t, d, v=None):
    v = v or {}
    sky(c, [(0, "#14100e"), (1, "#2a1c14")])
    k = ease(t / 0.35)
    A.M.face(c, 300); n = v.get("n", "1"); e = c.text_extents(n)
    stx(c, W / 2 - e.x_advance / 2, 560, n, k, (1.0, 0.82, 0.3))


SC = dict(L.SCENES, birth=birth, grave=grave, quiet=quiet_boy, split=split_rich, truth=truth, hsick=hadrian_sick, tree=family_tree,
          afraid=afraid, power=power_shadow, teacher=teacher, epictetus=epictetus, thanks=thanks_list, awork=antoninus_work,
          respect=respect, senate=senate, march=march, tribes=tribes, treasury=treasury, taxes=taxes, sick=sick_emperor,
          dmap=danube_map, book=book, argue=argue, mirror=mirror, rumor=rumor, half=half_empire, forgive=forgive,
          cfall=cassius_falls, hand=handed_letters, sun=sunrise_set, lampout=lamp_out, five=five_emperors, store=bookstore, lesson=lesson)

HAD_BOY = {"a": HADRIAN, "b": BOY}
ANT_M = {"a": ANTONINUS, "b": dict(EMP, laurel=False)}
EAST = {"sky": [(0, "#c89a5a"), (1, "#f0d090")]}
NORTH = {"sky": [(0, "#5d7391"), (1, "#c8d4e0")], "mtn": "#7b8fa8", "ground": "#e9eff5", "snow": True, "lead": EMP}
_ = None
SENT = [
    # HOOK 0-8
    ("camp", _, "180 AD"), ("tent",), ("tent",), ("tent",),
    ("plague", _, "70,000,000 PEOPLE"), ("general",), ("tent",), _, ("tent", _, "MARCUS AURELIUS"),
    # 1: boy 9-18
    ("birth", _, "ROME, 121 AD"), ("grave",), ("quiet",), ("split",), ("truth",), _,
    ("palace", HAD_BOY), _, ("palace", HAD_BOY, "VERISSIMUS"), _,
    # 2: heir 19-43
    ("hsick",), ("tree",), _, _, ("afraid", _, "AGE 17"), _, _, ("power",), _, ("study",), ("study", _, "LAW"), ("study", _, "SPEECH"),
    ("teacher",), ("teacher", _, "PHILOSOPHY"), ("epictetus",), _, ("study",), ("epictetus", _, "A FORMER SLAVE"),
    ("book", {"title": "TO HIMSELF", "sub": "BOOK ONE"}), ("thanks",), _, ("thanks", {"hi": 0}), ("thanks", {"hi": 1}), ("thanks", {"hi": 2}), ("tent",),
    # 3: emperor 44-62
    ("palace", ANT_M, "23 YEARS"), ("awork",), _, ("respect",), _, ("palace", ANT_M), ("senate", _, "161 AD"),
    ("thrones",), _, _, ("thrones", _, "TWO EMPERORS"), ("march", EAST), _, ("plague", _, "THE PLAGUE"), _, ("plague", _, "MILLIONS"),
    ("danube",), _, ("tent",),
    # 4: palace sold 63-73
    ("tribes", _, "THE NORTHERN WAR"), _, ("march", NORTH), ("treasury",), _, ("taxes",), ("forum",), _,
    ("forum", _, "2 MONTHS"), ("forum",), ("forum",),
    # 5: war 74-91
    ("march", NORTH), _, ("sick",), ("danube", _, "12 YEARS"), ("dmap",), _, ("tent",), ("book", {"title": "TO HIMSELF"}), _,
    ("book",), ("argue",), _, ("tent", _, "DON'T COMPLAIN"), ("tent", _, "DO YOUR DUTY"), ("tent", _, "BE KIND"), ("tent", _, "PAIN PASSES"),
    ("mirror",), _,
    # 6: betrayal 92-103
    ("rumor", _, "175 AD"), ("general", _, "AVIDIUS CASSIUS"), ("half",), ("forgive",), _, ("cfall",), _, ("hand",),
    ("letters",), _, _, _,
    # 7: sunset 104-116
    ("grave", {"stones": [960], "people": [(EMP_OLD, 640, 0.75)]}), ("grave", {"stones": [700, 960, 1220, 1480], "people": [(EMP_OLD, 380, 0.7)]}), _,
    ("march", NORTH), _, _, ("deathbed", _, "180 AD"), ("deathbed", _, "AGE 58"), ("deathbed",), ("sun",), _, ("lampout",),
    ("five", _, "THE FIVE GOOD EMPERORS"),
    # 8: legacy 117-142
    ("book",), _, ("store",), ("modern",), ("modern", _, "STRESS"), ("modern", _, "ANGRY PEOPLE"), ("modern", _, "LOSS"),
    ("modern", _, "FEAR"), ("modern", {"book": True}),
    ("lesson", {"n": "1"}), ("lesson", {"n": "1"}, "CONTROL YOUR RESPONSE"), _, ("lesson", {"n": "2"}), ("lesson", {"n": "2"}, "DO YOUR WORK"), _,
    ("lesson", {"n": "3"}), ("lesson", {"n": "3"}, "EVERY HARD DAY ENDS"), _, ("lesson", {"n": "4"}), ("lesson", {"n": "4"}, "BE GRATEFUL"), _,
    ("lesson", {"n": "5"}), ("lesson", {"n": "5"}, "YOUR TIME IS LIMITED"), _, ("thrones",), ("tent",),
    # END 143-144
    ("camp", _, "SHARE • LIKE • COMMENT"), _,
]


def shots_from_timing(tm):
    sents = [(ci, s) for ci, ch in enumerate(tm["chapters"]) for p in ch["paras"] for s in p["sentences"]]
    assert len(sents) == len(SENT), (len(sents), len(SENT))
    shots, labels = [], []
    chap_start = {ch["paras"][0]["sentences"][0]["t0"]: ch["chapter"] for ci, ch in enumerate(tm["chapters"]) if ci not in (0, len(tm["chapters"]) - 1)}
    for i, ((ci, s), spec) in enumerate(zip(sents, SENT)):
        if spec is not None:
            shots.append({"t0": s["t0"] - 0.15 if i else 0.0, "scene": SC[spec[0]], "v": spec[1] if len(spec) > 1 else None,
                          "card": chap_start.get(s["t0"]), "i": len(shots)})
            if len(spec) > 2 and spec[2]: labels.append((s["t0"], s["t1"] + 0.4, spec[2]))
    for k in range(len(shots)): shots[k]["t1"] = shots[k + 1]["t0"] if k + 1 < len(shots) else tm["total"]
    return shots, labels, [s for _, s in sents]


def build(ep="ep02", t_from=0.0, t_to=None, out=None):
    tm = json.load(open(os.path.join(HERE, "out", ep, "timing.json")))
    shots, labels, sents = shots_from_timing(tm)
    total = tm["total"]; t_to = t_to or total
    out = out or os.path.join(ROOT, "videos", "stoic_long", f"anim_{ep}.mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-ss", f"{t_from:.3f}", "-i", os.path.join(HERE, "out", ep, "voice.wav"),
                          "-filter_complex", "[0:v]noise=alls=4:allf=t,vignette=PI/6,format=yuv420p[v];"
                          "[1:a]aresample=48000,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
                          "aecho=0.8:0.5:40|75:0.10|0.06,pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
                          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "6M", "-bufsize", "12M",
                          "-c:a", "aac", "-b:a", "160k", "-t", f"{t_to - t_from:.3f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); si = 0
    for f in range(int(round(t_from * FPS)), int(round(t_to * FPS))):
        t = f / FPS
        while si < len(shots) - 1 and t >= shots[si + 1]["t0"]: si += 1
        sh = shots[si]; lt = t - sh["t0"]; d = max(0.5, sh["t1"] - sh["t0"])
        c = cairo.Context(s); c.set_line_join(cairo.LINE_JOIN_ROUND)
        z = 1.0 + 0.05 * ease(lt / d) if sh["i"] % 2 == 0 else 1.05 - 0.05 * ease(lt / d)
        px = (sh["i"] % 3 - 1) * 25 * ease(lt / d)
        c.save(); c.translate(W / 2 + px, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        sh["scene"](c, lt, d, sh["v"]); c.restore()
        for (a, b, txt) in labels:
            if a <= t < b: label(c, txt, min(1, (t - a) / 0.2) * min(1, (b - t) / 0.25))
        cur = next((x for x in sents if x["t0"] - 0.05 <= t < x["t1"] + 0.3), None)
        if cur: L.sub_text(c, cur["text"])
        if sh["card"] and lt < 2.4: L.chapter_card(c, sh["card"], min(1, lt / 0.3) * min(1, (2.4 - lt) / 0.4))
        if lt < 0.1 and si > 0: c.rectangle(0, 0, W, H); c.set_source_rgba(0.04, 0.04, 0.07, 1 - lt / 0.1); c.fill()
        s.flush(); p.stdin.write(bytes(s.get_data()))
        if f % (FPS * 30) == 0: print(f"{int(t // 60)}:{int(t % 60):02d} / {int(total // 60)}:{int(total % 60):02d}", flush=True)
    p.stdin.close(); p.wait(); print("GOTOVO", out)


def preview(idx, outp):
    tm = json.load(open(os.path.join(HERE, "out", "ep02", "timing.json")))
    shots, labels, sents = shots_from_timing(tm)
    fs = []
    for k in idx:
        sh = shots[k]; d = sh["t1"] - sh["t0"]; t = sh["t0"] + d * 0.6
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); sh["scene"](c, d * 0.6, d, sh["v"])
        for (a, b, txt) in labels:
            if a <= t < b: label(c, txt, 1)
        cur = next((x for x in sents if x["t0"] - 0.05 <= t < x["t1"] + 0.3), None)
        if cur: L.sub_text(c, cur["text"])
        f = f"{outp}_{k}.png"; s.write_to_png(f); fs.append(f)
    print(len(shots), "kadrova"); return fs


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        preview([int(x) for x in sys.argv[3:]], sys.argv[2])
    else:
        build()
