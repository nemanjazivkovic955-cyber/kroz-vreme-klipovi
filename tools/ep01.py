"""Epizoda 1: Odakle su dosli Srbi?"""
import math, sys, os
from engine import *

OUT = os.path.dirname(os.path.abspath(__file__)) + "/out"
os.makedirs(OUT, exist_ok=True)

# ---- Scena 1: hook / naslov (0-6s)
def s1(ctx, t, sp):
    sky(ctx, "#5f3dc4", "#9775fa")
    sparkles(ctx, t, 26, 1)
    caption(ctx, "Odakle su došli", t, 0.0, y=420, size=96, color="#ffffff")
    caption(ctx, "SRBI?", t, 0.5, y=560, size=170, color="#ffd43b")
    a = ease((t - 1.6) / 0.5)
    if a > 0:
        text_c(ctx, "Kroz vreme sa Milom, Lukom i Sovom Sofijom", W / 2, 1340, 44, "#ffffff", "#3b1f8f", 8, a)
        text_c(ctx, "Epizoda 1", W / 2, 1460, 52, "#ffd43b", "#3b1f8f", 8, a)
    for i, (who, x) in enumerate((("mila", 270), ("luka", 810))):
        k = pop((t - 0.9 - i * 0.2) / 0.7)
        if k > 0:
            kid(ctx, x, 1230 + (1 - k) * 800, 1.0, who, t, wave=t > 2.2, jump=0)
    k = pop((t - 1.3) / 0.7)
    if k > 0:
        owl(ctx, 540, 1110 + (1 - k) * 900, 1.05, t, flap=t < 2.5)

# ---- Scena 2: soba, pitanje (6s-15s)
D2 = [(0.4, 4.2, "Luka", "Sova Sofija, odakle su došli naši preci?"),
      (4.4, 9.0, "Sofija", "Hajde da vidimo! Okrenite čarobni peščani sat!")]
def s2(ctx, t, sp):
    room(ctx, t)
    kid(ctx, 230, 1130, 0.95, "mila", t, talking=sp == "Mila", look=1)
    kid(ctx, 470, 1130, 0.95, "luka", t, talking=sp == "Luka", look=1)
    owl(ctx, 820, 1130, 1.0, t, talking=sp == "Sofija", look=-1, flap=t > 7.5)
    g = ease((t - 6.5) / 1.5)
    hourglass(ctx, 820, 680 - 20 * math.sin(t * 2), 0.9, t, glow=g)

# ---- Scena 3: kroz vreme (15-19s)
def s3(ctx, t, sp):
    ctx.rectangle(0, 0, W, H); col(ctx, "#1b1145"); ctx.fill()
    cx, cy = W / 2, 820
    colors = ["#ff6b6b", "#ffd43b", "#69db7c", "#4dabf7", "#b197fc"]
    for i in range(60):
        ang = i * 0.45 + t * 3
        r = (i * 18 + t * 260) % 1100
        ctx.arc(cx + math.cos(ang) * r, cy + math.sin(ang) * r, 10 + r / 40, 0, 2 * math.pi)
        col(ctx, colors[i % 5], 0.85); ctx.fill()
    hourglass(ctx, cx, cy, 1.1 + 0.1 * math.sin(t * 6), t * 4, glow=1)
    s = 0.55
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(t * 2.2); ctx.translate(-cx, -cy)
    kid(ctx, cx - 330, cy + 150, s, "mila", t, jump=0)
    kid(ctx, cx + 330, cy + 150, s, "luka", t)
    owl(ctx, cx, cy - 300, s, t, flap=True)
    ctx.restore()
    caption(ctx, "Pre oko 1400 godina...", t, 0.8, y=1380, size=80, color="#ffd43b")

# ---- Scena 4: seoba preko Dunava (19-32s)
D4 = [(0.6, 5.6, "Sofija", "Srbi su deo velike porodice naroda koji se zovu Sloveni."),
      (5.8, 12.6, "Sofija", "Pre oko 1400 godina prešli su reku Dunav i stigli na Balkan.")]
