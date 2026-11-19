"""Gradi CREATIVE PRODUCTION DATABASE iz svih izvora produkcija u repou.
Izlaz: studio/production_db.json (sve produkcije) i studio/visual_history.json (snimak -> gde je korišćen).
Ručne ocene/lekcije se čitaju iz studio/evaluations.json (po id-u ili po "family").
Upotreba: python3 studio/db.py
"""
import os, sys, json, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path[:0] = [os.path.join(ROOT, "motivacija"), os.path.join(ROOT, "the_price")]
OUT = os.path.join(ROOT, "studio")


def clean(s): return s.replace("*", "")


def fid(x):  # normalizuj identitet snimka
    x = x.split(":")[-1]
    x = os.path.splitext(os.path.basename(x))[0]
    x = x[2:] if x.startswith("p_") else x
    import re as _re
    m = _re.match(r"^(?:px|money|power_flight|power_jet|power_man|power_phone|lux_woman|car|city|nature|travel|workout|snow)_(\d+)$", x)
    return f"pexels_{m.group(1)}" if m else x


prods = []


def add(**k):
    k.setdefault("footage", []); k["footage"] = [fid(f) for f in k["footage"]]
    prods.append(k)


# 1) Quote of the Day (v1 bez lekcije, v2 sa lekcijom) + mozaik
try:
    from quotes import QUOTES
    for k, q in QUOTES.items():
        fam = "rich_life_mosaic" if k.startswith("rl") else ("quote_v2" if q.get("lesson") else "quote_v1")
        add(id=k, family=fam, format="TikTok 9:16 ~27 s", topic=q.get("category", "general"),
            hook=clean(q["lines"][0]), text=[clean(x) for x in q["lines"]] + ([clean(q["lesson"])] if q.get("lesson") else []),
            ending=clean(q.get("lesson") or q["lines"][-1]), footage=[q["broll"]],
            visual_style="stok pozadina + tekst preko (QOTD kartica)" if fam != "quote_v1" else "stok pozadina + beli/zlatni tekst",
            music="cinematic_piano (bez muzike verzija za TikTok)", editing="statičan tekst po rečenici, fade",
            output=f"videos/{q.get('outdir', 'motivacija')}/{k}.mp4")
except Exception as e:
    print("quotes:", e)

# 2) TikTok loop klipovi
try:
    import shortloop
    for k, v in shortloop.LOOPS.items():
        shots = v.get("shots") or []
        add(id=f"loop_{k}", family="tiktok_loop_v1", format="TikTok 9:16 12 s loop, bez zvuka",
            topic=v.get("caption", ""), hook=clean(v["texts"][0]), text=[clean(t) for t in v["texts"]],
            ending=clean(v["texts"][-1]), footage=[v["loop_src"]] + shots,
            visual_style="hladan kolor, punch-in, 12 rezova po 1 s" + (" (svi iz ISTOG snimka)" if not shots else ""),
            music="nema (korisnik dodaje)", editing="tekst na 4 udarca, rez na 2 udarca @120 BPM, loop isti snimak",
            output=f"videos/tiktok_loops/{k if k.startswith('m') else 'loop_' + k}.mp4")
except Exception as e:
    print("loops:", e)

# 2b) TikTok loop v2 (svaka rečenica svoj kadar)
try:
    from tiktok_loops_v2 import LOOPS_V2
    for k, v in LOOPS_V2.items():
        fs = [v["loop"][0]] + [s[0] for sl in v["shots"] if sl for s in sl]
        add(id=k, family="tiktok_loop_v2", format="TikTok 9:16 12 s loop, bez zvuka", topic=v["caption"],
            hook=clean(v["texts"][0]), text=[clean(t) for t in v["texts"]], ending=clean(v["texts"][-1]), footage=fs,
            visual_style="paleta po kadru, auto-ekspozicija, kadar po rečenici", music="nema (korisnik dodaje)",
            editing="2 s po tekstu, 2 reza po 1 s na vrhuncu, kontinualan loop spoj", output=f"videos/tiktok_loops/{k}.mp4")
except Exception as e:
    print("loops_v2:", e)

# 3) Inspirativni govori
try:
    import talks
    for k, v in talks.TALKS.items():
        add(id=f"talk_{k}", family="talk_v1", format="TikTok 9:16 ~30 s, glas + muzika", topic=v["title"],
            hook=v["script"][0][0], text=[s for s, _ in v["script"]], ending=v["script"][-1][0], footage=v["shots"],
            visual_style="filmski kolor teal/zlato, meki prelazi, elegantni serif titlovi",
            music=v["music"], editing="xfade 0.7 s, push-in 6%", output=f"videos/the_price/talk_{k}_9x16.mp4")
    import water
    add(id="talk_water", family="talk_v1", format="TikTok 9:16 69 s, glas + muzika", topic="BE LIKE WATER",
        hook=water.TALK["segments"][0][2], text=[s[2] for s in water.TALK["segments"]], ending=water.TALK["segments"][-1][2],
        footage=[n for n, _ in water.SHOTS], visual_style="vodopadi, filmski kolor", music="mixkit_871",
        editing="xfade 0.7 s", output="videos/the_price/be_like_water_9x16.mp4")
except Exception as e:
    print("talks:", e)

