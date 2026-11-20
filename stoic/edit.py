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
    # ---- v4 ŽIVI (zahtev korisnika: promena slika, teme i 'malo življe') - topliji kolor, udarac zumom, završni burst 0.25 s
    11: {"style": "live", "hook": "This is why you can't stay consistent.", "word": "HABITS", "line": "small wins. daily.",
        "loop": ("mk_44448", 0.5, 3.0, "", "košarka"),
        "shots": [
("mk_42541", 0.5, None, "", "fudbal"),
                  ("mk_725", 0.5, None, "", "vijača"),
                  ("mk_43776", 0.5, None, "", "klavir"),  # 483 gitara odbačena: bljesak scenskog svetla
                  ("mk_3168", 0.55, None, "", "plivanje"),
                  ("mk_873", 0.62, None, "", "tenis"),
                  ("mk_591", 0.4, None, "", "atletika"),
                  ("mk_472", 0.5, None, "", "bubnjevi"),
                  ("mk_52316", 0.5, None, "eq=gamma=1.3", "teretana"),
                  ("mk_3171", 0.5, None, "", "plivanje"),
                  ("mk_759", 0.5, None, "", "teretana"),
                  ("mk_2273", 0.55, None, "", "košarka", 0.25),
                  ("mk_43494", 0.55, None, "", "fudbal", 0.25),
                  ("mk_878", 0.4, None, "", "tenis", 0.25),
                  ("mk_1367", 0.5, None, "", "skejt", 0.25),],
        "caption": "Motivation starts it. Habits finish it. What's one small habit you never skip? \U0001F447",
        "tags": "#stoicism #discipline #mindset #habits #consistency",
        "sound": "upbeat phonk / energetic trap (trending ↗) - udarac na 0.5 s, završnica na 0.25 s"},
    12: {"style": "live", "hook": "Your comfort is your cage.", "word": "GROWTH", "line": "get uncomfortable.",
        "loop": ("mk_41010", 0.3, 4.5, "", "salto"),
        "shots": [
("mk_3373", 0.5, None, "", "sneg"),
                  ("mk_1276", 0.5, None, "", "skok-voda"),
                  ("mk_3378", 0.55, None, "", "sneg"),
                  ("mk_3362", 0.62, None, "", "vrh"),
                  ("mk_2186", 0.6, None, "", "vodopad"),
                  ("mk_40742", 0.5, None, "eq=gamma=1.2", "veslanje"),
                  ("mk_4016", 0.5, None, "", "ski"),
                  ("mk_52497", 0.5, None, "", "skok-voda"),
                  ("mk_50244", 0.5, None, "", "veslanje"),
                  ("mk_3340", 0.6, None, "", "ski"),
                  ("mk_4568", 0.55, None, "", "skejt", 0.25),
                  ("mk_25542", 0.5, None, "", "vodopad", 0.25),
                  ("mk_1366", 0.62, None, "", "skejt", 0.25),
                  ("mk_3333", 0.65, None, "", "vrh", 0.25),],
        "caption": "Growth lives right outside what feels safe. What's one thing you've been avoiding? \U0001F447",
        "tags": "#stoicism #discipline #mindset #growth #selfimprovement",
        "sound": "epic phonk / adrenaline beat (trending ↗) - udarac na 0.5 s, završnica na 0.25 s"},
    13: {"style": "live", "hook": "Watch who claps when you win.", "word": "CIRCLE", "line": "choose your people.",
        "loop": ("mk_40147", 0.25, 8.0, "", "daj-pet"),
        "shots": [
("mk_44469", 0.5, None, "", "košarka"),
                  ("mk_3621", 0.55, None, "", "ples"),
                  ("mk_43486", 0.3, None, "eq=gamma=1.3", "fudbal"),
                  ("mk_4185", 0.5, None, "", "publika"),
                  ("mk_1375", 0.5, None, "", "skejt"),
                  ("mk_51296", 0.5, None, "eq=gamma=1.2", "ples"),
                  ("mk_4155", 0.5, None, "", "vatromet"),
                  ("mk_44464", 0.5, None, "", "košarka"),
                  ("mk_46874", 0.45, None, "", "žurka"),
                  ("mk_4344", 0.5, None, "", "žurka-klub"),
                  ("mk_341", 0.5, None, "", "ruke-gore", 0.25),
                  ("mk_4151", 0.5, None, "", "vatromet", 0.25),
                  ("mk_51540", 0.75, None, "eq=gamma=1.3", "slavlje", 0.25),  # 43499 odbačen: reklamni natpis sponzora
                  ("mk_4401", 0.5, None, "", "gužva", 0.25),],
        "caption": "Real ones celebrate you loudly. Who was first to clap for your last win? \U0001F447",
        "tags": "#stoicism #discipline #mindset #friendship #loyalty",
        "sound": "feel-good phonk / hype beat (trending ↗) - udarac na 0.5 s, završnica na 0.25 s"},
    14: {"style": "live", "hook": "Nobody owes you anything.", "word": "EARN", "line": "go get it.",
        "loop": ("mk_2285", 0.5, 5.0, "", "košarka"),
        "shots": [
("mk_43484", 0.45, None, "", "fudbal"),
                  ("mk_877", 0.5, None, "", "tenis"),
                  ("mk_3338", 0.5, None, "", "ski"),
                  ("mk_3624", 0.45, None, "", "ples"),
                  ("mk_2923", 0.5, None, "", "fudbal"),
                  ("mk_869", 0.5, None, "", "tenis"),
                  ("mk_4437", 0.6, None, "", "ulica"),
                  ("mk_3356", 0.4, None, "", "ski"),
                  ("mk_4152", 0.5, None, "", "vatromet"),
                  ("mk_50243", 0.5, None, "", "veslanje"),
                  ("mk_3628", 0.5, None, "", "ples", 0.25),
                  ("mk_2275", 0.5, None, "", "košarka", 0.25),
                  ("mk_583", 0.45, None, "", "zagrevanje", 0.25),
                  ("mk_4156", 0.5, None, "", "vatromet", 0.25),],
        "caption": "Nobody is handing it to you. Earn it. What are you going after this year? \U0001F447",
        "tags": "#stoicism #discipline #mindset #hustle #goals",
        "sound": "hard phonk / hype trap (trending ↗) - udarac na 0.5 s, završnica na 0.25 s"},
    15: {"style": "live", "hook": "Busy is not the same as focused.", "word": "PURPOSE", "line": "pick one direction.",
        "loop": ("mk_421", 0.45, 9.0, "", "dim"),
        "shots": [
("mk_4180", 0.5, None, "", "stanica"),
                  ("mk_683", 0.5, None, "", "iskre"),
                  ("mk_4390", 0.5, None, "eq=gamma=1.2", "stanica"),
                  ("mk_349", 0.5, None, "", "hodnik"),
                  ("mk_677", 0.5, None, "", "prah"),
                  ("mk_4026", 0.5, None, "", "scena"),
                  ("mk_4244", 0.5, None, "", "vatromet"),
                  ("mk_478", 0.5, None, "", "pevačica"),
                  ("mk_4154", 0.5, None, "", "pokretne-stepenice"),
                  ("mk_3619", 0.55, None, "", "ples"),
                  ("mk_4064", 0.5, None, "", "vatromet", 0.25),
                  ("mk_42742", 0.5, None, "", "igra", 0.25),
                  ("mk_3622", 0.5, None, "", "ples", 0.25),
                  ("mk_52507", 0.5, None, "", "voda-igra", 0.25),],
        "caption": "Doing a lot is not the same as doing what matters. What's your ONE thing right now? \U0001F447",
        "tags": "#stoicism #discipline #mindset #focus #purpose",
        "sound": "dark-to-hype phonk / beat drop (trending ↗) - udarac na 0.5 s, završnica na 0.25 s"},
    # ---- v5 PRIČA (zaključan koncept 19.11.): jedan junak, problem -> okret -> rezultat; slika = rečenica
    16: {"mode": "story", "hook": "Everyone gets knocked down.", "word": "RISE", "line": "get back up.",
        "loop": ("mk_40962", 0.43, 3.5, "eq=gamma=1.2", "boks-meč"),          # krvav bokser sedi u uglu
        "shots": [("mk_40969", 0.28, 1.6, "", "boks-meč", 1.0),                # udarac u lice (pad)
                  ("mk_40961", 0.50, 2.0, "", "boks-meč", 0.5),                # protivnik misli da je gotovo
                  ("mk_40958", 0.50, 1.8, "", "boks-meč", 1.0),                # RISE: odlučno lice (oštro)
                  ("mk_40970", 0.50, None, "", "boks-meč", 0.5),               # gard gore
                  ("mk_40972", 0.50, None, "", "boks-meč", 0.5),               # pod pritiskom, i dalje stoji
                  ("mk_40967", 0.45, None, "", "boks-meč", 0.5),               # get back up: vraća se u razmenu
                  ("mk_40954", 0.55, None, "", "boks-meč", 0.5),               # ide napred
                  ("mk_40968", 0.45, 7.5, "", "boks-meč", 0.5),                # rukavica bez logoa (7.5 s)
                  ("mk_40974", 0.50, 6.8, "", "boks-meč", 1.0)],               # udarac pogađa (rezultat), bez logoa
        "caption": "Getting knocked down isn't the end. Staying down is. When did you last get back up? \U0001F447",
        "tags": "#stoicism #discipline #mindset #resilience #boxing",
        "sound": "emotional cinematic phonk / slow build to drop (trending ↗) - drop na 4.0 s (get back up)"},
    # ---- v5 PRIČA u stilu LUXE NOIR (korisnik: "u njegovom stilu montiranja"): rez na ~0.25 s (7/8 frejmova = 1/8 @120 BPM)
    17: {"mode": "story", "hook": "They see the car. Not the 5AM alarms.", "word": "SACRIFICE", "line": "pay now. live later.",
        "loop": ("mk_75", 0.5, 7.0, "eq=gamma=1.5", "luks-noir"),            # kabriolet (ono što vide / rezultat); 74 odbačen: vidi se samo točak
        "shots": [
                  ("mk_18302", 0.5, None, "", "luks-noir", 0.2333),  # novac na stolu
                  ("mk_51571", 0.5, None, "", "luks-noir", 0.2667),  # šampanjac
                  ("mk_66", 0.68, None, "eq=gamma=1.7", "luks-noir", 0.2333),  # crveni auto u garaži
                  ("mk_4317", 0.5, None, "", "luks-noir", 0.2667),  # luka u zalasku
                  ("mk_18297", 0.5, None, "", "luks-noir", 0.2333),  # novčanik pun para
                  ("mk_18305", 0.85, None, "", "luks-noir", 0.2667),  # novčanice padaju
                  ("mk_50753", 0.55, None, "", "luks-noir", 0.2333),  # gasi budilnik u zoru
                  ("mk_52079", 0.5, None, "eq=gamma=1.3", "luks-noir", 0.2667),  # teretana
                  ("mk_39834", 0.5, None, "", "luks-noir", 0.2333),  # budilnik
                  ("mk_52087", 0.45, None, "eq=gamma=1.3", "luks-noir", 0.2667),  # konopci
                  ("mk_241", 0.4, None, "", "luks-noir", 0.2333),  # potpisuje
                  ("mk_4830", 0.55, None, "", "luks-noir", 0.2667),  # radi u odelu
                  ("mk_52080", 0.5, None, "eq=gamma=1.3", "luks-noir", 0.2333),  # šipka
                  ("mk_4758", 0.55, None, "", "luks-noir", 0.2667),  # utišava budilnik
                  ("mk_52091", 0.5, None, "eq=gamma=1.3", "luks-noir", 0.2333),  # trening
                  ("mk_4813", 0.5, None, "", "luks-noir", 0.2667),  # sastanak
                  ("mk_51553", 0.5, None, "", "luks-noir", 0.2333),  # čaše šampanjca
                  ("mk_30013", 0.5, None, "", "luks-noir", 0.2667),  # dogovor
                  ("mk_4351", 0.5, None, "", "luks-noir", 0.2333),  # marina
                  ("mk_52415", 0.5, None, "", "luks-noir", 0.2667),  # šampanjac izbliza
                  ("mk_40077", 0.5, None, "", "luks-noir", 0.2333),  # luka odozgo
                  ("mk_51631", 0.5, None, "", "luks-noir", 0.2667),  # puni čašu
                  ("mk_4045", 0.5, None, "", "luks-noir", 0.2333),  # luksuzni bazen
                  ("mk_50", 0.15, None, "eq=gamma=1.35", "luks-noir", 0.2667),  # crveni auto - rezultat
                  ],
        "caption": "Everyone wants the lifestyle. Nobody wants the 5AM part. Would you trade 5 years for it? \U0001F447",
        "tags": "#stoicism #discipline #mindset #sacrifice #luxurylifestyle",
        "sound": "dark luxury phonk / fast trap (trending ↗) - rez na svaku osminu (0.25 s)"},
    # ---- krug: LUXE montaža + priča (20.11.); #20 preskočen: premalo zanatskih kadrova bez brenda
    18: {"mode": "story", "hook": "They called it lonely. It was focus.", "word": "SOLITUDE", "line": "the quiet hours count.",
        "loop": ("mk_50133", 0.15, 6.0, "eq=gamma=1.2", "noć-rad"),  # mladić uči noću
        "shots": [
                  ("mk_1793", 0.5, None, "eq=gamma=1.3", "noć-rad", 0.5),  # lampa nad stolom
                  ("mk_52198", 0.4, None, "eq=gamma=1.2", "noć-rad", 0.5),  # tišina sobe
                  ("mk_308", 0.55, None, "", "noć-rad", 0.5),  # laptop, grad kroz prozor
                  ("mk_1728", 0.3, None, "eq=gamma=1.5", "noć-rad", 0.2333),  # kod na ekranu
                  ("mk_1781", 0.5, None, "", "noć-rad", 0.2667),  # kucanje
                  ("mk_50111", 0.5, None, "", "noć-rad", 0.2333),  # sto pun beleški
                  ("mk_1730", 0.45, None, "", "noć-rad", 0.2667),  # kafa i laptop
                  ("mk_50109", 0.5, None, "", "noć-rad", 0.2333),  # beleške
                  ("mk_242", 0.6, None, "", "noć-rad", 0.2667),  # kucanje noću
                  ("mk_50116", 0.55, None, "", "noć-rad", 0.2333),  # crta grafikon
                  ("mk_29997", 0.5, None, "", "noć-rad", 0.2667),  # 3D model u radionici
                  ("mk_3983", 0.5, None, "eq=gamma=1.2", "noć-rad", 0.5),  # mesec nad šumom
                  ("mk_4038", 0.5, None, "", "noć-rad", 0.5),  # polarna svetlost
                  ("mk_42653", 0.55, None, "", "noć-rad", 0.5),  # završava rad
                  ("mk_4954", 0.5, None, "", "noć-rad", 1.0),  # zatvara laptop
                  ],
        "caption": "Some of your best work happens when nobody's watching. What do you work on when everyone's asleep? \U0001F447",
        "tags": "#stoicism #discipline #mindset #solitude #nightwork",
        "sound": "slowed lo-fi phonk / dark ambient (trending ↗) - rez na osminu u sredini"},
    19: {"mode": "story", "hook": "You want it now. That's why you don't have it.", "word": "DELAY", "line": "wait for it.",
        "loop": ("mk_44086", 0.45, 4.0, "", "odlaganje"),  # jede krofnu - odmah
        "shots": [
                  ("mk_52219", 0.5, None, "", "odlaganje", 0.5),  # žitarice padaju
                  ("mk_4919", 0.55, None, "", "odlaganje", 0.5),  # kupovina telefonom
                  ("mk_52213", 0.5, None, "", "odlaganje", 0.5),  # šarene žitarice
                  ("mk_4911", 0.5, None, "", "odlaganje", 0.2333),  # skrolovanje u krevetu
                  ("mk_52207", 0.5, None, "", "odlaganje", 0.2667),  # čokoladne kuglice
                  ("mk_42133", 0.5, None, "", "odlaganje", 0.2333),  # skrol prodaje
                  ("mk_4801", 0.4, None, "", "odlaganje", 0.2667),  # telefon za stolom
                  ("mk_18263", 0.5, None, "", "odlaganje", 0.2333),  # broji novčiće - štednja
                  ("mk_18307", 0.5, None, "eq=gamma=1.4", "odlaganje", 0.2667),  # baca novčić
                  ("mk_43699", 0.5, None, "", "odlaganje", 0.2333),  # presađuje biljku
                  ("mk_43697", 0.5, None, "", "odlaganje", 0.2667),  # listovi rastu
                  ("mk_43702", 0.5, None, "", "odlaganje", 0.5),  # sadi
                  ("mk_4776", 0.5, None, "", "odlaganje", 0.5),  # zaliva
                  ("mk_43706", 0.5, None, "", "odlaganje", 0.5),  # cvet procvetao
                  ("mk_4998", 0.5, None, "", "odlaganje", 0.5),  # jezero u zalasku - mir
                  ("mk_4881", 0.5, None, "", "odlaganje", 0.5),  # polje suncokreta - žetva
                  ],
        "caption": "Everything good takes longer than you want. What are you willing to wait for? \U0001F447",
        "tags": "#stoicism #discipline #mindset #patience #delayedgratification",
        "sound": "calm-to-epic phonk (trending ↗) - rez na osminu u sredini"},
    21: {"mode": "story", "hook": "See it before you build it.", "word": "VISION", "line": "then build it.",
        "loop": ("mk_42182", 0.5, 4.0, "", "gradnja-vizija"),  # dete slaže lego
        "shots": [
                  ("mk_42196", 0.5, None, "", "gradnja-vizija", 0.5),  # devojčica gradi
                  ("mk_2858", 0.45, None, "", "gradnja-vizija", 0.5),  # ruka crta
                  ("mk_29984", 0.4, None, "", "gradnja-vizija", 0.5),  # beležnica i olovke
                  ("mk_1437", 0.5, None, "", "gradnja-vizija", 0.2333),  # nacrt na gradilištu
                  ("mk_41602", 0.45, None, "", "gradnja-vizija", 0.2667),  # akvarel
                  ("mk_40310", 0.6, None, "", "gradnja-vizija", 0.2333),  # detalj slike
                  ("mk_44708", 0.5, None, "eq=gamma=1.7", "gradnja-vizija", 0.2667),  # kontroler drona
                  ("mk_44644", 0.5, None, "", "gradnja-vizija", 0.2333),  # dron na nebu (623 elise odbačene: crno)
                  ("mk_1440", 0.5, None, "", "gradnja-vizija", 0.2667),  # stavlja šlem
                  ("mk_1457", 0.5, None, "", "gradnja-vizija", 0.2333),  # cigle
                  ("mk_1442", 0.55, None, "", "gradnja-vizija", 0.2667),  # gradilište
                  ("mk_600", 0.5, None, "", "gradnja-vizija", 0.5),  # gleda zgradu
                  ("mk_581", 0.6, None, "", "gradnja-vizija", 0.5),  # dron nad zgradom
                  ("mk_613", 0.5, None, "eq=gamma=1.6", "gradnja-vizija", 0.5),  # dron nad šumom
                  ("mk_2788", 0.5, None, "", "gradnja-vizija", 0.5),  # kuće u šumi odozgo
                  ("mk_4854", 0.5, None, "", "gradnja-vizija", 0.5),  # silueta i grad u zalasku
                  ],
        "caption": "Every building was a drawing first. What are you building right now? \U0001F447",
        "tags": "#stoicism #discipline #mindset #vision #builder",
        "sound": "cinematic build-up phonk (trending ↗) - rez na osminu u sredini"},
    # ---- krug 20.11 (2): novi materijal, 4 nova sveta
    22: {"mode": "story", "hook": "Waves don't stop. Learn to ride them.", "word": "ADAPT", "line": "ride it.",
        "loop": ("mk_1065", 0.62, 5.0, "", "surf"),  # surfer gleda more
        "shots": [
                  ("mk_1071", 0.5, None, "", "surf", 0.5),  # talas se ruši odozgo
                  ("mk_1070", 0.5, None, "", "surf", 0.5),  # bela pena
                  ("mk_38933", 0.5, None, "", "surf", 0.5),  # talasi stižu
                  ("mk_1042", 0.5, None, "", "surf", 0.2333),  # vesla kroz talas
                  ("mk_1163", 0.6, None, "", "surf", 0.2667),  # surfer na talasu
                  ("mk_1032", 0.55, None, "", "surf", 0.2333),  # trči sa daskom
                  ("mk_1074", 0.5, None, "", "surf", 0.2667),  # talas odozgo
                  ("mk_1127", 0.6, None, "", "surf", 0.2333),  # hvata talas
                  ("mk_1075", 0.5, None, "", "surf", 0.2667),  # talas odozgo
                  ("mk_1128", 0.62, None, "", "surf", 0.2333),  # vozi talas
                  ("mk_38939", 0.5, None, "", "surf", 0.2667),  # surferi na moru
                  ("mk_1045", 0.5, None, "", "surf", 0.5),  # silueta u zalasku
                  ("mk_1002", 0.4, None, "", "surf", 0.5),  # ka moru
                  ("mk_1220", 0.5, None, "", "surf", 0.5),  # silueta sa daskom
                  ("mk_38901", 0.5, None, "", "surf", 0.5),  # zalazak nad talasima
                  ("mk_1069", 0.6, None, "", "surf", 0.5),  # na obali
                  ],
        "caption": "Life won't calm down for you. Learn to move with it. What wave are you riding right now? \U0001F447",
        "tags": "#stoicism #discipline #mindset #adapt #surfing",
        "sound": "ocean phonk / cinematic slow build (trending ↗) - rez na osminu u sredini"},
    23: {"mode": "story", "hook": "Think three moves ahead.", "word": "STRATEGY", "line": "play the long game.",
        "loop": ("mk_49885", 0.45, 6.0, "", "šah"),  # čovek razmišlja nad šahom
        "shots": [
                  ("mk_5339", 0.55, None, "", "šah", 0.5),  # povlači figuru
                  ("mk_49721", 0.5, None, "", "šah", 0.5),  # tabla
                  ("mk_49731", 0.5, None, "", "šah", 0.5),  # figure pod svetlom
                  ("mk_49714", 0.5, None, "eq=gamma=1.4", "šah", 0.2333),  # crne figure
                  ("mk_49734", 0.5, None, "eq=gamma=1.4", "šah", 0.2667),  # izbliza
                  ("mk_49723", 0.5, None, "", "šah", 0.2333),  # bočno
                  ("mk_49710", 0.5, None, "eq=gamma=1.3", "šah", 0.2667),  # tabla izbliza
                  ("mk_49716", 0.5, None, "eq=gamma=1.3", "šah", 0.2333),  # pogled na tablu
                  ("mk_49733", 0.5, None, "eq=gamma=1.3", "šah", 0.2667),  # figure u poziciji
                  ("mk_49909", 0.5, None, "", "šah", 0.2333),  # luksuzna tabla
                  ("mk_49906", 0.5, None, "", "šah", 0.2667),  # mermer i sat
                  ("mk_4762", 0.5, None, "", "šah", 1.0),  # deca igraju - učenje
                  ("mk_49725", 0.5, None, "eq=gamma=1.5", "šah", 1.5),  # dama stoji sama - pobeda
                  ],
        "caption": "Most people play for today. Winners play for 5 years from now. What's your next move? \U0001F447",
        "tags": "#stoicism #discipline #mindset #strategy #chess",
        "sound": "dark chess phonk / slow piano trap (trending ↗) - rez na osminu u sredini"},
    24: {"mode": "story", "hook": "How you start is how you finish.", "word": "RITUAL", "line": "own your mornings.",
        "loop": ("mk_808", 0.4, 4.0, "", "jutro"),  # šolja na suncu
        "shots": [
                  ("mk_4984", 0.45, None, "", "jutro", 0.5),  # sipa kafu u filter
                  ("mk_816", 0.5, None, "", "jutro", 0.5),  # voda kroz filter
                  ("mk_4982", 0.5, None, "", "jutro", 0.5),  # zrna kafe
                  ("mk_42906", 0.45, None, "", "jutro", 0.2333),  # razbija jaja
                  ("mk_236", 0.5, None, "", "jutro", 0.2667),  # puni šolju
                  ("mk_42909", 0.5, None, "", "jutro", 0.2333),  # jaje u tiganju
                  ("mk_41859", 0.5, None, "", "jutro", 0.2667),  # kapućino
                  ("mk_43925", 0.5, None, "", "jutro", 0.2333),  # seče voće
                  ("mk_810", 0.6, None, "", "jutro", 0.2667),  # latte art
                  ("mk_43912", 0.5, None, "", "jutro", 0.2333),  # zdrav doručak
                  ("mk_10428", 0.5, None, "", "jutro", 0.2667),  # sok od pomorandže
                  ("mk_4866", 0.5, None, "", "jutro", 0.5),  # doručak na stolu
                  ("mk_43935", 0.5, None, "eq=gamma=1.5", "jutro", 1.0),  # šolja se puši
                  ("mk_4992", 0.5, None, "", "jutro", 1.0),  # kafa na zrnima
                  ],
        "caption": "Win the morning, win the day. What's the first thing you do after you wake up? \U0001F447",
        "tags": "#stoicism #discipline #mindset #morningroutine #habits",
        "sound": "lo-fi morning phonk / chill trap (trending ↗) - rez na osminu u sredini"},
    25: {"mode": "story", "hook": "Masters were beginners who didn't quit.", "word": "MASTERY", "line": "repeat until great.",
        "loop": ("mk_43048", 0.55, 5.0, "", "kuhinja-zanat"),  # kuvar u kuhinji
        "shots": [
                  ("mk_42464", 0.5, None, "", "kuhinja-zanat", 0.5),  # meša brašno
                  ("mk_1669", 0.5, None, "", "kuhinja-zanat", 0.5),  # testo
                  ("mk_42467", 0.45, None, "", "kuhinja-zanat", 0.5),  # mesi
                  ("mk_43055", 0.5, None, "", "kuhinja-zanat", 0.2333),  # seče beli luk
                  ("mk_43021", 0.5, None, "", "kuhinja-zanat", 0.2667),  # seče na dasci
                  ("mk_42469", 0.5, None, "", "kuhinja-zanat", 0.2333),  # oblikuje picu
                  ("mk_43037", 0.5, None, "", "kuhinja-zanat", 0.2667),  # seče precizno
                  ("mk_43063", 0.5, None, "", "kuhinja-zanat", 0.2333),  # prži
                  ("mk_4678", 0.5, None, "eq=gamma=1.3", "kuhinja-zanat", 0.2667),  # roštilj
                  ("mk_40534", 0.5, None, "", "kuhinja-zanat", 0.2333),  # seče paradajz
                  ("mk_50052", 0.5, None, "", "kuhinja-zanat", 0.2667),  # puni tortu
                  ("mk_50017", 0.5, None, "", "kuhinja-zanat", 0.5),  # glazira tortu
                  ("mk_50015", 0.5, None, "", "kuhinja-zanat", 1.0),  # završava tortu
                  ("mk_2430", 0.5, None, "", "kuhinja-zanat", 1.0),  # gurmansko jelo - rezultat
                  ],
        "caption": "Every expert was once terrible at it. What skill are you practicing every day? \U0001F447",
        "tags": "#stoicism #discipline #mindset #mastery #craft",
        "sound": "focused phonk / rhythmic kitchen beat (trending ↗) - rez na osminu u sredini"},
    # ---- MOĆ/NOVAC/ŽENE/PUTOVANJA (zaključano 20.11.): svaka slika = moć, novac, luksuz
    26: {"mode": "story", "hook": "Broke is a habit. So is rich.", "word": "RICH", "line": "build the habit.",
        "loop": ("mk_4301", 0.5, 4.0, "", "novac-luks"),  # luka sa jahtama (miran, čist loop)
        "shots": [
                  ("mk_18304", 0.5, None, "", "novac-luks", 0.5),  # prelistava dolare
                  ("mk_18249", 0.5, 2.0, "", "novac-luks", 0.5),  # novčanice od 100$ (18261 odbačen: unutrašnji rezovi)
                  ("mk_22741", 0.6, None, "eq=gamma=1.3", "novac-luks", 0.5),  # žena pije vino (18247 odbačen: skriven rez)
                  ("mk_42649", 0.4, None, "", "novac-luks", 0.2333),  # prezentuje prihode
                  ("mk_40075", 0.5, None, "", "novac-luks", 0.2667),  # jahte kod plaže
                  ("mk_2889", 0.5, None, "", "novac-luks", 0.2333),  # luksuzno ostrvo
                  ("mk_44500", 0.5, None, "eq=gamma=1.3", "novac-luks", 0.2667),  # terasa
                  ("mk_1270", 0.5, None, "", "novac-luks", 0.2333),  # žena na ivici bazena
                  ("mk_4046", 0.5, None, "", "novac-luks", 0.2667),  # luksuzni hotel
                  ("mk_4641", 0.5, None, "", "novac-luks", 0.2333),  # bazen sa pogledom
                  ("mk_4198", 0.5, None, "", "novac-luks", 0.2667),  # hotelska soba
                  ("mk_2883", 0.5, None, "", "novac-luks", 0.5),  # vile na vodi, hidroavion
                  ("mk_5368", 0.5, None, "", "novac-luks", 1.0),  # jahta kod ostrva
                  ("mk_4999", 0.5, None, "", "novac-luks", 1.0),  # zalazak nad zalivom
                  ],
        "caption": "Rich isn't a paycheck, it's a set of habits. Which habit are you building this year? \U0001F447",
        "tags": "#stoicism #discipline #mindset #money #wealthylifestyle",
        "sound": "dark luxury trap / money phonk (trending ↗) - rez na osminu u sredini"},
    27: {"mode": "story", "hook": "Walk in like you own the room.", "word": "POWER", "line": "carry yourself.",
        "loop": ("mk_309", 0.4, 8.0, "", "biznis-moc"),  # čovek u odelu, telefon, grad
        "shots": [
                  ("mk_317", 0.4, None, "", "biznis-moc", 0.5),  # biznismen telefonira noću
                  ("mk_4169", 0.5, None, "", "biznis-moc", 0.5),  # ulaz u zgradu
                  ("mk_4802", 0.5, None, "", "biznis-moc", 0.5),  # kraj sastanka
                  ("mk_4809", 0.5, None, "", "biznis-moc", 0.2333),  # sastanak odozgo
                  ("mk_42648", 0.3, None, "", "biznis-moc", 0.2667),  # prezentacija
                  ("mk_30012", 0.5, None, "", "biznis-moc", 0.2333),  # dogovor
                  ("mk_4144", 0.5, None, "eq=gamma=1.8", "biznis-moc", 0.2667),  # grad noću
                  ("mk_40673", 0.5, None, "", "biznis-moc", 0.2333),  # neboderi odozdo
                  ("mk_4007", 0.5, None, "", "biznis-moc", 0.2667),  # avion sleće
                  ("mk_4368", 0.5, None, "", "biznis-moc", 0.2333),  # iznad oblaka
                  ("mk_40099", 0.5, None, "", "biznis-moc", 0.2667),  # obala u zalasku
                  ("mk_4840", 0.55, None, "", "biznis-moc", 0.5),  # silueta raširenih ruku
                  ("mk_44391", 0.5, None, "", "biznis-moc", 1.0),  # ostrvo iz vazduha
                  ("mk_10332", 0.5, None, "", "biznis-moc", 1.0),  # plaža odozgo
                  ],
        "caption": "Confidence is quiet. Presence is loud. Do you walk in like you belong there? \U0001F447",
        "tags": "#stoicism #discipline #mindset #power #success",
        "sound": "boss phonk / dark business trap (trending ↗) - rez na osminu u sredini"},
    28: {"mode": "story", "hook": "Level up. They will notice.", "word": "STATUS", "line": "become the prize.",
        "loop": ("mk_70", 0.62, 6.0, "", "žene-auta"),  # žena kod sportskog auta
        "shots": [
                  ("mk_44547", 0.45, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.5),  # žena u autu, naočare
                  ("mk_44541", 0.55, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.5),  # žena u sportskom autu
                  ("mk_44544", 0.55, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.5),  # žena kod sportskog auta
                  ("mk_44542", 0.5, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.2333),  # sedi u autu
                  ("mk_44555", 0.5, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.2667),  # na autu
                  ("mk_44557", 0.5, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.2333),  # u autu
                  ("mk_44556", 0.5, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.2667),  # naslonjena na auto
                  ("mk_44545", 0.5, None, "eq=gamma=1.5:contrast=1.2", "žene-auta", 0.2333),  # na sportskom autu
                  ("mk_71", 0.62, None, "", "žene-auta", 0.2667),  # naslonjena na auto
                  ("mk_43192", 0.6, None, "", "žene-auta", 0.2333),  # kabriolet
                  ("mk_4699", 0.5, None, "", "žene-auta", 0.2667),  # džet ski
                  ("mk_44530", 0.5, None, "", "žene-auta", 0.5),  # ivica bazena
                  ("mk_3159", 0.5, None, "", "žene-auta", 1.0),  # pored bazena
                  ("mk_1272", 0.5, None, "", "žene-auta", 1.0),  # izlazi iz bazena
                  ],
        "caption": "Stop chasing. Start becoming. Who are you becoming this year? \U0001F447",
        "tags": "#stoicism #discipline #mindset #levelup #luxurylifestyle",
        "sound": "luxury phonk / smooth dark trap (trending ↗) - rez na osminu u sredini"},
    # ---- NAJVIRALNIJI (20.11.): AI materijal iz Canve (originalan, bez logoa) + priča "smejali su se -> dokaz"
    29: {"mode": "story", "hook": "At 25 they laughed. At 30 they asked how.", "word": "PROOF", "line": "let them watch.",
        "loop": ("aic_full", 0.5, 1.5, "eq=gamma=1.45:contrast=1.08", "ai-luks"),                 # čovek ide ka svom autu ispred nebodera
        "shots": [("aic_man", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.5),          # on, s leđa
                  ("aic_tail", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.5),         # stop svetla i odraz
                  ("aic_city", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.5),         # grad koji gleda
                  ("aig_full", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.5),         # PROOF: 3 ujutru, sam
                  ("aig_face", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.5),         # lice nad laptopom
                  ("aig_window", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.5),       # kiša i grad kroz prozor
                  ("mk_4692", 0.5, None, "", "ai-luks", 1.5),         # ostrvo
                  ("aic_wheel", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.75),       # njegov auto
                  ("aic_tower", 0.5, 0.5, "eq=gamma=1.45:contrast=1.08", "ai-luks", 0.75)],      # njegov grad
        "caption": "They laughed at the plan. Now they ask for the plan. Who doubted you? \U0001F447",
        "tags": "#stoicism #discipline #mindset #success #provethemwrong",
        "sound": "slowed dark phonk / emotional trap (trending ↗) - drop na 4.0 s (let them watch)"},
    # ---- ŽIVI snimci (korisnik: "žive snimke, ne AI"): poker/rizik/moć
    30: {"mode": "story", "best": True, "hook": "Everyone bets on something. Bet on yourself.", "word": "RISK", "line": "go all in.",
        "hits": [2.0, 4.0],  # punch-in + blic 2 frejma na smeni teksta (RISK, go all in)
        "loop": ("mk_40603", 0.5, 6.2, "eq=gamma=1.4", "poker-moc"),   # JUNAK: čovek u odelu, gleda u kameru (hook = najjači kadar)
        "shots": [("mk_40600", 0.4, None, "eq=gamma=1.4", "poker-moc", 0.5),   # njegove ruke, manžetne - sprema se
                  ("mk_5231", 0.6, 0.0, "eq=gamma=1.45", "poker-moc", 0.5),  # BET ON YOURSELF: crvena kravata, gura žetone na sto
                  ("mk_40512", 0.5, None, "eq=gamma=1.3", "poker-moc", 0.5),       # karte se dele - opklada
                  ("mk_5245", 0.5, None, "eq=gamma=1.35", "poker-moc", 0.3333),     # RISK: žetoni padaju (udarac 2.0)
                  ("mk_40507", 0.5, None, "eq=gamma=1.8", "poker-moc", 0.3333),  # uzima žetone za ulog
                  ("mk_40501", 0.42, 2.3, "eq=gamma=1.95", "poker-moc", 0.3333),  # ruka obara kulu žetona
                  ("mk_5238", 0.42, 5.35, "eq=gamma=1.45", "poker-moc", 0.3333),  # baca kockice
                  ("mk_5234", 0.6, 4.35, "eq=gamma=1.45", "poker-moc", 0.3333),  # viri u karte: dva keca
                  ("mk_40510", 0.5, 1.35, "eq=gamma=2.0", "poker-moc", 0.3333),  # baca žeton uvis - opklada (40500: natpis na stolu; 40498: mutno)
                  ("mk_5230", 0.45, 3.7, "eq=gamma=1.9:contrast=1.08", "poker-moc", 1.0),  # GO ALL IN: gura sve žetone (ruke kroz ceo kadar)
                  ("mk_5240", 0.5, None, "", "poker-moc", 0.75),       # kraljevska kenta
                  ("mk_40511", 0.5, None, "eq=gamma=1.45", "poker-moc", 0.75)],     # skida kulu žetona - dobitak
        "caption": "Nobody's going to bet on you until you do. What are you going all in on? \U0001F447",
        "tags": "#stoicism #discipline #mindset #betonyourself #success",
        "sound": "dark casino phonk / slow suspense trap (trending ↗) - drop na 4.0 s (go all in)"},
    # ---- 20.11. 18:00 NY (hype recept #2, skaut: Pexels set Mizuno K + Mixkit satovi)
    31: {"mode": "story", "hits": [2.0, 4.0], "hook_y": 0.25, "hook": "The rich buy time, not things.", "word": "TIME", "line": "buy back your hours.",
        "loop": ("px_13801264", 0.5, 2.0, "eq=gamma=1.3", "preduzetnik-sat"),   # JUNAK: portret pred NYSE, gleda u kameru (hook + kraj, svetao)
        "shots": [("px_13801280", 0.5, 3.0, "eq=gamma=1.3", "preduzetnik-sat", 0.5),   # BUY TIME: gleda u sat
                  ("px_13801270", 0.5, 1.5, "", "preduzetnik-sat", 0.5),               # potpisuje - kupuje
                  ("px_13801275", 0.5, 4.4, "eq=gamma=1.3", "preduzetnik-sat", 0.5),               # NOT THINGS: spušta i odlaže telefon
                  ("mk_28887", 0.5, 4.4, "", "preduzetnik-sat", 0.3333),               # TIME: sekundara prelazi 12
                  ("px_13801281", 0.5, 5.8, "eq=gamma=1.2", "preduzetnik-sat", 0.3333),            # glava u šaci na klupi (1440p)
                  ("mk_28893", 0.0, 1.5, "", "preduzetnik-sat", 0.3333),               # osovina + obe kazaljke + broj 10
                  ("px_13801276", 0.5, 0.2, "eq=gamma=1.4", "preduzetnik-sat", 0.3333),            # zabrinut nad laptopom u sumrak
                  ("mk_39824", 0.45, 2.0, "", "preduzetnik-sat", 0.3333),              # metalni sat, brze kazaljke
                  ("px_13801293", 0.5, 3.8, "eq=gamma=1.45", "preduzetnik-sat", 0.3334),# trlja oči - prodao vreme
                  ("px_13801288", 0.5, 4.4, "", "preduzetnik-sat", 0.5),               # BUY BACK: rukovanje
                  ("px_13801230", 0.5, 9.2, "", "preduzetnik-sat", 0.5),               # slobodan: ide ka kameri u zlatnom svetlu, sako preko ramena
                  ("px_13801271", 0.5, 2.6, "eq=gamma=1.35", "preduzetnik-sat", 0.5),               # partnerka stiska pesnicu - dobra vest
                  ("px_13801273", 0.5, 3.6, "eq=gamma=1.3", "preduzetnik-sat", 1.0)],  # high five - kraj, pa loop na portret
        "caption": "Money comes back. Hours don't. What would you do with 10 free hours a week? \U0001F447",
        "tags": "#entrepreneur #mindset #success #timeismoney #businessmotivation",
        "sound": "smooth dark trap / ticking-clock intro (trending ↗) - drop na 4.0 s (buy back your hours). Pexels snimci: Mizuno K (pexels.com/@mizunokozuki)"},
    32: {"mode": "story", "hits": [2.0, 4.0], "flash": (0.22, 0.08), "hook_y": 0.70, "hook": "Six weeks left in this year.", "word": "SPRINT", "line": "finish it loud.",
        "loop": ("mk_51534", 0.50, 1.5, "eq=gamma=1.7", "gala-sprint"),   # JUNAKINJA: gleda gore, razmišlja (hook + kraj, šav loop-a 1.0-2.0)
        "shots": [("mk_51562", 0.45, 3.0, "", "gala-sprint", 0.7667),                  # SIX WEEKS LEFT: godina se puni kao čaša (jedino točenje)
                  ("mk_51530", 0.72, 0.4, "eq=gamma=1.15", "gala-sprint", 0.7333),     # ona podiže čašu, odlučuje
                  ("mk_51529", 0.78, 3.6, "eq=gamma=1.2", "gala-sprint", 0.7667),     # SPRINT: naginje se i kucne čašom (tamno pod reč)
                  ("mk_51539", 0.92, 7.2, "eq=gamma=1.6", "gala-sprint", 1.0),  # noć, muškarac u mraku pali prskalicu (crno pod reč SPRINT)
                  ("mk_51537", 0.45, 4.5667, "eq=contrast=1.1", "gala-sprint", 2.7333)],                 # FINISH IT LOUD: čep puca tačno na 4.0, vrisak, flaša gore
        "caption": "Most people wait for January. Six weeks is enough to change your year. What will you finish before Dec 31? \U0001F447",
        "tags": "#newyeargoals #mindset #discipline #success #luxurylifestyle",
        "sound": "euphoric build / celebratory trap (trending ↗) - tiho do 2 s, drop na 4.0 s (čep puca)"},
    33: {"mode": "story", "hits": [2.0, 4.0], "hook": "Fifty years ago, this was sand.", "word": "AMBITION", "line": "build from nothing.",
        "loop": ("mk_49833", 0.38, 3.0, "", "pesak-grad"),   # beli toranj, dron (prvi frejm svetao)
        "shots": [("mk_51785", 0.15, 8.0, "eq=gamma=1.3", "pesak-grad", 0.5),                # WAS SAND: prazna crvena pustinja do horizonta
                  ("mk_2786", 0.5, 3.0, "", "pesak-grad", 0.5),                 # prvi trag kroz pesak
                  ("mk_51794", 0.5, 19.0, "eq=gamma=1.35", "pesak-grad", 0.5),               # pustinja, tek par baraka
                  ("mk_3970", 0.5, 11.0, "eq=contrast=1.2", "pesak-grad", 0.4),                 # AMBITION (hit 2.0): kran u suncu
                  ("mk_40718", 0.57, 0.4, "eq=gamma=1.55", "pesak-grad", 0.4),  # kran na tornju
                  ("mk_49870", 0.5, 0.4, "eq=gamma=1.4", "pesak-grad", 0.4),                # toranj sa kranom raste
                  ("mk_1587", 0.15, 0.3, "eq=gamma=1.3", "pesak-grad", 0.4),                # kostur zgrade u suncu
                  ("mk_2010", 0.5, 3.7, "", "pesak-grad", 0.4),                 # kran + avion
                  ("mk_49872", 0.5, 3.0, "eq=gamma=1.45", "pesak-grad", 0.7667),             # BUILD (hit 4.0): osvetljen toranj u sumrak
                  ("mk_49873", 0.5, 8.0, "eq=gamma=1.95:contrast=1.08", "pesak-grad", 0.7333), # noćni grad, svetla
                  ("mk_49871", 0.5, 1.0, "eq=gamma=1.6", "pesak-grad", 1.0)],               # toranj nad gradom u plavom satu -> loop dnevni toranj
        "caption": "Every skyline started as empty sand. What are you building from nothing? \U0001F447",
        "tags": "#ambition #mindset #success #skyline #luxurylifestyle",
        "sound": "We could stay here or we could go up (trending ↗, rani trend) ili cinematic build-up phonk, drop na 4.0 s"},
}


