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

# (izvor, x-centar, start ili None=40%, dodatni filter, VRSTA kadra) - najviše 2 kadra iste vrste po klipu (pravilo korisnika:
# bez ponavljanja istih ili sličnih slika); snimci se ne ponavljaju ni između klipova ni sa ranijim serijama (studio/visual_history.json)
EDITS = {
    1: {"word": "PATIENCE", "line": "patience pays.",
        "loop": ("mk_28888", 0.42, 6.0, "eq=gamma=1.35", "sat"),
        "shots": [("mk_64", 0.5, 6.0, "eq=gamma=1.5", "auto-unutra"),
                  ("mk_18296", 0.5, 4.0, "", "novac"),
                  ("mk_4446", 0.45, 5.0, "eq=gamma=1.3", "jahta"),
                  ("mk_231", 0.62, 8.0, "", "čovek-odelo"),
                  ("mk_53", 0.5, 4.0, "", "auto"),
                  ("mk_22739", 0.5, None, "eq=gamma=1.6", "šampanjac"),
                  ("mk_3673", 0.5, 4.0, "eq=gamma=1.3", "sat"),
                  ("mk_4076", 0.62, 5.0, "eq=gamma=1.2", "restoran"),
                  ("mk_43770", 0.62, None, "", "klavir"),
                  ("mk_4067", 0.5, 5.0, "", "tunel"),
                  ("mk_18303", 0.5, 4.0, "", "novac"),
                  ("mk_4087", 0.55, 6.0, "", "grad-noć"),
                  ("mk_51559", 0.50, None, "", "šampanjac"),  # čaša se puni (40502 pretamno, 51549 etiketa sa tekstom)
                  ("mk_4805", 0.5, 5.0, "", "čovek-odelo"),
                  ("mk_4196", 0.5, None, "", "hotel"),
                  ("mk_30016", 0.5, 3.0, "eq=gamma=1.2", "dogovor")],
        "caption": "My mind 24/7 \U0001F9E0\u2694\ufe0f",
        "tags": "#stoicism #discipline #success #mindset #wealthylifestyle",
        "sound": "slowed phonk / dark luxury trap (trending ↗) - udarac na svakih 0.5 s"},
    2: {"word": "HUNGER", "line": "stay hungry.",
        "loop": ("mk_40964", 0.50, 5.0, "eq=gamma=1.2", "boks"),
        "shots": [("mk_4596", 0.42, None, "eq=gamma=1.4", "zavoji"),
                  ("mk_40948", 0.35, None, "", "boks"),
                  ("mk_52084", 0.62, None, "eq=gamma=1.3", "lice"),
                  ("mk_52088", 0.55, None, "eq=gamma=1.3", "sprava"),
                  ("mk_731", 0.62, None, "eq=gamma=1.2", "sopstvena-težina"),
                  ("mk_40276", 0.50, None, "eq=gamma=1.6", "džak"),
                  ("mk_44439", 0.50, None, "", "lice"),
                  ("mk_597", 0.70, None, "", "silueta"),
                  ("mk_735", 0.50, None, "eq=gamma=1.2", "sopstvena-težina"),
                  ("mk_40246", 0.50, None, "eq=gamma=1.6", "skok"),
                  ("mk_52094", 0.43, None, "eq=gamma=1.3", "sprava"),
                  ("mk_608", 0.55, None, "", "trčanje"),
                  ("mk_40275", 0.50, None, "eq=gamma=1.3", "odmor")],
        "caption": "4AM club. No days off. \U0001F94A\U0001F525",
        "tags": "#stoicism #discipline #mindset #gymmotivation #stayhungry",
        "sound": "hard phonk / aggressive drift phonk (trending ↗) - udarac na svakih 0.5 s"},
    3: {"word": "SILENCE", "line": "move in silence.",
        "loop": ("mk_42039", 0.50, 8.0, "eq=gamma=1.5", "auto-noć"),
        "shots": [("mk_2026", 0.50, None, "eq=gamma=1.4", "tunel"),
                  ("mk_42037", 0.45, None, "eq=gamma=1.7", "auto-noć"),
                  ("mk_40746", 0.50, None, "eq=gamma=1.9", "ulica-noć"),
                  ("mk_2709", 0.50, None, "", "vatra"),
                  ("mk_4383", 0.30, None, "eq=gamma=1.3", "most"),
                  ("mk_4431", 0.50, None, "eq=gamma=1.2", "metro"),
                  ("mk_50998", 0.50, None, "eq=gamma=1.6", "grad-odozgo"),
                  ("mk_1724", 0.60, None, "eq=gamma=1.2", "knjiga"),
                  ("mk_4646", 0.50, None, "eq=gamma=1.2", "kanal"),
                  ("mk_42782", 0.50, None, "", "vatra"),  # moderni kamin (32631 odbačen: van fokusa)
                  ("mk_3361", 0.55, None, "", "avion"),
                  ("mk_40672", 0.50, None, "", "metro"),
                  ("mk_41161", 0.55, None, "eq=gamma=1.5", "ulica-noć"),
                  ("mk_42343", 0.50, None, "eq=gamma=1.7", "grad-odozgo"),
                  ("mk_4433", 0.50, None, "", "mesec")],
        "caption": "Let them wonder. \U0001F92B\U0001F303",
        "tags": "#stoicism #discipline #mindset #moveinsilence #nightdrive",
        "sound": "slowed dark phonk / night drive (trending ↗) - udarac na svakih 0.5 s"},
    4: {"word": "FREEDOM", "line": "earn your freedom.",
        "loop": ("mk_2385", 0.50, 10.0, "", "čovek-priroda"),
        "shots": [("mk_44651", 0.45, None, "", "put"),
                  ("mk_39912", 0.55, None, "", "motor"),
                  ("mk_4204", 0.60, None, "", "avion"),
                  ("mk_1076", 0.55, None, "", "gliser"),
                  ("mk_52427", 0.35, None, "", "put"),
                  ("mk_2049", 0.40, None, "", "kormilo"),
                  ("mk_43114", 0.55, None, "", "motor"),
                  ("mk_5008", 0.50, None, "", "more-odozgo"),
                  ("mk_40901", 0.50, None, "", "bicikl"),
                  ("mk_3298", 0.40, None, "", "avion"),
                  ("mk_5363", 0.62, None, "", "more-odozgo"),
                  ("mk_4839", 0.18, None, "", "čovek-priroda"),
                  ("mk_51689", 0.50, None, "", "planina"),
                  ("mk_4281", 0.55, None, "", "planina"),
                  ("mk_38948", 0.50, None, "", "zalazak")],
        "caption": "One day this will be normal. \u2708\ufe0f\U0001F305",
        "tags": "#stoicism #discipline #mindset #freedom #travel",
        "sound": "emotional phonk / cinematic trap (trending ↗) - udarac na svakih 0.5 s"},
    5: {"word": "FOCUS", "line": "no distractions.",
        "loop": ("mk_609", 0.40, 9.0, "", "trčanje"),
        "shots": [("mk_39825", 0.50, None, "", "odbrojavanje"),
                  ("mk_44147", 0.50, None, "", "klavir"),
                  ("mk_40765", 0.45, None, "", "trčanje"),
                  ("mk_50695", 0.60, None, "", "pisanje"),
                  ("mk_41943", 0.62, None, "eq=gamma=1.3", "brzinomer"),
                  ("mk_13807", 0.55, None, "", "knjiga"),
                  ("mk_4827", 0.35, None, "", "tastatura"),
                  ("mk_43798", 0.50, None, "", "meditacija"),
                  ("mk_39779", 0.55, None, "", "sat"),
                  ("mk_43446", 0.50, 11.4, "eq=gamma=1.2", "slikanje"),
                  ("mk_52451", 0.50, None, "", "put"),
                  ("mk_40891", 0.60, None, "", "bicikl"),
                  ("mk_39855", 0.50, None, "eq=gamma=1.3", "pisanje"),
                  ("mk_4852", 0.50, None, "", "put")],
        "caption": "Locked in. \U0001F512\U0001F3AF",
        "tags": "#stoicism #discipline #mindset #focus #productivity",
        "sound": "slowed phonk / dark motivational beat (trending ↗) - udarac na svakih 0.5 s"},
    # ---- v3 (lekcija 22-23): krupna hook rečenica 0-2 s + brzi edit; 2 od 5 sa tipom hook-a "This is why..."
    6: {"hook": "This is why you're always tired.", "word": "ENERGY", "line": "guard it.",
        "loop": ("mk_39786", 0.22, 5.0, "", "krevet"),
        "shots": [("mk_31413", 0.50, None, "eq=gamma=1.7", "telefon"),
                  ("mk_51399", 0.50, None, "eq=gamma=2.0", "krevet"),
                  ("mk_372", 0.28, None, "", "hrana"),
                  ("mk_31412", 0.57, None, "eq=gamma=1.7", "telefon"),
                  ("mk_3533", 0.50, None, "", "hrana"),
                  ("mk_28883", 0.50, None, "eq=gamma=1.5", "sat"),
                  ("mk_50755", 0.35, None, "", "tuš"),
                  ("mk_10342", 0.50, None, "", "voda"),
                  ("mk_4985", 0.21, None, "", "kafa"),
                  ("mk_4851", 0.50, None, "", "hodanje"),
                  ("mk_3572", 0.43, None, "", "kafa"),
                  ("mk_51106", 0.72, None, "", "sunce"),
                  ("mk_2002", 0.50, None, "", "park")],
        "caption": "Your phone is stealing your mornings. What's the first thing you do when you wake up? \U0001F447",
        "tags": "#stoicism #discipline #mindset #morningroutine #energy",
        "sound": "slowed phonk / dark ambient beat (trending ↗) - udarac na svakih 0.5 s"},
    7: {"hook": "This is why you're still broke.", "word": "WEALTH", "line": "build, don't spend.",
        "loop": ("mk_18264", 0.43, 5.0, "", "kartica"),
        "shots": [("mk_42136", 0.50, None, "", "telefon-kupovina"),
                  ("mk_992", 0.43, None, "", "kupovina"),
                  ("mk_42123", 0.72, None, "", "telefon-kupovina"),
                  ("mk_4147", 0.50, None, "", "kupovina"),
                  ("mk_3671", 0.87, None, "eq=gamma=1.5", "odbrojavanje"),
                  ("mk_4893", 0.65, None, "", "hodanje"),
                  ("mk_1439", 0.35, None, "", "plan"),
                  ("mk_4010", 0.50, None, "", "gradnja"),
                  ("mk_4648", 0.14, None, "", "posao"),
                  ("mk_42333", 0.50, None, "", "gradnja"),
                  ("mk_39828", 0.57, None, "", "sat"),
                  ("mk_4997", 0.50, None, "", "nagrada")],
        "caption": "Everyone wants to look rich. Few want to build it. Be honest - spender or builder? \U0001F447",
        "tags": "#stoicism #discipline #mindset #moneymindset #wealth",
        "sound": "dark luxury trap / slowed phonk (trending ↗) - udarac na svakih 0.5 s"},
    8: {"hook": "Stop telling people your plans.", "word": "SECRET", "line": "let results talk.",
        "loop": ("mk_2501", 0.65, 5.0, "", "brava"),
        "shots": [("mk_2514", 0.21, None, "", "kuća"),
                  ("mk_2490", 0.72, None, "eq=gamma=1.3", "ruševina"),
                  ("mk_41043", 0.50, None, "eq=gamma=1.4", "kreda"),
                  ("mk_18312", 0.50, None, "", "voda"),
                  ("mk_43300", 0.79, None, "", "penjanje"),
                  ("mk_1202", 0.50, None, "eq=gamma=1.4", "drvo"),
                  ("mk_87", 0.35, None, "eq=gamma=1.2", "čovek-šuma"),  # 1706 orao odbačen: nestaje na nebu
                  ("mk_43322", 0.50, None, "eq=gamma=1.4", "penjanje"),
                  ("mk_3308", 0.50, None, "eq=gamma=1.3", "planina"),
                  ("mk_51110", 0.50, None, "", "sunce"),
                  ("mk_3335", 0.50, None, "", "vrh"),
                  ("mk_4396", 0.50, None, "", "planina")],
        "caption": "Work in silence. Let the results do the talking. Do you share your goals or keep them quiet? \U0001F447",
        "tags": "#stoicism #discipline #mindset #workinsilence #goals",
        "sound": "slowed dark phonk / mysterious beat (trending ↗) - udarac na svakih 0.5 s"},
    9: {"hook": "The calm ones are the dangerous ones.", "word": "CALM", "line": "stay unshaken.",
        "loop": ("mk_5002", 0.50, 6.0, "", "jezero"),
        "shots": [("mk_4149", 0.50, None, "", "pustinja"),
                  ("mk_51506", 0.50, None, "eq=gamma=1.3", "talasi"),
                  ("mk_41864", 0.50, None, "eq=gamma=1.5", "čaj"),
                  ("mk_4285", 0.43, None, "", "pustinja"),
                  ("mk_3352", 0.50, None, "eq=gamma=1.4", "sneg"),
                  ("mk_34363", 0.50, None, "", "more"),
                  ("mk_1954", 0.50, None, "", "talasi"),
                  ("mk_3317", 0.43, None, "", "sneg"),
                  ("mk_43605", 0.0, None, "", "reka"),  # levo: drveće + voda (sredina je prazna voda)
                  ("mk_51104", 0.50, None, "", "šuma"),
                  ("mk_4048", 0.50, None, "", "nebo"),
                  ("mk_5030", 0.50, None, "", "jezero")],
        "caption": "Loud people react. Calm people respond. Which one are you? \U0001F447",
        "tags": "#stoicism #discipline #mindset #calm #selfcontrol",
        "sound": "deep ambient / slowed cinematic phonk (trending ↗) - udarac na svakih 0.5 s"},
    10: {"hook": "Read this before you quit.", "word": "ENDURE", "line": "quit later. not today.",
        "loop": ("mk_50922", 0.14, 8.0, "eq=gamma=1.3", "zid-penjanje"),
        "shots": [("mk_4755", 0.50, None, "", "povreda"),
                  ("mk_41054", 0.57, None, "", "penjanje"),
                  ("mk_44621", 0.35, None, "", "pustinja"),
                  ("mk_50925", 0.35, None, "", "zid-penjanje"),
                  ("mk_26110", 0.50, None, "", "patike"),
                  ("mk_43298", 0.50, None, "", "penjanje"),
                  ("mk_345", 0.50, None, "", "ravnoteža"),
                  ("mk_50199", 0.50, None, "", "pustinja"),
                  ("mk_41091", 0.65, None, "", "zid-trening"),
                  ("mk_51793", 0.50, None, "", "pustinja-odozgo"),
                  ("mk_41045", 0.50, None, "", "stena"),
                  ("mk_3371", 0.50, None, "", "sneg-planina"),
                  ("mk_3370", 0.50, None, "", "sneg-planina")],
        "caption": "The hardest part is the part right before it works. Who needs to hear this today? \U0001F447",
        "tags": "#stoicism #discipline #mindset #neverquit #resilience",
        "sound": "emotional phonk / epic slowed beat (trending ↗) - udarac na svakih 0.5 s"},
}


