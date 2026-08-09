#!/usr/bin/env python3
"""Render specific pages of a PDF to PNG so they can be visually inspected
(e.g. via Claude Code's Read tool, which can view images).

Renders at a fixed pixel width regardless of source page size, which keeps
the image -- and therefore the token cost of looking at it -- consistent
across books with wildly different page dimensions.

Usage:
  rasterize_pages.py <pdf> <outdir> <page> [<page> ...] [--width 900]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument("outdir")
    parser.add_argument("pages", nargs="+", type=int)
    parser.add_argument("--width", type=int, default=900, help="Output pixel width")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    written = []
    for page in args.pages:
        prefix = outdir / f"page-{page:04d}"
        try:
            subprocess.run(
                ["pdftoppm", "-png", "-f", str(page), "-l", str(page),
                 "-scale-to-x", str(args.width), "-scale-to-y", "-1",
                 args.pdf, str(prefix)],
                check=True, capture_output=True, text=True, timeout=120,
            )
        except subprocess.CalledProcessError as exc:
            print(json.dumps({"ok": False, "page": page, "error": exc.stderr}), file=sys.stderr)
            continue
        except subprocess.TimeoutExpired:
            print(json.dumps({"ok": False, "page": page, "error": "timeout"}), file=sys.stderr)
            continue

        # poppler suffixes the single rendered page with -1, -01, or -001
        # depending on total page count in the source doc.
        matches = sorted(outdir.glob(f"page-{page:04d}-*.png"))
        if matches:
            written.append({"page": page, "path": str(matches[0])})

    print(json.dumps({"ok": True, "images": written}, indent=2))
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
