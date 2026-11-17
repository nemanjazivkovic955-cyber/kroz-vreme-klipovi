"""Dizajn v2 za QUOTE OF THE DAY klipove: animirani tekst rec-po-rec, zlatne istaknute reci,
vinjeta, staklena kartica za pouku i poziv na akciju. Crta providni overlay kadar po kadar (pycairo).

U tekstu recenica oznaci istaknutu rec zvezdicama: "Be like the *sun*."
"""
import math
import cairo

W, H = 1080, 1920
GOLD = (1.0, 0.80, 0.30)
WHITE = (1, 1, 1)
QUOTE_FONT = "Anton"
SERIF = "DM Serif Display"
SANS = "Poppins"


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def _face(ctx, family, size, bold=False, italic=False):
    ctx.select_font_face(family, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def _shadow_text(ctx, x, y, s, rgb, a=1.0, blur=True):
    if blur:
        for r, al in ((9, 0.10), (5, 0.18), (2, 0.30)):
            for dx, dy in ((r, r), (-r, r), (r, -r), (-r, -r), (0, r), (r, 0), (0, -r), (-r, 0)):
                ctx.move_to(x + dx * 0.5 + 2, y + dy * 0.5 + 4); ctx.text_path(s)
            ctx.set_source_rgba(0, 0, 0, al * a); ctx.fill()
    ctx.move_to(x, y); ctx.set_source_rgba(*rgb, a); ctx.show_text(s)


def _tokens(text):
    """'Be like the *sun*.' -> [('BE', False), ..., ('SUN.', True)]"""
    out = []
    for w in text.split():
        hl = "*" in w
        out.append((w.replace("*", "").upper(), hl))
    return out


def _layout(ctx, toks, maxw):
    space = ctx.text_extents(" ").x_advance
    lines, cur, curw = [], [], 0
    for w, hl in toks:
        ww = ctx.text_extents(w).x_advance
        if cur and curw + space + ww > maxw:
            lines.append((cur, curw)); cur, curw = [], 0
        cur.append((w, hl, ww)); curw += (space if len(cur) > 1 else 0) + ww
    if cur: lines.append((cur, curw))
    return lines, space


def _balanced(ctx, toks, maxw):
    lines, sp = _layout(ctx, toks, maxw)
    n = len(lines)
    while maxw > 300:
        l2, _ = _layout(ctx, toks, maxw - 12)
        if len(l2) != n: break
        maxw -= 12; lines = l2
    return lines, sp


def vignette(ctx):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.55)
    g.add_color_stop_rgba(0.38, 0, 0, 0, 0.10)
    g.add_color_stop_rgba(0.62, 0, 0, 0, 0.10)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.65)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()


def header(ctx, t, text="Quote of the Day"):
    a = ease((t - 0.1) / 0.7)
    if a <= 0: return
    y = 300 - 20 * (1 - a)
    # veliki zlatni navodnik
    _face(ctx, SERIF, 170, italic=True)
    e = ctx.text_extents("“")
    _shadow_text(ctx, W / 2 - e.x_advance / 2, y - 40, "“", GOLD, 0.95 * a)
    _face(ctx, SERIF, 64, italic=True)
    e = ctx.text_extents(text)
    _shadow_text(ctx, W / 2 - e.x_advance / 2, y + 60, text, WHITE, a)
    # zlatna linija sa rombom
    w = 150 * a; yy = y + 95
    ctx.set_source_rgba(*GOLD, a); ctx.set_line_width(3)
    ctx.move_to(W / 2 - 18 - w, yy); ctx.line_to(W / 2 - 18, yy); ctx.stroke()
    ctx.move_to(W / 2 + 18, yy); ctx.line_to(W / 2 + 18 + w, yy); ctx.stroke()
    ctx.move_to(W / 2, yy - 9); ctx.line_to(W / 2 + 9, yy); ctx.line_to(W / 2, yy + 9); ctx.line_to(W / 2 - 9, yy)
    ctx.close_path(); ctx.fill()