def check_variety(n):
    """Najviše 2 kadra iste vrste u klipu; nijedan izvor dvaput u klipu ni u dva klipa serije."""
    e = EDITS[n]; from collections import Counter
    kinds = Counter([e["loop"][4]] + [x[4] for x in e["shots"]])
    bad = {k: v for k, v in kinds.items() if v > 2}
    srcs = [x[0] for x in e["shots"]] + [e["loop"][0]]
    other = {x[0] for m, o in EDITS.items() if m != n for x in o["shots"] + [o["loop"]]}
    rep = [x for x in srcs if srcs.count(x) > 1 or x in other]
    assert not bad and not rep, f"edit {n}: previše iste vrste {bad} / ponovljen izvor {rep}"


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
        bt, bb = (cy - 260, cy + 230) if (e.get("hook") and t < 2.0) else (cy - 170, cy + 120)
        g = cairo.LinearGradient(0, bt, 0, bb)
        for st, al in ((0, 0), (0.3, 0.42), (0.7, 0.42), (1, 0)): g.add_color_stop_rgba(st, 0, 0, 0, al)
        c.rectangle(0, bt, W, bb - bt); c.set_source(g); c.fill()
        hook = e.get("hook")  # v3 (lekcija 22): krupna hook rečenica 0-2 s, čita se i na sličici profila
        if hook and t < 2.0:
            M.face(c, 84, cairo.FONT_WEIGHT_BOLD)
            words = hook.split(); lines = M.wrap(c, words, M.MAXW)
            if len(lines) > 2: lines = M.balance3(c, words, M.MAXW)
            lh = 84 * 1.18
            for li, ln in enumerate(lines):
                s_ = " ".join(ln); tw = c.text_extents(s_).x_advance; x = M.CX - tw / 2
                y = cy + (li - (len(lines) - 1) / 2) * lh + 30
                M.BOXES.append((x, y - 70, x + tw, y + 20))
                M.shadow_text(c, x, y, s_, 1.0)
        elif t < split:
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
    check_variety(n)
    lname, lx, a, lex = e["loop"][:4]
    full = os.path.join(M.TMP, f"e{n}_loop.mp4")
    M.render_shot(full, lname, a - BEAT, 2 * BEAT, lx, 1.00, 1.04, lex)
    head, tail = os.path.join(M.TMP, f"e{n}_head.mp4"), os.path.join(M.TMP, f"e{n}_tail.mp4")
    M.cut(full, head, BEAT, BEAT); M.cut(full, tail, 0.0, BEAT)
    parts = [head]
    for k, (nm, xc, st, ex, _kind) in enumerate(shots, 1):
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
