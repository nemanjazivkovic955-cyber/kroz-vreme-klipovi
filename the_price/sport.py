"""Sportski motivacioni TikTok klipovi (9:16): brzi rezovi, govor (Kokoro), titlovi, Mixkit bubnjevi.
Upotreba: python3 sport.py gym|fighter|run [9x16|16x9]
"""
import os, sys, re, json, subprocess
import numpy as np
import produce as P

HERE = P.HERE
BROLL = os.path.join(HERE, "..", "motivacija", "broll")
TTS = "/home/user/tts"

VIDEOS = {
    "gym": {
        "title": "NO EXCUSES", "music": "mixkit_466.mp3", "music_start": 4,
        "shots": [("B:workout_29569378", 1), ("B:workout_11023725", 1), ("B:workout_34901409", 1), ("B:workout_4944398", 1),
                  ("B:workout_8691730", 1), ("B:workout_29569378", 1), ("B:workout_11023725", 1), ("B:workout_4944398", 1),
                  ("B:workout_34901409", 1), ("B:workout_8691730", 1), ("B:workout_29569378", 1), ("B:workout_4944398", 1)],
        "script": [("Nobody is coming to make you strong.", 0.5), ("Every rep you skip...", 0.3),
                   ("someone else is doing.", 0.7), ("You're not tired.", 0.3), ("You're uncomfortable.", 0.7),
                   ("And comfort never built anything.", 0.7), ("So pick it up.", 0.3), ("One more rep.", 0.3),
                   ("Then one more.", 0.8), ("That's the secret.", 0.3), ("There is no secret.", 0.0)],
        "key": {"strong", "skip", "tired", "uncomfortable", "comfort", "pick", "rep", "secret"},
    },
    "fighter": {
        "title": "FIGHTER", "music": "mixkit_679.mp3", "music_start": 8,
        "shots": [("S:06_bandage", 1), ("B:workout_7314350", 1), ("S:07_boxer", 1), ("B:workout_6296377", 1),
                  ("S:08_bag", 1), ("B:workout_7187460", 1), ("B:workout_7314350", 1), ("S:07_boxer", 1),
                  ("S:08_bag", 1), ("B:workout_7187460", 1), ("B:workout_6296377", 1), ("S:06_bandage", 1)],
        "script": [("Every champion was once a beginner...", 0.3), ("who refused to quit.", 0.8),
                   ("They got hit.", 0.3), ("They fell.", 0.3), ("They got back up.", 0.8),
                   ("Pain is temporary.", 0.3), ("Pride is forever.", 0.8),
                   ("When your body says stop...", 0.4), ("your mind says: not yet.", 0.8),
                   ("Train like you're fighting for your life.", 0.4), ("Because you are.", 0.0)],
        "key": {"champion", "quit", "hit", "fell", "up", "pain", "pride", "stop", "yet", "life", "are"},
    },
    "run": {
        "title": "KEEP RUNNING", "music": "mixkit_759.mp3", "music_start": 14,
        "shots": [("S:04_runner", 1), ("B:workout_32240945", 1), ("B:workout_31939567", 1), ("B:run_19523592", 1),
                  ("B:workout_8691730", 1), ("S:04_runner", 1), ("B:workout_32240945", 1), ("B:run_19523592", 1),
                  ("B:workout_31939567", 1), ("B:workout_32240945", 1), ("S:04_runner", 1)],
        "script": [("Run when you feel like it...", 0.3), ("and run when you don't.", 0.8),
                   ("The road doesn't care how you feel.", 0.7), ("Every mile is a promise...", 0.3),
                   ("you keep to yourself.", 0.8), ("Slow is fine.", 0.3), ("Stopping isn't.", 0.8),
                   ("One day you'll look back...", 0.4), ("and see the version of you", 0.2),
                   ("that never stopped running.", 0.0)],
        "key": {"run", "don't", "road", "feel", "mile", "promise", "slow", "stopping", "isn't", "running", "you"},
    },
}

GRADE = ("eq=contrast=1.2:saturation=0.9:brightness=-0.03,"
         "colorbalance=rs=-0.04:bs=0.06:rh=0.06:gh=0.02:bh=-0.05")


def voice(name, v):
    sys.path.insert(0, TTS)
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(TTS, "kokoro-v1.0.onnx"), os.path.join(TTS, "voices-v1.0.bin"))
    sr = 24000; t = 1.0; segs = []; parts = []
    for txt, gap in v["script"]:
        s, _ = k.create(txt, voice="am_onyx", speed=0.95, lang="en-us")
        segs.append((round(t, 2), round(t + len(s) / sr, 2), txt)); parts.append((t, s)); t += len(s) / sr + gap
    total = t + 3.0
    out = np.zeros(int(total * sr))
    for st, s in parts: i = int(st * sr); out[i:i + len(s)] += s
    wav = os.path.join(P.TMP, f"sp_{name}.wav"); sf.write(wav, out, sr)
    return wav, segs, total


