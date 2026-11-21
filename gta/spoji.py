"""Spaja slike u uspravni TikTok video 1080x1920: zamucena pozadina, blagi zum, prelazi.
Upotreba: python3 gta/spoji.py izlaz.mp4 slika1.jpg:trajanje slika2.jpg:trajanje ...
"""
import subprocess, sys

FPS = 30
XF = 0.6  # trajanje prelaza


def main():
    out = sys.argv[1]
    items = []
    for a in sys.argv[2:]:
        p, d = a.rsplit(":", 1)
        items.append((p, float(d)))
    inputs, fc = [], ""
    for i, (p, d) in enumerate(items):
        inputs += ["-loop", "1", "-t", str(d), "-i", p]
        n = int(d * FPS)
        zin = i % 2 == 0 and i != len(items) - 1  # naizmenicno; poslednja se zavrsava cela
        z = f"1+0.08*on/{n}" if zin else f"1.08-0.08*on/{n}"
        fc += (f"[{i}:v]split[a{i}][b{i}];"
               f"[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
               f"gblur=sigma=40,eq=brightness=-0.25:saturation=1.1[bg{i}];"
               f"[b{i}]scale=2160:-2,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
               f"d=1:s=1080x1608:fps={FPS}[fg{i}];"
               f"[bg{i}][fg{i}]overlay=0:(H-h)/2,format=yuv420p,trim=duration={d},setpts=PTS-STARTPTS[s{i}];")
    last, t = "s0", items[0][1]
    trans = ["fade", "fadewhite", "fade", "fade"]
    for i in range(1, len(items)):
        off = t - XF
        fc += f"[{last}][s{i}]xfade=transition={trans[(i - 1) % len(trans)]}:duration={XF}:offset={off:.2f}[x{i}];"
        last = f"x{i}"; t = off + items[i][1]
    fc = fc.rstrip(";")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + inputs +
                   ["-filter_complex", fc, "-map", f"[{last}]", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium",
                    "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    print("OK", out, round(t, 2), "s")


if __name__ == "__main__":
    main()
