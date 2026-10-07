#!/usr/bin/env bash
# Builds the two formula booklets and checks every formula and number in them.
# Usage: ./build.sh                     (both booklets + checks)
#        ./build.sh quantum-chemistry   (one booklet)
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$PWD
BUILD=$ROOT/build
OUT=$ROOT/pdf
mkdir -p "$BUILD" "$OUT"

declare -A NAME=([quantum-chemistry]=Formula-Booklet_Quantum-Chemistry
                 [physics]=Formula-Booklet_Physics)
BOOKS=(quantum-chemistry physics)
[ $# -gt 0 ] && BOOKS=("$@")

for b in "${BOOKS[@]}"; do
  [ -n "${NAME[$b]:-}" ] || { echo "unknown booklet: $b"; exit 1; }
  echo "== $b"
  (cd src && for pass in 1 2; do
     pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" "$b.tex" \
       > "$BUILD/$b.stdout" 2>&1 \
       || { echo "!! $b failed, see $BUILD/$b.log"; tail -30 "$BUILD/$b.log"; exit 1; }
   done)
  echo "   overfull boxes: $(grep -c Overfull "$BUILD/$b.log" || true)"
  cp "$BUILD/$b.pdf" "$OUT/${NAME[$b]}.pdf"
done

if [ $# -eq 0 ]; then
  echo "== checks"
  python3 tools/check_formulas.py | tail -1
fi
