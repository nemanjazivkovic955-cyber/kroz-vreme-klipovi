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

# ---------- likovi (v2: senke, gradijenti, ekspresivne oci) ----------
def shade(h, f):
    """f<0 tamnije, f>0 svetlije."""
    r, g, b = rgb(h)
    if f < 0:
        r, g, b = r * (1 + f), g * (1 + f), b * (1 + f)
    else:
        r, g, b = r + (1 - r) * f, g + (1 - g) * f, b + (1 - b) * f
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(c * 255)))) for c in (r, g, b))

def paint(ctx, base, lw, light=0.22, dark=-0.18, outline=None, a=1.0, radial=False):
    """Popuni putanju gradijentom (svetlo gore-levo, tamnije dole-desno) i obrubi tamnijom nijansom boje."""
    x0, y0, x1, y1 = ctx.path_extents()
    w, h = max(1, x1 - x0), max(1, y1 - y0)
    if radial:
        cx, cy = x0 + w * 0.36, y0 + h * 0.3
        g = cairo.RadialGradient(cx, cy, 0, cx, cy, max(w, h) * 0.85)
    else:
        g = cairo.LinearGradient(x0 + w * 0.2, y0, x0 + w * 0.6, y1)
    g.add_color_stop_rgba(0, *rgb(shade(base, light)), a)
    g.add_color_stop_rgba(1, *rgb(shade(base, dark)), a)
    ctx.set_source(g); ctx.fill_preserve()
    col(ctx, outline or shade(base, -0.55), a); ctx.set_line_width(lw); ctx.stroke()

def ground_shadow(ctx, x, y, w, a=0.22):
    ctx.save(); ctx.translate(x, y); ctx.scale(w, w * 0.18)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
    g.add_color_stop_rgba(0, 0, 0, 0, a); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.fill(); ctx.restore()

def gloss(ctx, x, y, rx, ry, a=0.35, rot=-0.5):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); col(ctx, "#ffffff", a); ctx.fill()

def _blink(t, seed, period=3.7):
    ph = (t + seed * 1.37) % period
    return min(1.0, abs(ph - 0.09) / 0.09) if ph < 0.18 else 1.0

