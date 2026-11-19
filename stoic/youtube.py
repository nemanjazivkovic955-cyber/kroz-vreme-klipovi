"""STOIC RULES — YouTube Shorts verzija (isti vizuel kao TikTok, stoic/make.py).
Razlike prema TikTok verziji:
  - kraj: "Subscribe for rule #N+1" (umesto "Follow for rule #N+1")
  - ZVUK je ugrađen: sopstvena generisana tamna klavirska podloga (bez autorskih prava),
    jer se trending zvuk ne može dodati Shortu objavljenom preko Metricool-a.
    Podloga se vrti u krug bez šava (kraj prelazi u početak), udarac na 2.0 s (hook -> pravilo), 120 BPM.
  - opis: YouTube naslov + opis (+ #shorts) u <ime>_opis.txt
Izlaz: videos/stoic_youtube/stoic_rule_yt_NN.mp4
Upotreba: python3 stoic/youtube.py 1 [2 3 ...]
"""
import os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make as M
from rules import RULES

OUT = os.path.join(ROOT, "videos", "stoic_youtube")
SR = 44100
# a-mol, po pravilu (seed = broj pravila) bira se drugi redosled akorda -> svaki Short ima svoju podlogu
CHORDS = {"Am": [45, 52, 57, 60, 64], "F": [41, 48, 53, 57, 60], "C": [36, 43, 48, 52, 55],
          "G": [43, 50, 55, 59, 62], "Dm": [38, 45, 50, 53, 57], "Em": [40, 47, 52, 55, 59]}
PROGS = [["Am", "F", "C", "G"], ["Am", "Dm", "F", "Em"], ["Am", "F", "Dm", "Em"], ["Am", "C", "G", "F"], ["Am", "Em", "F", "G"]]


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)


def piano(f, d, vel):
    t = np.arange(int(d * SR)) / SR
    x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.6 + k * 0.9)) for k, a in ((1, 1.0), (2, 0.35), (3, 0.12), (4, 0.05)))
    return x * np.minimum(1, t / 0.004) * vel


def music(path, n, dur):
    """Ciklična podloga tačno dur sekundi: sve što pređe kraj vraća se na početak (loop bez šava)."""
    N = int(dur * SR); out = np.zeros(N)
    def add(sig, start):
        i0 = int(start * SR) % N
        idx = (np.arange(len(sig)) + i0) % N
        np.add.at(out, idx, sig)
    prog = PROGS[(n - 1) % len(PROGS)]
    beat = 0.5; bar = beat * 4  # 120 BPM -> takt 2 s = jedan segment teksta
    rng = np.random.default_rng(n)
    for b in range(int(round(dur / bar))):
        ch = CHORDS[prog[b % 4]]; t0 = b * bar
        # pad: tihi niski akord (bas + kvinta), dug, meki
        tt = np.arange(int(bar * 1.6 * SR)) / SR
        env = np.minimum(1, tt / 0.6) * np.exp(-tt * 0.55)
        pad = sum(np.sin(2 * np.pi * hz(m) * tt) * g for m, g in ((ch[0] - 12, 0.20), (ch[0], 0.10), (ch[1], 0.06))) * env
        add(pad, t0)
        # klavir: retke note na udarcima (1, 2.5, 3, 4)
        for k, pos in enumerate((0.0, 1.5, 2.0, 3.0)):
            m = ch[2 + (k + int(rng.integers(0, 2))) % 3] + 12
            add(piano(hz(m), 2.4, 0.11 if k == 0 else 0.07), t0 + pos * beat)
    # "udarac" na 2.0 s: duboki sub (hook -> pravilo) + na 9.0 s tiši (prelaz na CTA)
    for at, g in ((2.0, 0.55), (9.0, 0.3)):
        tt = np.arange(int(1.2 * SR)) / SR
        f = 55 * np.exp(-tt * 3) + 38
        add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3.2) * g, at)
    # reverb (ciklični eho) -> rep note se prelije u početak
    dry = out.copy()
    for d, g in ((0.09, 0.30), (0.19, 0.22), (0.31, 0.16), (0.47, 0.11), (0.71, 0.07)):
        out += np.roll(dry, int(d * SR)) * g
    out = np.tanh(out * 1.4)
    out = out / (np.abs(out).max() + 1e-9) * 0.8
    st = np.stack([out, np.roll(out, 240)], 1)  # blaga širina stereo slike
    with wave.open(path, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def make(n):
    r = RULES[n]
    os.makedirs(OUT, exist_ok=True)
    M.CTA = "Subscribe for rule #{n}"
    M.OUT = M.TMP  # tihu međuverziju drži u stoic/out
    silent = M.make(n)
    wav = os.path.join(M.TMP, f"yt{n}.wav"); music(wav, n, M.TOTAL)
    out = os.path.join(OUT, f"stoic_rule_yt_{n:02d}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", silent, "-i", wav,
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    title = f"Stoic Rule #{n}: {r['hook'].rstrip('.')} #shorts"
    desc = (f"{r['caption']}\n\nStoic rule #{n}: {' '.join(r['rule'])}\n\n"
            f"Subscribe for rule #{n + 1} — one stoic rule every day.\n\n{r['tags']} #shorts\n")
    open(out.replace(".mp4", "_opis.txt"), "w").write(f"NASLOV: {title}\n\nOPIS:\n{desc}")
    print(out)
    return out, title, desc


if __name__ == "__main__":
    for x in sys.argv[1:] or [str(k) for k in RULES]:
        make(int(x))
