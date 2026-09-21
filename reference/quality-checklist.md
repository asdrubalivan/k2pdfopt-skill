# Quality checklist and sampling method

## Why sampling, and why this formula

Rendering and inspecting every page of a 1500-page book would burn a
prohibitive number of tokens. But most k2pdfopt conversion problems are
**systemic** — a wrong device profile, a broken column-detection call, an
over-aggressive DPI setting — meaning they show up on most pages, not one
random page. That reframes the question from "estimate the defect rate
precisely" (needs hundreds of samples, and the sample size *grows* with the
book) to "if a problem affects at least P% of pages, what's the fewest pages
I need to check for a C% chance of catching it at least once?" — which does
**not** grow with the book's length:

```
n = ceil( ln(1 - C) / ln(1 - P) )
```

`scripts/sample_plan.py` computes this (default C=0.95, P=0.10 → 29 pages,
whether the book is 40 pages or 1500). It also always adds a few fixed
anchor pages (first page, ~10%, ~50%, ~90%, last page), since front matter,
a table of contents, and back matter disproportionately expose bugs that a
pure statistical sample can miss by chance.

**Accepted trade-off:** this catches recurring/systemic problems, not a
single one-off bad page buried in an otherwise-fine book. That's the
deliberate cost of not rendering all 1500 pages — state it in the final
report rather than implying a full-book guarantee.

Tightening `--prevalence` (e.g. to 0.05) roughly doubles the sample for a
correspondingly rarer problem; loosening it (e.g. to 0.20) roughly halves
it. Use a tighter value only if the user asks for an unusually thorough
check, and say so when reporting results either way.

## Checklist for each sampled page

Render the sample with `scripts/rasterize_pages.py` and look at each image
(the Read tool displays PNG/JPEG images directly). For every sampled page,
check:

- **Not clipped** — no text or image content cut off at the page edges.
- **Legible at device size** — font is neither so small it strains
  reading nor so large it wastes the screen, given the target device's
  panel size from `decision-guide.md`.
- **Columns intact** — multi-column source text reads in the correct
  order, not merged or interleaved.
- **Images present and reasonably sharp** — where the source page had an
  image or figure, it survived the conversion and isn't a garbled or
  blank block.
- **Orientation correct** — no unexpectedly rotated pages.
- **Not blank/corrupted** — a page that should have content isn't empty
  or full of rendering artifacts.
- **Reading order correct** — especially on pages with sidebars,
  footnotes, or captions.
- **Line count within target** (only when the user set a max-lines-per-page
  / large-print requirement) — see `decision-guide.md`'s large-print
  section. `-fs` sets a median, so a page or two slightly over by 1-3
  lines is expected variance, not a fail; a *systemic* pattern of
  overshoot (most sampled pages over target) means the calibration needs
  another pass, ideally on the taller of the target devices first.

A sampled page **fails** the checklist if it breaks any of the above **in a
way that looks likely to repeat** (e.g. a global margin or column-detection
problem) rather than a one-off. Note which criterion failed — that maps
directly to a row in `decision-guide.md`'s symptom table.

## File weight for image-only (scanned) books

Check with `scripts/check_output_weight.py --image-only`. Rule of thumb, not
a hard law — flag it if avg KB/page exceeds roughly:

- **~180 KB/page** for a grayscale e-ink target — usually means DPI is set
  higher than the device's panel can even display. See `decision-guide.md`'s
  "File-weight tuning" section for what actually moves this number (and
  the counterintuitive case where a lower `-jpg` quality makes it *worse*)
  before spending retries on it.

This check only applies to image-only output. A reflowed-text conversion of
an image-only source, or any book with a real text layer, doesn't have a
meaningful per-page weight threshold — skip the check (or run without
`--image-only` to record the number without judging it).
