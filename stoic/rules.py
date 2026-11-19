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
}
