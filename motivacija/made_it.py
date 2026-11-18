"""YouTube video "I MADE IT": Mixkit 16:9 klipovi + crno-zlatni tekst koji prati kadar, redosled price."""
import os
import text_16x9 as T
import assemble_youtube as A

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "videos", "youtube", "made_it_16x9")
TXT = os.path.join(HERE, "..", "videos", "youtube", "made_it_16x9_tekst")
OUT = os.path.join(HERE, "..", "videos", "youtube", "i_made_it_youtube.mp4")

# redosled = prica: od nule -> kola -> devojke/stil -> destinacije -> uspeh/slavlje
STORY = [
    ("kola_04", "Started from *zero*."),
    ("kola_05", "Nobody *believed*."),
    ("kola_03", "I kept *going*."),
    ("kola_01", "Now the *garage* is full."),
    ("kola_02", "Earned, not *given*."),
    ("kola_06", "Sunset drives. *No* alarm clock."),
    ("kola_07", "My time is *mine*."),
    ("kola_08", "All eyes on *me*."),
    ("kola_09", "The work paid *off*."),
    ("kola_10", "Dream car. *Real* life."),
    ("kola_11", "No more *someday*."),
    ("devojke_06", "Good company. *Good* life."),
    ("devojke_07", "*Energy* attracts energy."),
    ("devojke_08", "*Class* never shouts."),
    ("devojke_09", "Elegance is a *choice*."),
    ("destinacije_06", "Next stop: *Dubai*."),
    ("destinacije_05", "Higher than *ever*."),
    ("destinacije_08", "The city is *mine*."),
    ("destinacije_03", "Views I *worked* for."),
    ("destinacije_04", "Rest is *earned*."),
    ("devojke_10", "Summer *every* day."),
    ("devojke_11", "*Paradise* mode."),
    ("destinacije_09", "From grind to *paradise*."),
    ("destinacije_10", "Freedom looks like *this*."),
    ("destinacije_01", "Every *sunset* is a reward."),
    ("destinacije_02", "Peace bought with *discipline*."),
    ("uspeh_09", "Deals on the *water*."),
    ("uspeh_10", "Partners, not *bosses*."),
    ("uspeh_05", "Nights on the *yacht*."),
    ("uspeh_06", "Once just a *dream*."),
    ("uspeh_01", "Pop it. You *earned* it."),
    ("uspeh_02", "Celebrate the *grind*."),
    ("uspeh_03", "Same friends. *New* level."),
    ("uspeh_04", "I *made* it."),
]

if __name__ == "__main__":
    T.render_all(dict(STORY), SRC, TXT, tag="mi")
    A.build([n for n, _ in STORY], TXT, OUT, title="I MADE IT", sub="Cars  •  Destinations  •  Lifestyle",
            outro_sub="for more success motivation", music_start=0)
