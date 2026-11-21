import sys, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
voice, out = sys.argv[1], sys.argv[2]
lines = sys.argv[3:]
for i, t in enumerate(lines):
    s, sr = k.create(t, voice=voice, speed=0.88, lang="en-us")
    sf.write(f"{out}_{i}.wav", s, sr); print(i, round(len(s)/sr, 2), "s")