def s4(ctx, t, sp):
    sky(ctx)
    sun(ctx, 880, 260, 70, t)
    clouds(ctx, t, (380, 520))
    hills(ctx, 1000, "#8ce99a", "#51cf66")
    for x in (80, 990):
        tree(ctx, x, 800, 0.8, t)
    river(ctx, 740, t, 130, "Dunav")
    ctx.rectangle(0, 870, W, 400); col(ctx, "#51cf66"); ctx.fill()
    caption(ctx, "7. vek", t, 0.2, y=230, size=70, color="#ffffff")
    # kolona ljudi ide s leva na desno
    group = [("#c92a2a", True, True, False), ("#1971c2", False, False, True), ("#2b8a3e", False, True, False),
             ("#e8590c", True, False, False), ("#862e9c", False, False, True)]
    for i, (c, beard, bundle, skirt) in enumerate(group):
        x = -250 + i * 230 + t * 75
        x = ((x + 300) % (W + 600)) - 300
        villager(ctx, x, 1130, 0.62, t + i, tunic=c, beard=beard, bundle=bundle, skirt=skirt,
                 hair=["#5c3a1a", "#f2c14e", "#2b1d14"][i % 3])
    # deca i sova posmatraju
    kid(ctx, 90, 1165, 0.42, "mila", t, look=1)
    owl(ctx, 990, 1165, 0.42, t, talking=sp == "Sofija")

# ---- Scena 5: selo (32-44s)
D5 = [(0.4, 3.8, "Luka", "A šta su ovde radili?"),
      (4.0, 11.6, "Sofija", "Gradili su kuće od drveta, orali njive i čuvali ovce.")]
def s5(ctx, t, sp):
    sky(ctx, "#74c0fc", "#e7f5ff")
    sun(ctx, 160, 260, 65, t)
    clouds(ctx, t, (420,))
    hills(ctx, 1080, "#a9e34b", "#82c91e")
    # njiva
    for k in range(7):
        ctx.move_to(560 + k * 70, 900); ctx.line_to(470 + k * 90, 1130)
        col(ctx, "#e9b949"); ctx.set_line_width(26); ctx.stroke()
    log_house(ctx, 270, 980, 0.95, (t - 4.0) / 2.0)
    log_house(ctx, 760, 900, 0.7, (t - 5.5) / 2.0)
    tree(ctx, 980, 980, 0.7, t)
    for i, x in enumerate((150, 330, 520)):
        sheep(ctx, x + math.sin(t * 0.8 + i) * 20, 1150 + (i % 2) * 40, 0.9, t)
    villager(ctx, 860, 1160, 0.5, t, tunic="#c92a2a", walking=False, beard=True)
    kid(ctx, 90, 1165, 0.42, "luka", t, talking=sp == "Luka", look=1)
    owl(ctx, 990, 1165, 0.42, t, talking=sp == "Sofija", look=-1)

# ---- Scena 6: gostoprimstvo (44-58s)
D6 = [(0.4, 3.8, "Mila", "Gle! Došao je neki umorni putnik!"),
      (4.0, 13.6, "Sofija", "Stari Sloveni su bili poznati po gostoprimstvu. Putnika su dočekivali kao prijatelja.")]
def s6(ctx, t, sp):
    sky(ctx, "#ffa94d", "#ffe8cc")
    sun(ctx, 540, 520, 90, t)
    hills(ctx, 1080, "#94d82d", "#74b816")
    log_house(ctx, 760, 1000, 1.05, 1.0)
    # putnik dolazi sleva i staje
    px = min(380, -150 + t * 180)
    walking = px < 380
    villager(ctx, px, 1180, 0.68, t, tunic="#868e96", walking=walking, bundle=True, hair="#adb5bd", beard=True)
    # domacica izlazi sa hlebom
    ha = ease((t - 4.5) / 1.0)
    hx = 800 - 160 * ha
    villager(ctx, hx, 1180, 0.68, t, tunic="#c2255c", walking=0 < ha < 1, skirt=True, hair="#7a3e12")
    if ha > 0:
        b = pop((t - 5.3) / 0.8)
        if b > 0:
            bread(ctx, hx - 75, 1000 - 20 * b, 0.9 * b)
    if t > 7.5:
        sparkles(ctx, t, 10, 7, "#ffffff")
        # srce
        k = pop((t - 7.5) / 0.8); x, y, r = 520, 560, 55 * k
        ctx.move_to(x, y + r); ctx.curve_to(x - r * 2, y - r * 0.5, x - r * 0.6, y - r * 1.8, x, y - r * 0.6)
        ctx.curve_to(x + r * 0.6, y - r * 1.8, x + r * 2, y - r * 0.5, x, y + r)
        fill_stroke(ctx, "#ff6b6b", "#c92a2a", 6)
    kid(ctx, 90, 1165, 0.42, "mila", t, talking=sp == "Mila", look=1)
    owl(ctx, 990, 1165, 0.42, t, talking=sp == "Sofija", look=-1)