def check_variety(n):
    """Najviše 2 kadra iste vrste u klipu; nijedan izvor dvaput u klipu ni u dva klipa serije."""
    e = EDITS[n]; from collections import Counter
    kinds = Counter([e["loop"][4]] + [x[4] for x in e["shots"]])
    bad = {k: v for k, v in kinds.items() if v > 2}
    srcs = [x[0] for x in e["shots"]] + [e["loop"][0]]
    other = {x[0] for m, o in EDITS.items() if m != n for x in o["shots"] + [o["loop"]]}
    rep = [x for x in srcs if srcs.count(x) > 1 or x in other]
    if e.get("mode") == "story": bad = {}  # KONCEPT: jedan svet/junak unutar klipa; raznovrsnost proverava 'stale' između klipova
    assert not bad and not rep, f"edit {n}: previše iste vrste {bad} / ponovljen izvor {rep}"
    # STALNO PRAVILO KORISNIKA: svaki put nova tema i nove scene
    words = [o["word"] for m, o in EDITS.items() if m != n]
    hooks = [o.get("hook") for m, o in EDITS.items() if m != n and o.get("hook")]
    assert e["word"] not in words, f"edit {n}: tema/reč '{e['word']}' već korišćena"
    assert not e.get("hook") or e["hook"] not in hooks, f"edit {n}: hook već korišćen"
    # vrsta scene ne sme biti u 3+ od prethodnih 5 klipova (tera nove scene iz kruga u krug)
    prev = [EDITS[m] for m in sorted(EDITS) if m < n][-5:]
    pk = [{o["loop"][4]} | {x[4] for x in o["shots"]} for o in prev]
    stale = [k for k in kinds if sum(k in q for q in pk) >= 3]
    assert not stale, f"edit {n}: scene previše korišćene u prethodnih 5 klipova: {stale}"
    # snimak ne sme postojati u istoriji SVIH ranijih serija (studio/visual_history.json, samo raste)
    import json as _j, re as _re
    _vh = _j.load(open(os.path.join(HERE, "..", "studio", "visual_history.json")))
    def _fid(x):
        m = _re.match(r"^(?:px|money|power_flight|power_jet|power_man|power_phone|lux_woman|car|city|nature|travel|workout|snow)_(\d+)$", x)
        return f"pexels_{m.group(1)}" if m else x
    old = [x for x in srcs if [p for p in _vh.get(_fid(x), []) if p != f"stoic_edit_{n:02d}"]]
    assert not old, f"edit {n}: snimci već korišćeni u ranijim klipovima: {old}"


