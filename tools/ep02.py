"""Epizoda 2: Prvi srpski knezovi"""
import math, sys, os
from engine import *

OUT = os.path.dirname(os.path.abspath(__file__)) + "/out/ep02"
os.makedirs(OUT, exist_ok=True)
FINAL = os.path.dirname(os.path.abspath(__file__)) + "/../videos/ep02_prvi_srpski_knezovi.mp4"

# ---- pomocni crtezi
def crown(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-90, 40); ctx.line_to(-90, -30); ctx.line_to(-45, 10); ctx.line_to(0, -55)
    ctx.line_to(45, 10); ctx.line_to(90, -30); ctx.line_to(90, 40); ctx.close_path()
    fill_stroke(ctx, "#fcc419", "#a35f00", 7, a)
    for cx, c in ((-45, "#e03131"), (0, "#1c7ed6"), (45, "#e03131")):
        ctx.arc(cx, 22, 11, 0, 2 * math.pi); col(ctx, c, a); ctx.fill()
    ctx.restore()

def fortress(ctx, x, y, s, grow=1.0):
    g = ease(grow)
    if g <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s * g)
    ctx.rectangle(-220, -260, 440, 260); fill_stroke(ctx, "#ced4da", "#495057", 7)
    for tx in (-260, 180):
        ctx.rectangle(tx, -360, 80, 360); fill_stroke(ctx, "#adb5bd", "#495057", 7)
        for k in range(3):
            ctx.rectangle(tx + k * 30, -390, 20, 30); fill_stroke(ctx, "#adb5bd", "#495057", 5)
    for k in range(7):
        ctx.rectangle(-210 + k * 62, -290, 36, 30); fill_stroke(ctx, "#ced4da", "#495057", 5)
    rrect(ctx, -55, -130, 110, 130, 50); fill_stroke(ctx, "#7a4a24", "#3a2a1e", 6)
    ctx.restore()

def flag(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, -200); col(ctx, "#5c3a1a"); ctx.set_line_width(10); ctx.stroke()
    for i, c in enumerate(("#c92a2a", "#1864ab", "#ffffff")):
        ctx.move_to(0, -200 + i * 30)
        for k in range(11):
            xx = k * 13; ctx.line_to(xx, -200 + i * 30 + math.sin(t * 5 + k * 0.6) * 6)
        for k in range(10, -1, -1):
            xx = k * 13; ctx.line_to(xx, -170 + i * 30 + math.sin(t * 5 + k * 0.6) * 6)
        ctx.close_path(); col(ctx, c); ctx.fill()
    ctx.restore()

def church(ctx, x, y, s, grow=1.0):
    g = ease(grow)
    if g <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * g, s * g)
    ctx.rectangle(-150, -200, 300, 200); fill_stroke(ctx, "#fff4e6", "#7a4a24", 7)
    ctx.move_to(-80, -200); ctx.curve_to(-80, -330, 80, -330, 80, -200); fill_stroke(ctx, "#e8590c", "#7a4a24", 7)
    ctx.move_to(0, -290); ctx.line_to(0, -380); ctx.move_to(-30, -350); ctx.line_to(30, -350)
    col(ctx, "#fab005"); ctx.set_line_width(12); ctx.stroke()
    rrect(ctx, -40, -110, 80, 110, 38); fill_stroke(ctx, "#7a4a24", "#3a2a1e", 6)
    ctx.restore()

# ---- Scena 1: naslov (0-6s)
def s1(ctx, t, sp):
    sky(ctx, "#5f3dc4", "#9775fa")
    sparkles(ctx, t, 26, 2)
    caption(ctx, "Ko su bili", t, 0.0, y=400, size=96, color="#ffffff")
    caption(ctx, "PRVI SRPSKI", t, 0.4, y=540, size=118, color="#ffd43b")
    caption(ctx, "KNEZOVI?", t, 0.7, y=680, size=140, color="#ffd43b")
    a = ease((t - 1.8) / 0.5)
    if a > 0:
        text_c(ctx, "Kroz vreme sa Milom, Lukom i Sovom Sofijom", W / 2, 1340, 44, "#ffffff", "#3b1f8f", 8, a)
        text_c(ctx, "Epizoda 2", W / 2, 1460, 52, "#ffd43b", "#3b1f8f", 8, a)
    for i, (who, x) in enumerate((("mila", 270), ("luka", 810))):
        k = pop((t - 0.9 - i * 0.2) / 0.7)
        if k > 0:
            kid(ctx, x, 1230 + (1 - k) * 800, 1.0, who, t, wave=t > 2.2)
    k = pop((t - 1.3) / 0.7)
    if k > 0:
        owl(ctx, 540, 1110 + (1 - k) * 900, 1.05, t, flap=t < 2.5)
        crown(ctx, 540, 745 + (1 - k) * 900, 0.7)

