"""STOIC EDIT — "edit" format po uzoru na velike motivacione naloge (analiza reference 19.11.):
brzi rezovi na svaki udarac (0.5 s @120 BPM), tamni noćni luksuz/snaga, MINIMALAN tekst:
proređena reč (hook) pa jedan kratak red malim slovima. Bez zvuka (korisnik dodaje trending zvuk).
Loop: prvi i poslednji kadar su uzastopni delovi istog snimka.
Upotreba: python3 stoic/edit.py 5
"""
import os, sys, json, subprocess
import cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make as M

W, H, FPS, BEAT = M.W, M.H, M.FPS, 0.5

EDITS = {
    5: {"word": "PATIENCE", "line": "patience pays.",
        "loop": ("mk_28888", 0.42, 6.0, "eq=gamma=1.35"),     # čovek u odelu gleda sat
        "shots": [("mk_64", 0.5, 6.0, "eq=gamma=1.5"),         # instrument tabla noću
                  ("mk_18296", 0.5, 4.0, ""),                  # brojanje novčanica
                  ("mk_4446", 0.45, 5.0, "eq=gamma=1.3"),      # jahta noću u luci
                  ("mk_231", 0.62, 8.0, ""),                   # čovek na krovu u sumrak
                  ("mk_53", 0.5, 4.0, ""),                    # sportski auto, sunce na haubi (63 odbačen: samo crvena površina)
                  ("mk_18304", 0.5, 5.0, ""),                  # prelistavanje dolara
                  ("mk_3673", 0.5, 4.0, "eq=gamma=1.3"),       # mehanizam sata
                  ("mk_4076", 0.62, 5.0, "eq=gamma=1.2"),      # restoran nad gradom noću
                  ("mk_4805", 0.5, 5.0, ""),                   # poslovni čovek u odelu (151 odbačen: sivo bez detalja)
                  ("mk_4067", 0.5, 5.0, ""),                   # noćni tunel (65 odbačen: tamna mrlja)
                  ("mk_18303", 0.5, 4.0, ""),                  # novac gori
                  ("mk_4087", 0.55, 6.0, ""),                  # grad noću
                  ("mk_30016", 0.5, 3.0, "eq=gamma=1.2"),     # stisak ruke u odelu (49 odbačen: bela mrlja)
                  ("px_6700180", 0.5, 6.0, "eq=gamma=1.4"),    # čovek u privatnom avionu
                  ("mk_18249", 0.5, 4.0, ""),                  # novčanice od 100$
                  ("px_30351567", 0.5, 6.0, "")],              # jahta u zalasku
        "caption": "My mind 24/7 \U0001F9E0⚔️",
        "tags": "#stoicism #discipline #success #mindset #wealthylifestyle",
        "sound": "slowed phonk / dark luxury trap (trending ↗) - udarac na svakih 0.5 s"},
}


def overlay(e, n, total, path):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "qtrle", path], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    split = 4.0  # proređena reč 0-4 s (hook), red 4 s - kraj
    for f in range(int(round(total * FPS))):
        t = f / FPS
        c = cairo.Context(s); c.set_operator(cairo.OPERATOR_CLEAR); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
        cy = H * 0.44
        if t < split:
            M.face(c, 54, cairo.FONT_WEIGHT_NORMAL)
            letters = list(e["word"]); gap = 34
            ws = [c.text_extents(L).x_advance for L in letters]; tw = sum(ws) + gap * (len(ws) - 1)
            x = M.CX - tw / 2
            M.BOXES.append((x, cy - 50, x + tw, cy + 12))
            for L, w_ in zip(letters, ws):
                M.shadow_text(c, x, cy, L, 1.0); x += w_ + gap
        else:
            a = min(1.0, (t - split) / 0.12)
            M.face(c, 62, cairo.FONT_WEIGHT_BOLD)
            s_ = e["line"]; tw = c.text_extents(s_).x_advance; x = M.CX - tw / 2
            M.BOXES.append((x, cy - 55, x + tw, cy + 15))
            M.shadow_text(c, x, cy, s_, a)
        M.face(c, 34, cairo.FONT_WEIGHT_BOLD); tag = f"STOIC RULE #{n}"
        c.move_to(64, 262); c.set_source_rgba(0, 0, 0, 0.5); c.show_text(tag)
        c.move_to(62, 260); c.set_source_rgba(1, 1, 1, 0.82); c.show_text(tag)
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()


def make(n):
    e = EDITS[n]; M.BOXES.clear()
    shots = e["shots"]; total = BEAT * (len(shots) + 2)
    lname, lx, a, lex = e["loop"]
    full = os.path.join(M.TMP, f"e{n}_loop.mp4")
    M.render_shot(full, lname, a - BEAT, 2 * BEAT, lx, 1.00, 1.04, lex)
    head, tail = os.path.join(M.TMP, f"e{n}_head.mp4"), os.path.join(M.TMP, f"e{n}_tail.mp4")
    M.cut(full, head, BEAT, BEAT); M.cut(full, tail, 0.0, BEAT)
    parts = [head]
    for k, (nm, xc, st, ex) in enumerate(shots, 1):
        o = os.path.join(M.TMP, f"e{n}_{k:02d}.mp4")
        M.render_shot(o, nm, st, BEAT, xc, 1.00, 1.04, ex); parts.append(o)
    parts.append(tail)
    lst = os.path.join(M.TMP, f"e{n}_list.txt"); open(lst, "w").write("".join(f"file '{q}'\n" for q in parts))
    base = os.path.join(M.TMP, f"e{n}_base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], check=True)
    ov = os.path.join(M.TMP, f"e{n}_ov.mov"); overlay(e, n, total, ov)
    out = os.path.join(M.OUT, f"stoic_edit_{n:02d}.mp4"); part = out.replace(".mp4", ".part.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov, "-filter_complex",
                    "[0:v][1:v]overlay=format=auto,noise=alls=7:allf=t,format=yuv420p[v]", "-map", "[v]", "-an",
                    "-tune", "grain", "-maxrate", "22M", "-bufsize", "44M", "-t", f"{total}", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", part], check=True)
    os.replace(part, out)
    open(out.replace(".mp4", "_opis.txt"), "w").write(f"{e['caption']}\n\n{e['tags']}\n\nZvuk (dodaješ u TikTok-u): {e['sound']}\n")
    safe = all(x0 >= 0 and y0 >= 0 and x1 <= M.SAFE_R and y1 <= M.SAFE_B for x0, y0, x1, y1 in M.BOXES)
    print(out, total, "s", len(parts), "kadrova, tekst u sigurnoj zoni:", safe)


if __name__ == "__main__":
    for x in sys.argv[1:] or ["5"]:
        make(int(x))
