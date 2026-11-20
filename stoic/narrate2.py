"""Naracija v2 (bez prekida): ceo PASUS se izgovara odjednom (prirodan tok), granice rečenica se nalaze iz pauza u zvuku.
Bez agresivnog sečenja ivica, bez eha. Izlaz: voice.wav (24 kHz) + timing.json istog oblika kao narrate.py.
Upotreba: python3 stoic/narrate2.py <scenario.md> <izlazni_folder> [glas]   (podrazumevano bm_fable)"""
import os, sys, re, json, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import youtube as YT
from narrate import parse
from kokoro_onnx import Kokoro
SR, PARA, CHAP = 24000, 0.75, 1.6


def voices(names):
    vs = {}
    for v in names:
        f = os.path.join(YT.TTS_DIR, v + ".bin")
        if not os.path.exists(f):
            import subprocess; subprocess.run(["curl", "-sSfLo", f, YT.TTS_URL + f"voices/{v}.bin"], check=True)
        vs[v] = np.fromfile(f, dtype=np.float32).reshape(-1, 1, 256)
    p = os.path.join(YT.TTS_DIR, "v2_voices.npz"); np.savez(p, **vs); os.replace(p, p[:-4] + ".bin")
    return Kokoro(os.path.join(YT.TTS_DIR, "model.onnx"), p[:-4] + ".bin")


def boundaries(a, sents):
    """Granice rečenica = pauze u zvuku najbliže očekivanim mestima (po broju slova)."""
    if len(sents) == 1: return [0.0, len(a) / SR]
    win = int(0.02 * SR); env = np.sqrt(np.convolve(a ** 2, np.ones(win) / win, "same"))
    quiet = env < max(0.008, 0.06 * np.percentile(env, 95))
    gaps, i = [], 0  # tihi odsečci duži od 120 ms
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if (j - i) / SR > 0.12: gaps.append(((i + j) / 2 / SR, (j - i) / SR))
            i = j
        else: i += 1
    tot = len(a) / SR; L = [len(s) for s in sents]; cum = np.cumsum(L)[:-1] / sum(L)
    cuts, used = [], set()
    for frac in cum:
        exp = frac * tot
        cand = [(abs(g - exp) - 0.3 * dur, g) for g, dur in gaps if g not in used and (not cuts or g > cuts[-1])]
        g = min(cand)[1] if cand else exp
        used.add(g); cuts.append(g)
    return [0.0] + cuts + [tot]


def main(md, out, voice="bm_fable", speed=0.86):
    os.makedirs(out, exist_ok=True)
    k = voices([voice]); chapters = parse(md); t = 0.0; voice_parts = []; tl = []
    for ch in chapters:
        c0 = t; paras = []
        for p in ch["paras"]:
            sents = [s.strip() for s in re.findall(r"[^.?!:]+[.?!:]+", p) if s.strip()] or [p]
            a, sr = k.create(" ".join(sents), voice=voice, speed=speed, lang="en-gb" if voice.startswith("b") else "en-us")
            nz = np.where(np.abs(a) > 0.002)[0]; a = a[max(0, nz[0] - 1200): nz[-1] + 4800]   # blago sečenje, rep ostaje
            b = boundaries(a, sents)
            ss = [{"t0": round(t + b[i], 3), "t1": round(t + b[i + 1], 3), "text": s} for i, s in enumerate(sents)]
            voice_parts.append((t, a)); t += len(a) / SR + PARA
            paras.append({"t0": ss[0]["t0"], "t1": round(t, 3), "sentences": ss})
        t += CHAP
        tl.append({"chapter": ch["title"], "scene": ch["scene"], "t0": round(c0, 3), "t1": round(t, 3), "paras": paras})
        print(f"{int(c0 // 60)}:{int(c0 % 60):02d} {ch['title']}", flush=True)
    total = t + 1.5
    vt = np.zeros(int(total * SR))
    for s0, a in voice_parts:
        i = int(s0 * SR); n = len(a); f = np.ones(n); r = int(0.01 * SR); f[:r] = np.linspace(0, 1, r); f[-r:] = np.linspace(1, 0, r)
        vt[i:i + n] += a * f
    with wave.open(os.path.join(out, "voice.wav"), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((vt / (np.abs(vt).max() + 1e-9) * 0.9 * 32767).astype(np.int16).tobytes())
    json.dump({"total": round(total, 3), "voice": voice, "chapters": tl}, open(os.path.join(out, "timing.json"), "w"), indent=1, ensure_ascii=False)
    print(f"UKUPNO {int(total // 60)}:{int(total % 60):02d}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], *(sys.argv[3:4] or []))
