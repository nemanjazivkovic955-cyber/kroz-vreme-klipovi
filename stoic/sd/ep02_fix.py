"""Ponovno crtanje slabih ilustracija dugog videa #2 (posle pregleda svih 103)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen as G
import ep02_prompts as P   # isti stil
OUT = os.path.join(HERE, "ep02")
LEG = "roman legionaries in red cloaks with iron helmets and rectangular shields marching on foot through snowy mountains, emperor in a red cloak walking in front"
AUC = "outdoor ancient roman street market auction in front of a temple, a merchant holding up a golden cup, marble statues and silk dresses for sale, crowd of romans in togas bidding, sunny day"
FIX2 = {
    34: ("old grey-bearded roman senator in a blue toga writing on scrolls at a wooden desk in an ancient roman office, oil lamp, window with moon", "computer, monitor, screen, laptop, clock, modern furniture", 3401),
    49: ("a roman auctioneer standing on a wooden platform holding up a shining golden cup, tables with marble statues, silver plates and silk dresses, crowd of romans in togas raising hands to bid, forum", "tablecloth, banquet, restaurant, chairs", 4911),
    76: ("old roman emperor with grey beard and laurel wreath lying ill on a simple cot under a blanket inside a military tent, pale face, orange sunset light", "writing, desk, book, sitting", 7601),
    78: ("a young roman officer in a helmet standing at the entrance of a tent, looking at an old dying emperor lying on a cot, warm sunset light", "writing, desk, book", 7801),
}
FIX = {
    8: ("ancient roman street in the 2nd century, small houses with red tile roofs, a roman temple with columns, people in togas and tunics, bright morning", "renaissance, baroque, church, dome", 801),
    9: ("a woman in a green cloak and an old man in a white toga holding the hand of a small boy at an ancient roman stone tomb stele, cypress trees, grey rainy day", "cross, church, christian, crucifix", 901),
    12: ("a small roman boy in a beige tunic speaking calmly to tall roman adults in togas in a sunny stone courtyard", "chibi, anime, cute cartoon, big eyes", 1201),
    45: ("germanic barbarian warriors with round shields and spears walking across a frozen river in a winter forest, roman wooden fort on the far bank", "ship, boat, steamship, vessel", 4501),
    46: (LEG, "horse, horses, rider, cavalry", 4601), 53: (LEG, "horse, horses, rider, cavalry", 5301), 75: (LEG, "horse, horses, rider, cavalry", 7501),
    47: ("an empty wooden treasure chest, open and completely empty inside, in a dark stone vault, dust, single oil lamp", "gold, coins, treasure, jewels", 4701),
    49: (AUC, "tablecloth, banquet, restaurant, chairs, wedding, dining", 4901), 50: (AUC, "tablecloth, banquet, restaurant, chairs, wedding, dining", 5001),
    51: (AUC, "tablecloth, banquet, restaurant, chairs, wedding, dining", 5101), 52: (AUC, "tablecloth, banquet, restaurant, chairs, wedding, dining", 5201),
    66: ("crowd of romans in togas whispering secrets in an ancient roman forum, worried faces, roman temple with columns", "dome, church, basilica, cathedral", 6601),
}
base_neg = G.NEG
prompts = json.load(open(os.path.join(OUT, "prompts.json")))
for i, (p, neg, seed) in (FIX2 if "--fix2" in sys.argv else FIX).items():
    G.NEG = base_neg + ", " + neg
    for f in (f"up_{i:03d}.png", f"shot_{i:03d}_depth.npy"):
        if os.path.exists(os.path.join(OUT, f)): os.remove(os.path.join(OUT, f))
    G.gen(os.path.join(OUT, f"shot_{i:03d}.png"), p, seed=seed, w=896, h=512, steps=6)
    prompts[i] = p
json.dump(prompts, open(os.path.join(OUT, "prompts.json"), "w"), indent=1)
print("FIX_GOTOVO")