# ---- Scena 2: pitanje (6-14s)
D2 = [(0.4, 3.8, "Mila", "Ko je vodio Srbe kad su stigli na Balkan?"),
      (4.0, 8.0, "Sofija", "Knezovi! Hajde da ih upoznamo!")]
def s2(ctx, t, sp):
    room(ctx, t)
    kid(ctx, 230, 1130, 0.95, "mila", t, talking=sp == "Mila", look=1)
    kid(ctx, 470, 1130, 0.95, "luka", t, look=1)
    owl(ctx, 820, 1130, 1.0, t, talking=sp == "Sofija", look=-1, flap=t > 6.0)
    hourglass(ctx, 820, 680 - 20 * math.sin(t * 2), 0.9, t, glow=ease((t - 5.5) / 1.5))

# ---- Scena 3: kroz vreme (14-18s)
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
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(t * 2.2); ctx.translate(-cx, -cy)
    kid(ctx, cx - 330, cy + 150, 0.55, "mila", t)
    kid(ctx, cx + 330, cy + 150, 0.55, "luka", t)
    owl(ctx, cx, cy - 300, 0.55, t, flap=True)
    ctx.restore()
    caption(ctx, "Pre oko 1200 godina...", t, 0.8, y=1380, size=80, color="#ffd43b")

# ---- Scena 4: Viseslav (18-30s)
D4 = [(0.5, 5.6, "Sofija", "Prvi srpski knez čije ime znamo zvao se Višeslav."),
      (5.8, 11.6, "Sofija", "Živeo je krajem 8. veka i vodio je zajednicu srpskih plemena.")]
def s4(ctx, t, sp):
    sky(ctx, "#74c0fc", "#e7f5ff")
    sun(ctx, 880, 260, 70, t); clouds(ctx, t, (420,))
    hills(ctx, 1080, "#a9e34b", "#82c91e")
    log_house(ctx, 200, 960, 0.75, 1.0); log_house(ctx, 900, 940, 0.6, 1.0)
    caption(ctx, "Knez VIŠESLAV", t, 0.2, y=230, size=80, color="#ffffff")
    villager(ctx, 540, 1150, 0.85, t, tunic="#862e9c", walking=False, beard=True, talking=False)
    k = pop((t - 1.0) / 0.8)
    if k > 0: crown(ctx, 540, 1150 - 0.85 * 330 - 20, 0.45 * k)
    for i, x in enumerate((260, 820)):
        villager(ctx, x, 1180, 0.55, t + i, tunic=["#1971c2", "#2b8a3e"][i], walking=False, hair="#2b1d14")
    kid(ctx, 90, 1165, 0.42, "luka", t, look=1)
    owl(ctx, 990, 1165, 0.42, t, talking=sp == "Sofija", look=-1)

# ---- Scena 5: Vlastimir i tvrdjava (30-44s)
D5 = [(0.4, 3.6, "Luka", "A ko je bio najjači knez?"),
      (3.8, 8.8, "Sofija", "Knez Vlastimir! On je ujedinio srpske zemlje u jednu kneževinu."),
      (9.0, 13.6, "Sofija", "Gradio je tvrđave i branio svoj narod.")]
def s5(ctx, t, sp):
    sky(ctx, "#ffa94d", "#ffe8cc")
    sun(ctx, 160, 300, 70, t)
    hills(ctx, 1080, "#94d82d", "#74b816")
    fortress(ctx, 600, 1000, 1.0, (t - 8.8) / 1.6)
    if t > 10.4: flag(ctx, 640, 610, 0.9, t)
    caption(ctx, "Knez VLASTIMIR", t, 3.8, y=230, size=80, color="#ffffff")
    villager(ctx, 270, 1180, 0.75, t, tunic="#c92a2a", walking=False, beard=True)
    if t > 4.0: crown(ctx, 270, 1180 - 0.75 * 330 - 18, 0.4 * pop((t - 4.0) / 0.8))
    kid(ctx, 90, 1165, 0.42, "luka", t, talking=sp == "Luka", look=1)
    owl(ctx, 990, 1165, 0.42, t, talking=sp == "Sofija", look=-1)

