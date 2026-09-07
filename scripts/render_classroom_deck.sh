#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 DECK.pptx OUT_DIR" >&2
  exit 2
fi

DECK="$1"
OUT="$2"
mkdir -p "$OUT/pdf" "$OUT/png"

if ! command -v libreoffice >/dev/null 2>&1; then
  echo "libreoffice is required" >&2
  exit 2
fi
if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "pdftoppm is required (poppler-utils)" >&2
  exit 2
fi

base="$(basename "$DECK" .pptx)"
libreoffice --headless --convert-to pdf --outdir "$OUT/pdf" "$DECK" >/tmp/classroom_lo.log 2>&1 || {
  cat /tmp/classroom_lo.log >&2
  exit 1
}
PDF="$OUT/pdf/$base.pdf"
[[ -f "$PDF" ]] || { echo "PDF was not produced: $PDF" >&2; cat /tmp/classroom_lo.log >&2; exit 1; }

pdftoppm -png -r 144 "$PDF" "$OUT/png/slide" >/tmp/classroom_pdftoppm.log 2>&1
python3 "$(dirname "$0")/make_contact_sheet.py" "$OUT/png" "$OUT/contact-sheet.png" --columns 3 --thumb-width 640

echo "Rendered: $PDF"
echo "PNGs:     $OUT/png"
echo "Contact:  $OUT/contact-sheet.png"
