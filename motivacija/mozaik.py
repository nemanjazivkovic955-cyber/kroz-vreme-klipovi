"""Mozaik efekat za profil (TikTok / YouTube Shorts, 3 kolone):
velika crno-zlatna slika se sece na 3x2 dela; svaki deo je prva sekunda (naslovna slika) jednog klipa.
Kad se klipovi okace redom, na profilu se spoje u jednu sliku.

Upotreba: python3 mozaik.py <folder_klipova> RED1 RED2 id1 id2 id3 id4 id5 id6
  (id1 = gore levo ... id6 = dole desno). Kaciti OBRNUTIM redom: id6 prvi, id1 poslednji.
"""
import os, sys, math, random, subprocess
import cairo

TW, TH = 1080, 1920
COLS, ROWS = 3, 2
CW, CH = TW * COLS, TH * ROWS
HOLD = 1.2   # koliko traje naslovna plocica
XF = 0.35    # prelaz u klip


def gold(y0, y1):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, 1.0, 0.93, 0.62)
    g.add_color_stop_rgb(0.45, 0.98, 0.78, 0.28)
    g.add_color_stop_rgb(0.55, 0.86, 0.60, 0.14)
    g.add_color_stop_rgb(1, 1.0, 0.85, 0.42)
    return g


def canvas(path, words):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, CW, CH)
    c = cairo.Context(s)
    c.set_source_rgb(0.02, 0.02, 0.025); c.paint()
    # zlatni sjaj u sredini svakog reda
    for r in range(ROWS):
        cy = TH * r + TH / 2
        g = cairo.RadialGradient(CW / 2, cy, 0, CW / 2, cy, CW * 0.6)
        g.add_color_stop_rgba(0, 0.85, 0.62, 0.18, 0.28); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.rectangle(0, TH * r, CW, TH); c.set_source(g); c.fill()
    # dijagonalni zraci svetla
    rnd = random.Random(7)
    for i in range(14):
        x = rnd.uniform(-CW * 0.2, CW * 1.1); w = rnd.uniform(40, 160)
        c.save(); c.translate(x, 0); c.rotate(0.35)
        g = cairo.LinearGradient(0, 0, w, 0)
        g.add_color_stop_rgba(0, 1, 0.85, 0.4, 0); g.add_color_stop_rgba(0.5, 1, 0.85, 0.4, 0.06); g.add_color_stop_rgba(1, 1, 0.85, 0.4, 0)
        c.rectangle(0, -CH, w, CH * 3); c.set_source(g); c.fill(); c.restore()
    # zlatne cestice
    for i in range(500):
        x, y, r = rnd.uniform(0, CW), rnd.uniform(0, CH), rnd.uniform(1.5, 6)
        c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 0.82, 0.35, rnd.uniform(0.15, 0.7)); c.fill()
    # ogromne reci, po jedna u svakom redu, centrirane u srednjem delu plocice (sigurno i za 3:4 isecanje)
    c.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    for r, wd in enumerate(words):
        size = 1500
        c.set_font_size(size); e = c.text_extents(wd)
        k = min((CW * 0.9) / e.width, 1150 / e.height); size *= k
        c.set_font_size(size); e = c.text_extents(wd)
        x = CW / 2 - e.width / 2 - e.x_bearing
        y = TH * r + TH / 2 - e.height / 2 - e.y_bearing
        c.move_to(x + 18, y + 26); c.text_path(wd); c.set_source_rgba(0, 0, 0, 0.7); c.fill()
        c.move_to(x, y); c.text_path(wd)
        c.set_source(gold(y + e.y_bearing, y + e.y_bearing + e.height)); c.fill_preserve()
        c.set_source_rgba(0.35, 0.22, 0.03, 1); c.set_line_width(10); c.stroke()
    # tanke zlatne linije izmedju redova
    c.set_source_rgba(1, 0.82, 0.35, 0.8); c.set_line_width(6)
    for r in range(ROWS):
        for yy in (TH * r + 150, TH * r + TH - 150):
            c.move_to(CW * 0.06, yy); c.line_to(CW * 0.94, yy); c.stroke()
    s.write_to_png(path)
    return s


def tiles(full, outdir):
    paths = []
    src = cairo.ImageSurface.create_from_png(full)
    for r in range(ROWS):
        for col in range(COLS):
            t = cairo.ImageSurface(cairo.FORMAT_RGB24, TW, TH)
            c = cairo.Context(t); c.set_source_surface(src, -col * TW, -r * TH); c.paint()
            p = os.path.join(outdir, f"tile_{r * COLS + col + 1}.png"); t.write_to_png(p); paths.append(p)
    return paths


def prepend(tile, clip, out, audio):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip],
                             capture_output=True, text=True).stdout)
    fc = (f"[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p,trim=duration={HOLD + XF}[a];"
          f"[1:v]fps=30,format=yuv420p,setsar=1[b];"
          f"[a][b]xfade=transition=zoomin:duration={XF}:offset={HOLD}[v]")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", str(HOLD + XF), "-i", tile, "-i", clip,
           "-filter_complex", fc + (f";[1:a]adelay={int(HOLD * 1000)}|{int(HOLD * 1000)}[au]" if audio else ""),
           "-map", "[v]"] + (["-map", "[au]"] if audio else []) + \
          ["-t", f"{d + HOLD:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "8M", "-bufsize", "16M",
           "-pix_fmt", "yuv420p"] + (["-c:a", "aac", "-b:a", "160k"] if audio else []) + ["-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    folder, w1, w2 = sys.argv[1], sys.argv[2], sys.argv[3]
    ids = sys.argv[4:]
    assert len(ids) == COLS * ROWS
    os.makedirs(os.path.join(folder, "mozaik"), exist_ok=True)
    full = os.path.join(folder, "mozaik", "profil_pregled.png")
    canvas(full, [w1, w2])
    tl = tiles(full, os.path.join(folder, "mozaik"))
    for i, qid in enumerate(ids):
        for sub, au in (("", True), ("bez_muzike", False)):
            src = os.path.join(folder, sub, f"{qid}.mp4")
            tmp = src + ".mz.mp4"
            prepend(tl[i], src, tmp, au)
            os.replace(tmp, src)
        print("ok", qid, "-> plocica", i + 1)
