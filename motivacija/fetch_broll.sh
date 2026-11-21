#!/bin/sh
# Ulaz: fajl sa redovima "ime url". Preuzima, svodi na 1080x1920 bez zvuka (max 40 s) u broll/<ime>.mp4.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)/broll"
TMPD="$(mktemp -d)"
while read -r name url; do
  [ -z "$name" ] && continue
  [ -f "$DIR/$name.mp4" ] && { echo "skip $name"; continue; }
  curl -sSfo "$TMPD/$name.src" "$url"
  ffmpeg -nostdin -loglevel error -y -i "$TMPD/$name.src" -t 30 -an \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
    -c:v libx264 -preset veryfast -crf 24 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -movflags +faststart "$DIR/$name.mp4"
  rm -f "$TMPD/$name.src"
  echo "ok $name $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$DIR/$name.mp4")"
done < "$1"
rmdir "$TMPD" 2>/dev/null || true
