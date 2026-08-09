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
    "full_page_scan_images": bool,  # true if sampled pages are dominated by one
                                     # full-page-sized image, regardless of any text
                                     # layer on top (see note below)
    "image_codecs": [str],        # distinct "enc" values seen across sampled pages
    "has_jpeg2000": bool,
    "sampled_pages_for_images": int
  }

Note on `image_only` vs `full_page_scan_images`: `image_only` answers "is there
any extractable text at all?" -- it goes false for scanned books that carry an
invisible OCR text layer (e.g. Internet Archive/Scribe output), even though the
page is visually still 100% the scanned image. `full_page_scan_images` answers
the question that actually matters for deciding whether to flatten JPEG2000
content: "is the dominant image on each sampled page roughly the size of the
whole page?" A scan-with-OCR-layer book is `image_only=false` but
`full_page_scan_images=true`. Confirmed the hard way on a real Internet
Archive/Scribe scan (JPX + JBIG2 mask per page, real OCR text layer): relying
on `image_only` alone as the JPEG2000-flatten gate misses this case and lets
the expensive codec pass straight through to k2pdfopt's native-mode output.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TEXT_SAMPLE_PAGES = 5
IMAGE_SAMPLE_PAGES = 50
MIN_CHARS_PER_PAGE_FOR_TEXT_LAYER = 20
# A sampled page counts as "full-page scan" if its largest image covers at
# least this fraction of the page area (leaves room for scan margins/borders).
FULL_PAGE_COVERAGE_THRESHOLD = 0.85
# Fraction of sampled pages-with-images that must be full-page for the whole
# document to be flagged full_page_scan_images.
FULL_PAGE_PAGE_FRACTION = 0.8


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


def get_image_rows(pdf: str, page_count: int) -> tuple[list[str], list[list[str]]]:
    """Return (header columns, data rows) from `pdfimages -list`, sampled
    over the first IMAGE_SAMPLE_PAGES pages. Shared by get_image_codecs and
    get_full_page_scan_images so both read the same sample once."""
    last_page = min(page_count, IMAGE_SAMPLE_PAGES)
    out = run(["pdfimages", "-list", "-f", "1", "-l", str(last_page), pdf])
    lines = [l for l in out.splitlines() if l.strip()]
    if len(lines) <= 2:
        return [], []
    header = lines[0].split()
    rows = [row.split() for row in lines[2:]]
    return header, rows


def get_image_codecs(header: list[str], rows: list[list[str]]) -> list[str]:
    if "enc" not in header:
        return []
    enc_idx = header.index("enc")
    codecs = set()
    for cols in rows:
        if len(cols) > enc_idx:
            codecs.add(cols[enc_idx])
    return sorted(codecs)


def get_page_size_inches(pdf: str) -> tuple[float, float] | None:
    """Parse pdfinfo's "Page size: <w> x <h> pts" line. Returns None if the
    document has variable page sizes (pdfinfo omits/varies the line) --
    full-page-scan detection is skipped in that case rather than guessing."""
    out = run(["pdfinfo", pdf])
    for line in out.splitlines():
        if line.startswith("Page size:"):
            parts = line.split(":", 1)[1].split()
            try:
                w_pts, h_pts = float(parts[0]), float(parts[2])
                return w_pts / 72.0, h_pts / 72.0
            except (IndexError, ValueError):
                return None
    return None


def get_full_page_scan_images(
    header: list[str], rows: list[list[str]], page_size_in: tuple[float, float] | None
) -> bool:
    """True if most sampled pages-with-images are dominated by one image
    roughly the size of the full page -- the signal that actually predicts
    expensive-codec-on-full-page-scan, independent of whether a (possibly
    OCR-only) text layer also happens to be present. See module docstring."""
    if page_size_in is None:
        return False
    required = {"page", "type", "width", "height", "x-ppi", "y-ppi"}
    if not required.issubset(header):
        return False
    idx = {name: header.index(name) for name in required}
    page_w_in, page_h_in = page_size_in
    page_area = page_w_in * page_h_in
    if page_area <= 0:
        return False

    best_coverage_by_page: dict[str, float] = {}
    for cols in rows:
        if len(cols) <= max(idx.values()) or cols[idx["type"]] != "image":
            continue
        try:
            width_px = float(cols[idx["width"]])
            height_px = float(cols[idx["height"]])
            x_ppi = float(cols[idx["x-ppi"]])
            y_ppi = float(cols[idx["y-ppi"]])
        except ValueError:
            continue
        if x_ppi <= 0 or y_ppi <= 0:
            continue
        img_area = (width_px / x_ppi) * (height_px / y_ppi)
        coverage = min(img_area / page_area, 1.0)
        page_key = cols[idx["page"]]
        best_coverage_by_page[page_key] = max(best_coverage_by_page.get(page_key, 0.0), coverage)

    if not best_coverage_by_page:
        return False
    full_page_count = sum(
        1 for c in best_coverage_by_page.values() if c >= FULL_PAGE_COVERAGE_THRESHOLD
    )
    return (full_page_count / len(best_coverage_by_page)) >= FULL_PAGE_PAGE_FRACTION


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
        img_header, img_rows = get_image_rows(pdf, page_count)
        codecs = get_image_codecs(img_header, img_rows)
        page_size_in = get_page_size_inches(pdf)
        full_page_scan = get_full_page_scan_images(img_header, img_rows, page_size_in)
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
        "full_page_scan_images": full_page_scan,
        "image_codecs": codecs,
        "has_jpeg2000": has_jp2,
        "sampled_pages_for_images": min(page_count, IMAGE_SAMPLE_PAGES),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
