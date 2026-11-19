"""REGISTAR SNIMAKA — pravilo korisnika (19.11.): snimak koji je jednom iskorišćen više se NIKAD ne koristi
(ni u drugoj seriji, ni na drugoj platformi, ni u dugom videu).
Izvori: studio/visual_history.json (ranije serije), stoic/rules.py (TikTok Stoic), stoic/edit.py, i
studio/footage_used.json (sve što je renderovano odavde; upisuje register()).
check(prod, ids) baca grešku ako je bilo koji snimak već korišćen u DRUGOJ produkciji.
"""
import os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
REG = os.path.join(HERE, "footage_used.json")


def norm(x):
    m = re.match(r"(mk)_(\d+)", x)
    return f"mk_{m.group(2)}" if m else x


def used():
    u = {}
    vh = os.path.join(HERE, "visual_history.json")
    if os.path.exists(vh):
        for k, v in json.load(open(vh)).items(): u.setdefault(norm(k), set()).update(v)
    sys.path.insert(0, os.path.join(ROOT, "stoic"))
    try:
        from rules import RULES
        for n, r in RULES.items():
            if n in TIKTOK_RULES:  # samo pravila koja su stvarno objavljena na TikTok-u
                for s in [r["loop"]] + r["shots"]: u.setdefault(norm(s[0]), set()).add(f"tiktok_stoic_rule_{n:02d}")
        import edit
        for n, e in edit.EDITS.items():
            for s in [e["loop"]] + e["shots"]: u.setdefault(norm(s[0]), set()).add(f"tiktok_stoic_edit_{n:02d}")
    except Exception as e:
        print("upozorenje registra:", e)
    if os.path.exists(REG):
        for prod, ids in json.load(open(REG)).items():
            for i in ids: u.setdefault(norm(i), set()).add(prod)
    return u


TIKTOK_RULES = {1, 2, 3, 4}


def check(prod, ids):
    u = used(); bad = {i: sorted(u[norm(i)] - {prod}) for i in ids if u.get(norm(i), set()) - {prod}}
    dup = {i for i in ids if ids.count(i) > 1}
    if bad or dup:
        raise SystemExit(f"[registar] {prod}: snimci već korišćeni: {bad} / ponovljeni u istom videu: {sorted(dup)}")


def register(prod, ids):
    r = json.load(open(REG)) if os.path.exists(REG) else {}
    r[prod] = sorted({norm(i) for i in ids}); json.dump(r, open(REG, "w"), indent=1)


if __name__ == "__main__":
    u = used(); print(len(u), "iskorišćenih snimaka")
