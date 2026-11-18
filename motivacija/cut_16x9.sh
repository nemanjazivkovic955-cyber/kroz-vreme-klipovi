#!/bin/sh
# Ulaz: redovi "grupa L|P url". L = horizontalni izvor, P = uspravni (iseca se srednja traka 16:9).
# Izlaz: videos/youtube/rich_edit_16x9/<grupa>_NN.mp4, 4 s, 1920x1080, bez zvuka, luksuzni kolor.
set -e
OUT="$(cd "$(dirname "$0")/.." && pwd)/videos/youtube/rich_edit_16x9"; mkdir -p "$OUT"
TMPD="$(mktemp -d)"
GRADE="eq=contrast=1.15:saturation=0.92:brightness=-0.02,colorbalance=rs=-0.03:bs=0.04:rh=0.06:gh=0.025:bh=-0.06,vignette=PI/5"
i=0
while read -r grp kind url; do
  [ -z "$grp" ] && continue
  i=$((i+1)); src="$TMPD/s$i.mp4"
  curl -sSfo "$src" "$url"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
  if [ "$kind" = "L" ]; then VF="scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
  else VF="crop=iw:iw*9/16:0:ih*0.42-iw*9/32,scale=1920:1080"; fi
  for frac in 0.2 0.6; do
    st=$(python3 -c "d=$d;s=d*$frac;print(round(max(0,min(s,d-4.1)),2))")
    n=$(ls "$OUT" | grep -c "^${grp}_" || true); n=$((n+1)); f=$(printf "%s/%s_%02d.mp4" "$OUT" "$grp" "$n")
    ffmpeg -nostdin -loglevel error -y -ss "$st" -t 4 -i "$src" -vf "$VF,fps=30,$GRADE" -an \
      -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -movflags +faststart "$f"
    echo "ok $(basename "$f") ($kind)"
    python3 -c "import sys; sys.exit(0 if $d>=9 else 1)" || break
  done
  rm -f "$src"
done < "$1"
rm -rf "$TMPD"
