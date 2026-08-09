# Decision guide

Concepts and confirmed flags for picking k2pdfopt parameters. The exact
flag list always lives in `cli-reference.md` (regenerated from the user's
actual installed binary via `scripts/generate_cli_reference.py`); this file
adds the *decisions* on top of it. Flag names below were confirmed against
k2pdfopt v2.55 (arm64, w/MuPDF,DjVuLibre,OCR) — re-verify against
`cli-reference.md` if the installed version differs.

## Running headless (no interactive prompts)

k2pdfopt's help and some runtime queries are an interactive pager/prompt by
default. For unattended runs, always include:

```
-ui- -x
```

`-ui-` turns off interactive input queries (default is *on* on Linux/macOS);
`-x` exits immediately on completion instead of waiting for `<Enter>`.

**Flag order matters**: `-mode <name>` expands to a whole bundle of other
flags (including `-dev` and orientation), and later flags on the command
line override earlier ones. Always put `-mode` *first* and put
`-dev`/`-w`/`-h`/`-dpi`/`-jpg`/`-ls-` *after* it, or the mode's bundled
defaults silently win.

**Orientation gotcha (confirmed the hard way):** `-mode fw` and `-mode fp`
bundle **landscape** orientation by default — the output pages come out
sideways on a portrait e-reader. For normal portrait reading, always append
`-ls-` right after the mode. Baseline invocation for this skill's actual
job (portrait output sized to a real e-reader panel):

```
-mode fw -ls- -dev <alias> -ui- -x -o <out> <in>
```

Verify orientation is upright in every Step 5 sample, not just layout —
it's easy to visually skim past a correctly-laid-out page and miss that
the whole page is rotated 90°.

## Picking a mode (`-mode`)

| Mode | What it does | Use for |
|---|---|---|
| `def` (default, i.e. no `-mode` at all) | Reflow with OCR text layer, up to 2-column auto-detect, bitmapped output | Scanned/image-only books — the common case for this skill |
| `fw` (`fitwidth`/`sopdf`) | Fits content to device width, **no reflow**, native PDF output, preserves original layout. **Defaults to landscape — add `-ls-` for portrait.** | Already well-laid-out native PDFs (comics, magazines, heavily designed pages) where reflow would break the design |
| `2col` | Native PDF output tuned for 2-column layouts | Native (non-scanned) 2-column articles/papers |
| `fp` (`fitpage`) | Fits each whole source page to the display, no reflow. **Also defaults to landscape — add `-ls-` for portrait.** | Similar to `fw` but fits the whole page instead of just its width |
| `tm` (`trim`) | Trims to content margins, native output, output size matches trimmed source | Well-formatted PDFs that just need whitespace trimmed |
| `copy` | Bitmapped copy at the same dimensions, no reflow | Rarely useful for e-readers directly; mostly a building block |
| `crop` / `concat` | Used with `-cbox` cropping workflows | Not relevant to whole-book conversion |

Default to `def` for the scanned/image-only case this skill mostly handles
(see `inspect_pdf.py`'s `image_only` field). If `image_only` is false (the
source has a real text layer / was exported from an ebook, not scanned),
try `fw` first — it's far less likely to mangle an already-good layout than
forcing a reflow.

## Device profiles (`-dev`)

Default is `-dev kindle2` if omitted. Run `-dev ?` (already captured in
`cli-reference.md`'s "Device profiles" section) to list every alias this
specific build ships with — the list is fixed, small, and does **not**
include most modern hardware by exact name. As of v2.55, the closest
built-in aliases to the two devices this skill targets are:

| Target | Closest built-in alias | That alias's real geometry |
|---|---|---|
| Kindle (Paperwhite/Voyage/Oasis class) | `kv` (Kindle Voyage/PW3+/Oasis) | 1016 × 1364, 300 dpi |
| Kindle (newer, larger panel) | `ko2` (Kindle Oasis 2) | 1200 × 1583, 300 dpi |
| Kobo Libra | `kol` (Kobo Libra H2O) | 1264 × 1527, 300 dpi |

None of these exactly match the newest panels (e.g. Kindle Paperwhite
11th-gen is 1236 × 1648 @300dpi; Kobo Libra 2 is 1264 × 1680 @300dpi) — the
alias will produce a very close but not pixel-perfect fit. If the user
wants an exact match, skip `-dev` and set geometry manually instead:

```
-w <px> -h <px> -dpi <dpi>
```

using the exact panel numbers for their model (ask the user to confirm the
exact model if unsure — panel specs shift across hardware revisions).

`-dr <multiplier>` scales width, height, and DPI together (e.g. `-dr 2`
doubles all three) — a quick way to try a sharper/heavier or
softer/lighter output without recomputing geometry by hand.

## Large print / max lines per page (accessibility)

When the user wants noticeably bigger text or caps how many lines fit on a
page (e.g. for low-vision readability), don't reach for `-mode fw`'s zoom —
it just scales the whole page photo, so bigger text runs off the screen
edges. Use **reflow mode with an explicit font size** instead:

```
-mode def -col 1 -fs <points> -ocr- -dev <alias> -ui- -x -o <out> <in>
```

`-fs <points>` scales the output so the **median** font size is that many
points (confirmed flag, see `cli-reference.md`). `-col 1` avoids
multi-column reflow for a straightforward single-narrative book; `-ocr-`
skips OCR since reflow always rasterizes to bitmap (native/selectable text
is incompatible with reflow — see `-n` in `cli-reference.md`), and this
skill's use case already has real source text, so there's nothing worth
re-OCRing. **Trade-off to state to the user:** reflowed output loses
text-selectability/search on the device, in exchange for controlled font
size. Worth calling out explicitly, not just doing silently.

**There is no universal `-fs` value — it must be calibrated per book and
per device.** Two confirmed reasons:

1. Source books differ in original font size/density, so the same `-fs`
   produces different line counts on different books.
2. **Taller device panels fit MORE lines at the same `-fs`, not fewer** —
   line count scales with page height. Confirmed empirically: at the same
   `-fs`, `kol` (1527px tall) fit noticeably more lines per page than `kv`
   (1364px tall). Don't assume a bigger/taller panel is "safer" for a
   line-count ceiling — it's the opposite. As a starting point when moving
   an already-calibrated `-fs` to a taller device, scale it up by roughly
   the height ratio (`new_fs ≈ old_fs × new_height / old_height`), then
   re-verify — it's a starting guess, not exact (line breaks depend on
   word lengths, not just geometry).

