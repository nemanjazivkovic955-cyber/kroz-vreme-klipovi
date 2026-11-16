"""Kroz vreme - engine za crtane klipove (Mila, Luka i Sova Sofija).
Crta 1080x1920 @30fps kadrove pomocu pycairo i salje ih u ffmpeg.
Svaka epizoda definise listu scena: (trajanje, draw_fn, dijalozi).
"""
import math, random, subprocess, os, sys
import cairo

W, H, FPS = 1080, 1920, 30
FONT = "Poppins"

# ---------- osnovno ----------
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

def pop(x):  # elasticni "pop" 0->1
    x = max(0.0, min(1.0, x))
    return 1 - math.cos(x * math.pi * 2.2) * math.exp(-x * 5) if x < 1 else 1.0

def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def col(ctx, h, a=1.0):
    r, g, b = rgb(h)
    ctx.set_source_rgba(r, g, b, a)

def ellipse(ctx, x, y, rx, ry):
    ctx.save(); ctx.translate(x, y); ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()

def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

def fill_stroke(ctx, fillc, strokec="#3a2a1e", lw=6, a=1.0):
    col(ctx, fillc, a); ctx.fill_preserve()
    col(ctx, strokec, a); ctx.set_line_width(lw); ctx.stroke()

def vgrad(ctx, y0, y1, c0, c1):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *rgb(c0)); g.add_color_stop_rgb(1, *rgb(c1))
    return g

# ---------- tekst ----------
def font(ctx, size, bold=True):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

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

def text_c(ctx, text, cx, y, size, color="#ffffff", outline="#2b1d14", ow=10, a=1.0, maxw=900, lh=1.18):
    """Centriran tekst sa obrubom (stil crtanog). Vraca visinu."""
    font(ctx, size)
    lines = wrap(ctx, text, maxw)
    for i, ln in enumerate(lines):
        e = ctx.text_extents(ln)
        x = cx - e.x_advance / 2; yy = y + i * size * lh
        ctx.move_to(x, yy); ctx.text_path(ln)
        if ow:
            col(ctx, outline, a); ctx.set_line_width(ow); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.stroke_preserve()
        col(ctx, color, a); ctx.fill()
    return len(lines) * size * lh

SPEAKERS = {
    "Sofija": "#8a5a2b", "Mila": "#d6336c", "Luka": "#1c7ed6", "": "#5c3d99",
}

def speech_box(ctx, speaker, text, t_in, t, chars_per_s=38):
    """Okvir sa dijalogom na dnu (iznad TikTok UI). Tekst se 'kuca'."""
    a = ease((t - t_in) / 0.25)
    if a <= 0: return
    n = int((t - t_in) * chars_per_s)
    shown = text if n >= len(text) else text[:n]
    x, y, w = 70, 1170, 940
    font(ctx, 54)
    lines = wrap(ctx, text, w - 90)
    h = 70 + len(lines) * 66
    yoff = (1 - a) * 40
    ctx.save(); ctx.translate(0, yoff)
    # senka
    rrect(ctx, x + 8, y + 12, w, h, 40); col(ctx, "#000000", 0.18 * a); ctx.fill()
    rrect(ctx, x, y, w, h, 40); col(ctx, "#fffaf0", a); ctx.fill_preserve()
    col(ctx, SPEAKERS.get(speaker, "#5c3d99"), a); ctx.set_line_width(8); ctx.stroke()
    if speaker:
        font(ctx, 40)
        tw = ctx.text_extents(speaker).x_advance
        rrect(ctx, x + 40, y - 34, tw + 50, 64, 32); col(ctx, SPEAKERS.get(speaker), a); ctx.fill()
        ctx.move_to(x + 65, y + 12); col(ctx, "#ffffff", a); ctx.show_text(speaker)
    font(ctx, 54)
    # kucanje: prikazi samo prvih n karaktera, ali zadrzi prelom redova punog teksta
    left = len(shown)
    for i, ln in enumerate(lines):
        part = ln[:max(0, left)]
        left -= len(ln) + 1
        ctx.move_to(x + 45, y + 95 + i * 66); col(ctx, "#2b1d14", a); ctx.show_text(part)
    ctx.restore()

