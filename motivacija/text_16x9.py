"""Dodaje kratak crno-zlatni tekst koji prati poentu klipa na 16:9 YouTube klipove.
Ulaz: videos/youtube/rich_edit_16x9/*.mp4  ->  izlaz: videos/youtube/rich_edit_16x9_tekst/*.mp4
Istaknuta rec u *zvezdicama* = crna slova na zlatnoj traci.
"""
import os, subprocess
import cairo
import design2 as D

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "videos", "youtube", "rich_edit_16x9")
OUT = os.path.join(HERE, "..", "videos", "youtube", "rich_edit_16x9_tekst")
W, H = 1920, 1080

TEXTS = {
    "kola_01": "Top down. *No* limits.",
    "kola_02": "Work *now*. Cruise later.",
    "kola_03": "Dream it. *Drive* it.",
    "kola_04": "They *doubted*. Now they watch.",
    "kola_05": "Details make *millions*.",
    "kola_06": "Built, not *borrowed*.",
    "kola_07": "Move with *winners*.",
    "kola_08": "Your circle is your *speed*.",
    "kola_09": "Stay in your *lane*.",
    "kola_10": "Full speed *ahead*.",
    "kola_11": "Patience *pays*.",
    "kola_12": "Earned in *silence*.",
    "kola_13": "The city never *sleeps*.",
    "kola_14": "Neither do *I*.",
    "kola_15": "Light at the *end*.",
    "kola_16": "Keep *driving*.",
    "moc_01": "Fly *private*.",
    "moc_02": "Think *bigger*.",
    "moc_03": "Deals at *40,000* feet.",
    "moc_04": "Sign your own *checks*.",
    "novac_01": "This is the *goal*.",
    "novac_02": "Own the *view*.",
    "novac_03": "Money *talks*.",
    "novac_04": "Wealth *whispers*.",
    "novac_05": "Life by *design*.",
    "novac_06": "Not by *accident*.",
    "zene_luksuz_01": "Celebrate *every* win.",
}


def text_png(path, text, size=130):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    # blago zatamnjenje donje polovine radi citljivosti
    g = cairo.LinearGradient(0, H * 0.45, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    D._face(c, D.QUOTE_FONT, size)
    lines, sp = D._balanced(c, D._tokens(text), W * 0.8)
    lh = size * 1.1
    y0 = H * 0.80 - (len(lines) - 1) * lh + size * 0.35
    for li, (words, lw) in enumerate(lines):
        x = W / 2 - lw / 2 - sum(16 for (_, h, _) in words if h)
        y = y0 + li * lh
        for (w, hl, ww) in words:
            if hl:
                x += 16
                D._rrect(c, x - 14, y - size * 0.86, ww + 28, size * 1.02, 12)
                c.set_source_rgba(0, 0, 0, 0.4); c.set_line_width(8); c.stroke_preserve()
                c.set_source(D._gold_grad(y - size * 0.86, y + size * 0.16)); c.fill()
                c.move_to(x, y); c.set_source_rgb(0.04, 0.03, 0.02); c.show_text(w)
            else:
                D._shadow_text(c, x, y, w, D.GOLD, 1.0, outline=8)
            x += ww + sp + (16 if hl else 0)
    s.write_to_png(path)


os.makedirs(OUT, exist_ok=True)
tmp = os.path.join(HERE, "out"); os.makedirs(tmp, exist_ok=True)
for name, text in TEXTS.items():
    src = os.path.join(SRC, name + ".mp4")
    if not os.path.exists(src): continue
    png = os.path.join(tmp, f"t16_{name}.png"); text_png(png, text)
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", src, "-loop", "1", "-t", "4", "-i", png,
                    "-filter_complex", "[1:v]format=rgba,fade=t=in:st=0.1:d=0.3:alpha=1,fade=t=out:st=3.6:d=0.35:alpha=1[t];"
                    "[0:v][t]overlay=format=auto,format=yuv420p[v]", "-map", "[v]", "-t", "4", "-an",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-movflags", "+faststart",
                    os.path.join(OUT, name + ".mp4")], check=True)
    print("ok", name)