**Calibration procedure** (cheap — never do this against the full book):

1. Pick a representative body-text page range from the source, e.g.
   `-p 13-17` (skip cover/TOC/front matter). Run the candidate `-fs` against
   just that range for the target device.
2. `rasterize_pages.py` a couple of those output pages, and either read
   them directly or build an HTML comparison page with
   `scripts/build_size_picker.py <out.html> "label=path.png" ...` for 2-3
   candidate sizes side by side, open it (`open <out.html>` on macOS), and
   let the user pick with `AskUserQuestion` — this is the preferred flow
   when the user has a size preference to weigh in on, not just a hard
   numeric target.
3. Count lines per sampled page by eye. `-fs` sets a **median**, not a hard
   per-page ceiling — expect roughly ±1-3 lines of variance page to page
   (dialogue-heavy or short-paragraph pages pack more, tighter lines than
   narrative prose). A page or two slightly over the target in a full-book
   sample is expected variance, not a failed calibration; treat it as a
   retry trigger only if it's a systemic pattern, not a one-off.
4. Once calibrated per device, run the full book, then still run the
   normal Step 5 sample-and-verify — confirm the line-count holds
   generally, not just on the calibration excerpt.

## JPEG2000 handling

Many k2pdfopt builds are not linked against a JPEG2000 decoder, so feeding
a JP2-embedded PDF straight in can fail outright or silently produce
blank/corrupted pages. poppler (which `inspect_pdf.py` and `pdftoppm` use)
reliably decodes JP2. When `inspect_pdf.py` reports `has_jpeg2000: true`
**and** `image_only: true`, pre-flatten with `flatten_jp2_to_jpeg.py` before
handing the file to k2pdfopt — this sidesteps the decoder gap entirely by
letting poppler do the JP2 decode once, up front. (The installed v2.55
build does report `w/MuPDF` support, which bundles OpenJPEG — so JP2 may
work directly; flattening first is still the safer default since a failure
here is silent/hard to detect, not a crash.)

Do **not** flatten when `image_only` is false — the PDF has a live text
layer worth preserving, and rasterizing would destroy it. In that mixed
case, run k2pdfopt directly on the original file and only take the
symptom-driven fallback below if it actually fails.

## Symptom → flag to adjust

When a sampled output page fails the checklist in `quality-checklist.md`,
match the symptom to a flag, then confirm current syntax/defaults in
`cli-reference.md` before retrying:

| Symptom | Flag to adjust |
|---|---|
| Output pages are sideways/landscape instead of upright/portrait | `-ls-` right after `-mode` (`fw` and `fp` default to landscape — see the orientation gotcha above) |
| Text clipped at page edges / columns cut off | `-mode` — try `def` vs `fw` vs `2col` (see table above) |
| Two-column layout merged into scrambled text | `-col <maxcol>` — force `-col 1` or `-col 2` instead of auto-detect |
| Text reflowed when the source was already well laid out | `-mode fw` or `-mode tm` (native output, no reflow) |
| Font too small or too large to read on the device | `-dpi` (or `-dr` to scale everything at once) |
| Images blurry, muddy, or over-compressed | `-dpi` up, `-jpg <quality>` up (default quality is 90) |
| Output file far heavier than expected for an image-only book | `-dpi` down, `-jpg <quality>` down |
| Margins too wide/narrow, content pushed to one side | `-m <val>` (margin to ignore), `-om <val>` (output margins) |
| Low-contrast scan looks washed out | `-cmax`, `-g` (gamma), `-s` (sharpen), `-wt` (white threshold) |
| Pages missing, duplicated, or out of order | `-p <pagelist>` used in the invocation, and the source's actual page count from `inspect_pdf.py` |

Re-run with one adjusted flag at a time where practical, so it's clear
which change fixed (or didn't fix) the sampled symptom. Cap retries at 3
attempts per device — see `SKILL.md` for what to do if it's still failing
after that.