def _eyes(ctx, x, y, s, t, seed, look=0.0, iris="#6b4423", skin="#ffd8b5",
          size=1.0, lashes=False, brow="#5c3a1a", talking=False, gap=30):
    op = _blink(t, seed)
    rx, ry = 21 * s * size, 26 * s * size
    lift = (3 + 3 * abs(math.sin(t * 4))) * s if talking else 0
    for i, dx in enumerate((-gap, gap)):
        ex = x + dx * s
        # belo oka
        ellipse(ctx, ex, y, rx, ry)
        g = cairo.LinearGradient(0, y - ry, 0, y + ry)
        g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(1, *rgb("#dfe7f2"))
        ctx.set_source(g); ctx.fill()
        ctx.save(); ellipse(ctx, ex, y, rx, ry); ctx.clip()
        ix, iy = ex + look * 7 * s, y + 3 * s
        ir = 15.5 * s * size
        gi = cairo.RadialGradient(ix - ir * 0.2, iy - ir * 0.3, 0, ix, iy, ir)
        gi.add_color_stop_rgb(0, *rgb(shade(iris, 0.35))); gi.add_color_stop_rgb(1, *rgb(shade(iris, -0.35)))
        ctx.arc(ix, iy, ir, 0, 2 * math.pi); ctx.set_source(gi); ctx.fill()
        ctx.arc(ix, iy, ir * 0.52, 0, 2 * math.pi); col(ctx, "#1a120c"); ctx.fill()
        ctx.arc(ix - ir * 0.38, iy - ir * 0.42, ir * 0.34, 0, 2 * math.pi); col(ctx, "#ffffff"); ctx.fill()
        ctx.arc(ix + ir * 0.35, iy + ir * 0.35, ir * 0.14, 0, 2 * math.pi); col(ctx, "#ffffff", 0.9); ctx.fill()
        # gornji kapak (treptanje) + senka kapka
        lid = y - ry + 2 * ry * (1 - op)
        ctx.rectangle(ex - rx - 2, y - ry - 2, 2 * rx + 4, lid - (y - ry) + 2)
        col(ctx, skin); ctx.fill()
        ctx.rectangle(ex - rx, lid, 2 * rx, 6 * s); col(ctx, "#000000", 0.08); ctx.fill()
        ctx.restore()
        # obrub oka (gornja linija deblja)
        ellipse(ctx, ex, y, rx, ry); col(ctx, "#3a2a1e"); ctx.set_line_width(2.5 * s); ctx.stroke()
        ctx.save(); ctx.translate(ex, y); ctx.scale(rx, ry)
        ctx.arc(0, 0, 1, math.pi * 1.1, math.pi * 1.9); ctx.restore()
        col(ctx, "#2b1d14"); ctx.set_line_width(5 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        if lashes:
            side = -1 if dx < 0 else 1
            for k in range(2):
                a0 = math.pi * (1.12 + 0.08 * k) if side < 0 else math.pi * (1.88 - 0.08 * k)
                px, py = ex + math.cos(a0) * rx, y + math.sin(a0) * ry
                ctx.move_to(px, py); ctx.line_to(px + side * 9 * s, py - (7 - k * 3) * s)
            col(ctx, "#2b1d14"); ctx.set_line_width(3.5 * s); ctx.stroke()
        # obrve
        by_ = y - ry - 13 * s - lift
        side = -1 if dx < 0 else 1
        ctx.move_to(ex - 16 * s, by_ + (2 if side < 0 else -1) * s)
        ctx.curve_to(ex - 6 * s, by_ - 7 * s, ex + 6 * s, by_ - 7 * s, ex + 16 * s, by_ + (-1 if side < 0 else 2) * s)
        col(ctx, brow); ctx.set_line_width(6 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()

def _mouth(ctx, x, y, s, t, talking, w=20):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if talking:
        o = 0.3 + 0.7 * abs(math.sin(t * 13)) * (0.6 + 0.4 * abs(math.sin(t * 5.3)))
        hh = (6 + 16 * o) * s
        ctx.move_to(x - w * s, y - 2 * s)
        ctx.curve_to(x - w * 0.6 * s, y - 6 * s, x + w * 0.6 * s, y - 6 * s, x + w * s, y - 2 * s)
        ctx.curve_to(x + w * 0.7 * s, y + hh, x - w * 0.7 * s, y + hh, x - w * s, y - 2 * s)
        ctx.close_path(); ctx.save(); ctx.clip_preserve()
        col(ctx, "#6b1220"); ctx.fill()
        ctx.rectangle(x - w * s, y - 8 * s, 2 * w * s, 7 * s); col(ctx, "#ffffff"); ctx.fill()
        ellipse(ctx, x, y + hh, w * 0.6 * s, hh * 0.55); col(ctx, "#ff8fa3"); ctx.fill()
        ctx.restore()
        ctx.move_to(x - w * s, y - 2 * s)
        ctx.curve_to(x - w * 0.7 * s, y + hh, x + w * 0.7 * s, y + hh, x + w * s, y - 2 * s)
        col(ctx, "#3a2a1e"); ctx.set_line_width(3 * s); ctx.stroke()
    else:
        ctx.move_to(x - w * s, y - 4 * s)
        ctx.curve_to(x - w * 0.4 * s, y + 10 * s, x + w * 0.4 * s, y + 10 * s, x + w * s, y - 4 * s)
        col(ctx, "#8b1e2d"); ctx.set_line_width(5 * s); ctx.stroke()
        for sd in (-1, 1):
            ctx.move_to(x + sd * (w + 2) * s, y - 8 * s); ctx.line_to(x + sd * (w - 2) * s, y - 1 * s)
        col(ctx, "#8b1e2d"); ctx.set_line_width(3 * s); ctx.stroke()

def _blush(ctx, x, y, s, r=20, a=0.45):
    g = cairo.RadialGradient(x, y, 0, x, y, r * s)
    g.add_color_stop_rgba(0, *rgb("#ff6b81"), a); g.add_color_stop_rgba(1, *rgb("#ff6b81"), 0)
    ctx.set_source(g); ctx.arc(x, y, r * s, 0, 2 * math.pi); ctx.fill()

def _shoe(ctx, x, y, s, base, lw, sole="#f1f3f5"):
    ctx.move_to(x - 26 * s, y); ctx.curve_to(x - 30 * s, y - 26 * s, x + 8 * s, y - 30 * s, x + 20 * s, y - 16 * s)
    ctx.curve_to(x + 36 * s, y - 12 * s, x + 40 * s, y, x + 34 * s, y); ctx.close_path()
    paint(ctx, base, lw)
    ctx.move_to(x - 26 * s, y - 3 * s); ctx.line_to(x + 36 * s, y - 3 * s)
    col(ctx, sole); ctx.set_line_width(6 * s); ctx.stroke()
    gloss(ctx, x - 6 * s, y - 20 * s, 9 * s, 4 * s, 0.45, -0.2)

def _hand(ctx, x, y, s, skin, lw):
    ctx.arc(x, y, 17 * s, 0, 2 * math.pi); paint(ctx, skin, lw, radial=True)
    ellipse(ctx, x - 13 * s, y - 6 * s, 7 * s, 10 * s); paint(ctx, skin, lw * 0.8)

def _embroidery(ctx, x0, x1, y, s, c1="#e03131", c2="#ffd43b", h=16):
    """Narodni vez: niz rombova."""
    n = max(3, int((x1 - x0) / (26 * s)))
    step = (x1 - x0) / n
    for i in range(n):
        cx = x0 + step * (i + 0.5)
        ctx.move_to(cx, y - h / 2 * s); ctx.line_to(cx + step * 0.42, y); ctx.line_to(cx, y + h / 2 * s); ctx.line_to(cx - step * 0.42, y)
        ctx.close_path(); col(ctx, c1 if i % 2 == 0 else c2); ctx.fill()
        ctx.arc(cx, y, 2.6 * s, 0, 2 * math.pi); col(ctx, "#ffffff"); ctx.fill()

def kid(ctx, x, y, s, who, t, talking=False, wave=False, look=0.0, jump=0.0):
    """who: 'mila' ili 'luka'. (x,y) = tacka izmedju stopala. Visina ~ 470*s."""
    mila = who == "mila"
    seed = 1.0 if mila else 2.7
    by = -abs(math.sin(t * 2.2 + seed)) * 6 * s - jump * s
    shirt = "#e64980" if mila else "#228be6"
    skin = "#ffd8b5"
    lw = 4 * s
    ground_shadow(ctx, x, y + 2 * s, 95 * s * (1 - min(0.4, (-by) / (300 * s))))
    ctx.save(); ctx.translate(0, by)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # noge + obuca
    for dx in (-28, 28):
        if mila:
            rrect(ctx, x + (dx - 11) * s, y - 125 * s, 22 * s, 112 * s, 10 * s); paint(ctx, skin, lw)
            rrect(ctx, x + (dx - 12) * s, y - 48 * s, 24 * s, 34 * s, 8 * s); paint(ctx, "#ffffff", lw, outline="#adb5bd")
            _shoe(ctx, x + dx * s, y, s, "#c92a2a", lw)
        else:
            rrect(ctx, x + (dx - 14) * s, y - 128 * s, 28 * s, 118 * s, 10 * s); paint(ctx, "#364fc7", lw)
            ctx.move_to(x + (dx - 4) * s, y - 120 * s); ctx.line_to(x + (dx - 4) * s, y - 30 * s)
            col(ctx, "#4c6ef5", 0.6); ctx.set_line_width(2.5 * s); ctx.stroke()
            _shoe(ctx, x + dx * s, y, s, "#f1f3f5", lw, sole="#fa5252")
            ctx.move_to(x + (dx - 8) * s, y - 17 * s); ctx.line_to(x + (dx + 14) * s, y - 11 * s)
            col(ctx, "#fa5252"); ctx.set_line_width(4 * s); ctx.stroke()
    # telo
    if mila:
        ctx.move_to(x - 46 * s, y - 285 * s)
        ctx.curve_to(x - 10 * s, y - 295 * s, x + 10 * s, y - 295 * s, x + 46 * s, y - 285 * s)
        ctx.curve_to(x + 70 * s, y - 220 * s, x + 88 * s, y - 160 * s, x + 96 * s, y - 108 * s)
        ctx.curve_to(x + 50 * s, y - 96 * s, x - 50 * s, y - 96 * s, x - 96 * s, y - 108 * s)
        ctx.curve_to(x - 88 * s, y - 160 * s, x - 70 * s, y - 220 * s, x - 46 * s, y - 285 * s)
        ctx.close_path(); paint(ctx, shirt, lw)
        # nabori haljine
        for k in (-1, 0, 1):
            ctx.move_to(x + k * 28 * s, y - 215 * s); ctx.curve_to(x + k * 36 * s, y - 170 * s, x + k * 46 * s, y - 140 * s, x + k * 52 * s, y - 110 * s)
            col(ctx, shade(shirt, -0.25), 0.6); ctx.set_line_width(3 * s); ctx.stroke()
        # jelek (prsluk) sa zlatnim obrubom
        ctx.move_to(x - 44 * s, y - 284 * s); ctx.curve_to(x - 50 * s, y - 250 * s, x - 52 * s, y - 225 * s, x - 48 * s, y - 210 * s)
        ctx.line_to(x - 12 * s, y - 210 * s); ctx.line_to(x - 18 * s, y - 286 * s); ctx.close_path()
        ctx.move_to(x + 44 * s, y - 284 * s); ctx.curve_to(x + 50 * s, y - 250 * s, x + 52 * s, y - 225 * s, x + 48 * s, y - 210 * s)
        ctx.line_to(x + 12 * s, y - 210 * s); ctx.line_to(x + 18 * s, y - 286 * s); ctx.close_path()
        paint(ctx, "#862e9c", lw * 0.8, outline="#fcc419")
        for sd in (-1, 1):
            for k in range(3):
                ctx.arc(x + sd * 32 * s, y - (265 - k * 20) * s, 3.5 * s, 0, 2 * math.pi); col(ctx, "#fcc419"); ctx.fill()
        # vez na rubu haljine i pojas
        _embroidery(ctx, x - 84 * s, x + 84 * s, y - 122 * s, s)
        ctx.move_to(x - 56 * s, y - 210 * s); ctx.line_to(x + 56 * s, y - 210 * s)
        col(ctx, "#fcc419"); ctx.set_line_width(8 * s); ctx.stroke()
    else:
        ctx.move_to(x - 58 * s, y - 285 * s)
        ctx.curve_to(x - 20 * s, y - 296 * s, x + 20 * s, y - 296 * s, x + 58 * s, y - 285 * s)
        ctx.curve_to(x + 66 * s, y - 230 * s, x + 64 * s, y - 170 * s, x + 60 * s, y - 120 * s)
        ctx.line_to(x - 60 * s, y - 120 * s)
        ctx.curve_to(x - 64 * s, y - 170 * s, x - 66 * s, y - 230 * s, x - 58 * s, y - 285 * s)
        ctx.close_path(); paint(ctx, shirt, lw)
        # okovratnik + pruga + zvezdica
        ctx.move_to(x - 24 * s, y - 291 * s); ctx.curve_to(x - 10 * s, y - 268 * s, x + 10 * s, y - 268 * s, x + 24 * s, y - 291 * s)
        col(ctx, "#1864ab"); ctx.set_line_width(7 * s); ctx.stroke()
        ctx.rectangle(x - 63 * s, y - 205 * s, 126 * s, 16 * s); col(ctx, "#ffffff", 0.9); ctx.fill()
        ctx.rectangle(x - 63 * s, y - 185 * s, 126 * s, 8 * s); col(ctx, "#fcc419"); ctx.fill()
        cx_, cy_ = x + 30 * s, y - 245 * s
        for k in range(10):
            r = (13 if k % 2 == 0 else 5.5) * s
            a = -math.pi / 2 + k * math.pi / 5
            (ctx.move_to if k == 0 else ctx.line_to)(cx_ + math.cos(a) * r, cy_ + math.sin(a) * r)
        ctx.close_path(); col(ctx, "#fcc419"); ctx.fill()
        # pojas pantalona
        rrect(ctx, x - 62 * s, y - 136 * s, 124 * s, 26 * s, 8 * s); paint(ctx, "#364fc7", lw)
        rrect(ctx, x - 10 * s, y - 133 * s, 20 * s, 20 * s, 4 * s); paint(ctx, "#fcc419", 2 * s)
    # vrat
    rrect(ctx, x - 16 * s, y - 300 * s, 32 * s, 24 * s, 6 * s); col(ctx, shade(skin, -0.12)); ctx.fill()
    # ruke
    for side in (-1, 1):
        ctx.save(); ctx.translate(x + side * 52 * s, y - 268 * s)
        if wave and side == 1:
            ctx.rotate(-2.3 + math.sin(t * 9) * 0.35)
        else:
            ctx.rotate(side * -0.22 + math.sin(t * 2 + side) * 0.05)
        if mila:  # puf rukavi bele kosulje
            ellipse(ctx, 0, 14 * s, 24 * s, 26 * s); paint(ctx, "#ffffff", lw, outline="#adb5bd")
            ctx.move_to(-11 * s, 30 * s); ctx.curve_to(-12 * s, 70 * s, -10 * s, 95 * s, -9 * s, 108 * s)
            ctx.line_to(9 * s, 108 * s); ctx.curve_to(10 * s, 95 * s, 12 * s, 70 * s, 11 * s, 30 * s); ctx.close_path()
            paint(ctx, skin, lw)
        else:
            ctx.move_to(-17 * s, 0); ctx.curve_to(-18 * s, 25 * s, -16 * s, 45 * s, -14 * s, 58 * s)
            ctx.line_to(14 * s, 58 * s); ctx.curve_to(16 * s, 45 * s, 18 * s, 25 * s, 17 * s, 0); ctx.close_path()
            paint(ctx, shirt, lw)
            rrect(ctx, -11 * s, 52 * s, 22 * s, 58 * s, 10 * s); paint(ctx, skin, lw)
        _hand(ctx, 0, 116 * s, s, skin, lw)
        ctx.restore()
    # glava
    tilt = math.sin(t * 3.1 + seed) * 0.05 if talking else math.sin(t * 0.9 + seed) * 0.02
    hx, hy = x, y - 370 * s
    ctx.save(); ctx.translate(hx, hy + 80 * s); ctx.rotate(tilt); ctx.translate(-hx, -(hy + 80 * s))
    hair = "#7a3e12" if mila else "#f2c14e"
    if mila:  # zadnja kosa + pletenice sa masnicama
        ctx.arc(hx, hy - 2 * s, 98 * s, math.pi * 0.85, math.pi * 2.15); ctx.close_path(); paint(ctx, hair, lw)
        for side in (-1, 1):
            sw = math.sin(t * 2.4 + side) * 4 * s
            for k in range(4):
                ex, ey = hx + side * (94 + k * 2) * s + sw * k * 0.4, hy + (18 + k * 30) * s
                ellipse(ctx, ex, ey, 21 * s - k * 1.5 * s, 18 * s); paint(ctx, hair, lw, radial=True)
                ctx.move_to(ex - 12 * s, ey - 8 * s); ctx.curve_to(ex - 2 * s, ey + 2 * s, ex + 6 * s, ey + 4 * s, ex + 14 * s, ey - 2 * s)
                col(ctx, shade(hair, 0.3), 0.6); ctx.set_line_width(3 * s); ctx.stroke()
            bx, byy = hx + side * 102 * s + sw * 1.6, hy + 140 * s
            for sd in (-1, 1):
                ctx.move_to(bx, byy); ctx.curve_to(bx + sd * 20 * s, byy - 18 * s, bx + sd * 26 * s, byy + 12 * s, bx, byy)
                ctx.close_path(); paint(ctx, "#e03131", 3 * s)
            ctx.arc(bx, byy, 6 * s, 0, 2 * math.pi); paint(ctx, "#c92a2a", 2.5 * s)
            ctx.move_to(bx, byy); ctx.line_to(bx + side * 2 * s, byy + 26 * s)
            col(ctx, hair); ctx.set_line_width(9 * s); ctx.stroke()
    # usi
    for side in (-1, 1):
        ellipse(ctx, hx + side * 88 * s, hy + 12 * s, 17 * s, 22 * s); paint(ctx, skin, lw)
        ellipse(ctx, hx + side * 90 * s, hy + 13 * s, 7 * s, 11 * s); col(ctx, "#f4a988", 0.8); ctx.fill()
    # lice
    ctx.move_to(hx - 90 * s, hy - 5 * s)
    ctx.curve_to(hx - 92 * s, hy - 95 * s, hx + 92 * s, hy - 95 * s, hx + 90 * s, hy - 5 * s)
    ctx.curve_to(hx + 88 * s, hy + 70 * s, hx + 40 * s, hy + 92 * s, hx, hy + 92 * s)
    ctx.curve_to(hx - 40 * s, hy + 92 * s, hx - 88 * s, hy + 70 * s, hx - 90 * s, hy - 5 * s)
    ctx.close_path(); paint(ctx, skin, lw, light=0.3, dark=-0.08, radial=True)
    # kosa spreda
    if mila:
        ctx.move_to(hx - 96 * s, hy + 10 * s)
        ctx.curve_to(hx - 104 * s, hy - 110 * s, hx + 104 * s, hy - 110 * s, hx + 96 * s, hy + 10 * s)
        ctx.curve_to(hx + 80 * s, hy - 30 * s, hx + 50 * s, hy - 46 * s, hx + 26 * s, hy - 40 * s)
        ctx.curve_to(hx + 10 * s, hy - 60 * s, hx - 20 * s, hy - 50 * s, hx - 30 * s, hy - 38 * s)
        ctx.curve_to(hx - 60 * s, hy - 50 * s, hx - 84 * s, hy - 30 * s, hx - 96 * s, hy + 10 * s)
        ctx.close_path(); paint(ctx, hair, lw)
        ctx.move_to(hx - 50 * s, hy - 72 * s); ctx.curve_to(hx - 20 * s, hy - 88 * s, hx + 20 * s, hy - 88 * s, hx + 44 * s, hy - 74 * s)
        col(ctx, shade(hair, 0.45), 0.7); ctx.set_line_width(7 * s); ctx.stroke()
        # cvet u kosi
        fx, fy = hx + 62 * s, hy - 62 * s
        for k in range(5):
            a = k * 2 * math.pi / 5 + 0.3
            ctx.arc(fx + math.cos(a) * 10 * s, fy + math.sin(a) * 10 * s, 8 * s, 0, 2 * math.pi); paint(ctx, "#ffffff", 2 * s, outline="#e64980")
        ctx.arc(fx, fy, 6 * s, 0, 2 * math.pi); col(ctx, "#fcc419"); ctx.fill()
    else:
        ctx.move_to(hx - 94 * s, hy + 6 * s)
        ctx.curve_to(hx - 106 * s, hy - 100 * s, hx - 20 * s, hy - 140 * s, hx + 40 * s, hy - 112 * s)
        ctx.curve_to(hx + 90 * s, hy - 98 * s, hx + 104 * s, hy - 40 * s, hx + 94 * s, hy + 6 * s)
        tips = [(70, -36), (50, -58), (28, -40), (6, -64), (-18, -44), (-42, -62), (-62, -36), (-82, -30)]
        prev = (94, 6)
        for (tx, ty) in tips:
            ctx.line_to(hx + (prev[0] + tx) / 2 * s, hy + ((prev[1] + ty) / 2 - 22) * s)
            ctx.line_to(hx + tx * s, hy + ty * s); prev = (tx, ty)
        ctx.close_path(); paint(ctx, hair, lw)
        # cuperak
        ctx.move_to(hx + 4 * s, hy - 120 * s); ctx.curve_to(hx + 10 * s, hy - 160 * s, hx + 40 * s, hy - 160 * s, hx + 46 * s, hy - 140 * s)
        ctx.curve_to(hx + 30 * s, hy - 146 * s, hx + 20 * s, hy - 135 * s, hx + 24 * s, hy - 118 * s); ctx.close_path(); paint(ctx, hair, lw)
        for k in range(3):
            ctx.move_to(hx + (-50 + k * 34) * s, hy - (96 - k * 6) * s); ctx.line_to(hx + (-34 + k * 34) * s, hy - (76 - k * 4) * s)
        col(ctx, shade(hair, 0.5), 0.8); ctx.set_line_width(5 * s); ctx.stroke()
    _blush(ctx, hx - 54 * s, hy + 38 * s, s)
    _blush(ctx, hx + 54 * s, hy + 38 * s, s)
    _eyes(ctx, hx, hy + 6 * s, s, t, seed, look, iris="#2f9e44" if mila else "#1c7ed6", skin=skin,
          lashes=mila, brow=shade(hair, -0.35), talking=talking)
    # nos
    ctx.move_to(hx - 6 * s, hy + 34 * s); ctx.curve_to(hx - 2 * s, hy + 40 * s, hx + 4 * s, hy + 40 * s, hx + 7 * s, hy + 34 * s)
    col(ctx, "#d9895f"); ctx.set_line_width(4 * s); ctx.stroke()
    _mouth(ctx, hx, hy + 58 * s, s, t, talking, w=19)
    ctx.restore()
    ctx.restore()

def owl(ctx, x, y, s, t, talking=False, flap=False, look=0.0):
    """Sova Sofija. (x,y) = dno (noge). Visina ~ 330*s."""
    by = -abs(math.sin(t * 1.8)) * 5 * s
    lw = 4 * s
    body, wing, belly = "#b07a45", "#8a5a2b", "#f1d3a8"
    ground_shadow(ctx, x, y + 2 * s, 110 * s)
    ctx.save(); ctx.translate(0, by)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # rep
    for k in (-1, 0, 1):
        ctx.move_to(x + k * 22 * s - 14 * s, y - 40 * s); ctx.line_to(x + k * 30 * s, y + 4 * s); ctx.line_to(x + k * 22 * s + 14 * s, y - 40 * s)
        ctx.close_path(); paint(ctx, wing, lw)
    # krila (iza tela) sa perima
    for side in (-1, 1):
        ctx.save(); ctx.translate(x + side * 92 * s, y - 210 * s)
        ang = (math.sin(t * 14) * 0.5 + 0.4) if flap else 0.08 + math.sin(t * 1.8) * 0.03
        ctx.rotate(side * ang)
        ctx.move_to(0, -10 * s)
        ctx.curve_to(side * 50 * s, 0, side * 56 * s, 90 * s, side * 30 * s, 150 * s)
        ctx.line_to(side * 14 * s, 128 * s); ctx.line_to(side * 4 * s, 150 * s); ctx.line_to(-side * 8 * s, 124 * s)
        ctx.curve_to(-side * 22 * s, 80 * s, -side * 20 * s, 20 * s, 0, -10 * s)
        ctx.close_path(); paint(ctx, wing, lw)
        for k in range(3):
            ctx.move_to(-side * 6 * s, (50 + k * 26) * s); ctx.curve_to(side * 12 * s, (60 + k * 26) * s, side * 30 * s, (55 + k * 26) * s, side * 38 * s, (40 + k * 26) * s)
            col(ctx, shade(wing, -0.3), 0.7); ctx.set_line_width(3 * s); ctx.stroke()
        ctx.restore()
    # telo
    ctx.move_to(x, y - 320 * s)
    ctx.curve_to(x + 90 * s, y - 320 * s, x + 122 * s, y - 220 * s, x + 116 * s, y - 130 * s)
    ctx.curve_to(x + 110 * s, y - 40 * s, x + 60 * s, y - 12 * s, x, y - 12 * s)
    ctx.curve_to(x - 60 * s, y - 12 * s, x - 110 * s, y - 40 * s, x - 116 * s, y - 130 * s)
    ctx.curve_to(x - 122 * s, y - 220 * s, x - 90 * s, y - 320 * s, x, y - 320 * s)
    ctx.close_path(); paint(ctx, body, lw, light=0.25, dark=-0.15, radial=True)
    # stomak sa perjem
    ellipse(ctx, x, y - 112 * s, 76 * s, 92 * s); paint(ctx, belly, 0.01, light=0.3, dark=-0.08, outline=belly, radial=True)
    for r in range(4):
        n = 3 + (r % 2)
        for c in range(n):
            fx = x + (c - (n - 1) / 2) * 32 * s
            fy = y - (165 - r * 30) * s
            ctx.move_to(fx - 12 * s, fy); ctx.curve_to(fx - 8 * s, fy + 14 * s, fx + 8 * s, fy + 14 * s, fx + 12 * s, fy)
            col(ctx, "#c49a6c"); ctx.set_line_width(3.5 * s); ctx.stroke()
    # usi (perca)
    for side in (-1, 1):
        ctx.move_to(x + side * 48 * s, y - 300 * s)
        ctx.curve_to(x + side * 70 * s, y - 330 * s, x + side * 92 * s, y - 350 * s, x + side * 104 * s, y - 352 * s)
        ctx.curve_to(x + side * 104 * s, y - 320 * s, x + side * 100 * s, y - 290 * s, x + side * 92 * s, y - 270 * s)
        ctx.close_path(); paint(ctx, wing, lw)
    # disk lica
    for side in (-1, 1):
        ctx.arc(x + side * 45 * s, y - 242 * s, 58 * s, 0, 2 * math.pi)
        g = cairo.RadialGradient(x + side * 45 * s, y - 242 * s, 20 * s, x + side * 45 * s, y - 242 * s, 58 * s)
        g.add_color_stop_rgba(0, *rgb("#f8e3c4"), 1); g.add_color_stop_rgba(1, *rgb("#e2b886"), 0.9)
        ctx.set_source(g); ctx.fill()
    # oci
    op = _blink(t, 0.5, 4.1)
    for dx in (-45, 45):
        ex, ey = x + dx * s, y - 245 * s
        ctx.arc(ex, ey, 40 * s, 0, 2 * math.pi); col(ctx, "#ffffff"); ctx.fill()
        ctx.save(); ctx.arc(ex, ey, 40 * s, 0, 2 * math.pi); ctx.clip()
        ix, iy = ex + look * 9 * s, ey + 3 * s
        gi = cairo.RadialGradient(ix - 6 * s, iy - 6 * s, 0, ix, iy, 26 * s)
        gi.add_color_stop_rgb(0, *rgb("#ffd43b")); gi.add_color_stop_rgb(1, *rgb("#e67700"))
        ctx.arc(ix, iy, 26 * s, 0, 2 * math.pi); ctx.set_source(gi); ctx.fill()
        ctx.arc(ix, iy, 14 * s, 0, 2 * math.pi); col(ctx, "#1a120c"); ctx.fill()
        ctx.arc(ix - 9 * s, iy - 10 * s, 8 * s, 0, 2 * math.pi); col(ctx, "#ffffff"); ctx.fill()
        ctx.arc(ix + 8 * s, iy + 8 * s, 3.5 * s, 0, 2 * math.pi); col(ctx, "#ffffff", 0.9); ctx.fill()
        lid = ey - 40 * s + 80 * s * (1 - op) * 0.98 + 80 * s * 0.12
        ctx.rectangle(ex - 42 * s, ey - 42 * s, 84 * s, lid - (ey - 42 * s)); col(ctx, shade(body, 0.1)); ctx.fill()
        ctx.restore()
        ctx.arc(ex, ey, 40 * s, 0, 2 * math.pi); col(ctx, "#3a2a1e"); ctx.set_line_width(3 * s); ctx.stroke()
        # naocare sa odsjajem
        ctx.arc(ex, ey, 49 * s, 0, 2 * math.pi); col(ctx, "#ffffff", 0.08); ctx.fill_preserve()
        col(ctx, "#5f3dc4"); ctx.set_line_width(8 * s); ctx.stroke()
        ctx.arc(ex, ey, 49 * s, 0, 2 * math.pi); col(ctx, "#9775fa"); ctx.set_line_width(2.5 * s); ctx.stroke()
        ctx.save(); ctx.arc(ex, ey, 45 * s, 0, 2 * math.pi); ctx.clip()
        ctx.move_to(ex - 40 * s, ey - 4 * s); ctx.line_to(ex - 4 * s, ey - 40 * s); ctx.line_to(ex + 8 * s, ey - 40 * s); ctx.line_to(ex - 40 * s, ey + 8 * s)
        ctx.close_path(); col(ctx, "#ffffff", 0.28); ctx.fill(); ctx.restore()
    ctx.move_to(x - 4 * s, y - 252 * s); ctx.curve_to(x - 2 * s, y - 260 * s, x + 2 * s, y - 260 * s, x + 4 * s, y - 252 * s)
    col(ctx, "#5f3dc4"); ctx.set_line_width(7 * s); ctx.stroke()
    # obrve (perje iznad ociju)
    lift = (4 * abs(math.sin(t * 4))) * s if talking else 0
    for side in (-1, 1):
        ctx.move_to(x + side * 15 * s, y - 300 * s - lift); ctx.curve_to(x + side * 40 * s, y - 312 * s - lift, x + side * 70 * s, y - 308 * s - lift, x + side * 88 * s, y - 292 * s - lift)
        col(ctx, shade(wing, -0.25)); ctx.set_line_width(7 * s); ctx.stroke()
    # kljun
    o = (abs(math.sin(t * 12)) * 14 * s) if talking else 0
    if o > 1:
        ctx.move_to(x - 13 * s, y - 196 * s + o * 0.2); ctx.line_to(x + 13 * s, y - 196 * s + o * 0.2); ctx.line_to(x, y - 178 * s + o)
        ctx.close_path(); paint(ctx, "#f08c00", 3 * s)
    ctx.move_to(x - 19 * s, y - 208 * s); ctx.curve_to(x - 10 * s, y - 214 * s, x + 10 * s, y - 214 * s, x + 19 * s, y - 208 * s)
    ctx.curve_to(x + 12 * s, y - 194 * s, x + 4 * s, y - 182 * s, x, y - 178 * s)
    ctx.curve_to(x - 4 * s, y - 182 * s, x - 12 * s, y - 194 * s, x - 19 * s, y - 208 * s)
    ctx.close_path(); paint(ctx, "#fcc419", 3 * s)
    gloss(ctx, x - 5 * s, y - 202 * s, 6 * s, 3 * s, 0.6, -0.3)
    # nogice
    for dx in (-35, 35):
        for k in (-1, 0, 1):
            ctx.move_to(x + dx * s, y - 16 * s); ctx.line_to(x + (dx + k * 14) * s, y)
        col(ctx, "#e8590c"); ctx.set_line_width(8 * s); ctx.stroke()
        for k in (-1, 0, 1):
            ctx.move_to(x + dx * s, y - 16 * s); ctx.line_to(x + (dx + k * 14) * s, y)
        col(ctx, "#ffa94d"); ctx.set_line_width(4 * s); ctx.stroke()
    ctx.restore()

def villager(ctx, x, y, s, t, tunic="#c92a2a", walking=True, beard=False, bundle=False, hair="#5c3a1a", skirt=False, talking=False):
    """Stari Sloven / Slovenka. (x,y) = stopala. Visina ~ 430*s."""
    lw = 4 * s
    skin = "#f3c79b"
    ph = t * 6 + x * 0.01
    sw = math.sin(ph) * 0.35 if walking else 0
    by = -abs(math.sin(ph)) * 8 * s if walking else 0
    ground_shadow(ctx, x, y + 2 * s, 80 * s)
    ctx.save(); ctx.translate(0, by)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # noge sa obojcima i opancima
    for k, side in enumerate((-1, 1)):
        ctx.save(); ctx.translate(x + side * 18 * s, y - 130 * s); ctx.rotate(sw * side)
        rrect(ctx, -12 * s, 0, 24 * s, 122 * s, 8 * s); paint(ctx, "#e9d8a6", lw)
        for j in range(3):
            ctx.move_to(-12 * s, (30 + j * 26) * s); ctx.line_to(12 * s, (44 + j * 26) * s)
        col(ctx, "#8d6e47"); ctx.set_line_width(3 * s); ctx.stroke()
        ctx.move_to(-18 * s, 128 * s); ctx.curve_to(-20 * s, 108 * s, 18 * s, 106 * s, 28 * s, 118 * s)
        ctx.curve_to(36 * s, 116 * s, 38 * s, 108 * s, 34 * s, 104 * s); ctx.curve_to(42 * s, 110 * s, 40 * s, 128 * s, 30 * s, 128 * s)
        ctx.close_path(); paint(ctx, "#8b5a2b", lw)
        ctx.restore()
    # telo
    if skirt:
        ctx.move_to(x - 44 * s, y - 300 * s); ctx.curve_to(x - 10 * s, y - 308 * s, x + 10 * s, y - 308 * s, x + 44 * s, y - 300 * s)
        ctx.curve_to(x + 62 * s, y - 220 * s, x + 74 * s, y - 150 * s, x + 80 * s, y - 92 * s)
        ctx.curve_to(x + 30 * s, y - 84 * s, x - 30 * s, y - 84 * s, x - 80 * s, y - 92 * s)
        ctx.curve_to(x - 74 * s, y - 150 * s, x - 62 * s, y - 220 * s, x - 44 * s, y - 300 * s)
        ctx.close_path()
    else:
        ctx.move_to(x - 52 * s, y - 300 * s); ctx.curve_to(x - 20 * s, y - 310 * s, x + 20 * s, y - 310 * s, x + 52 * s, y - 300 * s)
        ctx.curve_to(x + 62 * s, y - 230 * s, x + 62 * s, y - 160 * s, x + 58 * s, y - 112 * s)
        ctx.line_to(x - 58 * s, y - 112 * s)
        ctx.curve_to(x - 62 * s, y - 160 * s, x - 62 * s, y - 230 * s, x - 52 * s, y - 300 * s)
        ctx.close_path()
    paint(ctx, tunic, lw)
    if skirt:  # pregaca
        ctx.move_to(x - 36 * s, y - 200 * s); ctx.line_to(x + 36 * s, y - 200 * s); ctx.line_to(x + 44 * s, y - 100 * s); ctx.line_to(x - 44 * s, y - 100 * s)
        ctx.close_path(); paint(ctx, "#f8f0e3", lw * 0.8, outline="#c9b48e")
        _embroidery(ctx, x - 40 * s, x + 40 * s, y - 116 * s, s, h=12)
    else:
        _embroidery(ctx, x - 54 * s, x + 54 * s, y - 126 * s, s, c2="#f8f0e3", h=12)
    # okovratnik sa vezom
    ctx.move_to(x - 22 * s, y - 304 * s); ctx.line_to(x, y - 270 * s); ctx.line_to(x + 22 * s, y - 304 * s)
    col(ctx, "#ffd43b"); ctx.set_line_width(6 * s); ctx.stroke()
    # pojas
    ctx.move_to(x - 56 * s, y - 182 * s); ctx.line_to(x + 56 * s, y - 182 * s)
    col(ctx, "#ffd43b"); ctx.set_line_width(10 * s); ctx.stroke()
    ctx.move_to(x - 56 * s, y - 182 * s); ctx.line_to(x + 56 * s, y - 182 * s)
    col(ctx, "#e03131"); ctx.set_line_width(3 * s); ctx.set_dash([6 * s, 6 * s]); ctx.stroke(); ctx.set_dash([])
    if bundle:
        ctx.move_to(x - 30 * s, y - 300 * s); ctx.line_to(x + 40 * s, y - 180 * s); col(ctx, "#6f4518"); ctx.set_line_width(7 * s); ctx.stroke()
        ctx.arc(x - 72 * s, y - 280 * s, 55 * s, 0, 2 * math.pi); paint(ctx, "#a68a64", lw, radial=True)
        ctx.move_to(x - 100 * s, y - 320 * s); ctx.curve_to(x - 80 * s, y - 300 * s, x - 60 * s, y - 300 * s, x - 40 * s, y - 320 * s)
        col(ctx, shade("#a68a64", -0.3)); ctx.set_line_width(3 * s); ctx.stroke()
    for side in (-1, 1):
        ctx.save(); ctx.translate(x + side * 50 * s, y - 285 * s); ctx.rotate(-sw * side * 0.8 + side * -0.15)
        rrect(ctx, -12 * s, 0, 24 * s, 108 * s, 11 * s); paint(ctx, tunic, lw)
        ctx.rectangle(-12 * s, 86 * s, 24 * s, 8 * s); col(ctx, "#ffd43b"); ctx.fill()
        ctx.arc(0, 114 * s, 14 * s, 0, 2 * math.pi); paint(ctx, skin, lw, radial=True)
        ctx.restore()
    hx, hy = x, y - 365 * s
    ctx.save(); ctx.translate(hx, hy + 60 * s); ctx.rotate(math.sin(t * 3 + x) * 0.04 if talking else 0); ctx.translate(-hx, -(hy + 60 * s))
    for side in (-1, 1):
        ellipse(ctx, hx + side * 63 * s, hy + 6 * s, 12 * s, 16 * s); paint(ctx, skin, lw)
    ctx.arc(hx, hy, 65 * s, 0, 2 * math.pi); paint(ctx, skin, lw, light=0.3, dark=-0.08, radial=True)
    if skirt:  # marama
        ctx.move_to(hx - 74 * s, hy + 10 * s)
        ctx.curve_to(hx - 84 * s, hy - 90 * s, hx + 84 * s, hy - 90 * s, hx + 74 * s, hy + 10 * s)
        ctx.curve_to(hx + 60 * s, hy - 30 * s, hx - 60 * s, hy - 30 * s, hx - 74 * s, hy + 10 * s)
        ctx.close_path(); paint(ctx, "#f8f0e3", lw, outline="#c9b48e")
        for k in range(5):
            ctx.arc(hx + (k - 2) * 24 * s, hy - 48 * s + abs(k - 2) * 5 * s, 5 * s, 0, 2 * math.pi); col(ctx, "#e03131"); ctx.fill()
    else:
        ctx.move_to(hx - 68 * s, hy + 2 * s)
        ctx.curve_to(hx - 76 * s, hy - 84 * s, hx + 76 * s, hy - 84 * s, hx + 68 * s, hy + 2 * s)
        ctx.curve_to(hx + 50 * s, hy - 30 * s, hx + 20 * s, hy - 40 * s, hx, hy - 32 * s)
        ctx.curve_to(hx - 20 * s, hy - 40 * s, hx - 50 * s, hy - 30 * s, hx - 68 * s, hy + 2 * s)
        ctx.close_path(); paint(ctx, hair, lw)
        ctx.move_to(hx - 30 * s, hy - 52 * s); ctx.curve_to(hx - 10 * s, hy - 60 * s, hx + 10 * s, hy - 60 * s, hx + 26 * s, hy - 52 * s)
        col(ctx, shade(hair, 0.4), 0.6); ctx.set_line_width(5 * s); ctx.stroke()
    if beard:
        ctx.move_to(hx - 56 * s, hy + 6 * s)
        ctx.curve_to(hx - 60 * s, hy + 70 * s, hx - 20 * s, hy + 96 * s, hx, hy + 98 * s)
        ctx.curve_to(hx + 20 * s, hy + 96 * s, hx + 60 * s, hy + 70 * s, hx + 56 * s, hy + 6 * s)
        ctx.curve_to(hx + 40 * s, hy + 30 * s, hx + 20 * s, hy + 26 * s, hx, hy + 30 * s)
        ctx.curve_to(hx - 20 * s, hy + 26 * s, hx - 40 * s, hy + 30 * s, hx - 56 * s, hy + 6 * s)
        ctx.close_path(); paint(ctx, hair, lw)
        for k in (-1, 0, 1):
            ctx.move_to(hx + k * 20 * s, hy + 50 * s); ctx.line_to(hx + k * 22 * s, hy + 78 * s)
        col(ctx, shade(hair, 0.35), 0.6); ctx.set_line_width(3 * s); ctx.stroke()
        ctx.move_to(hx - 30 * s, hy + 26 * s); ctx.curve_to(hx - 12 * s, hy + 14 * s, hx + 12 * s, hy + 14 * s, hx + 30 * s, hy + 26 * s)
        col(ctx, shade(hair, -0.2)); ctx.set_line_width(9 * s); ctx.stroke()
    op = _blink(t, x * 0.013, 4.3)
    for dx in (-22, 22):
        if op < 0.4:
            ctx.move_to(hx + (dx - 8) * s, hy - 2 * s); ctx.line_to(hx + (dx + 8) * s, hy - 2 * s)
            col(ctx, "#2b1d14"); ctx.set_line_width(4 * s); ctx.stroke()
        else:
            ellipse(ctx, hx + dx * s, hy - 2 * s, 8 * s, 10 * s); col(ctx, "#2b1d14"); ctx.fill()
            ctx.arc(hx + (dx - 2.5) * s, hy - 6 * s, 3 * s, 0, 2 * math.pi); col(ctx, "#ffffff"); ctx.fill()
        ctx.move_to(hx + (dx - 11) * s, hy - 20 * s); ctx.line_to(hx + (dx + 11) * s, hy - 22 * s)
        col(ctx, shade(hair, -0.3) if not skirt else "#5c3a1a"); ctx.set_line_width(5 * s); ctx.stroke()
    _blush(ctx, hx - 36 * s, hy + 16 * s, s, 14, 0.35); _blush(ctx, hx + 36 * s, hy + 16 * s, s, 14, 0.35)
    ctx.move_to(hx - 5 * s, hy + 12 * s); ctx.curve_to(hx - 2 * s, hy + 17 * s, hx + 3 * s, hy + 17 * s, hx + 6 * s, hy + 12 * s)
    col(ctx, "#c97b50"); ctx.set_line_width(3.5 * s); ctx.stroke()
    if talking:
        ellipse(ctx, hx, hy + 34 * s, 11 * s, (4 + 8 * abs(math.sin(t * 12))) * s); col(ctx, "#6b1220"); ctx.fill()
    elif not beard:
        ctx.move_to(hx - 13 * s, hy + 28 * s); ctx.curve_to(hx - 5 * s, hy + 36 * s, hx + 5 * s, hy + 36 * s, hx + 13 * s, hy + 28 * s)
        col(ctx, "#8b1e2d"); ctx.set_line_width(4 * s); ctx.stroke()
    ctx.restore()
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
