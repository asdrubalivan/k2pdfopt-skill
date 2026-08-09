#!/usr/bin/env python3
"""Build a single-row before/after comparison image for the README from
individual page renders (e.g. produced by scripts/rasterize_pages.py).

Not part of the skill's runtime toolset (scripts/) on purpose -- this is
maintenance tooling for regenerating docs/screenshots/*.png, not something
SKILL.md's conversion flow ever invokes.

Usage:
  build_comparison_image.py <out.png> "label=path.png" [...] [--panel-width 420] [--blur RADIUS]

--blur applies a Gaussian blur to every panel in this invocation -- used to
obscure a copyrighted photo/logo while still showing the overall look
(e.g. grayscale vs. color) of a page.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CAPTION_HEIGHT = 40
PADDING = 16


def load_panel(path: str, width: int, blur: float | None) -> Image.Image:
    im = Image.open(path).convert("RGB")
    ratio = width / im.width
    im = im.resize((width, int(im.height * ratio)))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(radius=blur))
    return im


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_png")
    parser.add_argument("pairs", nargs="+", help='"label=path.png" pairs, one per panel')
    parser.add_argument("--panel-width", type=int, default=420)
    parser.add_argument("--blur", type=float, default=None, help="Gaussian blur radius applied to every panel")
    args = parser.parse_args()

    panels = []
    for pair in args.pairs:
        label, _, path = pair.partition("=")
        panels.append((label, load_panel(path, args.panel_width, args.blur)))

    row_h = max(im.height for _, im in panels)
    canvas_w = len(panels) * args.panel_width + (len(panels) + 1) * PADDING
    canvas_h = row_h + CAPTION_HEIGHT + 2 * PADDING
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except OSError:
        font = ImageFont.load_default()

    x = PADDING
    for label, im in panels:
        canvas.paste(im, (x, CAPTION_HEIGHT + PADDING))
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text((x + (args.panel_width - text_w) // 2, 8), label, fill="black", font=font)
        x += args.panel_width + PADDING

    Path(args.out_png).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.out_png)
    print(args.out_png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