def caption(ctx, text, t, t_in=0.0, y=300, size=72, color="#ffd43b"):
    a = ease((t - t_in) / 0.35)
    if a <= 0: return
    s = 0.6 + 0.4 * pop((t - t_in) / 0.6)
    ctx.save(); ctx.translate(W / 2, y); ctx.scale(s, s); ctx.translate(-W / 2, -y)
    text_c(ctx, text, W / 2, y, size, color=color, a=a, ow=14)
    ctx.restore()

# ---------- pozadine ----------
def sky(ctx, top="#74c0fc", bottom="#d0ebff"):
    ctx.rectangle(0, 0, W, H); ctx.set_source(vgrad(ctx, 0, H, top, bottom)); ctx.fill()

def sun(ctx, x, y, r, t):
    for i in range(12):
        ang = i * math.pi / 6 + t * 0.3
        ctx.move_to(x + math.cos(ang) * (r + 15), y + math.sin(ang) * (r + 15))
        ctx.line_to(x + math.cos(ang) * (r + 55), y + math.sin(ang) * (r + 55))
    col(ctx, "#ffd43b"); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.arc(x, y, r, 0, 2 * math.pi); fill_stroke(ctx, "#ffe066", "#f59f00", 8)

def cloud(ctx, x, y, s=1.0, a=0.95):
    col(ctx, "#ffffff", a)
    for dx, dy, r in ((0, 0, 50), (55, -25, 60), (115, 0, 50), (55, 15, 55)):
        ctx.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); ctx.fill()

def clouds(ctx, t, ys=(420, 560, 700)):
    for i, y in enumerate(ys):
        x = ((t * (25 + i * 12) + i * 420) % (W + 400)) - 250
        cloud(ctx, x, y, 0.9 + 0.2 * i)

def hills(ctx, base=1150, c1="#69db7c", c2="#40c057"):
    ctx.move_to(0, base - 150)
    ctx.curve_to(300, base - 330, 600, base - 120, W, base - 260)
    ctx.line_to(W, H); ctx.line_to(0, H); ctx.close_path(); col(ctx, c1); ctx.fill()
    ctx.move_to(0, base - 40)
    ctx.curve_to(350, base - 160, 700, base + 20, W, base - 90)
    ctx.line_to(W, H); ctx.line_to(0, H); ctx.close_path(); col(ctx, c2); ctx.fill()

def tree(ctx, x, y, s=1.0, t=0.0):
    sw = math.sin(t * 1.5 + x) * 4 * s
    ctx.rectangle(x - 14 * s, y - 90 * s, 28 * s, 90 * s); fill_stroke(ctx, "#8d5a2b", "#5c3a1a", 4 * s)
    for dx, dy, r in ((0, -170, 70), (-50, -120, 55), (50, -120, 55)):
        ctx.arc(x + dx * s + sw, y + dy * s, r * s, 0, 2 * math.pi)
        fill_stroke(ctx, "#2f9e44", "#1b6b2f", 5 * s)

def river(ctx, y, t, h=120, label=None):
    ctx.move_to(0, y)
    for i in range(0, W + 1, 20):
        ctx.line_to(i, y + math.sin(i / 90 + t * 2) * 10)
    ctx.line_to(W, y + h); ctx.line_to(0, y + h); ctx.close_path()
    col(ctx, "#4dabf7"); ctx.fill()
    col(ctx, "#ffffff", 0.6); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(6):
        xx = ((k * 220 + t * 80) % (W + 200)) - 100
        ctx.move_to(xx, y + h * 0.45); ctx.line_to(xx + 70, y + h * 0.45); ctx.stroke()
    if label:
        text_c(ctx, label, W / 2, y + h * 0.68, 46, "#ffffff", "#1864ab", 8)