def quote_line(ctx, t, text, t0, t1, size=96):
    """Rec-po-rec ulaz (klizi gore + fade), izlaz fade. t0..t1 = vreme prikaza."""
    if t < t0 or t > t1: return
    _face(ctx, QUOTE_FONT, size)
    lines, sp = _balanced(ctx, _tokens(text), W * 0.82)
    lh = size * 1.12
    cy = 0.43 * H
    y0 = cy - (len(lines) - 1) * lh / 2 + size * 0.35
    out_a = 1 - ease((t - (t1 - 0.35)) / 0.35)
    k = 0
    for li, (words, lw) in enumerate(lines):
        x = W / 2 - lw / 2
        y = y0 + li * lh
        for (w, hl, ww) in words:
            p = ease((t - t0 - 0.08 * k) / 0.35)
            if p > 0:
                a = p * out_a
                yy = y + 26 * (1 - p)
                if hl:  # zlatni podvucen naglasak
                    ctx.rectangle(x - 4, yy + 10, (ww + 8) * p, 8)
                    ctx.set_source_rgba(*GOLD, 0.55 * a); ctx.fill()
                _shadow_text(ctx, x, yy, w, GOLD if hl else WHITE, a)
            x += ww + sp; k += 1


def dots(ctx, t, idx, n, a=1.0):
    gap = 30; x0 = W / 2 - (n - 1) * gap / 2; y = 1330
    for i in range(n):
        r = 7 if i == idx else 5
        ctx.arc(x0 + i * gap, y, r, 0, 2 * math.pi)
        if i == idx: ctx.set_source_rgba(*GOLD, a)
        else: ctx.set_source_rgba(1, 1, 1, 0.45 * a)
        ctx.fill()


def _rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def lesson_card(ctx, t, text, t0, t1):
    if t < t0: return
    p = ease((t - t0) / 0.5)
    a = p * (1 - ease((t - (t1 - 0.4)) / 0.4))
    _face(ctx, SANS, 54, bold=True)
    lines, sp = _balanced(ctx, [(w.replace("*", ""), "*" in w) for w in text.split()], W * 0.70)
    lh = 70
    ch = 150 + len(lines) * lh
    cw = 900; cx = (W - cw) / 2; cy = 0.43 * H - ch / 2 + 30 * (1 - p)
    sc = 0.94 + 0.06 * p
    ctx.save(); ctx.translate(W / 2, cy + ch / 2); ctx.scale(sc, sc); ctx.translate(-W / 2, -(cy + ch / 2))
    _rrect(ctx, cx, cy, cw, ch, 36); ctx.set_source_rgba(0.04, 0.04, 0.06, 0.58 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*GOLD, 0.9 * a); ctx.set_line_width(3); ctx.stroke()
    # natpis
    _face(ctx, SANS, 34, bold=True)
    lab = "  ".join("TODAY'S LESSON")
    lab = "T O D A Y ' S   L E S S O N"
    e = ctx.text_extents(lab)
    _shadow_text(ctx, W / 2 - e.x_advance / 2, cy + 78, lab, GOLD, a, blur=False)
    for sx in (-1, 1):
        dx = W / 2 + sx * (e.x_advance / 2 + 26); dy = cy + 66
        ctx.move_to(dx, dy - 8); ctx.line_to(dx + 8, dy); ctx.line_to(dx, dy + 8); ctx.line_to(dx - 8, dy); ctx.close_path()
        ctx.set_source_rgba(*GOLD, a); ctx.fill()
    _face(ctx, SANS, 54, bold=True)
    for li, (words, lw) in enumerate(lines):
        x = W / 2 - lw / 2; y = cy + 160 + li * lh
        for (w, hl, ww) in words:
            _shadow_text(ctx, x, y, w, GOLD if hl else WHITE, a, blur=False)
            x += ww + sp
    ctx.restore()


def cta(ctx, t, t0):
    a = ease((t - t0) / 0.6)
    if a <= 0: return
    _face(ctx, SANS, 32, bold=True)
    s = "SAVE THIS  •  SHARE IT WITH SOMEONE WHO NEEDS IT"
    e = ctx.text_extents(s)
    _shadow_text(ctx, W / 2 - e.x_advance / 2, 1640, s, WHITE, 0.85 * a)


def draw(ctx, t, q, per, dur):
    """Ceo overlay za trenutak t."""
    vignette(ctx)
    header(ctx, t, q.get("header_text", "Quote of the Day"))
    lines = q["lines"]
    n = len(lines) + (1 if q.get("lesson") else 0)
    for i, ln in enumerate(lines):
        a = 0.6 + i * per
        quote_line(ctx, t, ln, a, a + per - 0.1, q.get("size", 96))
    if q.get("lesson"):
        a = 0.6 + len(lines) * per
        lesson_card(ctx, t, q["lesson"], a, dur + 1)
        cta(ctx, t, a + 0.8)
    idx = min(n - 1, int(max(0, t - 0.6) // per))
    dots(ctx, t, idx, n, ease((t - 0.4) / 0.6))
