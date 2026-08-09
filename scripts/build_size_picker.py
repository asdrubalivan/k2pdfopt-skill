#!/usr/bin/env python3
"""Build a small local HTML page comparing candidate -fs (font size)
renders side by side, so the user can eyeball real rendered pages at
actual size before committing to a full-book conversion.

Usage:
  build_size_picker.py <out.html> <label1>=<image1.png> [<label2>=<image2.png> ...]

Images are embedded as data: URIs so the page is a single self-contained
file -- open it directly (e.g. `open <out.html>` on macOS).
"""
import base64
import sys
from pathlib import Path

TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><title>k2pdfopt - comparar tamaño de letra</title>
<style>
  body {{ font-family: -apple-system, sans-serif; background: #1e1e1e; color: #eee; margin: 0; padding: 24px; }}
  h1 {{ font-size: 16px; font-weight: 600; color: #aaa; margin: 0 0 20px; }}
  .row {{ display: flex; gap: 20px; align-items: flex-start; overflow-x: auto; }}
  .card {{ background: #fff; border-radius: 8px; padding: 12px; flex: 0 0 auto; }}
  .card img {{ display: block; max-width: 320px; border: 1px solid #ccc; }}
  .label {{ color: #111; font-weight: 700; margin-bottom: 8px; font-size: 14px; }}
</style></head>
<body>
<h1>Comparación de tamaño de letra -- elige la opción y dile a Claude cuál prefieres</h1>
<div class="row">
{cards}
</div>
</body></html>
"""

CARD = """  <div class="card">
    <div class="label">{label}</div>
    <img src="data:image/png;base64,{data}">
  </div>
"""


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    out_path = Path(sys.argv[1])
    cards = []
    for arg in sys.argv[2:]:
        label, _, img_path = arg.partition("=")
        data = base64.b64encode(Path(img_path).read_bytes()).decode("ascii")
        cards.append(CARD.format(label=label, data=data))

    out_path.write_text(TEMPLATE.format(cards="".join(cards)))
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
