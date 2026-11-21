"""STOIC RULES — podaci serije (brief: stoic/BRIEF.md).
shots: (izvor u stoic/src bez .mp4, x-centar kropa 0-1, start s ili None)
loop: (izvor, x, a) — kadar hook-a počinje u a; kraj klipa je [a-1, a] istog snimka -> neprimetan loop.
"""

RULES = {
    1: {"theme": "kontrola",
        "hook": "Stop wasting energy on this.",
        "rule": ["You can't control what happens to you.",
                 "You can only control how you respond.",
                 "That's where your power is."],
        "loop": ("mk_4059", 0.50, 2.70),           # oluja nad okeanom, munja u 1. frejmu
        "loop_extra": "colortemperature=temperature=12000:pl=0.9,eq=saturation=0.55:contrast=1.15",  # izvor je smeđ -> čelično plava oluja
        "shots": [("mk_3428", 0.50, 4.0),         # prolaznici u sumrak - svet koji ne kontrolišeš (4240 odbačen: treperi)
                  ("mk_4832", 0.50, 3.0),         # čovek s leđa, miran
                  ("mk_41739", 0.50, 4.0, "eq=gamma=1.5:saturation=0.9")],  # ruke drže sveću - toplo svetlo kao jedini akcenat, posvetljeno
        "caption": "Most people waste their whole day fighting this. Which part do you struggle to let go of?",
        "tags": "#stoicism #mindset #discipline #motivation #selfcontrol",
        "sound": "dark piano / slowed cinematic strings (trending ↗)"},
    2: {"theme": "tišina",
        "hook": "The strongest people do this quietly.",
        "rule": ["Don't explain yourself to everyone.",
                 "Silence is not weakness.",
                 "It's control."],
        "loop": ("mk_402", 0.31, 6.0),            # čovek u senci, silueta
        "shots": [("mk_2846", 0.31, 5.0),         # kiša na prozoru - buka sveta
                  ("mk_4063", 0.43, 4.0),         # statua na steni u oblacima - tiha snaga
                  ("mk_49736", 0.50, 3.0, "eq=gamma=1.75")],       # šahovski kralj se okreće - kontrola
        "caption": "Not everyone deserves an explanation. When did staying silent win for you?",
        "tags": "#stoicism #mindset #discipline #motivation #silence",
        "sound": "slowed dark phonk / deep ambient bass (trending ↗)"},
    3: {"theme": "mišljenje drugih",
        "hook": "This is why people don't respect you.",
        "rule": ["Their opinion of you is not your business.",
                 "Your character is.",
                 "Focus on that."],
        "loop": ("mk_434", 0.67, 7.0),            # silueta čoveka u dimu
        "loop_extra": "eq=contrast=1.45:gamma=1.1:saturation=0.6",  # izvući siluetu iz dima
        "shots": [("mk_2716", 0.95, 4.0, "eq=gamma=1.5"),         # kiša kaplje sa krova - tuđa buka
                  ("mk_1759", 0.43, 3.0),         # kamene statue - karakter
                  ("mk_41744", 0.50, 4.0)],       # plamen sveće izbliza - fokus
        "caption": "Their opinion doesn't pay your bills. Whose opinion are you still carrying?",
        "tags": "#stoicism #mindset #discipline #motivation #selfrespect",
        "sound": "dark cello / sad cinematic piano (trending ↗)"},
    4: {"theme": "disciplina",
        "hook": "Motivation is lying to you.",
        "rule": ["Motivation fades by noon.",
                 "Discipline shows up anyway.",
                 "Be the one who shows up."],
        "loop": ("mk_50957", 0.50, 3.0),          # dim se uvija na tamnoj površini - iluzija
        "shots": [("mk_41741", 0.50, 4.0, "eq=gamma=1.55"),        # sveće dogorevaju - motivacija se gasi
                  ("mk_22729", 0.50, 4.0),        # kišna mračna šuma - uslovi su loši, ipak
                  ("mk_2752", 0.64, 5.0, "eq=brightness=-0.07:gamma=0.85")],  # čovek sam stoji na steni - budi taj (49725 odbačen: isti kao kralj u #2)
        "caption": "Motivation is a feeling. Discipline is a decision. What do you show up for when you don't feel like it?",
        "tags": "#stoicism #mindset #discipline #motivation #selfdiscipline",
        "sound": "hard dark phonk / epic war drums (trending ↗)"},
}
