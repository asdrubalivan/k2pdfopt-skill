#!/usr/bin/env python3
"""Check whether a converted PDF's file size is reasonable for its page
count -- catches the "image-only book got shipped with far too much DPI
or quality" failure mode called out in reference/quality-checklist.md.

Usage:
  check_output_weight.py <pdf> [--max-kb-per-page 180] [--image-only]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def get_page_count(pdf: str) -> int:
    proc = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, timeout=30)
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError("pdfinfo did not report a page count")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument("--max-kb-per-page", type=float, default=180.0,
                         help="Threshold for image-only books (see quality-checklist.md)")
    parser.add_argument("--image-only", action="store_true",
                         help="Set when the source is a scanned/image-only book; "
                              "text-reflow output has no meaningful threshold here.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.is_file():
        print(json.dumps({"ok": False, "error": f"not a file: {args.pdf}"}))
        return 1

    try:
        pages = get_page_count(args.pdf)
    except RuntimeError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1

    size_bytes = pdf_path.stat().st_size
    kb_per_page = (size_bytes / 1024) / max(pages, 1)

    result = {
        "ok": True,
        "page_count": pages,
        "file_size_bytes": size_bytes,
        "kb_per_page": round(kb_per_page, 1),
        "max_kb_per_page": args.max_kb_per_page,
        "image_only": args.image_only,
    }
    if args.image_only:
        result["too_heavy"] = kb_per_page > args.max_kb_per_page
    else:
        result["too_heavy"] = None
        result["note"] = "Threshold only applies to image-only output; skip this check for reflowed text."

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
