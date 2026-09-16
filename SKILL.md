---
name: k2pdfopt
description: Converts a PDF book into e-reader-ready PDFs for Kindle and Kobo Libra using k2pdfopt, then verifies the result by sampling rendered pages instead of the whole book. Use when the user wants to convert, optimize, reflow, or shrink a PDF book for Kindle or Kobo, or explicitly mentions k2pdfopt.
---

Converts a source PDF book into one or more e-reader-ready PDFs with
k2pdfopt, checking the result against a page sample before calling it done
instead of trusting the conversion blind or rendering every page.

Reference material is disclosed on demand, not inlined here:

- `reference/installation.md` — how to get a k2pdfopt binary at all (no
  Homebrew formula exists — confirmed, don't retry `brew install k2pdfopt`).
- `reference/decision-guide.md` — confirmed flags for mode/device/quality
  selection, JPEG2000 handling, and the symptom → flag table used when a
  conversion needs fixing.
- `reference/quality-checklist.md` — the sampling math and the per-page
  checklist used in Step 5.
- `reference/cli-reference.md` — generated from the user's actual
  installed k2pdfopt binary; the source of truth for exact flag names and
  the device profile list this specific build ships with.

## Step 0: Resolve the binary

Run `scripts/resolve_binary.py`. On success it prints the resolved path and
version. On failure, there's no binary yet — read `reference/installation.md`
and work through its options with the user (there is no Homebrew formula;
don't attempt `brew install k2pdfopt`). Once a binary is in hand, persist it
with `scripts/resolve_binary.py --set <path>` so future runs don't ask
again. (Resolution order: `$K2PDFOPT_BIN`, then
`~/.config/k2pdfopt-skill/config.json`, then `k2pdfopt` on `PATH`.)

Done when: a validated binary path is in hand.

## Step 1: Inspect the source PDF

Run `scripts/inspect_pdf.py <source.pdf>`. Read `page_count`, `image_only`,
`full_page_scan_images`, and `has_jpeg2000` from its JSON output — every
later step branches on these.

Done when: that JSON has been read and parsed, not just produced.

## Step 2: Pre-flatten JPEG2000 if needed

If `has_jpeg2000` is true and **either** `image_only` **or**
`full_page_scan_images` is true, run
`scripts/flatten_jp2_to_jpeg.py <source.pdf> <flattened.pdf>` and use
`<flattened.pdf>` as the input for every step from here on. See
`reference/decision-guide.md` for why both signals matter — `image_only`
alone misses scanned books that carry an invisible OCR text layer (it
reads as "has text", but the page is still 100% the scanned image
underneath). Otherwise skip straight to Step 3 with the original file.

Done when: the working input file for Step 4 is decided.

## Step 3: Pick target device(s)

If the user already named Kindle, Kobo, or a specific model, use that. If
they just said "my e-reader" or didn't say, ask (don't assume) — default
suggestion: produce both a Kindle and a Kobo Libra output, since that's the
common case.

For each target device, check `reference/cli-reference.md`. If it's still
the placeholder, or its `source_mtime` comment no longer matches the
resolved binary's actual mtime, regenerate it first:

```
python3 scripts/generate_cli_reference.py <resolved-binary-path> reference/cli-reference.md
```

Then look up that device's built-in profile, or fall back to the panel
geometry table in `reference/decision-guide.md`.

Done when: each target device has a concrete k2pdfopt invocation planned
(profile name, or explicit width/height/DPI).

## Step 3.5: Large-print calibration (only if the user wants bigger text / a max lines-per-page)

Skip this step entirely unless the user asked for larger text, mentioned
low vision/accessibility, or gave a lines-per-page ceiling. When they did,
read `reference/decision-guide.md`'s large-print section and calibrate
`-fs` (font size in points) **per target device** against a small page
range from the source (e.g. `-p 13-17`), not the full book — taller panels
fit more lines at the same `-fs`, so a value calibrated on one device does
not carry over to another.

If the user has a size preference to weigh in on rather than a strict
numeric target, generate 2-3 candidate renders and let them choose visually:
`scripts/build_size_picker.py <out.html> "label=img.png" ...`, then open it
(`open <out.html>` on macOS) and ask with `AskUserQuestion`.

Done when: a calibrated `-fs` (or user-picked size) is set for every target
device that needs one.

## Step 3.75: Preview before the full run

Skip this step only if Step 3.5 already rendered and showed a calibrated
preview for every target device — that satisfies this step too.

Otherwise, before spending 60-150s+ per device on the full book, render a
fast preview so the user sees real output before committing to the full
run:

1. Pick a small representative page range from the Step 2 working input
   (e.g. 5 body-text pages, skipping cover/front matter) — the same range
   for every device.
2. For each target device, run the resolved binary with `-p <range>` and
   the exact flags planned for the full run (mode, `-dev`/geometry),
   writing to a throwaway preview file.
3. `scripts/rasterize_pages.py` 1-2 pages from each device's preview
   output and `scripts/build_contact_sheet.py` into one labeled sheet;
   Read it (the Read tool displays images) so the user sees the preview
   before the full run starts.

Done when: a preview has been shown for every target device.

## Step 4: Run k2pdfopt

Only after the Step 3.75 preview has been shown, for each target device
run the resolved binary against the Step 2 input, writing to
`<source-basename>-<device>.pdf` next to the source file. Attempt 1 of 3
per device.

**Run every device's conversion in the background, in parallel**, not
foreground/sequential. A real book easily takes 60-150s+ (color and
large-print/reflow runs are the slowest), which blows past a foreground
tool call's default timeout — confirmed the hard way. Backgrounding also
lets multiple target devices convert at the same time instead of one after
another. Poll/await each job and only move to Step 5 for a device once its
job has actually finished — never assume completion from elapsed time.

Always include `-ui- -x` for non-interactive, non-blocking execution, and
put `-mode`/`-dev`/geometry flags in the order documented in
`decision-guide.md` (`-mode` first — it bundles other flags and later
flags on the line override it).

Done when: an output PDF file exists for every target device.

## Step 5: Verify with a sample

For each output file:

1. `scripts/sample_plan.py <page_count>` → sampled page numbers (see
   `reference/quality-checklist.md` for the math and defaults; pass
   `--prevalence 0.05` instead of the 0.10 default only if the user asked
   for an unusually thorough check).
2. `scripts/rasterize_pages.py <output.pdf> <tmp-dir> <pages...>` → one PNG
   per sampled page.
3. `scripts/build_contact_sheet.py <tmp-dir> <sheet-prefix>` → groups those
   PNGs into 1-3 labeled grid images instead of one image per page. Read
   the resulting sheet(s) (the Read tool displays images) and score every
   labeled page against the checklist in `reference/quality-checklist.md`
   — this is the token-efficient way to look at ~30 pages: a couple of
   image reads instead of ~30.
4. If `image_only` or `full_page_scan_images` was true in Step 1, also run
   `scripts/check_output_weight.py <output.pdf> --image-only`.

When multiple target devices share the same source and the same `-mode`
with **no** device-specific `-fs` calibration (pure geometry differences),
it's reasonable to run the full sample on the first device and a smaller
spot-check (a handful of anchor pages) on the rest, since a content/reflow
defect would show up on both. Say so plainly in the Step 7 report rather
than silently skipping coverage.

This shortcut does **not** apply when Step 3.5 calibrated a per-device
`-fs` — line count is height-dependent (confirmed: a taller panel fits more
lines at the same `-fs`), so each device's output needs its own full
sample, not just a spot-check of the first device's.

Done when: every sampled page has been read and scored, and the weight
check (if applicable) has run.

## Step 6: Fix and retry if the sample failed

If any sampled page failed the checklist, or the weight check flagged
`too_heavy: true`: look up the failing symptom in
`reference/decision-guide.md`'s symptom table, adjust the one matching
concept in the k2pdfopt invocation, and go back to Step 4 for that device.
Change one concept at a time so it's clear what fixed it.

Cap at 3 total attempts per device. If it still fails after 3, stop —
report to the user exactly which pages/criteria failed and what was tried,
rather than continuing to loop or silently shipping a bad conversion.

Done when: every device's output passes the sample, or 3 attempts have run
and the failure has been reported.

## Step 7: Report

For each device, report: output file path, page count, file size, how many
pages were sampled and at what confidence/prevalence setting, and the
checklist result. Name the accepted trade-off plainly — sampling catches
systemic problems, not a guaranteed single bad page somewhere in the book.