_BEST = None


def best_moment(name, d, xc):
    """Najjači trenutak u snimku (zahtev korisnika: 'najbrutalnija slika iz snimka, ne bilo koja').
    Boduje prozore dužine d po: oštrini (Laplacian), kontrastu, licu u kadru (Haar), umerenom pokretu,
    kazna za izgoreno/pretamno. Gleda samo deo koji ostaje posle vertikalnog kropa (xc)."""
    global _BEST
    import json as _j, cv2, numpy as np
    cache = os.path.join(HERE, "out", "best_moments.json")
    if _BEST is None:
        _BEST = _j.load(open(cache)) if os.path.exists(cache) else {}
    key = f"{name}|{d:.3f}|{xc}"
    if key in _BEST: return _BEST[key]
    cap = cv2.VideoCapture(M.src(name)); fps = cap.get(5) or 30; n = int(cap.get(7))
    face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    step = max(1, int(fps / 6)); feats = []; prev = None
    for k in range(0, n, step):
        cap.set(1, k); ok, f = cap.read()
        if not ok: break
        h, w = f.shape[:2]
        if w > h:
            cw = int(h * 9 / 16); x0 = int((w - cw) * xc); f = f[:, x0:x0 + cw]
        g = cv2.cvtColor(cv2.resize(f, (270, 480)), cv2.COLOR_BGR2GRAY)
        sharp = cv2.Laplacian(g, cv2.CV_64F).var(); con = g.std(); lum = g.mean() / 255
        nf = len(face.detectMultiScale(g, 1.2, 5, minSize=(30, 30)))
        mot = 0.0 if prev is None else float(np.abs(g.astype(float) - prev).mean()); prev = g.astype(float)
        feats.append((k / fps, sharp, con, lum, nf, mot))
    cap.release()
    if not feats: return 0.0
    import numpy as np
    A = np.array([[x[1], x[2], x[4], x[5]] for x in feats]); lum = np.array([x[3] for x in feats])
    A = (A - A.min(0)) / (np.ptp(A, 0) + 1e-6)
    mot = A[:, 3]; score = 0.35 * A[:, 0] + 0.30 * A[:, 1] + 0.25 * (A[:, 2] > 0) + 0.10 * (1 - np.abs(mot - 0.4))
    score -= 0.6 * ((lum < 0.08) | (lum > 0.85))
    t = np.array([x[0] for x in feats]); L = t[-1]
    best, bs = 0.2, -9
    for i, ti in enumerate(t):
        if ti < 0.1 or ti + d > L - 0.1: continue
        win = score[(t >= ti) & (t <= ti + d)].mean()
        if win > bs: bs, best = win, float(ti)
    _BEST[key] = round(best, 2); os.makedirs(os.path.dirname(cache), exist_ok=True)
    _j.dump(_BEST, open(cache, "w"), indent=0)
    return _BEST[key]


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
        if e.get("hook") and t < 2.0 and e.get("hook_y"): cy = H * e["hook_y"]  # opciono: hook iznad lica (podrazumevano 0.44)
        # blaga tamna traka iza teksta - čitljivost na svetlim kadrovima (nebo, staza)
        bt, bb = (cy - 260, cy + 230) if (e.get("hook") and t < 2.0) else (cy - 170, cy + 120)
        g = cairo.LinearGradient(0, bt, 0, bb)
        for st, al in ((0, 0), (0.3, 0.42), (0.7, 0.42), (1, 0)): g.add_color_stop_rgba(st, 0, 0, 0, al)
        c.rectangle(0, bt, W, bb - bt); c.set_source(g); c.fill()
        hook = e.get("hook")  # v3 (lekcija 22): krupna hook rečenica 0-2 s, čita se i na sličici profila
        if hook and t < 2.0:
            pop = 0.9 + 0.1 * min(1.0, t / 0.15) if e.get("style") == "live" else 1.0
            c.save(); c.translate(M.CX, cy); c.scale(pop, pop); c.translate(-M.CX, -cy)
            M.face(c, 84, cairo.FONT_WEIGHT_BOLD)
            words = hook.split(); lines = M.wrap(c, words, M.MAXW)
            if len(lines) > 2: lines = M.balance3(c, words, M.MAXW)
            lh = 84 * 1.18
            for li, ln in enumerate(lines):
                s_ = " ".join(ln); tw = c.text_extents(s_).x_advance; x = M.CX - tw / 2
                y = cy + (li - (len(lines) - 1) / 2) * lh + 30
                M.BOXES.append((x, y - 70, x + tw, y + 20))
                M.shadow_text(c, x, y, s_, 1.0)
            c.restore()
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
            # STALNO PRAVILO KORISNIKA: CTA ispod završne poruke na svakom klipu
            ca = min(1.0, max(0.0, (t - split - 0.25) / 0.2))
            M.face(c, 34, cairo.FONT_WEIGHT_BOLD)
            cta = "SHARE  •  LIKE  •  COMMENT FOR MORE"; cw = c.text_extents(cta).x_advance; cx_ = M.CX - cw / 2
            M.BOXES.append((cx_, cy + 60, cx_ + cw, cy + 100))
            M.shadow_text(c, cx_, cy + 92, cta, ca)
        s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()


