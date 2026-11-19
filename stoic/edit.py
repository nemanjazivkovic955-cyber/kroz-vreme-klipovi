"""STOIC EDIT — "edit" format po uzoru na velike motivacione naloge (analiza reference 19.11.):
brzi rezovi na svaki udarac (0.5 s @120 BPM), tamni noćni luksuz/snaga, MINIMALAN tekst:
proređena reč (hook) pa jedan kratak red malim slovima. Bez zvuka (korisnik dodaje trending zvuk).
Loop: prvi i poslednji kadar su uzastopni delovi istog snimka.
Upotreba: python3 stoic/edit.py [1 2 3 4 5]\nBez natpisa u uglu (odluka korisnika 19.11.).
"""
import os, sys, json, subprocess
import cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make as M

W, H, FPS, BEAT = M.W, M.H, M.FPS, 0.5

EDITS = {
    1: {"word": "PATIENCE", "line": "patience pays.",
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
    2: {"word": "HUNGER", "line": "stay hungry.",
        "loop": ("mk_40964", 0.50, 5.0, "eq=gamma=1.2"),      # bokser pognute glave u uglu ringa
        "shots": [("mk_4596", 0.42, None, "eq=gamma=1.4"),     # zavija ruke
                  ("mk_40948", 0.35, None, ""),                # bokser u gardu
                  ("mk_52084", 0.62, None, "eq=gamma=1.3"),    # fokusiran pogled
                  ("mk_52088", 0.55, None, "eq=gamma=1.3"),    # konopci
                  ("mk_40276", 0.50, None, "eq=gamma=1.6"),    # udarci u džak (vertikalno)
                  ("mk_40988", 0.45, None, ""),                # iscrpljen borac (50979 odbačen: skriveni rez u izvoru)
                  ("mk_52094", 0.43, None, "eq=gamma=1.3"),    # teška šipka
                  ("mk_731", 0.62, None, "eq=gamma=1.2"),      # sklekovi
                  ("mk_44439", 0.50, None, ""),                # znojavo lice
                  ("mk_735", 0.50, None, "eq=gamma=1.2"),      # zgibovi
                  ("mk_40971", 0.50, None, "eq=gamma=1.4"),    # mladi bokser (vertikalno)
                  ("mk_597", 0.70, None, ""),                  # silueta pije vodu
                  ("mk_40788", 0.50, None, "eq=gamma=1.6"),    # bučica (vertikalno)
                  ("mk_608", 0.55, None, ""),                  # silueta trkača u gradu
                  ("mk_40978", 0.45, None, "")],               # iscrpljena borkinja
        "caption": "4AM club. No days off. \U0001F94A\U0001F525",
        "tags": "#stoicism #discipline #mindset #gymmotivation #stayhungry",
        "sound": "hard phonk / aggressive drift phonk (trending ↗) - udarac na svakih 0.5 s"},
    3: {"word": "SILENCE", "line": "move in silence.",
        "loop": ("mk_42039", 0.50, 8.0, "eq=gamma=1.5"),                  # pogled iz auta, noćni saobraćaj
        "shots": [("mk_2026", 0.50, None, "eq=gamma=1.4"),     # mračan tunel
                  ("mk_42037", 0.45, None, "eq=gamma=1.7"),                # prozor auta, svetla
                  ("mk_40746", 0.50, None, "eq=gamma=1.9"),    # noćna šetnja (vertikalno)
                  ("mk_4383", 0.30, None, "eq=gamma=1.3"),     # most noću
                  ("mk_49876", 0.50, None, "eq=gamma=2.0"),    # avenija odozgo (vertikalno)
                  ("mk_50998", 0.50, None, "eq=gamma=1.6"),                # kružni tok noću
                  ("mk_40640", 0.50, None, "eq=gamma=1.8"),    # grad noću
                  ("mk_42343", 0.50, None, "eq=gamma=1.7"),    # grad noću iz vazduha (4136 odbačen: treperenje svetala u tunelu)
                  ("mk_34562", 0.50, None, "eq=gamma=1.9"),    # dve avenije (vertikalno)
                  ("mk_49846", 0.45, None, "eq=gamma=1.3"),    # grad iz vazduha
                  ("mk_3361", 0.55, None, ""),                 # krilo aviona nad gradom
                  ("mk_41161", 0.55, None, "eq=gamma=1.5"),    # avenija noću
                  ("mk_4646", 0.50, None, "eq=gamma=1.2"),     # kanal noću
                  ("mk_49878", 0.50, None, "eq=gamma=2.0"),    # grad noću (vertikalno)
                  ("mk_4433", 0.50, None, "")],                # pun mesec
        "caption": "Let them wonder. \U0001F92B\U0001F303",
        "tags": "#stoicism #discipline #mindset #moveinsilence #nightdrive",
        "sound": "slowed dark phonk / night drive (trending ↗) - udarac na svakih 0.5 s"},
    4: {"word": "FREEDOM", "line": "earn your freedom.",
        "loop": ("mk_2385", 0.50, 10.0, ""),                  # čovek raširenih ruku na vrhu
        "shots": [("mk_44651", 0.45, None, ""),                # put, POV
                  ("mk_39912", 0.55, None, ""),                # motor na praznom putu
                  ("mk_4204", 0.60, None, ""),                 # krilo aviona, ružičasto nebo
                  ("mk_52427", 0.35, None, ""),                # sportski auto na krivini
                  ("mk_2049", 0.40, None, ""),                 # ruka na kormilu čamca
                  ("mk_43114", 0.55, None, ""),                # motor kroz pustinju
                  ("mk_5008", 0.50, None, ""),                 # tirkizni zaliv odozgo (40102 odbačen: treći kadar krila aviona)
                  ("mk_52454", 0.55, None, ""),                # vozač, sunce na putu
                  ("mk_5363", 0.62, None, ""),                 # gliser iz vazduha
                  ("mk_3298", 0.40, None, ""),                 # poletanje
                  ("mk_41545", 0.50, None, ""),                # planine iz vazduha (44370 odbačen: drugi zalazak nad morem)
                  ("mk_4839", 0.18, None, ""),                 # čovek i pas gledaju zalazak
                  ("mk_51689", 0.50, None, ""),                # snežni vrh
                  ("mk_4281", 0.55, None, ""),                 # planina pod zvezdama
                  ("mk_38948", 0.50, None, "")],               # sunce nad morem
        "caption": "One day this will be normal. \u2708\ufe0f\U0001F305",
        "tags": "#stoicism #discipline #mindset #freedom #travel",
        "sound": "emotional phonk / cinematic trap (trending ↗) - udarac na svakih 0.5 s"},
    5: {"word": "FOCUS", "line": "no distractions.",
        "loop": ("mk_609", 0.40, 9.0, ""),                    # noge trkača na stazi
        "shots": [("mk_32809", 0.50, None, ""),                # trkač prolazi (vertikalno)
                  ("mk_40765", 0.45, None, ""),                # koraci, crno-belo
                  ("mk_39825", 0.50, None, ""),                # semafor odbrojava do nule
                  ("mk_40766", 0.50, None, ""),                # trkač na mostu
                  ("mk_41943", 0.62, None, "eq=gamma=1.3"),    # brzinomer
                  ("mk_722", 0.50, None, ""),                  # trkač u šumi
                  ("mk_4827", 0.35, None, ""),                 # ruke na tastaturi
                  ("mk_32792", 0.50, None, ""),                # sprint (vertikalno)
                  ("mk_39779", 0.55, None, ""),                # pogled na sat
                  ("mk_606", 0.45, None, ""),                  # trkač na mostu, grad
                  ("mk_52451", 0.50, None, ""),                # prazan put u zoru
                  ("mk_32799", 0.50, None, ""),                # trkač na stazi
                  ("mk_4852", 0.50, None, ""),                 # put kroz drveće
                  ("mk_719", 0.50, None, ""),                  # trkač na stazi u parku
                  ("mk_52452", 0.50, None, "")],               # put u zoru
        "caption": "Locked in. \U0001F512\U0001F3AF",
        "tags": "#stoicism #discipline #mindset #focus #runningmotivation",
        "sound": "slowed phonk / dark motivational beat (trending ↗) - udarac na svakih 0.5 s"},
}


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def overlay(e, n, total, path):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "qtrle", path], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    split = 4.0  # proređena reč 0-4 s (hook), red 4 s - kraj
    for f in range(int(round(total * FPS))):
        t = f / FPS
        c = cairo.Context(s); c.set_operator(cairo.OPERATOR_CLEAR); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
        cy = H * 0.44
        # blaga tamna traka iza teksta - čitljivost na svetlim kadrovima (nebo, staza)
        g = cairo.LinearGradient(0, cy - 170, 0, cy + 120)
        for st, al in ((0, 0), (0.4, 0.38), (0.6, 0.38), (1, 0)): g.add_color_stop_rgba(st, 0, 0, 0, al)
        c.rectangle(0, cy - 170, W, 290); c.set_source(g); c.fill()
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
        if st is None: st = round(dur(M.src(nm)) * 0.4, 2)
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
    for x in sys.argv[1:] or [str(k) for k in EDITS]:
        make(int(x))
