#!/usr/bin/env python3
"""Inspect a source PDF and report the facts the skill needs to branch on.

Requires poppler-utils (pdfinfo, pdffonts, pdftotext, pdfimages) on PATH.

Usage:
  inspect_pdf.py <pdf-path>

Outputs one JSON object to stdout:
  {
    "page_count": int,
    "file_size_bytes": int,
    "has_embedded_fonts": bool,
    "has_text_layer": bool,       # heuristic: real, extractable text (not just OCR noise)
    "image_only": bool,           # true if this looks like a pure scanned-image book
    "image_codecs": [str],        # distinct "enc" values seen across sampled pages
    "has_jpeg2000": bool,
    "sampled_pages_for_images": int
  }
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TEXT_SAMPLE_PAGES = 5
IMAGE_SAMPLE_PAGES = 50
MIN_CHARS_PER_PAGE_FOR_TEXT_LAYER = 20


def run(cmd: list[str]) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"failed to run {' '.join(cmd)}: {exc}") from exc
    return proc.stdout


def get_page_count(pdf: str) -> int:
    out = run(["pdfinfo", pdf])
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError("pdfinfo did not report a page count")


def has_embedded_fonts(pdf: str) -> bool:
    out = run(["pdffonts", pdf])
    lines = [l for l in out.splitlines() if l.strip()]
    # pdffonts prints a 2-line header (name row + dashes row) even with no fonts.
    return len(lines) > 2


def estimate_text_layer(pdf: str, page_count: int) -> bool:
    last_page = min(page_count, TEXT_SAMPLE_PAGES)
    with tempfile.TemporaryDirectory() as tmp:
        txt_path = Path(tmp) / "sample.txt"
        run(["pdftotext", "-f", "1", "-l", str(last_page), pdf, str(txt_path)])
        text = txt_path.read_text(errors="ignore") if txt_path.exists() else ""
    non_ws_chars = len("".join(text.split()))
    avg_per_page = non_ws_chars / max(last_page, 1)
    return avg_per_page >= MIN_CHARS_PER_PAGE_FOR_TEXT_LAYER


def get_image_codecs(pdf: str, page_count: int) -> list[str]:
    last_page = min(page_count, IMAGE_SAMPLE_PAGES)
    out = run(["pdfimages", "-list", "-f", "1", "-l", str(last_page), pdf])
    lines = [l for l in out.splitlines() if l.strip()]
    if len(lines) <= 2:
        return []
    header = lines[0].split()
    try:
        enc_idx = header.index("enc")
    except ValueError:
        return []
    codecs = set()
    for row in lines[2:]:
        cols = row.split()
        if len(cols) > enc_idx:
            codecs.add(cols[enc_idx])
    return sorted(codecs)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    pdf = sys.argv[1]
    if not Path(pdf).is_file():
        print(json.dumps({"ok": False, "error": f"not a file: {pdf}"}))
        return 1

    try:
        page_count = get_page_count(pdf)
        fonts = has_embedded_fonts(pdf)
        text_layer = estimate_text_layer(pdf, page_count)
        codecs = get_image_codecs(pdf, page_count)
    except RuntimeError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1

    has_jp2 = any("2000" in c.lower() or c.lower() == "jpx" for c in codecs)
    image_only = (not fonts) and (not text_layer)

    result = {
        "ok": True,
        "page_count": page_count,
        "file_size_bytes": Path(pdf).stat().st_size,
        "has_embedded_fonts": fonts,
        "has_text_layer": text_layer,
        "image_only": image_only,
        "image_codecs": codecs,
        "has_jpeg2000": has_jp2,
        "sampled_pages_for_images": min(page_count, IMAGE_SAMPLE_PAGES),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
