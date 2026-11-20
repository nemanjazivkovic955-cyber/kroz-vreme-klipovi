"""Promptovi za ilustracije dugog videa #2 (po kadru iz stoic/anim_ep02.py SENT). Generiše stoic/sd/ep02/shot_NNN.png.
Upotreba: python3 stoic/sd/ep02_prompts.py   (preskače već gotove)"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); STOIC = os.path.dirname(HERE)
sys.path[:0] = [HERE, STOIC]
import gen as G
import anim_ep02 as E

G.STYLE = ("2d hand-drawn cartoon illustration, bold dark outlines, storybook animation background, soft painted shading, "
           "cinematic warm lighting, history documentary cartoon style, highly detailed environment, no text, no watermark")
G.NEG = ("nude, naked, topless, nsfw, photo, photorealistic, realistic, 3d render, modern tent, camping tent, nylon, text, letters, words, watermark, logo, "
         "signature, blurry, deformed, ugly, extra limbs, extra fingers")
M = "roman emperor Marcus Aurelius, man with short curly brown beard, laurel wreath, dark red cloak"
MO = "old roman emperor Marcus Aurelius, short curly grey beard, laurel wreath, dark red cloak, tired face"
BOY = "a small serious roman boy with brown hair in a simple beige tunic"
HAD = "old roman emperor Hadrian with white beard and laurel wreath in a purple toga"
ANT = "calm grey-bearded roman senator Antoninus in a blue toga"
CAMP = "ancient roman legion camp in deep snow at night, square brown leather roman tents, wooden palisade, campfires, snowy mountains, starry sky"
TENT = f"interior of an ancient roman military tent at night, {MO} sitting at a small wooden table writing on a scroll by an oil lamp, warm light"
P = {
    "camp": CAMP + ", one big command tent glowing warm from inside",
    "tent": TENT,
    "plague": "ancient parchment map of the roman empire around the mediterranean sea, many tiny cities and roads, huge crowds",
    "general": "roman general in purple cloak raising a sword in front of a roman army in the eastern desert at sunset, banners",
    "birth": "sunny ancient rome street with temples, red tile roofs, marble columns, people walking, bright morning",
    "grave": f"ancient roman cemetery on a grey rainy day, a mother in a green hooded cloak and an old grandfather in white toga holding hands with {BOY} at a stone grave",
    "quiet": f"{BOY} sitting alone on a stone bench in a quiet roman courtyard, reading a small scroll",
    "split": f"split scene: left side rich roman children playing with gold toys in a luxurious villa, right side {BOY} sleeping on a simple straw mat in a bare room",
    "truth": f"{BOY} standing honestly in front of roman adults, bright light, calm face",
    "palace": f"grand roman palace hall with marble columns and red curtains, {HAD} pointing at {BOY}",
    "hsick": f"{HAD} lying sick in bed in a dim palace room, oil lamp, purple blankets",
    "tree": f"three roman portraits on parchment connected by arrows: {HAD}, {ANT}, a young man with brown hair",
    "afraid": "nervous young roman man of seventeen in a white tunic standing in a huge marble palace hall, afraid, sweating, big shadows",
    "power": "an empty golden throne in a dark roman hall casting a huge shadow over a crowd of people",
    "study": "young roman man with brown hair reading scrolls in an ancient library full of scroll shelves, oil lamp, warm light",
    "teacher": "old roman philosopher teacher Rusticus with grey beard in green cloak handing a scroll to a young roman man in a library",
    "epictetus": "greek philosopher Epictetus, a former slave with a walking stick and broken chains, teaching calmly in a simple stone courtyard",
    "book": "an ancient leather bound journal and scrolls on a wooden table lit by an oil lamp in a dark tent",
    "thanks": "an old parchment scroll with a handwritten list on a wooden desk, quill and ink, warm candle light",
    "awork": f"{ANT} working at a desk full of scrolls from morning to night, window with sun and moon, palace office",
    "respect": f"{ANT} listening respectfully to a poor man in ragged brown clothes and a rich senator in a white toga, roman courtyard",
    "senate": "the roman senate hall full of senators in white togas offering a golden throne, marble columns",
    "thrones": f"two golden thrones side by side in a roman palace, two roman emperors with laurel wreaths, one in red cloak one in blue cloak",
    "march": "roman legion soldiers in red cloaks marching home along a dusty road in the eastern desert at sunset",
    "march_north": f"roman legion marching north through snowy mountains, {M} leading on foot, snow falling",
    "danube": f"frozen danube river in winter, roman army camp on the bank, {M} standing with soldiers by a campfire, snow",
    "tribes": "barbarian germanic warriors with shields crossing the frozen danube river in winter, roman forts on the far bank",
    "treasury": "an empty open wooden treasure chest in a dark roman vault, a few last gold coins, dust, lamp light",
    "taxes": "roman tax collector taking coins from poor citizens in a market square, worried faces",
    "forum": "public auction in the roman forum, tables full of golden cups, marble statues, paintings and silk dresses, crowd of romans buying",
    "sick": f"{MO} coughing in a cold army tent, pale, wrapped in a blanket, oil lamp",
    "dmap": "ancient parchment map of the danube river with two marked roman cities, mountains and forests drawn in ink",
    "argue": f"{MO} arguing with his own reflection in a bronze mirror inside a tent at night, oil lamp",
    "mirror": "modern bathroom mirror with a yellow sticky note on it, morning light, toothbrush, cozy",
    "rumor": "romans whispering rumors to each other in the crowded roman forum, worried faces, temple in background",
    "half": "ancient parchment map of the roman empire split in two halves, the eastern half colored dark purple",
    "forgive": f"{MO} speaking calmly to his loyal soldiers in a winter camp, gentle expression, snow",
    "cfall": "a fallen roman general's purple cloak and sword lying on the desert sand at dusk, soldiers walking away",
    "hand": f"a roman soldier handing a wooden box full of sealed letters to {MO} in a dark tent, lamp light",
    "letters": f"{MO} throwing sealed letters into a burning bronze brazier at night, sparks flying, firelight on his face",
    "deathbed": f"{MO} lying ill on a cot inside an army tent at sunset, a young roman officer standing at the entrance, orange light",
    "sun": "sun setting over snowy mountains and a roman army camp, dramatic orange and purple sky",
    "lampout": "an oil lamp going out on a wooden table inside a dark roman tent, last wisp of smoke, quill and scroll",
    "five": "five marble busts of roman emperors in a row in a museum hall, warm light, the last bust brighter",
    "store": "a cozy modern bookstore at night, shelves full of books, one book with a classical roman bust on the cover in the window",
    "modern": "a young man sitting on a bed at night in a small modern apartment, staring at his phone, blue screen light, city lights outside the window",
    "modern_book": "a young man sitting on a bed at night in a small modern apartment, reading an old philosophy book by a warm lamp",
    "lesson": "an old parchment scroll and a quill on a dark wooden table, single candle, dark moody background",
}


def prompt_for(sh):
    name = sh["scene"].__name__; v = sh["v"] or {}
    key = {"camp_ext": "camp", "tent_write": "tent", "plague_map": "plague", "rome_street": "birth", "palace": "palace", "study": "study",
           "thrones": "thrones", "forum_auction": "forum", "danube": "danube", "general": "general", "letters_burn": "letters",
           "deathbed": "deathbed", "modern": "modern", "birth": "birth", "grave": "grave", "quiet_boy": "quiet", "split_rich": "split",
           "truth": "truth", "hadrian_sick": "hsick", "family_tree": "tree", "afraid": "afraid", "power_shadow": "power", "teacher": "teacher",
           "epictetus": "epictetus", "thanks_list": "thanks", "antoninus_work": "awork", "respect": "respect", "senate": "senate",
           "march": "march", "tribes": "tribes", "treasury": "treasury", "taxes": "taxes", "sick_emperor": "sick", "danube_map": "dmap",
           "book": "book", "argue": "argue", "mirror": "mirror", "rumor": "rumor", "half_empire": "half", "forgive": "forgive",
           "cassius_falls": "cfall", "handed_letters": "hand", "sunrise_set": "sun", "lamp_out": "lampout", "five_emperors": "five",
           "bookstore": "store", "lesson": "lesson", "boy_mat": "split"}[name]
    if key == "march" and v.get("snow"): key = "march_north"
    if key == "modern" and v.get("book"): key = "modern_book"
    p = P[key]
    if key == "palace" and isinstance(v, dict) and v.get("a") is E.ANTONINUS:
        p = f"grand roman palace hall with marble columns, {ANT} teaching a young roman man with brown hair"
    if key == "grave" and v.get("people"):
        p = f"ancient roman cemetery on a grey day, {MO} standing alone in grief at " + ("several small graves" if len(v.get("stones", [])) > 1 else "a stone grave")
    return p


def main():
    tm = json.load(open(os.path.join(STOIC, "out", "ep02", "timing.json")))
    shots, labels, sents = E.shots_from_timing(tm)
    out = os.path.join(HERE, "ep02"); os.makedirs(out, exist_ok=True)
    json.dump([prompt_for(s) for s in shots], open(os.path.join(out, "prompts.json"), "w"), indent=1)
    for i, sh in enumerate(shots):
        f = os.path.join(out, f"shot_{i:03d}.png")
        if os.path.exists(f): continue
        G.gen(f, prompt_for(sh), seed=100 + i, w=896, h=512, steps=6)
    print("SVE_ILUSTRACIJE_GOTOVE")


if __name__ == "__main__":
    main()
