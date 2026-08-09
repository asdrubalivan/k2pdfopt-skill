#!/usr/bin/env python3
"""Compute a token-efficient, statistically-grounded page sample plan.

The question this answers is NOT "estimate the defect rate precisely" (that
needs hundreds of samples and doesn't shrink for big books) -- it's "if a
SYSTEMIC conversion problem affects at least P% of pages, what's the fewest
pages I need to look at to have a C% chance of seeing at least one instance?"

That sample size is:  n = ceil( ln(1 - C) / ln(1 - P) )

It does NOT grow with the book's page count (only with how rare a problem
you insist on being able to catch), which is exactly what keeps a 1500-page
book cheap to check. Defaults: C=0.95, P=0.10 -> n=29, regardless of length.

Trade-off to state plainly: this catches problems that recur across the
book (wrong device profile, bad margins, broken column detection, oversized
images...). It is not meant to catch a single one-off bad page -- that's
the accepted cost of not rendering all 1500 pages.

The plan also always includes a handful of fixed anchor pages (first
content page, ~10%, ~50%, ~90%, last page) since front matter, a
table of contents, and back matter are disproportionately likely to expose
layout bugs that a pure statistical sample can miss by chance.

Usage:
  sample_plan.py <total_pages> [--confidence 0.95] [--prevalence 0.10]
                 [--min 8] [--max 60]
"""
import argparse
import json
import math
import sys


def sample_size(total_pages: int, confidence: float, prevalence: float, min_n: int, max_n: int) -> int:
    if prevalence <= 0 or prevalence >= 1:
        raise ValueError("prevalence must be between 0 and 1")
    if confidence <= 0 or confidence >= 1:
        raise ValueError("confidence must be between 0 and 1")
    n = math.ceil(math.log(1 - confidence) / math.log(1 - prevalence))
    n = max(min_n, min(n, max_n, total_pages))
    return n


def stratified_pages(total_pages: int, n: int) -> list[int]:
    if total_pages <= n:
        return list(range(1, total_pages + 1))
    # Evenly spaced pages across the whole book (midpoint of n equal buckets),
    # deduplicated and sorted.
    pages = set()
    bucket = total_pages / n
    for i in range(n):
        page = round(bucket * i + bucket / 2)
        page = max(1, min(total_pages, page))
        pages.add(page)
    return sorted(pages)


def anchor_pages(total_pages: int) -> list[int]:
    if total_pages <= 1:
        return [1]
    anchors = {
        1,
        max(1, round(total_pages * 0.10)),
        max(1, round(total_pages * 0.50)),
        max(1, round(total_pages * 0.90)),
        total_pages,
    }
    return sorted(anchors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("total_pages", type=int)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--prevalence", type=float, default=0.10)
    parser.add_argument("--min", dest="min_n", type=int, default=8)
    parser.add_argument("--max", dest="max_n", type=int, default=60)
    args = parser.parse_args()

    n = sample_size(args.total_pages, args.confidence, args.prevalence, args.min_n, args.max_n)
    pages = sorted(set(stratified_pages(args.total_pages, n)) | set(anchor_pages(args.total_pages)))

    print(json.dumps({
        "total_pages": args.total_pages,
        "confidence": args.confidence,
        "prevalence_detectable": args.prevalence,
        "formula_sample_size": n,
        "pages": pages,
        "sample_count": len(pages),
        "note": (
            f"With {len(pages)} pages sampled, a problem affecting >= "
            f"{args.prevalence:.0%} of the book's pages has a >= "
            f"{args.confidence:.0%} chance of appearing at least once in this sample."
        ),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
