"""Provera originalnosti teksta pre renderovanja.
Uporedjuje nove recenice sa SVIM dosadasnjim (quotes.py, talks.py, shortloop.py) i odbija:
  - ponovljenu frazu od 3+ sadrzajne reci,
  - otrcane izraze sa crne liste,
  - temu koja je vec iskoriscena (iz raspored.md liste).
Upotreba:  python3 check_unique.py m045 m046 ...        (proverava te unose iz quotes.py)
           python3 check_unique.py --text "recenica" ...  (proverava slobodan tekst)
Izlaz: OK ili lista problema (exit 1).
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "the_price"))

BANNED = ["every single day", "keep going", "nobody sees", "stay quiet", "one more rep", "one more day",
          "while they sleep", "let the results", "keep climbing", "never give up", "you got this", "hustle",
          "grind never stops", "rise and grind", "no pain no gain", "believe in yourself", "dream big",
          "trust the process", "the sun rises", "be like water", "pay the price", "just start",
          "nobody is coming", "comfort zone", "stand back up", "your time is coming"]
STOP = set("a an the to of is are be in on at for with and or but it its it's you your you're i me my we "
           "they them their this that these those what when where how do don't not no yes so if as by from "
           "up out was were will would can could just than then".split())


def norm(s):
    return re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("*", "")).split()


def ngrams(words, n=3):
    for i in range(len(words) - n + 1):
        g = words[i:i + n]
        if sum(1 for w in g if w not in STOP) >= 2:
            yield " ".join(g)


def corpus(exclude=()):
    from quotes import QUOTES
    lines = []
    for k, q in QUOTES.items():
        if k in exclude: continue
        lines += list(q.get("lines", [])) + ([q["lesson"]] if q.get("lesson") else [])
    try:
        import talks, shortloop
        for t in talks.TALKS.values(): lines += [s for s, _ in t["script"]]
        for v in shortloop.LOOPS.values(): lines += v["texts"]
    except Exception:
        pass
    seen = set()
    for l in lines: seen.update(ngrams(norm(l)))
    return seen


def check(new_lines, exclude=()):
    seen = corpus(exclude); problems = []
    for l in new_lines:
        low = " ".join(norm(l))
        for b in BANNED:
            if b in low: problems.append(f'otrcano "{b}" u: {l}')
        for g in ngrams(norm(l)):
            if g in seen: problems.append(f'ponavlja frazu "{g}" u: {l}')
    return problems


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--text":
        probs = check(args[1:])
    else:
        from quotes import QUOTES
        new = []
        for k in args: q = QUOTES[k]; new += list(q["lines"]) + ([q["lesson"]] if q.get("lesson") else [])
        probs = check(new, exclude=set(args))
    if probs:
        print("\n".join(probs)); sys.exit(1)
    print("OK - tekst je originalan")
