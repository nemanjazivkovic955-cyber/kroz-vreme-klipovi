"""Serija inspirativnih govora za TikTok (9:16) i YouTube (16:9): svaki video drugaciji vizuelni svet,
isti stil - dubok glas (Kokoro), elegantni titlovi (DM Serif Italic, zlatne kljucne reci), prava muzika (Mixkit),
meki prelazi, filmski kolor, zavrsna kartica.
Upotreba: python3 talks.py <ime> [9x16|16x9]     imena: water, city, climb, storm
"""
import os, sys, re, subprocess
import numpy as np
import produce as P
import water as Wt

HERE = P.HERE
BROLL = os.path.join(HERE, "..", "motivacija", "broll")
TTS = "/home/user/tts"
XF = 0.7

TALKS = {
    "city": {
        "title": "WHILE THEY SLEEP", "music": "mixkit_88.mp3", "music_start": 0,
        "shots": ["S:03_midnight", "B:city_11390239", "S:09_typing", "S:10_overtime", "B:car_30028386",
                  "B:power_phone_8345041", "S:11_exhausted", "B:power_man_8345155", "S:20_burj", "B:money_19713848"],
        "script": [("While they sleep...", 0.6), ("you build.", 1.0), ("While they scroll...", 0.5), ("you work.", 1.0),
                   ("Nobody sees the late nights.", 0.4), ("Nobody claps for the quiet hours.", 0.9),
                   ("But every hour you give...", 0.4), ("is a brick in a house they will never understand.", 1.2),
                   ("So stay quiet.", 0.5), ("Stay focused.", 0.5), ("Let the results speak.", 0.0)],
        "key": {"sleep", "build", "work", "nights", "quiet", "hour", "brick", "focused", "results"},
    },
    "climb": {
        "title": "THE CLIMB", "music": "mixkit_350.mp3", "music_start": 0,
        "shots": ["B:mountains_11856435", "B:nature_39657533", "B:snow_6650177", "B:road_16535478",
                  "B:nature_38840179", "B:travel_8970213", "B:sunset_5189814", "B:stars_5747525"],
        "script": [("The mountain doesn't care how you feel.", 0.6), ("It doesn't get smaller...", 0.3),
                   ("because you're tired.", 1.0), ("You get stronger...", 0.3), ("because you keep climbing.", 1.0),
                   ("Every step is heavy.", 0.4), ("Every breath is hard.", 0.9),
                   ("But the view at the top...", 0.4), ("belongs only to the ones who didn't turn back.", 1.2),
                   ("Keep climbing.", 0.0)],
        "key": {"mountain", "feel", "smaller", "tired", "stronger", "climbing", "step", "view", "top", "back"},
    },
    "storm": {
        "title": "THE STORM", "music": "mixkit_679.mp3", "music_start": 6,
        "shots": ["B:lightning_5387436", "B:waves_8438341", "B:rain_18222676", "B:waves_12136143",
                  "B:nature_34769638", "B:lightning_5387436", "B:waves_8438341", "B:nature_30370640"],
        "script": [("Calm seas never made a strong sailor.", 0.9), ("The storm is not here to break you.", 0.5),
                   ("It's here to show you...", 0.3), ("what you're made of.", 1.0),
                   ("So let it rain.", 0.4), ("Let it thunder.", 0.9),
                   ("Stand in the middle of it...", 0.4), ("and don't move.", 1.1),
                   ("Because storms don't last forever.", 0.5), ("But you will.", 0.0)],
        "key": {"calm", "strong", "storm", "break", "made", "rain", "thunder", "middle", "move", "forever", "will"},
    },
}


def voice(name, script):
    sys.path.insert(0, TTS)
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(TTS, "kokoro-v1.0.onnx"), os.path.join(TTS, "voices-v1.0.bin"))
    sr = 24000; t = 1.5; segs = []; parts = []
    for txt, gap in script:
        s, _ = k.create(txt, voice="am_onyx", speed=0.88, lang="en-us")
        segs.append((round(t, 2), round(t + len(s) / sr, 2), txt)); parts.append((t, s)); t += len(s) / sr + gap
    total = t + 5.0
    out = np.zeros(int(total * sr))
    for st, s in parts: i = int(st * sr); out[i:i + len(s)] += s
    wav = os.path.join(P.TMP, f"talk_{name}.wav"); sf.write(wav, out, sr)
    return wav, segs, total


