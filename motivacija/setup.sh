#!/bin/sh
# Priprema okruzenja za generator motivacionih klipova (pycairo, numpy, Poppins font).
set -e
python3 -c "import cairo, numpy" 2>/dev/null || pip install -q pycairo numpy
if ! fc-list | grep -qi poppins; then
  mkdir -p "$HOME/.fonts"
  for w in Bold Regular; do
    curl -sSfLo "$HOME/.fonts/Poppins-$w.ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-$w.ttf"
  done
  fc-cache -f >/dev/null
fi
echo "setup ok"
