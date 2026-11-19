"""Naracija scenarija (.md) glasom George: svaka rečenica -> TTS, izlaz voice.wav + timing.json (poglavlja, pasusi, rečenice, scene).
Upotreba: python3 stoic/narrate.py stoic/scripts/long_ep02_marcus_aurelius.md stoic/out/ep02
"""
import os, sys, re, json, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import youtube as YT
SR, GAP, PARA, CHAP = 24000, 0.38, 0.35, 1.2


def parse(md):
    chapters, cur = [], None
    for line in open(md, encoding="utf8"):
        l = line.strip()
        m = re.match(r"## (\d+:\d+) — (.+)", l)
        if m:
            cur = {"title": m.group(2), "scene": "", "paras": []}; chapters.append(cur); continue
        if not cur or not l or l.startswith(("#", "---", "Glas", "Činjenice")): continue
        if l.startswith("[SCENA"): cur["scene"] = l.strip("[]").replace("SCENA: ", ""); continue
        cur["paras"].append(l)
    return chapters


def main(md, out):
    os.makedirs(out, exist_ok=True)
    k = YT.tts(); chapters = parse(md); t = 0.0; voice = []; tl = []
    for ci, ch in enumerate(chapters):
        c0 = t; paras = []
        for pi, p in enumerate(ch["paras"]):
            sents = [s.strip() for s in re.findall(r"[^.?!:]+[.?!:]+", p) if s.strip()] or [p]
            ss = []
            for s in sents:
                a, sr = k.create(s, voice=YT.VOICE, speed=0.95, lang=YT.LANG)
                nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 240): nz[-1] + 1200]
                voice.append((t, a)); ss.append({"t0": round(t, 3), "t1": round(t + len(a) / SR, 3), "text": s})
                t += len(a) / SR + GAP
            t += PARA; paras.append({"t0": ss[0]["t0"], "t1": round(t, 3), "sentences": ss})
        t += CHAP
        tl.append({"chapter": ch["title"], "scene": ch["scene"], "t0": round(c0, 3), "t1": round(t, 3), "paras": paras})
        print(f"{int(c0 // 60)}:{int(c0 % 60):02d} {ch['title']}", flush=True)
    total = t + 1.5
    vt = np.zeros(int(total * SR))
    for s0, a in voice:
        i = int(s0 * SR); vt[i:i + len(a)] += a
    with wave.open(os.path.join(out, "voice.wav"), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((vt / (np.abs(vt).max() + 1e-9) * 0.9 * 32767).astype(np.int16).tobytes())
    json.dump({"total": round(total, 3), "chapters": tl}, open(os.path.join(out, "timing.json"), "w"), indent=1, ensure_ascii=False)
    print(f"UKUPNO {int(total // 60)}:{int(total % 60):02d}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
