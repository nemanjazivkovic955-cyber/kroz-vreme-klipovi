"""STOIC RULES — YouTube Shorts verzija (isti vizuel kao TikTok, stoic/make.py).
Razlike prema TikTok verziji:
  - kraj: "Subscribe for rule #N+1" (umesto "Follow for rule #N+1")
  - ZVUK je ugrađen: sopstvena generisana tamna klavirska podloga (bez autorskih prava),
    jer se trending zvuk ne može dodati Shortu objavljenom preko Metricool-a.
    Podloga se vrti u krug bez šava (kraj prelazi u početak), udarac na 2.0 s (hook -> pravilo), 120 BPM.
  - GLAS: Kokoro TTS (am_onyx), svaki red se izgovara; trajanje segmenata prati govor (~13-15 s)
  - opis: YouTube naslov + opis (+ #shorts) u <ime>_opis.txt
Izlaz: videos/stoic_youtube/stoic_rule_yt_NN.mp4
Upotreba: python3 stoic/youtube.py 1 [2 3 ...]
"""
import os, sys, math, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "studio"))
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
    for at, g in ((M.SEG[1][0], 0.55), (M.SEG[-1][0], 0.3)):
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


TTS_DIR = os.path.join(HERE, "tts")  # Kokoro-82M (Apache 2.0, besplatno i za komercijalnu upotrebu), u .gitignore
TTS_URL = "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main/"
VOICE, LANG, SPEED = "bm_george", "en-gb", 1.0  # izbor korisnika 19.11.: George (britanski, dubok)
LEAD, PAD, BEAT = 0.05, 0.30, 0.25
# Šablon po klipu koji je "uhvatio" (Stoic rule #1, 200 pregleda na YouTube-u, 19.11.): ~10 s, BEZ muzike, samo glas.
MUSIC = False


def tts():
    import glob
    from kokoro_onnx import Kokoro
    os.makedirs(TTS_DIR, exist_ok=True)
    mp, vp = os.path.join(TTS_DIR, "model.onnx"), os.path.join(TTS_DIR, f"voices_{VOICE}.bin")
    if not os.path.exists(mp):
        subprocess.run(["curl", "-sSfLo", mp, TTS_URL + "onnx/model_quantized.onnx"], check=True)
    if not os.path.exists(vp):
        vs = {}
        for v in (VOICE,):
            f = os.path.join(TTS_DIR, v + ".bin")
            subprocess.run(["curl", "-sSfLo", f, TTS_URL + f"voices/{v}.bin"], check=True)
            vs[v] = np.fromfile(f, dtype=np.float32).reshape(-1, 1, 256)
        np.savez(vp + ".npz", **vs); os.replace(vp + ".npz", vp)
    return Kokoro(mp, vp)


def voice_lines(r, n):
    k = tts()
    lines = [r["hook"]] + r["rule"] + ["Subscribe for the next rule."]
    clips = []
    for ln in lines:
        a, sr = k.create(ln, voice=VOICE, speed=SPEED, lang=LANG)
        assert sr == 24000
        nz = np.where(np.abs(a) > 0.01)[0]  # odseci tišinu na krajevima
        a = a[max(0, nz[0] - 240): nz[-1] + 1200]
        clips.append(a)
    return clips


# YouTube Shorts imaju SVOJ tekst i SVOJE snimke (odluka korisnika 19.11.: drugi tekst i druge scene, isti princip + glas;
# snimak se nikad ne ponavlja, pa ni TikTok snimci).
YT_FOOTAGE = {
    1: {"hook": "Your whole life is decided here.",
        "rule": ["Every day you stand at a crossroads.", "Small steps decide where you end up.", "One light is enough to start."],
        "caption": "Every big change started with one small step. What step are you taking today?",
        "tags": "#stoicism #mindset #discipline #motivation #decisions",
        "loop": ("mk_1966", 0.50, 5.0), "loop_extra": "eq=gamma=1.1",          # dim (crno-belo) - energija koja se troši
        "shots": [("mk_4000", 0.55, 2.0),                                       # raskrsnica odozgo - svet koji ne kontrolišeš
                  ("mk_4893", 0.50, 0.5),                                       # koraci - tvoj odgovor
                  ("mk_3458", 0.50, 2.0, "eq=gamma=1.3")]},                    # sveća se pali u mraku - tvoja moć
    2: {"hook": "Strong people need this more than friends.",
        "rule": ["The crowd will always be loud.", "Real peace is found alone.", "Learn to enjoy your own company."],
        "caption": "Being alone is not the same as being lonely. When do you feel most at peace?",
        "tags": "#stoicism #mindset #discipline #motivation #solitude",
        "loop": ("mk_151", 0.42, 5.0),                                          # silueta čoveka kraj prozora - tiha snaga
        "shots": [("mk_4185", 0.50, 0.5),                                       # gomila na festivalu - "svima"
                  ("mk_3350", 0.62, 2.0),                                       # mesec nad šumom - tišina
                  ("mk_3438", 0.50, 2.0)]},                                    # sveće izbliza - kontrola
    3: {"hook": "This is quietly stealing your happiness.",
        "rule": ["Everyone is running their own race.", "Comparing yourself makes you a copy.", "Shine in your own light."],
        "caption": "Your only competition is who you were yesterday. Who do you catch yourself comparing to?",
        "tags": "#stoicism #mindset #discipline #motivation #selfworth",
        "loop": ("mk_4231", 0.50, 5.0),                                         # gomila pod kišobranima - tuđa mišljenja
        "shots": [("mk_4154", 0.50, 1.0),                                       # pokretne stepenice, prolaznici
                  ("mk_1038", 0.50, 1.0, "eq=gamma=1.1"),                      # čovek u snopu svetla - karakter
                  ("mk_3463", 0.50, 2.0)]},                                    # varnice - fokus
    4: {"hook": "Comfort is slowly ruining you.",
        "rule": ["Easy days build weak minds.", "Cold, hard roads build strength.", "Keep moving when it hurts."],
        "caption": "Growth lives on the other side of comfort. What hard thing are you avoiding?",
        "tags": "#stoicism #mindset #discipline #motivation #mentaltoughness",
        "loop": ("mk_1967", 0.50, 5.0), "loop_extra": "eq=gamma=1.2",          # dim se uvija - iluzija motivacije
        "shots": [("mk_3465", 0.50, 2.0),                                       # žar pada i gasi se - motivacija bledi
                  ("mk_3352", 0.50, 1.0),                                       # sneg pada u šumi - uslovi loši, ipak
                  ("mk_719", 0.45, 3.0)]},                                     # trkač dolazi kroz šumu - budi taj koji se pojavi
}