# ---- Scena 7: pouka (58-68s)
D7 = [(5.0, 9.8, "Mila", "Sutra ću i ja podeliti užinu sa drugarom!")]
def s7(ctx, t, sp):
    sky(ctx, "#ffe066", "#fff9db")
    sparkles(ctx, t, 22, 5, "#fab005")
    a = max(0.01, pop(t / 0.8))
    ctx.save(); ctx.translate(W / 2, 520); ctx.scale(a, a); ctx.translate(-W / 2, -520)
    rrect(ctx, 90, 300, 900, 560, 50); fill_stroke(ctx, "#ffffff", "#f08c00", 12)
    rrect(ctx, 330, 255, 420, 100, 50); col(ctx, "#f08c00"); ctx.fill()
    font(ctx, 64); e = ctx.text_extents("POUKA")
    ctx.move_to(W / 2 - e.x_advance / 2, 328); col(ctx, "#ffffff"); ctx.show_text("POUKA")
    ctx.restore()
    if t > 0.8:
        text_c(ctx, "Podeli ono što imaš.", W / 2, 470, 66, "#2b1d14", "#ffffff", 0, ease((t - 0.8) / 0.4), 800)
    if t > 2.2:
        text_c(ctx, "Dobrota je najveće bogatstvo.", W / 2, 640, 66, "#e8590c", "#ffffff", 0, ease((t - 2.2) / 0.4), 800)
    kid(ctx, 230, 1130, 0.75, "mila", t, talking=sp == "Mila")
    kid(ctx, 540, 1130, 0.75, "luka", t)
    owl(ctx, 850, 1130, 0.8, t)

# ---- Scena 8: kraj (68-74s)
def s8(ctx, t, sp):
    sky(ctx, "#5f3dc4", "#9775fa")
    sparkles(ctx, t, 26, 9)
    caption(ctx, "Sledeća epizoda:", t, 0.0, y=330, size=64, color="#ffffff")
    caption(ctx, "Prvi srpski knezovi", t, 0.4, y=450, size=86, color="#ffd43b")
    caption(ctx, "Zaprati da ne propustiš!", t, 1.4, y=1400, size=66, color="#ffffff")
    kid(ctx, 260, 1220, 0.9, "mila", t, wave=True)
    kid(ctx, 820, 1220, 0.9, "luka", t, wave=True)
    owl(ctx, 540, 1140, 0.95, t, flap=True)

SCENES = [
    ("s1", 6.0, s1, []), ("s2", 9.0, s2, D2), ("s3", 4.0, s3, []), ("s4", 13.0, s4, D4),
    ("s5", 12.0, s5, D5), ("s6", 14.0, s6, D6), ("s7", 10.0, s7, D7), ("s8", 6.0, s8, []),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "frames":
        for name, dur, fn, dl in SCENES:
            for tt in (dur * 0.35, dur * 0.85):
                frame_png(f"{OUT}/{name}_{tt:.1f}.png", fn, tt, dl)
    else:
        names = sys.argv[2:] or [s[0] for s in SCENES]
        for name, dur, fn, dl in SCENES:
            if name in names:
                render_scene(f"{OUT}/{name}.mp4", dur, fn, dl)