# ŽIVI stil (zahtev korisnika "malo življe"): toplije i zasićenije boje, udarac zumom na rezu, završni "burst" po 0.25 s
LIVE_GRADE = ("eq=saturation=1.18:contrast=1.10:brightness=0.015,"
              "colorbalance=rs=0.02:bs=-0.02:rm=0.02:bm=-0.03:rh=0.03:bh=-0.03")


def sdur(x):  # trajanje kadra: 6. polje ili 1 udarac (0.5 s); burst = 0.25 s (1/8 @120 BPM)
    return x[5] if len(x) > 5 else BEAT


def make(n):
    e = EDITS[n]; M.BOXES.clear()
    shots = e["shots"]; total = BEAT * 2 + sum(sdur(x) for x in shots)
    live = e.get("style") == "live"
    rk = dict(grade=LIVE_GRADE, vig="PI/6") if live else {}
    check_variety(n)
    odd = [x[0] for x in shots if abs(sdur(x) * FPS - round(sdur(x) * FPS)) > 0.05]  # lekcija 47: 0.75 s = 22.5 frejma -> kadar od 1 frejma
    if odd: print(f"UPOZORENJE edit {n}: trajanja nisu cela frejma ({odd}) - koristi 0.7667/0.7333")
    lname, lx, a, lex = e["loop"][:4]
    full = os.path.join(M.TMP, f"e{n}_loop.mp4")
    M.render_shot(full, lname, a - BEAT, 2 * BEAT, lx, 1.00, 1.04, lex, **rk)
    head, tail = os.path.join(M.TMP, f"e{n}_head.mp4"), os.path.join(M.TMP, f"e{n}_tail.mp4")
    M.cut(full, head, BEAT, BEAT); M.cut(full, tail, 0.0, BEAT)
    parts = [head]; t0 = BEAT
    hits = e.get("hits", [])  # opciono: punch-in + 2 frejma blica na kadru koji počinje u tim trenucima (podrazumevano isključeno)
    for k, x in enumerate(shots, 1):
        nm, xc, st, ex = x[:4]; d = sdur(x)
        if st is None: st = best_moment(nm, d, xc) if e.get("best") else round(dur(M.src(nm)) * 0.4, 2)
        o = os.path.join(M.TMP, f"e{n}_{k:02d}.mp4")
        hz = 0.12 if any(abs(t0 - h) < 0.02 for h in hits) else (0.07 if live else 0.0)
        M.render_shot(o, nm, st, d, xc, 1.00, 1.04, ex, hit=hz, **rk); parts.append(o); t0 += d
    parts.append(tail)
    lst = os.path.join(M.TMP, f"e{n}_list.txt"); open(lst, "w").write("".join(f"file '{q}'\n" for q in parts))
    base = os.path.join(M.TMP, f"e{n}_base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], check=True)
    ov = os.path.join(M.TMP, f"e{n}_ov.mov"); overlay(e, n, total, ov)
    # vizuelni udarac: beli blic 2 frejma (55% pa 25%) na trenucima iz "hits" (samo ako je zadato)
    flash = "".join(f",drawbox=t=fill:color=white@{a}:enable='eq(n,{int(round(h * FPS)) + i})'"
                    for h in e.get("hits", []) for i, a in enumerate(e.get("flash", (0.55, 0.25))))  # opciono "flash": slabiji blic (npr. (0.22, 0.08)) da ne gasi lice
    out = os.path.join(M.OUT, f"stoic_edit_{n:02d}.mp4"); part = out.replace(".mp4", ".part.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov, "-filter_complex",
                    f"[0:v][1:v]overlay=format=auto{flash},noise=alls={4 if live else 7}:allf=t,format=yuv420p[v]", "-map", "[v]", "-an",
                    "-tune", "grain", "-maxrate", "22M", "-bufsize", "44M", "-t", f"{total}", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", part], check=True)
    os.replace(part, out)
    open(out.replace(".mp4", "_opis.txt"), "w").write(f"{e['caption']}\n\nShare, like & comment for more \u2694\ufe0f\n\n{e['tags']}\n\nZvuk (dodaješ u TikTok-u): {e['sound']}\n")
    safe = all(x0 >= 0 and y0 >= 0 and x1 <= M.SAFE_R and y1 <= M.SAFE_B for x0, y0, x1, y1 in M.BOXES)
    print(out, total, "s", len(parts), "kadrova, tekst u sigurnoj zoni:", safe)


if __name__ == "__main__":
    for x in sys.argv[1:] or [str(k) for k in EDITS]:
        make(int(x))
