"""GTA 6 news #1 - 5 things you need to know (EN). Original graphics only:
no Rockstar footage, logos, artwork or music."""
import math, os, sys
import cairo
import numpy as np, wave, random
from engine import W, H, FPS, ease, pop, rgb, col, rrect, font, wrap, text_c, render_scene, frame_png

OUT = os.path.dirname(os.path.abspath(__file__)) + "/out"

PINK, CYAN, ORANGE, PURPLE, YELLOW = "#ff3cac", "#2de2e6", "#ff9f1c", "#2b0b4f", "#ffe66d"

def bg(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 1150)
    for s, c in ((0, "#12002b"), (0.45, "#5a0f6e"), (0.8, "#e0457b"), (1, "#ff9f1c")):
        g.add_color_stop_rgb(s, *rgb(c))
    ctx.rectangle(0, 0, W, 1150); ctx.set_source(g); ctx.fill()
    # zvezde
    rnd = random.Random(4)
    for i in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 600)
        a = 0.4 + 0.6 * abs(math.sin(t * 2 + i))
        ctx.arc(x, y, 2.5, 0, 6.3); col(ctx, "#ffffff", a * 0.8); ctx.fill()
    # sunce sa prugama
    cx, cy, r = W / 2, 1000, 330
    ctx.save(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
    g = cairo.LinearGradient(0, cy - r, 0, cy + r)
    g.add_color_stop_rgb(0, *rgb(YELLOW)); g.add_color_stop_rgb(1, *rgb(PINK))
    ctx.rectangle(0, cy - r, W, 2 * r); ctx.set_source(g); ctx.fill()
    for k in range(8):
        y = cy - 40 + k * 32 + (t * 20) % 32
        ctx.rectangle(0, y, W, 4 + k * 2.2); col(ctx, "#5a0f6e"); ctx.fill()
    ctx.restore()
    # palme (silhueta)
    for (px, sc, fl) in ((110, 1.0, 1), (970, 1.15, -1)):
        palm(ctx, px, 1150, sc, fl, t)
    # pod - perspektivna mreza
    ctx.rectangle(0, 1150, W, H - 1150); col(ctx, "#12002b"); ctx.fill()
    col(ctx, PINK, 0.85); ctx.set_line_width(3)
    for i in range(-14, 15):
        ctx.move_to(W / 2 + i * 30, 1150); ctx.line_to(W / 2 + i * 260, H); ctx.stroke()
    for k in range(14):
        z = ((k + (t * 1.2) % 1) / 14) ** 2.2
        y = 1150 + z * (H - 1150)
        ctx.move_to(0, y); ctx.line_to(W, y); ctx.stroke()
    ctx.move_to(0, 1150); ctx.line_to(W, 1150); col(ctx, CYAN); ctx.set_line_width(5); ctx.stroke()

def palm(ctx, x, y, s, fl, t):
    col(ctx, "#12002b")
    sway = math.sin(t * 1.2) * 8
    ctx.move_to(x - 14 * s, y); ctx.curve_to(x - 10 * s, y - 250 * s, x + fl * 30 * s, y - 420 * s, x + fl * 60 * s + sway, y - 560 * s)
    ctx.line_to(x + fl * 76 * s + sway, y - 556 * s)
    ctx.curve_to(x + fl * 50 * s, y - 410 * s, x + 16 * s, y - 250 * s, x + 14 * s, y); ctx.close_path(); ctx.fill()
    tx, ty = x + fl * 68 * s + sway, y - 560 * s
    for ang in (-2.9, -2.4, -1.9, -1.2, -0.7, -0.2, 0.3):
        a = ang + math.sin(t * 1.5 + ang) * 0.05
        ex, ey = tx + math.cos(a) * 230 * s, ty + math.sin(a) * 120 * s + 60 * s
        mx, my = tx + math.cos(a) * 120 * s, ty + math.sin(a) * 120 * s - 30 * s
        ctx.move_to(tx, ty); ctx.curve_to(mx, my - 20 * s, mx, my, ex, ey)
        ctx.curve_to(mx, my + 25 * s, mx, my + 10 * s, tx, ty + 12 * s); ctx.fill()

def neon(ctx, text, cx, y, size, color, a=1.0, maxw=930):
    font(ctx, size)
    lines = wrap(ctx, text, maxw)
    for i, ln in enumerate(lines):
        e = ctx.text_extents(ln); x = cx - e.x_advance / 2; yy = y + i * size * 1.12
        for lw, al in ((34, 0.10), (22, 0.18), (12, 0.35)):
            ctx.move_to(x, yy); ctx.text_path(ln); col(ctx, color, al * a)
            ctx.set_line_width(lw); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
        ctx.move_to(x, yy); ctx.text_path(ln); col(ctx, "#12002b", a); ctx.set_line_width(8); ctx.stroke_preserve()
        col(ctx, "#ffffff", a); ctx.fill()
    return len(lines) * size * 1.12

def card(ctx, t, num, title, sub, icon):
    """Kartica cinjenice. t = vreme od pocetka kartice."""
    a = ease(t / 0.3)
    s = 0.7 + 0.3 * pop(t / 0.6)
    ctx.save(); ctx.translate(W / 2, 700); ctx.scale(s, s); ctx.translate(-W / 2, -700)
    rrect(ctx, 70, 300, 940, 820, 50); col(ctx, "#12002b", 0.78 * a); ctx.fill_preserve()
    col(ctx, CYAN, a); ctx.set_line_width(7); ctx.stroke()
    # broj
    ctx.arc(W / 2, 300, 75, 0, 6.3); col(ctx, PINK, a); ctx.fill_preserve(); col(ctx, "#ffffff", a); ctx.set_line_width(6); ctx.stroke()
    font(ctx, 80); e = ctx.text_extents(str(num))
    ctx.move_to(W / 2 - e.x_advance / 2 - e.x_bearing, 300 + e.height / 2); col(ctx, "#ffffff", a); ctx.show_text(str(num))
    icon(ctx, W / 2, 520, t, a)
    h = neon(ctx, title, W / 2, 790, 76, PINK, ease((t - 0.25) / 0.3), 860)
    ta = ease((t - 0.7) / 0.3)
    if ta > 0:
        text_c(ctx, sub, W / 2, 790 + h + 20, 50, CYAN, "#12002b", 8, ta, 840)
    ctx.restore()

# ---- ikonice
def ic_calendar(ctx, x, y, t, a):
    rrect(ctx, x - 120, y - 110, 240, 220, 26); col(ctx, "#ffffff", a); ctx.fill()
    ctx.rectangle(x - 120, y - 110, 240, 60); col(ctx, PINK, a); ctx.fill()
    font(ctx, 38); e = ctx.text_extents("NOV"); ctx.move_to(x - e.x_advance / 2, y - 66); col(ctx, "#ffffff", a); ctx.show_text("NOV")
    font(ctx, 110); e = ctx.text_extents("19"); ctx.move_to(x - e.x_advance / 2 - e.x_bearing, y + 85); col(ctx, "#12002b", a); ctx.show_text("19")

def ic_nopc(ctx, x, y, t, a):
    rrect(ctx, x - 150, y - 110, 300, 190, 18); col(ctx, "#ffffff", a); ctx.set_line_width(14); ctx.stroke()
    ctx.rectangle(x - 20, y + 80, 40, 40); ctx.fill(); ctx.rectangle(x - 80, y + 118, 160, 14); ctx.fill()
    k = ease((t - 0.4) / 0.3)
    col(ctx, "#ff3b3b", a); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(x - 90, y - 70); ctx.line_to(x - 90 + 180 * k, y - 70 + 120 * k); ctx.stroke()
    if k > 0.5:
        kk = ease((t - 0.55) / 0.3)
        ctx.move_to(x + 90, y - 70); ctx.line_to(x + 90 - 180 * kk, y - 70 + 120 * kk); ctx.stroke()

def ic_palm(ctx, x, y, t, a):
    ctx.save(); ctx.arc(x, y, 125, 0, 6.3); col(ctx, ORANGE, a); ctx.fill_preserve(); ctx.clip()
    for k in range(4):
        ctx.rectangle(x - 130, y + 20 + k * 26, 260, 6 + k * 3); col(ctx, PINK, a); ctx.fill()
    ctx.restore()
    ctx.save(); ctx.translate(x + 15, y + 125); ctx.scale(0.42, 0.42); ctx.translate(-x - 15, -y - 125)
    palm(ctx, x + 15, y + 125, 1.0, -1, t)
    ctx.restore()

def ic_duo(ctx, x, y, t, a):
    for dx, c in ((-75, CYAN), (75, PINK)):
        ctx.arc(x + dx, y - 50, 50, 0, 6.3); col(ctx, c, a); ctx.fill()
        ctx.move_to(x + dx - 85, y + 120); ctx.curve_to(x + dx - 85, y + 10, x + dx + 85, y + 10, x + dx + 85, y + 120)
        ctx.close_path(); ctx.fill()

def ic_tag(ctx, x, y, t, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(-0.25 + math.sin(t * 3) * 0.05)
    ctx.move_to(-200, -80); ctx.line_to(110, -80); ctx.line_to(180, 0); ctx.line_to(110, 80); ctx.line_to(-200, 80); ctx.close_path()
    col(ctx, YELLOW, a); ctx.fill()
    ctx.arc(120, 0, 16, 0, 6.3); col(ctx, "#12002b", a); ctx.fill()
    font(ctx, 76); e = ctx.text_extents("$79.99"); ctx.move_to(-45 - e.x_advance / 2, 28); ctx.show_text("$79.99")
    ctx.restore()

FACTS = [
    ("Release: Nov 19, 2026", "PS5 and Xbox Series X|S", ic_calendar),
    ("No PC at launch", "PC players will have to wait", ic_nopc),
    ("Welcome to Leonida", "Vice City is back as the main hub", ic_palm),
    ("Two main characters", "Jason & Lucia", ic_duo),
    ("Standard: $79.99", "Ultimate: $99.99. The box has a download code, no disc", ic_tag),
]
HOOK, CARD, END = 3.2, 5.0, 4.0
AD = False
DUR = HOOK + CARD * len(FACTS) + END

def draw(ctx, t, sp):
    bg(ctx, t)
    if t < HOOK:
        neon(ctx, "5 things you", W / 2, 420, 100, CYAN, ease(t / 0.3))
        neon(ctx, "NEED to know", W / 2, 540, 110, PINK, ease((t - 0.3) / 0.3))
        a = ease((t - 0.8) / 0.3)
        if a > 0:
            s = 0.6 + 0.4 * pop((t - 0.8) / 0.6)
            ctx.save(); ctx.translate(W / 2, 720); ctx.scale(s, s); ctx.translate(-W / 2, -720)
            neon(ctx, "before GTA 6", W / 2, 720, 120, YELLOW, a)
            neon(ctx, "drops", W / 2, 855, 120, YELLOW, a)
            ctx.restore()
    elif t < HOOK + CARD * len(FACTS):
        i = int((t - HOOK) // CARD); lt = t - HOOK - i * CARD
        title, sub, icon = FACTS[i]
        card(ctx, lt, i + 1, title, sub, icon)
        # progres
        for k in range(len(FACTS)):
            rrect(ctx, 250 + k * 120, 210, 100, 14, 7)
            col(ctx, PINK if k < i else ("#ffffff" if k == i else "#ffffff"), 1 if k <= i else 0.3); ctx.fill()
    else:
        lt = t - HOOK - CARD * len(FACTS)
        neon(ctx, "Buying it day one?", W / 2, 480, 92, CYAN, ease(lt / 0.3))
        a = ease((lt - 0.4) / 0.3)
        if a > 0:
            s = 0.6 + 0.4 * pop((lt - 0.4) / 0.6)
            ctx.save(); ctx.translate(W / 2, 680); ctx.scale(s, s); ctx.translate(-W / 2, -680)
            neon(ctx, "YES or NO", W / 2, 680, 130, YELLOW, a)
            ctx.restore()
        neon(ctx, "in the comments", W / 2, 800, 64, "#ffffff", ease((lt - 0.8) / 0.3))
        b = ease((lt - 1.4) / 0.3)
        if b > 0:
            rrect(ctx, 190, 930, 700, 110, 55); col(ctx, PINK, b); ctx.fill()
            text_c(ctx, "Follow for daily GTA 6 news", W / 2, 1003, 46, "#ffffff", "#12002b", 0, b, 680)
    # oznaka reklame (pravilo kampanje)
    if AD:
        rrect(ctx, 60, 230, 150, 70, 20); col(ctx, "#ffffff", 0.95); ctx.fill()
        font(ctx, 44); ctx.move_to(88, 282); col(ctx, "#12002b"); ctx.show_text("AD")
    # disclaimer (uvek)
    text_c(ctx, "Fan-made news. Not affiliated with Rockstar Games.", W / 2, 1400, 30, "#ffffff", "#12002b", 0, 0.75, 900)

def synth_music(path, dur, bpm=104):
    sr = 44100; n = int(dur * sr); out = np.zeros(n); beat = 60 / bpm
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = [(45, [57, 60, 64]), (41, [53, 57, 60]), (48, [55, 60, 64]), (43, [55, 59, 62])]
    def add(st, seg):
        e = min(n, st + len(seg))
        if e > st: out[st:e] += seg[:e - st]
    def saw(f, d, amp, dec=4.0):
        tt = np.arange(int(d * sr)) / sr
        w = 2 * ((tt * f) % 1) - 1 + 0.5 * (2 * ((tt * f * 1.005) % 1) - 1)
        return w * np.minimum(1, tt / 0.005) * np.exp(-tt * dec) * amp
    t0, bar = 0.0, 0
    while t0 < dur:
        root, ch = prog[bar % 4]
        for b in range(4):
            st = int((t0 + b * beat) * sr)
            # kick
            tt = np.arange(int(0.25 * sr)) / sr
            add(st, np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.5)
            if b % 2 == 1:  # snare
                nl = int(0.18 * sr)
                add(st, (np.random.RandomState(bar * 4 + b).rand(nl) * 2 - 1) * np.exp(-np.arange(nl) / sr * 18) * 0.18)
            for k in range(4):  # bas osmine/šesnaestine
                add(int((t0 + (b + k / 4) * beat) * sr), saw(hz(root - 12 + (12 if k == 2 else 0)), beat / 4, 0.10, 10))
            for k in range(4):  # arpeggio
                m = ch[(b * 4 + k) % 3] + (12 if (b + k) % 4 == 3 else 0)
                add(int((t0 + (b + k / 4) * beat) * sr), saw(hz(m + 12), beat / 4, 0.045, 14))
        # pad
        for m in ch:
            tt = np.arange(int(4 * beat * sr)) / sr
            add(int(t0 * sr), np.sin(2 * np.pi * hz(m) * tt) * 0.035 * np.minimum(1, tt / 0.4) * np.minimum(1, (4 * beat - tt) / 0.3))
        t0 += 4 * beat; bar += 1
    fade = int(2.0 * sr); out[-fade:] *= np.linspace(1, 0, fade)
    out = np.tanh(out * 1.3); out = out / np.abs(out).max() * 0.6
    with wave.open(path, "w") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in (2.5, HOOK + 2.5, HOOK + CARD * 2 + 3, HOOK + CARD * 4 + 3.5, DUR - 1.5):
            frame_png(f"{OUT}/gta_{tt:.1f}.png", draw, tt)
    elif len(sys.argv) > 1 and sys.argv[1] == "ad":
        AD = True
        render_scene(f"{OUT}/gta6_5_things_AD_nosound.mp4", DUR, draw, fade_in=0)
    else:
        render_scene(f"{OUT}/gta_v.mp4", DUR, draw, fade_in=0)
        synth_music(f"{OUT}/gta_m.wav", DUR)
        import subprocess
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/gta_v.mp4", "-i", f"{OUT}/gta_m.wav",
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                        "-movflags", "+faststart", f"{OUT}/gta6_5_things.mp4"], check=True)