def room(ctx, t):
    ctx.rectangle(0, 0, W, H); ctx.set_source(vgrad(ctx, 0, 1150, "#ffe8cc", "#ffd8a8")); ctx.fill()
    ctx.rectangle(0, 1150, W, H - 1150); col(ctx, "#c08552"); ctx.fill()
    for i in range(0, W, 120):
        ctx.move_to(i, 1150); ctx.line_to(i, H); col(ctx, "#a06a3c"); ctx.set_line_width(4); ctx.stroke()
    # prozor
    rrect(ctx, 600, 430, 360, 330, 20); fill_stroke(ctx, "#a5d8ff", "#8d5a2b", 16)
    ctx.move_to(780, 430); ctx.line_to(780, 760); ctx.move_to(600, 595); ctx.line_to(960, 595)
    col(ctx, "#8d5a2b"); ctx.set_line_width(12); ctx.stroke()
    # polica sa knjigama
    ctx.rectangle(90, 560, 380, 22); col(ctx, "#8d5a2b"); ctx.fill()
    cols = ["#e03131", "#1971c2", "#2f9e44", "#f08c00", "#7048e8", "#c2255c"]
    x = 105
    for i, c in enumerate(cols):
        hh = 120 + (i * 37) % 50
        ctx.rectangle(x, 560 - hh, 46, hh); fill_stroke(ctx, c, "#3a2a1e", 3); x += 58

def hourglass(ctx, x, y, s, t, glow=0.0):
    if glow > 0:
        g = cairo.RadialGradient(x, y, 10, x, y, 220 * s)
        g.add_color_stop_rgba(0, 1, 0.9, 0.4, 0.8 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
        ctx.arc(x, y, 220 * s, 0, 2 * math.pi); ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-75, -125, 150, 22); fill_stroke(ctx, "#b5651d", "#5c3a1a", 5)
    ctx.rectangle(-75, 103, 150, 22); fill_stroke(ctx, "#b5651d", "#5c3a1a", 5)
    ctx.move_to(-55, -103); ctx.curve_to(-55, -30, -8, -15, -8, 0); ctx.curve_to(-8, 15, -55, 30, -55, 103)
    ctx.line_to(55, 103); ctx.curve_to(55, 30, 8, 15, 8, 0); ctx.curve_to(8, -15, 55, -30, 55, -103); ctx.close_path()
    fill_stroke(ctx, "#e7f5ff", "#5c3a1a", 5, 0.9)
    lvl = (t * 0.15) % 1
    ctx.move_to(-45 * (1 - lvl), -20 - 60 * (1 - lvl)); ctx.line_to(45 * (1 - lvl), -20 - 60 * (1 - lvl)); ctx.line_to(0, -5); ctx.close_path()
    col(ctx, "#fcc419"); ctx.fill()
    ctx.move_to(-50, 100); ctx.line_to(50, 100); ctx.line_to(0, 100 - 70 * lvl - 10); ctx.close_path(); ctx.fill()
    ctx.restore()

# ---------- likovi ----------
def _eyes(ctx, x, y, s, t, seed, look=0.0):
    blink = (math.sin(t * 1.3 + seed) > 0.985) or ((t + seed) % 3.7 < 0.12)
    for dx in (-28, 28):
        if blink:
            ctx.move_to(x + (dx - 12) * s, y); ctx.line_to(x + (dx + 12) * s, y)
            col(ctx, "#2b1d14"); ctx.set_line_width(5 * s); ctx.stroke()
        else:
            ellipse(ctx, x + dx * s, y, 15 * s, 19 * s); col(ctx, "#ffffff"); ctx.fill()
            ctx.arc(x + (dx + look * 5) * s, y + 2 * s, 10 * s, 0, 2 * math.pi); col(ctx, "#2b1d14"); ctx.fill()
            ctx.arc(x + (dx + look * 5 + 3) * s, y - 3 * s, 3.5 * s, 0, 2 * math.pi); col(ctx, "#ffffff"); ctx.fill()