# 4) THE PRICE
try:
    import produce
    for k, ep in produce.EPISODES.items():
        add(id=f"price_{k}", family="the_price", format="16:9 + 9:16 54 s", topic="cena uspeha",
            hook=ep["captions"][0][2].replace("*", ""), text=[c[2].replace("*", "") for c in ep["captions"]],
            ending=ep["captions"][-1][2].replace("*", ""), footage=[s[0] for s in ep["shots"]],
            visual_style="letterbox, hladno (muka) -> toplo (nagrada), zrno", music="sintetisani dark trap + SFX",
            editing="rezovi 2.0/2.6 s, riser + impact na preokretu", output=f"videos/the_price/{k}_the_price_16x9.mp4")
except Exception as e:
    print("price:", e)

# 5) YouTube kompilacije
try:
    import made_it
    add(id="yt_i_made_it", family="youtube_comp", format="YouTube 16:9 2:22", topic="I made it",
        hook=made_it.STORY[0][1].replace("*", ""), text=[t.replace("*", "") for _, t in made_it.STORY],
        ending=made_it.STORY[-1][1].replace("*", ""), footage=[f"made_it_16x9/{n}" for n, _ in made_it.STORY],
        visual_style="Mixkit lux, tekst donja trećina", music="cinematic_piano", editing="tvrdi rezovi 4 s",
        output="videos/youtube/i_made_it_youtube.mp4")
    import assemble_youtube as A
    add(id="yt_rich_life", family="youtube_comp", format="YouTube 16:9 1:54", topic="rich life",
        hook="RICH LIFE (kartica)", text=[], ending="SUBSCRIBE", footage=[f"rich_edit_16x9/{n}" for n in A.ORDER],
        visual_style="Pexels lux", music="cinematic_piano", editing="tvrdi rezovi 4 s", output="videos/youtube/rich_life_youtube.mp4")
except Exception as e:
    print("youtube:", e)

# 5b) Shorts "rich edit" (42 kratka klipa bez teksta) - snimci iz kataloga; ranije NIJE praćeno -> lažno "neiskorišćeno"
try:
    import ast
    src = open(os.path.join(ROOT, "motivacija", "cut_edit.py")).read()
    G = next(ast.literal_eval(n.value) for n in ast.parse(src).body
             if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "GROUPS")
    add(id="shorts_rich_edit", family="shorts_rich_edit", format="kratki isečci bez teksta (sync to beat)", topic="rich life",
        hook="-", text=[], ending="-", footage=[f for v in G.values() for f in v], visual_style="luksuz, topli zlatni kolor",
        music="nema", editing="isečci po 4 s", output="videos/shorts/rich_edit/")
except Exception as e:
    print("rich_edit:", e)

# 6) Stoic Rules serija
try:
    sys.path.insert(0, os.path.join(ROOT, "stoic"))
    from rules import RULES
    for n, r in RULES.items():
        add(id=f"stoic_rule_{n:02d}", family="stoic_rules", format="TikTok 9:16 10 s loop, bez zvuka", topic=r["theme"],
            hook=r["hook"], text=[r["hook"]] + r["rule"], ending=f"Follow for rule #{n + 1}",
            footage=[r["loop"][0]] + [s_[0] for s_ in r["shots"]], visual_style="tamno-hladni filmski, zrno, beli Poppins Bold",
            music="nema (korisnik dodaje)", editing="2/2.5/2.5/2/1 s, reči na 1/8 @120 BPM", output=f"videos/stoic/stoic_rule_{n:02d}.mp4")
    import edit as E_
    for n, e in E_.EDITS.items():
        add(id=f"stoic_edit_{n:02d}", family="stoic_edit", format="TikTok 9:16 9 s edit, bez zvuka", topic=e["word"].lower(),
            hook=" ".join(e["word"]), text=[" ".join(e["word"]), e["line"]], ending=e["line"],
            footage=[e["loop"][0]] + [x[0] for x in e["shots"]], visual_style="noćni luksuz, rez na svaki udarac",
            music="nema (korisnik dodaje)", editing="18 x 0.5 s @120 BPM", output=f"videos/stoic/stoic_edit_{n:02d}.mp4")
except Exception as e:
    print("stoic:", e)

# ocene
ev_path = os.path.join(OUT, "evaluations.json")
ev = json.load(open(ev_path)) if os.path.exists(ev_path) else {}
for p in prods:
    e = ev.get(p["id"]) or ev.get(p["family"])
    if e: p["evaluation"] = e
    ip = os.path.join(OUT, "inspections", f"{p['id']}.json")
    if os.path.exists(ip):  # izveštaj inspekcije STVARNOG rendera
        r = json.load(open(ip))
        p["inspection"] = {"report": f"studio/inspections/{p['id']}.md", "inspected_at": r["inspected_at"], "approval": r["approval"],
                           "issues": len(r["issues"]), "cuts": r["cuts"], "loop_seam": r.get("loop_seam")}

# vizuelna istorija
vh = {}
for p in prods:
    for f in dict.fromkeys(p["footage"]):
        vh.setdefault(f, []).append(p["id"])
json.dump(prods, open(os.path.join(OUT, "production_db.json"), "w"), indent=1, ensure_ascii=False)
json.dump(dict(sorted(vh.items(), key=lambda x: -len(x[1]))), open(os.path.join(OUT, "visual_history.json"), "w"),
          indent=1, ensure_ascii=False)
reused = {k: v for k, v in vh.items() if len(v) > 1}
print(f"{len(prods)} produkcija, {len(vh)} snimaka, {len(reused)} snimaka korišćeno više puta")
for k, v in list(sorted(reused.items(), key=lambda x: -len(x[1])))[:12]:
    print(f"  {k}: {len(v)}x -> {', '.join(v[:6])}{'…' if len(v) > 6 else ''}")
