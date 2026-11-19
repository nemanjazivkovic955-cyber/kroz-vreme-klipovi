"""Provera novog koncepta pre produkcije (ciklus B/D). Odbija:
- hook iste STRUKTURE kao skorašnji (npr. 'Watch this…', 'Nobody tells you…', 'Feeling X?') ili previše sličan tekstom,
- završetak sličan ranijem,
- snimak koji je već korišćen (visual_history.json),
- vizuelni tag koji je preupotrebljen u poslednjih N produkcija (npr. 'noć', 'tamno', 'planina').
Upotreba: python3 studio/check_concept.py --hook "…" --ending "…" --footage id1 id2 --tags noc grad
"""
import os, sys, json, re, argparse
ROOT = os.path.dirname(os.path.abspath(__file__))
PATTERNS = {
    "watch_this": r"\bwatch this\b", "nobody_tells": r"\bnobody (tells|sees|talks)\b", "feeling_q": r"^(feeling|still) \w+\??",
    "think_youre": r"\bthink you('| a)re\b", "stop_x": r"^stop \w+ing\b", "if_you": r"^if (you|your)\b",
    "look_at": r"^look (up|at)\b", "you_didnt": r"^you didn'?t\b", "this_x_costs": r"\bthis \w+ costs\b",
    "x_isnt_what": r"\bisn'?t what you think\b", "your_x_decide": r"^your \w+ decides?\b", "you_saw": r"^you saw\b",
}


def words(s): return set(w for w in re.sub(r"[^a-z' ]", " ", s.lower()).split() if len(w) > 3)


def sim(a, b):
    A, B = words(a), words(b)
    return len(A & B) / max(1, len(A | B))


def pattern(s):
    for k, p in PATTERNS.items():
        if re.search(p, s.lower()): return k
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", default=""); ap.add_argument("--ending", default="")
    ap.add_argument("--footage", nargs="*", default=[]); ap.add_argument("--tags", nargs="*", default=[])
    ap.add_argument("--recent", type=int, default=24)
    a = ap.parse_args()
    db = json.load(open(os.path.join(ROOT, "production_db.json")))
    vh = json.load(open(os.path.join(ROOT, "visual_history.json")))
    recent = db[-a.recent:]; probs = []
    pat = pattern(a.hook)
    if pat:
        used = [p["id"] for p in recent if pattern(p.get("hook", "")) == pat]
        if used: probs.append(f"HOOK struktura '{pat}' već korišćena skoro: {used}")
    for p in db:
        if a.hook and sim(a.hook, p.get("hook", "")) > 0.4: probs.append(f"HOOK previše sličan {p['id']}: {p['hook']}")
        if a.ending and sim(a.ending, p.get("ending", "")) > 0.4: probs.append(f"KRAJ previše sličan {p['id']}: {p['ending']}")
    for f in a.footage:
        if f in vh: probs.append(f"SNIMAK {f} već korišćen u {vh[f]}")
    tags_path = os.path.join(ROOT, "visual_tags.json")
    tags = json.load(open(tags_path)) if os.path.exists(tags_path) else []
    last = tags[-8:]
    for t in a.tags:
        n = sum(1 for e in last if t in e.get("tags", []))
        if n >= 3: probs.append(f"VIZUELNI TAG '{t}' u {n} od poslednjih 8 produkcija — promeni stil")
    print("\n".join(probs) if probs else "OK - koncept je nov")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
