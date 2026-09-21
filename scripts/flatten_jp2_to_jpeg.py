#!/usr/bin/env python3
"""Pre-flatten a pure-image, JPEG2000-backed PDF to a JPEG-backed PDF.

Why this exists: two independent reasons.

1. Many k2pdfopt builds are not linked against a JPEG2000 decoder
   (jasper/openjpeg), so feeding a JP2-embedded PDF straight to k2pdfopt
   can fail outright or silently produce blank/corrupted pages.
2. Even when k2pdfopt *can* decode it, JPEG2000 is expensive enough to
   decode that it near-reliably hangs or crawls on e-reader-class CPUs
   (both Kindle and Kobo) at render time on the device -- a problem a
   fast, successful desktop conversion will not reveal, since k2pdfopt's
   native-mode output (`-mode fw`/`tm`/`2col`) passes the original image
   data through untouched rather than re-encoding it.

poppler (pdftoppm) reliably decodes JP2, so we rasterize each page through
poppler and re-wrap the JPEGs into a new PDF -- then hand *that* to
k2pdfopt instead of the original.

Only use this when inspect_pdf.py's "image_only" OR "full_page_scan_images"
field is true. Don't use "image_only" alone as the gate -- it reads false
for a scanned book that carries an invisible OCR text layer (e.g. Internet
Archive/Scribe output), even though the page is still 100% the scanned
image visually; "full_page_scan_images" catches that case.
Rasterizing a page that carries a *real, live* text layer worth preserving
(a genuinely mixed native/typeset document with a few JPEG2000 figures)
would bake that text into a picture and destroy it -- that's the case
where neither field is true and this script should not run.

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
        # resolution= is required: PIL's PDF writer defaults to 72dpi for the
        # MediaBox if omitted, regardless of the pixels actually rasterized at
        # --dpi. Confirmed the hard way: without it, a page rasterized at
        # 300dpi got a MediaBox ~4x too large (e.g. 23x36in instead of the
        # real ~5.5x8.7in). k2pdfopt still "succeeds" on that malformed
        # input -- no crash, no error -- but its column/page-size heuristics
        # read the inflated physical size and over-split every page into
        # scrambled narrow strips.
        first.save(args.output_pdf, save_all=True, append_images=rest, resolution=args.dpi)

    print(f"wrote {args.output_pdf} ({len(pages)} pages, {args.dpi} dpi, q{args.quality})")
    return 0


def _page_num(path: Path) -> int:
    # poppler names pages "page-1.jpg", "page-01.jpg", or "page-001.jpg"
    # depending on the total page count -- pull the trailing digits.
    digits = "".join(ch for ch in path.stem.split("-")[-1] if ch.isdigit())
    return int(digits) if digits else 0


if __name__ == "__main__":
    sys.exit(main())
