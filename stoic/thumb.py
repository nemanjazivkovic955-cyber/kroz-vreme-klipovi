"""Thumbnail 1280x720 za dugi video: kadar iz snimka + krupan tekst. Upotreba: python3 stoic/thumb.py <mk_id> <sek> <out.jpg> "RED 1" "red 2" """
import sys, os, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make as M
src, ss, out, l1, l2 = sys.argv[1:6]
bg = out + ".bg.png"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", ss, "-i", M.src(src), "-frames:v", "1", "-vf",
                f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,{M.GRADE},eq=contrast=1.15:brightness=-0.04,vignette=PI/4", bg], check=True)
s = cairo.ImageSurface.create_from_png(bg); c = cairo.Context(s)
g = cairo.LinearGradient(0, 0, 760, 0)
g.add_color_stop_rgba(0, 0, 0, 0, 0.78); g.add_color_stop_rgba(1, 0, 0, 0, 0)
c.rectangle(0, 0, 1280, 720); c.set_source(g); c.fill()
def txt(t, size, y, rgb=(1, 1, 1), x=60):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    for dx, dy, a in ((0, 8, 0.7), (4, 6, 0.5)):
        c.move_to(x + dx, y + dy); c.set_source_rgba(0, 0, 0, a); c.show_text(t)
    c.move_to(x, y); c.set_source_rgb(*rgb); c.show_text(t)
words = l1.split()
txt(words[0], 230, 300, (1.0, 0.80, 0.25))
txt(" ".join(words[1:]), 118, 430)
txt(l2, 52, 540, (0.92, 0.92, 0.92))
s.write_to_png(out + ".png")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out + ".png", "-q:v", "2", out], check=True)
os.remove(bg); os.remove(out + ".png"); print(out)
