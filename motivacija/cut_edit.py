"""Kratki klipovi (bez teksta) za "Sync to beat" montazu u TikTok/YouTube: novac, kola, zene/luksuz, moc.
Svaki izvor -> 1 ili 2 isecka od LEN sekundi, isti luksuzni kolor (kontrast, topli zlatni tonovi, vinjeta).
Upotreba: python3 cut_edit.py [LEN]
"""
import os, subprocess, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "videos", "shorts", "rich_edit")
LEN = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
GROUPS = {
    "kola": ["car_39371057", "car_39371052", "car_40965920", "car_40061525", "car_32779590", "car_39421363", "car_35353790", "car_30028386"],
    "novac": ["money_6266251", "money_6326861", "money_7735913", "money_19713848", "money_30351567", "money_31030553"],
    "zene_luksuz": ["lux_woman_3402880", "lux_woman_4691250", "lux_woman_37572083", "lux_woman_31767702"],
    "moc": ["power_jet_29470443", "power_jet_35168475", "power_flight_6700180", "power_man_8345155", "power_phone_8345041", "city_11390239"],
}
GRADE = ("eq=contrast=1.15:saturation=0.92:brightness=-0.02,"
         "colorbalance=rs=-0.03:bs=0.04:rh=0.06:gh=0.025:bh=-0.06,vignette=PI/5")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


os.makedirs(OUT, exist_ok=True)
made = []
for g, names in GROUPS.items():
    n = 0
    for name in names:
        src = os.path.join(HERE, "broll", name + ".mp4")
        d = dur(src)
        starts = [max(0.3, d * 0.25 - LEN / 2)] if d < LEN * 3 else [d * 0.2, d * 0.62]
        for s in starts:
            if s + LEN > d: s = max(0, d - LEN)
            n += 1
            out = os.path.join(OUT, f"{g}_{n:02d}.mp4")
            subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{s:.2f}", "-t", str(LEN), "-i", src,
                            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30," + GRADE,
                            "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", out], check=True)
            made.append(os.path.basename(out))
print(len(made), "klipova:", " ".join(made))
