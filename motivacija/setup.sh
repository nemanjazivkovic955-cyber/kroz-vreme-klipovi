#!/bin/sh
# Priprema okruzenja za generator motivacionih klipova (pycairo, numpy, Poppins font).
set -e
python3 -c "import cairo, numpy" 2>/dev/null || pip install -q pycairo numpy
mkdir -p "$HOME/.fonts"
for f in poppins/Poppins-Bold poppins/Poppins-Regular poppins/Poppins-SemiBold anton/Anton-Regular dmserifdisplay/DMSerifDisplay-Italic; do
  n=$(basename "$f").ttf
  [ -f "$HOME/.fonts/$n" ] || curl -sSfLo "$HOME/.fonts/$n" "https://raw.githubusercontent.com/google/fonts/main/ofl/$f.ttf"
done
fc-cache -f >/dev/null
# Blender kao Python modul (renderovanje bez ekrana: Cycles na CPU)
python3 -c "import bpy" 2>/dev/null || pip install -q bpy
echo "setup ok"

# studio: inspektor kvaliteta + izbor najjačeg trenutka
pip install -q opencv-contrib-python-headless faster-whisper 2>/dev/null || true
