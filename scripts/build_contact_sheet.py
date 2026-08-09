#!/usr/bin/env python3
"""Arrange sampled page renders into a grid "contact sheet" so a whole
sample can be visually reviewed as 1-3 images instead of N separate Read
calls -- the same token-efficiency goal as the sampling math itself,
applied to the review step.

Usage:
  build_contact_sheet.py <outdir-with-page-*.png> <sheet-out-prefix>
                          [--cols 6] [--thumb-width 260] [--per-sheet 24]
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_NUM_RE = re.compile(r"page-(\d+)-")


def label_for(path: Path) -> str:
    m = PAGE_NUM_RE.search(path.name)
    return f"p{int(m.group(1))}" if m else path.stem


def build_sheet(images: list[Path], cols: int, thumb_width: int, out_path: Path) -> None:
    thumbs = []
    for p in images:
        im = Image.open(p).convert("RGB")
        ratio = thumb_width / im.width
        im = im.resize((thumb_width, int(im.height * ratio)))
        thumbs.append((label_for(p), im))

    row_h = max(im.height for _, im in thumbs) + 24  # room for label
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_width, rows * row_h), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except OSError:
        font = ImageFont.load_default()

    for i, (label, im) in enumerate(thumbs):
        col, row = i % cols, i // cols
        x, y = col * thumb_width, row * row_h
        sheet.paste(im, (x, y + 20))
        draw.text((x + 4, y), label, fill="red", font=font)

    sheet.save(out_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("indir", help="Directory containing page-*.png files (from rasterize_pages.py)")
    parser.add_argument("out_prefix", help="Output path prefix, e.g. /tmp/sheet -> /tmp/sheet-1.png, -2.png, ...")
    parser.add_argument("--cols", type=int, default=6)
    parser.add_argument("--thumb-width", type=int, default=260)
    parser.add_argument("--per-sheet", type=int, default=24)
    args = parser.parse_args()

    def sort_key(p: Path) -> int:
        m = PAGE_NUM_RE.search(p.name)
        return int(m.group(1)) if m else 0

    images = sorted(Path(args.indir).glob("page-*.png"), key=sort_key)
    if not images:
        print("no page-*.png files found", file=sys.stderr)
        return 1

    sheets = []
    for i in range(0, len(images), args.per_sheet):
        chunk = images[i : i + args.per_sheet]
        out_path = Path(f"{args.out_prefix}-{i // args.per_sheet + 1}.png")
        build_sheet(chunk, args.cols, args.thumb_width, out_path)
        sheets.append(str(out_path))

    print("\n".join(sheets))
    return 0


if __name__ == "__main__":
    sys.exit(main())