def _mouth(ctx, x, y, s, t, talking):
    if talking:
        o = 0.35 + 0.65 * abs(math.sin(t * 13))
        ellipse(ctx, x, y + 4 * s, 18 * s, 14 * s * o + 3 * s); col(ctx, "#8b1e2d"); ctx.fill()
    else:
        ctx.arc(x, y - 6 * s, 20 * s, 0.2 * math.pi, 0.8 * math.pi)
        col(ctx, "#8b1e2d"); ctx.set_line_width(5 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()

def kid(ctx, x, y, s, who, t, talking=False, wave=False, look=0.0, jump=0.0):
    """who: 'mila' ili 'luka'. (x,y) = tacka izmedju stopala. Visina ~ 470*s."""
    seed = 1.0 if who == "mila" else 2.7
    by = -abs(math.sin(t * 2.2 + seed)) * 6 * s - jump * s
    shirt = "#e64980" if who == "mila" else "#228be6"
    skin = "#ffd8b5"
    lw = 5 * s
    ctx.save(); ctx.translate(0, by)
    # noge
    for dx in (-30, 30):
        ctx.rectangle(x + (dx - 12) * s, y - 120 * s, 24 * s, 110 * s)
        fill_stroke(ctx, skin if who == "mila" else "#364fc7", "#3a2a1e", lw)
        ellipse(ctx, x + (dx + 6) * s, y - 8 * s, 30 * s, 15 * s); fill_stroke(ctx, "#5c3a1a", "#3a2a1e", lw)
    # telo
    if who == "mila":
        ctx.move_to(x - 45 * s, y - 280 * s); ctx.line_to(x + 45 * s, y - 280 * s)
        ctx.line_to(x + 90 * s, y - 110 * s); ctx.line_to(x - 90 * s, y - 110 * s); ctx.close_path()
        fill_stroke(ctx, shirt, "#3a2a1e", lw)
        # sara (narodni motiv)
        ctx.move_to(x - 70 * s, y - 150 * s); ctx.line_to(x + 70 * s, y - 150 * s)
        col(ctx, "#ffd43b"); ctx.set_line_width(10 * s); ctx.stroke()
    else:
        rrect(ctx, x - 60 * s, y - 285 * s, 120 * s, 175 * s, 30 * s); fill_stroke(ctx, shirt, "#3a2a1e", lw)
        ctx.rectangle(x - 60 * s, y - 140 * s, 120 * s, 30 * s); fill_stroke(ctx, "#364fc7", "#3a2a1e", lw)
    # ruke
    for side in (-1, 1):
        ctx.save(); ctx.translate(x + side * 55 * s, y - 265 * s)
        if wave and side == 1:
            ctx.rotate(-2.3 + math.sin(t * 9) * 0.35)
        else:
            ctx.rotate(side * -0.25 + math.sin(t * 2 + side) * 0.05)
        rrect(ctx, -13 * s, 0, 26 * s, 115 * s, 13 * s); fill_stroke(ctx, shirt, "#3a2a1e", lw)
        ctx.arc(0, 120 * s, 17 * s, 0, 2 * math.pi); fill_stroke(ctx, skin, "#3a2a1e", lw)
        ctx.restore()
    # glava
    hx, hy = x, y - 370 * s
    if who == "mila":  # pletenice
        for side in (-1, 1):
            for k in range(3):
                ctx.arc(hx + side * 92 * s, hy + (10 + k * 34) * s, 19 * s, 0, 2 * math.pi)
                fill_stroke(ctx, "#7a3e12", "#3a2a1e", lw)
            ctx.arc(hx + side * 92 * s, hy + 112 * s, 9 * s, 0, 2 * math.pi); fill_stroke(ctx, "#e03131", "#3a2a1e", 3 * s)
    ctx.arc(hx, hy, 90 * s, 0, 2 * math.pi); fill_stroke(ctx, skin, "#3a2a1e", lw)
    # kosa
    if who == "mila":
        ctx.arc(hx, hy - 5 * s, 92 * s, math.pi * 1.0, math.pi * 2.0)
        ctx.curve_to(hx + 60 * s, hy - 30 * s, hx - 20 * s, hy - 60 * s, hx - 92 * s, hy - 5 * s)
        fill_stroke(ctx, "#7a3e12", "#3a2a1e", lw)
    else:
        ctx.move_to(hx - 92 * s, hy - 10 * s)
        ctx.curve_to(hx - 100 * s, hy - 120 * s, hx + 100 * s, hy - 130 * s, hx + 92 * s, hy - 10 * s)
        for k in range(5):
            px = hx + 92 * s - k * 46 * s
            ctx.line_to(px - 23 * s, hy - 55 * s); ctx.line_to(px - 46 * s, hy - 30 * s)
        ctx.close_path(); fill_stroke(ctx, "#f2c14e", "#3a2a1e", lw)
    # lice
    for dx in (-52, 52):
        ellipse(ctx, hx + dx * s, hy + 30 * s, 16 * s, 10 * s); col(ctx, "#ff8787", 0.6); ctx.fill()
    _eyes(ctx, hx, hy + 5 * s, s, t, seed, look)
    _mouth(ctx, hx, hy + 50 * s, s, t, talking)
    ctx.restore()

def owl(ctx, x, y, s, t, talking=False, flap=False, look=0.0):
    """Sova Sofija. (x,y) = dno (noge). Visina ~ 330*s."""
    by = -abs(math.sin(t * 1.8)) * 5 * s
    lw = 5 * s
    ctx.save(); ctx.translate(0, by)
    # krila
    for side in (-1, 1):
        ctx.save(); ctx.translate(x + side * 95 * s, y - 180 * s)
        ang = (math.sin(t * 14) * 0.5 + 0.4) if flap else 0.08
        ctx.rotate(side * ang)
        ellipse(ctx, side * 10 * s, 40 * s, 38 * s, 85 * s); fill_stroke(ctx, "#8a5a2b", "#3a2a1e", lw)
        ctx.restore()
    # telo
    ellipse(ctx, x, y - 160 * s, 115 * s, 150 * s); fill_stroke(ctx, "#b07a45", "#3a2a1e", lw)
    ellipse(ctx, x, y - 120 * s, 75 * s, 100 * s); col(ctx, "#f1d3a8"); ctx.fill()
    for r in range(3):
        for c in range(3):
            ctx.arc(x + (c - 1) * 35 * s, y - (150 - r * 35) * s, 12 * s, 0.1 * math.pi, 0.9 * math.pi)
            col(ctx, "#c49a6c"); ctx.set_line_width(4 * s); ctx.stroke()
    # usi (perca)
    for side in (-1, 1):
        ctx.move_to(x + side * 60 * s, y - 290 * s); ctx.line_to(x + side * 100 * s, y - 345 * s)
        ctx.line_to(x + side * 95 * s, y - 270 * s); ctx.close_path(); fill_stroke(ctx, "#8a5a2b", "#3a2a1e", lw)
    # oci + naocare
    blink = (t + 0.5) % 4.1 < 0.12
    for dx in (-45, 45):
        ctx.arc(x + dx * s, y - 245 * s, 42 * s, 0, 2 * math.pi); fill_stroke(ctx, "#ffffff", "#3a2a1e", lw)
        if blink:
            ctx.move_to(x + (dx - 25) * s, y - 245 * s); ctx.line_to(x + (dx + 25) * s, y - 245 * s)
            col(ctx, "#2b1d14"); ctx.set_line_width(6 * s); ctx.stroke()
        else:
            ctx.arc(x + (dx + look * 8) * s, y - 242 * s, 20 * s, 0, 2 * math.pi); col(ctx, "#2b1d14"); ctx.fill()
            ctx.arc(x + (dx + look * 8 + 6) * s, y - 250 * s, 6 * s, 0, 2 * math.pi); col(ctx, "#ffffff"); ctx.fill()
        ctx.arc(x + dx * s, y - 245 * s, 50 * s, 0, 2 * math.pi); col(ctx, "#5f3dc4"); ctx.set_line_width(7 * s); ctx.stroke()
    ctx.move_to(x - 5 * s, y - 250 * s); ctx.line_to(x + 5 * s, y - 250 * s); ctx.stroke()
    # kljun
    o = (abs(math.sin(t * 12)) * 14 * s) if talking else 0
    ctx.move_to(x - 18 * s, y - 205 * s); ctx.line_to(x + 18 * s, y - 205 * s); ctx.line_to(x, y - 180 * s); ctx.close_path()
    fill_stroke(ctx, "#fab005", "#3a2a1e", 4 * s)
    if o > 1:
        ctx.move_to(x - 13 * s, y - 196 * s + o * 0.2); ctx.line_to(x + 13 * s, y - 196 * s + o * 0.2); ctx.line_to(x, y - 180 * s + o)
        ctx.close_path(); fill_stroke(ctx, "#f08c00", "#3a2a1e", 4 * s)
    # nogice
    for dx in (-35, 35):
        for k in (-1, 0, 1):
            ctx.move_to(x + dx * s, y - 14 * s); ctx.line_to(x + (dx + k * 14) * s, y)
        col(ctx, "#f08c00"); ctx.set_line_width(7 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()

def villager(ctx, x, y, s, t, tunic="#c92a2a", walking=True, beard=False, bundle=False, hair="#5c3a1a", skirt=False, talking=False):
    """Stari Sloven / Slovenka. (x,y) = stopala. Visina ~ 430*s."""
    lw = 5 * s
    ph = t * 6 + x * 0.01
    sw = math.sin(ph) * 0.35 if walking else 0
    by = -abs(math.sin(ph)) * 8 * s if walking else 0
    ctx.save(); ctx.translate(0, by)
    for k, side in enumerate((-1, 1)):
        ctx.save(); ctx.translate(x + side * 18 * s, y - 130 * s); ctx.rotate(sw * side)
        ctx.rectangle(-12 * s, 0, 24 * s, 125 * s); fill_stroke(ctx, "#e9d8a6", "#3a2a1e", lw)
        ellipse(ctx, 8 * s, 125 * s, 24 * s, 11 * s); fill_stroke(ctx, "#6f4518", "#3a2a1e", lw)
        ctx.restore()
    if skirt:
        ctx.move_to(x - 45 * s, y - 300 * s); ctx.line_to(x + 45 * s, y - 300 * s)
        ctx.line_to(x + 75 * s, y - 95 * s); ctx.line_to(x - 75 * s, y - 95 * s); ctx.close_path()
    else:
        rrect(ctx, x - 55 * s, y - 300 * s, 110 * s, 185 * s, 25 * s)
    fill_stroke(ctx, tunic, "#3a2a1e", lw)
    ctx.move_to(x - 55 * s, y - 175 * s); ctx.line_to(x + 55 * s, y - 175 * s)
    col(ctx, "#ffd43b"); ctx.set_line_width(9 * s); ctx.stroke()
    if bundle:
        ctx.arc(x - 70 * s, y - 280 * s, 55 * s, 0, 2 * math.pi); fill_stroke(ctx, "#a68a64", "#3a2a1e", lw)
    for side in (-1, 1):
        ctx.save(); ctx.translate(x + side * 50 * s, y - 285 * s); ctx.rotate(-sw * side * 0.8 + side * -0.15)
        rrect(ctx, -11 * s, 0, 22 * s, 110 * s, 11 * s); fill_stroke(ctx, tunic, "#3a2a1e", lw)
        ctx.arc(0, 113 * s, 14 * s, 0, 2 * math.pi); fill_stroke(ctx, "#f3c79b", "#3a2a1e", lw)
        ctx.restore()
    hx, hy = x, y - 365 * s
    ctx.arc(hx, hy, 65 * s, 0, 2 * math.pi); fill_stroke(ctx, "#f3c79b", "#3a2a1e", lw)
    ctx.arc(hx, hy - 8 * s, 67 * s, math.pi, 2 * math.pi); fill_stroke(ctx, hair, "#3a2a1e", lw)
    if skirt:  # marama
        ctx.arc(hx, hy - 10 * s, 70 * s, math.pi * 0.95, math.pi * 2.05); fill_stroke(ctx, "#f8f0e3", "#3a2a1e", lw)
    if beard:
        ctx.arc(hx, hy + 25 * s, 50 * s, 0.05 * math.pi, 0.95 * math.pi); fill_stroke(ctx, hair, "#3a2a1e", lw)
    for dx in (-22, 22):
        ctx.arc(hx + dx * s, hy - 2 * s, 7 * s, 0, 2 * math.pi); col(ctx, "#2b1d14"); ctx.fill()
    if talking:
        ellipse(ctx, hx, hy + 30 * s, 12 * s, (4 + 8 * abs(math.sin(t * 12))) * s); col(ctx, "#8b1e2d"); ctx.fill()
    elif not beard:
        ctx.arc(hx, hy + 18 * s, 15 * s, 0.2 * math.pi, 0.8 * math.pi); col(ctx, "#8b1e2d"); ctx.set_line_width(4 * s); ctx.stroke()
    ctx.restore()

def log_house(ctx, x, y, s, grow=1.0):
    """Drvena kuca. (x,y) = dno sredina. grow 0..1 = gradnja."""
    if grow <= 0: return
    w, h = 300 * s, 190 * s
    g = ease(grow)
    hh = h * min(1, g * 1.4)
    for i in range(int(hh // (24 * s)) + 1):
        yy = y - (i + 1) * 24 * s
        if y - yy > hh + 1: break
        rrect(ctx, x - w / 2, yy, w, 24 * s, 12 * s); fill_stroke(ctx, "#a0612b", "#5c3a1a", 3 * s)
    if g > 0.7:
        ra = ease((g - 0.7) / 0.3)
        ctx.move_to(x - w / 2 - 30 * s, y - h); ctx.line_to(x, y - h - 150 * s * ra); ctx.line_to(x + w / 2 + 30 * s, y - h)
        ctx.close_path(); fill_stroke(ctx, "#e9b949", "#9c6b0e", 5 * s)
        for k in range(-3, 4):
            ctx.move_to(x + k * 35 * s, y - h); ctx.line_to(x + k * 8 * s, y - h - 120 * s * ra)
        col(ctx, "#c99a2e"); ctx.set_line_width(3 * s); ctx.stroke()
        rrect(ctx, x - 35 * s, y - 120 * s, 70 * s, 120 * s, 8 * s); fill_stroke(ctx, "#6f4518", "#3a2a1e", 4 * s)

def sheep(ctx, x, y, s, t):
    b = -abs(math.sin(t * 3 + x)) * 4 * s
    for dx in (-25, 25):
        ctx.rectangle(x + (dx - 5) * s, y - 35 * s + b, 10 * s, 35 * s); col(ctx, "#343a40"); ctx.fill()
    for dx, dy in ((-30, -60), (0, -75), (30, -60), (-15, -50), (15, -50)):
        ctx.arc(x + dx * s, y + dy * s + b, 30 * s, 0, 2 * math.pi); col(ctx, "#f8f9fa"); ctx.fill()
    ellipse(ctx, x + 55 * s, y - 70 * s + b, 20 * s, 25 * s); col(ctx, "#343a40"); ctx.fill()

def bread(ctx, x, y, s):
    ellipse(ctx, x, y, 70 * s, 40 * s); fill_stroke(ctx, "#e8a54b", "#8a5a1a", 5 * s)
    for k in (-1, 0, 1):
        ctx.move_to(x + k * 30 * s - 10 * s, y - 25 * s); ctx.line_to(x + k * 30 * s + 10 * s, y - 5 * s)
    col(ctx, "#8a5a1a"); ctx.set_line_width(4 * s); ctx.stroke()
    ellipse(ctx, x, y - 32 * s, 14 * s, 8 * s); fill_stroke(ctx, "#ffffff", "#adb5bd", 2 * s)  # so

def sparkles(ctx, t, n=18, seed=3, color="#ffe066"):
    rnd = random.Random(seed)
    for i in range(n):
        x, y = rnd.uniform(60, W - 60), rnd.uniform(200, 1150)
        ph = rnd.uniform(0, 6.28)
        a = 0.5 + 0.5 * math.sin(t * 4 + ph)
        r = 10 + 8 * a
        ctx.move_to(x, y - r); ctx.line_to(x + r * 0.3, y - r * 0.3); ctx.line_to(x + r, y)
        ctx.line_to(x + r * 0.3, y + r * 0.3); ctx.line_to(x, y + r); ctx.line_to(x - r * 0.3, y + r * 0.3)
        ctx.line_to(x - r, y); ctx.line_to(x - r * 0.3, y - r * 0.3); ctx.close_path()
        col(ctx, color, a); ctx.fill()

def brand(ctx):
    """Mali znak serijala gore levo."""
    font(ctx, 34)
    text = "Kroz vreme"
    rrect(ctx, 40, 1500, ctx.text_extents(text).x_advance + 40, 54, 27); col(ctx, "#000000", 0.25); ctx.fill()

# ---------- render ----------
def speaking(dialog, t):
    for (a, b, who, txt) in dialog:
        if a <= t < b: return who
    return None

def render_scene(path, dur, draw, dialog=(), fade_in=0.25):
    tmp = path[:-4] + ".tmp.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    n = int(round(dur * FPS))
    for i in range(n):
        t = i / FPS
        ctx = cairo.Context(surf)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        draw(ctx, t, speaking(dialog, t))
        for (a, b, who, txt) in dialog:
            if a <= t < b + 0.0:
                speech_box(ctx, who, txt, a, t)
        if fade_in and t < fade_in:
            ctx.rectangle(0, 0, W, H); col(ctx, "#ffffff", 1 - t / fade_in); ctx.fill()
        surf.flush()
        p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, path)
    else:
        raise SystemExit("ffmpeg error " + path)

def frame_png(path, draw, t, dialog=()):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    draw(ctx, t, speaking(dialog, t))
    for (a, b, who, txt) in dialog:
        if a <= t < b: speech_box(ctx, who, txt, a, t)
    surf.write_to_png(path)

# ---------- muzika ----------
def music(path, dur, seed=1, bpm=112):
    import numpy as np, wave
    sr = 44100
    n = int(dur * sr)
    out = np.zeros(n)
    beat = 60 / bpm
    rnd = random.Random(seed)
    scale = [60, 62, 64, 67, 69, 72, 74, 76]
    prog = [(48, [60, 64, 67]), (43, [55, 59, 62]), (45, [57, 60, 64]), (41, [53, 57, 60])]
    def tone(f, d, amp, kind="tri"):
        tt = np.arange(int(d * sr)) / sr
        if kind == "tri":
            w = 2 * np.abs(2 * ((tt * f) % 1) - 1) - 1
        else:
            w = np.sin(2 * np.pi * f * tt)
        env = np.minimum(1, tt / 0.01) * np.exp(-tt * (3.5 if kind == "tri" else 1.5))
        return w * env * amp
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    tcur, bar = 0.0, 0
    motif = [rnd.choice(scale) for _ in range(8)]
    while tcur < dur:
        root, chord = prog[bar % 4]
        if bar % 4 == 0 and bar > 0:
            motif = [m if rnd.random() < 0.6 else rnd.choice(scale) for m in motif]
        for b in range(4):
            st = int((tcur + b * beat) * sr)
            seg = tone(hz(root if b % 2 == 0 else root + 7), beat * 0.9, 0.16, "sin")
            e = min(n, st + len(seg))
            if e > st: out[st:e] += seg[:e - st]
            for k in range(2):
                st2 = int((tcur + (b + k * 0.5) * beat) * sr)
                m = motif[(b * 2 + k) % 8]
                if rnd.random() < 0.85:
                    seg = tone(hz(m), beat * 0.6, 0.12)
                    e = min(n, st2 + len(seg))
                    if e > st2: out[st2:e] += seg[:e - st2]
            # cin (shaker)
            st3 = int((tcur + (b + 0.5) * beat) * sr)
            nl = int(0.04 * sr)
            seg = (np.random.RandomState(b + bar).rand(nl) * 2 - 1) * np.exp(-np.arange(nl) / sr * 80) * 0.05
            e = min(n, st3 + nl)
            if e > st3: out[st3:e] += seg[:e - st3]
        tcur += 4 * beat; bar += 1
    fade = int(2.5 * sr)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[:int(0.3 * sr)] *= np.linspace(0, 1, int(0.3 * sr))
    out = out / (np.abs(out).max() + 1e-9) * 0.5
    data = (out * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(data.tobytes())

def assemble(scene_files, audio, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for s in scene_files: f.write(f"file '{os.path.abspath(s)}'\n")
    silent = out[:-4] + ".silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", audio, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