def chunks(segs, key):
    out = []
    for a, b, txt in segs:
        w = txt.split(); pieces = []
        while len(w) > 4: pieces.append(" ".join(w[:3])); w = w[3:]
        pieces.append(" ".join(w))
        tot = sum(len(p) for p in pieces); x = a
        for p in pieces:
            d = (b - a) * len(p) / tot
            m = " ".join(f"*{x_}*" if re.sub(r"[^a-z']", "", x_.lower()) in key else x_ for x_ in p.split())
            out.append((round(x, 2), round(x + d, 2), m)); x += d
    return out


def seg(i, ref, d, W, H, tag):
    kind, n = ref.split(":")
    src = os.path.join(BROLL if kind == "B" else P.SRC, n + ".mp4"); L = P.dur(src)
    st = max(0.0, min(L * (0.15 + 0.12 * (i % 5)), L - d - 0.1))
    out = os.path.join(P.TMP, f"sp_{tag}_{W}_{i:02d}.mp4")
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={P.FPS},"
          f"scale=w='{W}*(1+0.08*t/{d})':h=-2:eval=frame,crop={W}:{H},setsar=1,{GRADE},vignette=PI/4.5,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{st:.2f}", "-t", f"{d:.2f}", "-i", src,
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", out], check=True)
    return out


def main(name, fmt="9x16"):
    v = VIDEOS[name]
    W, H = (1080, 1920) if fmt == "9x16" else (1920, 1080)
    wav, segs, total = voice(name, v)
    end_len = 3.0
    shot_total = total - end_len
    per = shot_total / len(v["shots"])
    parts = [seg(i, ref, per, W, H, name) for i, (ref, _) in enumerate(v["shots"])]
    parts.append(P.card_clip(os.path.join(P.TMP, f"sp_{name}_end_{W}.mp4"), end_len, W, H, v["title"], "FOLLOW FOR MORE"))
    lst = os.path.join(P.TMP, f"sp_{name}_{W}.txt")
    with open(lst, "w") as f:
        for p in parts: f.write(f"file '{p}'\n")
    base = os.path.join(P.TMP, f"sp_{name}_base_{W}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", base], check=True)
    ov = os.path.join(P.TMP, f"sp_{name}_cap_{W}.mov")
    P.caption_overlay({"captions": chunks(segs, v["key"])}, total, W, H, ov)
    # SFX: udarci na rezovima (blago) + impact na pocetku i na kartici
    fx = np.zeros(int(total * P.SR) + P.SR)
    P.add(fx, 0.0, P.impact(1.6), 0.6)
    for i in range(1, len(v["shots"])): P.add(fx, i * per - 0.25, P.whoosh(0.5, i), 0.18)
    P.add(fx, shot_total, P.impact(2.0), 0.5)
    fxw = os.path.join(P.TMP, f"sp_{name}_fx.wav"); P.write_wav(fxw, fx[:int(total * P.SR)] / (np.abs(fx).max() + 1e-9) * 0.9)
    music = os.path.join(HERE, "music", v["music"])
    out = os.path.join(P.OUTDIR, f"sport_{name}_{fmt}.mp4")
    fc = (f"[0:v][1:v]overlay=format=auto,noise=alls=5:allf=t,format=yuv420p[v];"
          f"[2:a]aresample=48000,highpass=f=70,equalizer=f=170:t=q:w=1:g=3,equalizer=f=3200:t=q:w=1.2:g=3,"
          f"acompressor=threshold=-22dB:ratio=4:attack=6:release=140:makeup=3,aecho=0.85:0.5:40|80:0.12|0.07,"
          f"pan=stereo|c0=c0|c1=c0,apad,atrim=0:{total},asplit=2[vo][sc];"
          f"[3:a]aresample=48000,atrim=start={v['music_start']}:duration={total},asetpts=PTS-STARTPTS,"
          f"afade=t=in:d=0.8,afade=t=out:st={total - 2.5}:d=2.5[mu];"
          f"[mu][sc]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=500[duck];"
          f"[4:a]volume=0.7[fx];[vo][duck][fx]amix=inputs=3:weights='1 0.9 0.8':normalize=0,loudnorm=I=-13:TP=-1.0:LRA=8[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov, "-i", wav, "-i", music, "-i", fxw,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-maxrate", "9M", "-bufsize", "18M",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    print("OK", os.path.abspath(out), round(total, 1), "s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "9x16")
