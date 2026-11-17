#!/usr/bin/env bash
# Builds dist/Hands-On_Cpp_Uditha_Landekumbura.pdf.
# Two passes: the first finds the page numbers, the second prints them in the contents.
set -euo pipefail
cd "$(dirname "$0")/.."
for pass in 1 2; do
  python3 tools/build.py pdf
  node tools/render.js
  python3 tools/pages.py
done
mkdir -p dist
python3 - <<'PY'
from pypdf import PdfWriter
w = PdfWriter()
for f in ['build/cover.pdf', 'build/body.pdf']:
    w.append(f)
w.add_metadata({'/Title': 'Hands-On C++', '/Author': 'Uditha Landekumbura'})
w.write('dist/Hands-On_Cpp_Uditha_Landekumbura.pdf')
PY
pdfinfo dist/Hands-On_Cpp_Uditha_Landekumbura.pdf | grep -E 'Pages|File size'