# ---- Scena 6: Mutimir i pokrstavanje (44-56s)
D6 = [(0.4, 3.6, "Mila", "Gle, grade crkvu!"),
      (3.8, 11.6, "Sofija", "Za vreme kneza Mutimira, oko 870. godine, Srbi su primili hrišćanstvo.")]
def s6(ctx, t, sp):
    sky(ctx, "#74c0fc", "#d0ebff")
    clouds(ctx, t, (380, 520))
    hills(ctx, 1080, "#8ce99a", "#51cf66")
    church(ctx, 600, 1050, 1.15, (t - 1.0) / 2.5)
    if t > 3.5: sparkles(ctx, t, 10, 11, "#ffffff")
    caption(ctx, "Knez MUTIMIR", t, 3.8, y=230, size=80, color="#ffffff")
    tree(ctx, 980, 980, 0.7, t)
    villager(ctx, 250, 1180, 0.7, t, tunic="#1864ab", walking=False, beard=True)
    if t > 4.0: crown(ctx, 250, 1180 - 0.7 * 330 - 18, 0.38 * pop((t - 4.0) / 0.8))
    kid(ctx, 90, 1165, 0.42, "mila", t, talking=sp == "Mila", look=1)
    owl(ctx, 990, 1165, 0.42, t, talking=sp == "Sofija", look=-1)

# ---- Scena 7: pouka (56-66s)
D7 = [(5.0, 9.6, "Luka", "Kad smo zajedno, jači smo!")]
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
        text_c(ctx, "Sloga čini snagu.", W / 2, 470, 66, "#2b1d14", "#ffffff", 0, ease((t - 0.8) / 0.4), 800)
    if t > 2.2:
        text_c(ctx, "Dobar vođa brine o svom narodu.", W / 2, 640, 62, "#e8590c", "#ffffff", 0, ease((t - 2.2) / 0.4), 800)
    kid(ctx, 230, 1130, 0.75, "mila", t)
    kid(ctx, 540, 1130, 0.75, "luka", t, talking=sp == "Luka")
    owl(ctx, 850, 1130, 0.8, t)

# ---- Scena 8: kraj (66-72s)
def s8(ctx, t, sp):
    sky(ctx, "#5f3dc4", "#9775fa")
    sparkles(ctx, t, 26, 9)
    caption(ctx, "Sledeća epizoda:", t, 0.0, y=330, size=64, color="#ffffff")
    caption(ctx, "Sveti Sava", t, 0.4, y=450, size=96, color="#ffd43b")
    caption(ctx, "Zaprati da ne propustiš!", t, 1.4, y=1400, size=66, color="#ffffff")
    kid(ctx, 260, 1220, 0.9, "mila", t, wave=True)
    kid(ctx, 820, 1220, 0.9, "luka", t, wave=True)
    owl(ctx, 540, 1140, 0.95, t, flap=True)

SCENES = [
    ("s1", 6.0, s1, []), ("s2", 8.0, s2, D2), ("s3", 4.0, s3, []), ("s4", 12.0, s4, D4),
    ("s5", 14.0, s5, D5), ("s6", 12.0, s6, D6), ("s7", 10.0, s7, D7), ("s8", 6.0, s8, []),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "frames":
        for name, dur, fn, dl in SCENES:
            for tt in (dur * 0.35, dur * 0.85):
                frame_png(f"{OUT}/{name}_{tt:.1f}.png", fn, tt, dl)
    else:
        files = []
        for name, dur, fn, dl in SCENES:
            render_scene(f"{OUT}/{name}.mp4", dur, fn, dl)
            files.append(f"{OUT}/{name}.mp4")
        total = sum(s[1] for s in SCENES)
        music(f"{OUT}/music.wav", total, seed=2)
        assemble(files, f"{OUT}/music.wav", os.path.abspath(FINAL))
        print("OK", os.path.abspath(FINAL))