def chunks(segs, key):
    out = []
    for a, b, txt in segs:
        w = txt.split(); pieces = []
        while len(w) > 5: pieces.append(" ".join(w[:4])); w = w[4:]
        pieces.append(" ".join(w))
        tot = sum(len(p) for p in pieces); x = a
        for p in pieces:
            d = (b - a) * len(p) / tot
            m = " ".join(f"*{q}*" if re.sub(r"[^a-z']", "", q.lower()) in key else q for q in p.split())
            out.append((round(x, 2), round(x + d, 2), m)); x += d
    return out


def seg(i, ref, d, W, H, tag):
    kind, n = ref.split(":")
    src = os.path.join(BROLL if kind == "B" else P.SRC, n + ".mp4"); L = P.dur(src)
    st = max(0.0, min(L * (0.2 + 0.1 * (i % 4)), L - d - 0.1))
    out = os.path.join(P.TMP, f"t_{tag}_{W}_{i:02d}.mp4")
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={P.FPS},"
          f"scale=w='{W}*(1+0.06*t/{d})':h=-2:eval=frame,crop={W}:{H},setsar=1,{Wt.GRADE},vignette=PI/5,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{st:.2f}", "-t", f"{d:.2f}", "-i", src,
                    "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", out], check=True)
    return out


def make(name, fmt="9x16"):
    v = TALKS[name]
    W, H = (1080, 1920) if fmt == "9x16" else (1920, 1080)
    wav, segs, total = voice(name, v["script"])
    end_len = 5.5
    card_start = segs[-1][0] - 0.3
    n = len(v["shots"])
    d = (card_start + XF * (n - 1)) / n
    parts = [seg(i, r, d, W, H, name) for i, r in enumerate(v["shots"])]
    parts.append(P.card_clip(os.path.join(P.TMP, f"t_{name}_end_{W}.mp4"), end_len, W, H, v["title"], "SHARE  •  LIKE  •  COMMENT FOR MORE"))
    durs = [d] * n + [end_len]
    inputs = sum([["-i", p] for p in parts], []); fc = ""; last = "0:v"; t = durs[0]
    for i in range(1, len(parts)):
        off = t - XF
        fc += f"[{last}][{i}:v]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}];"
        last = f"x{i}"; t = off + durs[i]
    total = round(t, 2)
    base = os.path.join(P.TMP, f"t_{name}_base_{W}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y"] + inputs + ["-filter_complex", fc.rstrip(";"),
                    "-map", f"[{last}]", "-c:v", "libx264", "-preset", "fast", "-crf", "16", base], check=True)
    ov = os.path.join(P.TMP, f"t_{name}_cap_{W}.mov")
    Wt.elegant_overlay(chunks(segs, v["key"]), total, W, H, ov)
    music = os.path.join(HERE, "music", v["music"])
    out = os.path.join(P.OUTDIR, f"talk_{name}_{fmt}.mp4"); tmp_out = out + ".part.mp4"
    fc = (f"[0:v][1:v]overlay=format=auto,noise=alls=5:allf=t,format=yuv420p[v];"
          f"[2:a]aresample=48000,highpass=f=70,equalizer=f=180:t=q:w=1:g=3,equalizer=f=3200:t=q:w=1.2:g=2.5,"
          f"equalizer=f=7500:t=q:w=1:g=-2,acompressor=threshold=-22dB:ratio=3.5:attack=8:release=160:makeup=3,"
          f"aecho=0.85:0.55:45|90|160:0.18|0.12|0.07,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{total},asplit=2[vo][sc];"
          f"[3:a]aresample=48000,atrim=start={v['music_start']}:duration={total},asetpts=PTS-STARTPTS,volume=0.9,"
          f"afade=t=in:d=2,afade=t=out:st={total - 4.5}:d=4.5[mu];"
          f"[mu][sc]sidechaincompress=threshold=0.04:ratio=4:attack=40:release=700:makeup=1[duck];"
          f"[vo][duck]amix=inputs=2:weights='1 0.85':normalize=0,loudnorm=I=-14:TP=-1.2:LRA=9[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", base, "-i", ov, "-i", wav, "-i", music,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "9M", "-bufsize", "18M",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", tmp_out], check=True)
    os.replace(tmp_out, out)  # nikad poluzavrsen fajl pod pravim imenom
    print("OK", os.path.abspath(out), total)


if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "9x16")