def footage(r):
    return [r["loop"][0]] + [s[0] for s in r["shots"]]


def make(n, voice=True):
    r = dict(RULES[n]); r.update(YT_FOOTAGE.get(n, {}))
    if n in YT_FOOTAGE and "loop_extra" not in YT_FOOTAGE[n]: r.pop("loop_extra", None)
    M.RULES[n] = r  # make.py čita M.RULES
    import footage as FG
    FG.check(f"yt_short_{n:02d}", footage(r))
    os.makedirs(OUT, exist_ok=True)
    M.CTA = "Subscribe for the next rule"
    M.SHOW_TEXT = True  # tekst preko ekrana i uz glas (odluka korisnika 19.11.)
    M.SHOW_TAG = False  # bez broja dela gore: Shorts se ubacuju bilo kojim redom
    M.OUT = M.TMP  # tihu međuverziju drži u stoic/out
    vtrack = None
    if voice:
        clips = voice_lines(r, n)
        segs, t = [], 0.0
        for i, a in enumerate(clips):  # segment = govor + predah, zaokruženo na udarac (120 BPM)
            d = max(2.0 if i == 0 else 1.25, math.ceil((LEAD + len(a) / 24000 + PAD) / BEAT) * BEAT)
            segs.append((t, t + d)); t += d
        M.SEG, M.TOTAL = segs, t
        M.WORD = 0.22
        vtrack = np.zeros(int(t * 24000) + 24000)
        for (s0, _), a in zip(segs, clips):
            i0 = int((s0 + LEAD) * 24000); vtrack[i0:i0 + len(a)] += a
        vtrack = vtrack[:int(t * 24000)]
    silent = M.make(n)
    wav = os.path.join(M.TMP, f"yt{n}.wav")
    pick = None
    if voice and not MUSIC:
        pass
    else:
      try:  # muzički inspektor: Mixkit numera po scenama i temi; ako ne uspe -> generisana podloga
        import music_inspector as MI
        txts = [r["hook"]] + r["rule"] + ["Subscribe for the next rule."]
        pick = MI.choose(f"short_{n:02d}", [(a, b, t) for (a, b), t in zip(M.SEG, txts)], silent, voice=voice)
        if pick: MI.cut(pick, wav, M.TOTAL, fade_in=0.15, fade_out=0.8)
      except Exception as e:
        print("muzički inspektor nije uspeo:", e); pick = None
      if not pick: music(wav, n, M.TOTAL)
      else: print(f"muzika: {pick['title']} (mixkit {pick['id']}) od {pick['offset']:.1f}s")
    out = os.path.join(OUT, f"stoic_rule_yt_{n:02d}.mp4")
    if vtrack is not None and not MUSIC:  # samo glas
        vw = os.path.join(M.TMP, f"yt{n}_voice.wav")
        with wave.open(vw, "w") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes((vtrack / (np.abs(vtrack).max() + 1e-9) * 0.9 * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", silent, "-i", vw, "-af",
                        "aresample=48000,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
                        "aecho=0.8:0.5:40|75:0.12|0.07,pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=7",
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                        "-t", f"{M.TOTAL}", "-movflags", "+faststart", out], check=True)
    elif vtrack is not None:
        vw = os.path.join(M.TMP, f"yt{n}_voice.wav")
        with wave.open(vw, "w") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes((vtrack / (np.abs(vtrack).max() + 1e-9) * 0.9 * 32767).astype(np.int16).tobytes())
        fc = ("[2:a]aresample=44100,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
              "aecho=0.8:0.5:40|75:0.12|0.07,volume=1.0,asplit[v1][v2];"
              "[1:a]volume=0.40[m];[m][v1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=300[md];"
              "[md][v2]amix=inputs=2:weights='1 1.6':normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]")
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", silent, "-i", wav, "-i", vw,
                        "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{M.TOTAL}", "-movflags", "+faststart", out], check=True)
    else:
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", silent, "-i", wav,
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    title = f"Stoic Rule: {r['hook'].rstrip('.')} #shorts"
    desc = (f"{r['caption']}\n\nStoic rule: {' '.join(r['rule'])}\n\n"
            f"Subscribe for the next rule — one stoic rule every day.\n\n{r['tags']} #shorts\n")
    open(out.replace(".mp4", "_opis.txt"), "w").write(f"NASLOV: {title}\n\nOPIS:\n{desc}")
    FG.register(f"yt_short_{n:02d}", footage(r))
    print(out)
    return out, title, desc


if __name__ == "__main__":
    for x in sys.argv[1:] or [str(k) for k in RULES]:
        make(int(x))
