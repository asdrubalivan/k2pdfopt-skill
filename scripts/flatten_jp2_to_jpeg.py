#!/usr/bin/env python3
"""Pre-flatten a pure-image, JPEG2000-backed PDF to a JPEG-backed PDF.

Why this exists: many k2pdfopt builds are not linked against a JPEG2000
decoder (jasper/openjpeg), so feeding a JP2-embedded PDF straight to
k2pdfopt can fail outright or silently produce blank/corrupted pages.
poppler (pdftoppm) reliably decodes JP2, so we rasterize each page through
poppler and re-wrap the JPEGs into a new PDF -- then hand *that* to
k2pdfopt instead of the original.

Only use this on pages that are genuinely image-only (see inspect_pdf.py's
"image_only" field). Rasterizing a page that carries live text would bake
that text into a picture and destroy the text layer.

Usage:
  flatten_jp2_to_jpeg.py <input.pdf> <output.pdf> [--dpi 300] [--quality 90]
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_pdf")
    parser.add_argument("output_pdf")
    parser.add_argument("--dpi", type=int, default=300, help="Rasterization DPI (match target device)")
    parser.add_argument("--quality", type=int, default=90, help="JPEG quality 1-100")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "page"
        try:
            subprocess.run(
                ["pdftoppm", "-jpeg", "-r", str(args.dpi), "-jpegopt", f"quality={args.quality}",
                 args.input_pdf, str(prefix)],
                check=True, capture_output=True, text=True, timeout=1800,
            )
        except subprocess.CalledProcessError as exc:
            print(f"pdftoppm failed: {exc.stderr}", file=sys.stderr)
            return 1
        except subprocess.TimeoutExpired:
            print("pdftoppm timed out", file=sys.stderr)
            return 1

        pages = sorted(Path(tmp).glob("page-*.jpg"), key=lambda p: _page_num(p))
        if not pages:
            print("pdftoppm produced no pages", file=sys.stderr)
            return 1

        images = [Image.open(p) for p in pages]
        first, rest = images[0], images[1:]
        first.save(args.output_pdf, save_all=True, append_images=rest)

    print(f"wrote {args.output_pdf} ({len(pages)} pages, {args.dpi} dpi, q{args.quality})")
    return 0


def _page_num(path: Path) -> int:
    # poppler names pages "page-1.jpg", "page-01.jpg", or "page-001.jpg"
    # depending on the total page count -- pull the trailing digits.
    digits = "".join(ch for ch in path.stem.split("-")[-1] if ch.isdigit())
    return int(digits) if digits else 0


if __name__ == "__main__":
    sys.exit(main())
