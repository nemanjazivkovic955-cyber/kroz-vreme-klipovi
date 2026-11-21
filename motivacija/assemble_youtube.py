"""Spaja 16:9 klipove sa tekstom u jedan YouTube video: uvodna kartica + klipovi (redosled price) + odjava + muzika."""
import os, subprocess, cairo, math, random
import design2 as D
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "videos", "youtube", "rich_edit_16x9_tekst")
OUT = os.path.join(HERE, "..", "videos", "youtube", "rich_life_youtube.mp4")
TMP = os.path.join(HERE, "out", "yt_asm"); os.makedirs(TMP, exist_ok=True)
W, H = 1920, 1080
ORDER = ["kola_15", "kola_16", "kola_01", "kola_02", "kola_11", "kola_12", "novac_03", "novac_04",
         "kola_09", "kola_10", "kola_07", "kola_08", "kola_13", "kola_14", "moc_03", "moc_04",
         "moc_01", "moc_02", "kola_05", "kola_06", "kola_03", "kola_04", "novac_01", "novac_02",
         "novac_05", "novac_06", "zene_luksuz_01"]


def card(path, big, small):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    c.set_source_rgb(0.02, 0.02, 0.025); c.paint()
    g = cairo.RadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.6)
    g.add_color_stop_rgba(0, 0.85, 0.62, 0.18, 0.30); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    rnd = random.Random(3)
    for i in range(220):
        c.arc(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1, 4), 0, 2 * math.pi)
        c.set_source_rgba(1, 0.82, 0.35, rnd.uniform(0.15, 0.6)); c.fill()
    c.select_font_face("Anton"); c.set_font_size(300); e = c.text_extents(big)
    x, y = W / 2 - e.width / 2 - e.x_bearing, H / 2 + 60
    c.move_to(x + 10, y + 14); c.text_path(big); c.set_source_rgba(0, 0, 0, 0.7); c.fill()
    c.move_to(x, y); c.text_path(big); c.set_source(D._gold_grad(y + e.y_bearing, y)); c.fill_preserve()
    c.set_source_rgba(0.35, 0.22, 0.03, 1); c.set_line_width(6); c.stroke()
    c.select_font_face("DM Serif Display", cairo.FONT_SLANT_ITALIC); c.set_font_size(64); e = c.text_extents(small)
    c.move_to(W / 2 - e.x_advance / 2, y + 120); c.set_source_rgb(*D.GOLD); c.show_text(small)
    c.set_source_rgba(*D.GOLD, 0.9); c.set_line_width(4)
    for yy in (y - 360, y + 170):
        c.move_to(W * 0.3, yy); c.line_to(W * 0.7, yy); c.stroke()
    s.write_to_png(path)


def still(png, out, d):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-loop", "1", "-t", str(d), "-i", png,
                    "-vf", f"zoompan=z='1+0.04*on/{int(d*30)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,"
                    f"fade=t=in:d=0.6,fade=t=out:st={d-0.5}:d=0.5,format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", out], check=True)


def build(order=ORDER, src=SRC, out=OUT, title="RICH LIFE", sub="Money  \u2022  Cars  \u2022  Power",
          outro_sub="for more rich life motivation", music_start=18):
    card(os.path.join(TMP, "intro.png"), title, sub)
    card(os.path.join(TMP, "outro.png"), "SUBSCRIBE", outro_sub)
    still(os.path.join(TMP, "intro.png"), os.path.join(TMP, "intro.mp4"), 3.0)
    still(os.path.join(TMP, "outro.png"), os.path.join(TMP, "outro.mp4"), 3.5)
    parts = [os.path.join(TMP, "intro.mp4")] + [os.path.join(src, n + ".mp4") for n in order] + [os.path.join(TMP, "outro.mp4")]
    total = 3.0 + 4 * len(order) + 3.5
    inputs = sum([["-i", p] for p in parts], [])
    fc = "".join(f"[{i}:v]fps=30,setsar=1,format=yuv420p[v{i}];" for i in range(len(parts)))
    fc += "".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[v];"
    music = os.path.join(HERE, "music", "cinematic_piano.mp3")
    fc += (f"[{len(parts)}:a]atrim=start={music_start}:duration={total},asetpts=PTS-STARTPTS,"
           f"afade=t=in:d=1.5,afade=t=out:st={total-3}:d=3,loudnorm=I=-16:TP=-1.5[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y"] + inputs + ["-i", music, "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "12M",
                    "-bufsize", "24M", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("OK", out, round(total, 1), "s")


if __name__ == "__main__":
    build()
