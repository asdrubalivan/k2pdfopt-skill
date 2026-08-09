# Getting a k2pdfopt binary

**There is no Homebrew formula or tap for k2pdfopt** — confirmed via
`brew search k2pdfopt` (no match) and `brew search --desc pdf` (no hit).
`brew install k2pdfopt` will always fail. Don't retry it; use one of the
paths below instead.

## Option A — already have a binary somewhere

If the user has a k2pdfopt binary sitting in a download folder or similar,
just move it somewhere durable and point the skill's config at it:

```
mkdir -p ~/.local/bin
mv <wherever>/k2pdfopt ~/.local/bin/k2pdfopt   # avoid Downloads/ if it gets periodically cleared
chmod +x ~/.local/bin/k2pdfopt
python3 scripts/resolve_binary.py --set ~/.local/bin/k2pdfopt
```

Verify architecture matches the machine before trusting it:

```
file ~/.local/bin/k2pdfopt      # or: lipo -info ~/.local/bin/k2pdfopt
```

On Apple Silicon, an `arm64` binary runs natively; an `x86_64`-only one
needs Rosetta 2 and will be slower to start.

## Option B — official precompiled binary (willus.com)

The author distributes precompiled binaries directly:
<https://www.willus.com/k2pdfopt/>. As of the last check, the official Mac
build is **Intel-only** (32/64-bit) — on Apple Silicon it runs under
Rosetta 2, not natively. Confirm architecture with `file`/`lipo` as above
before relying on it for large books (Rosetta translation adds startup
overhead, though it's usually fine for a batch conversion job).

## Option C — build from source (only real option for a native Apple Silicon binary)

The official source (also mirrored at
<https://github.com/mo3rfan/k2pdfopt>, which carries CMake build fixes and
a Dockerfile) builds cleanly on macOS with Homebrew-provided dependencies.
Confirmed working dependency set:

```
brew install cmake pkg-config mupdf leptonica jasper libpng jpeg-turbo zlib
```

`leptonica` is a **hard requirement** of the fork's `CMakeLists.txt`
(`pkg_search_module(LEPTONICA REQUIRED lept)`) even though it's optional in
the underlying C code. `mupdf` is picked up via `pkg-config` if present
(enables native PDF handling, JBIG2, OpenJPEG, FreeType together).
Ghostscript (`gs`, already common via Homebrew) is auto-detected via
`find_program` and used as an optional fallback renderer.

```
git clone --depth 1 https://github.com/mo3rfan/k2pdfopt.git
cd k2pdfopt
cmake -B build .
cmake --build build
./build/k2pdfopt -?      # sanity check
python3 scripts/resolve_binary.py --set "$(pwd)/build/k2pdfopt"
```

If `pkg_check_modules(MUPDF mupdf)` doesn't find MuPDF (Homebrew's mupdf
formula doesn't always ship a `.pc` file), the build still succeeds without
native MuPDF support — k2pdfopt falls back to its own bundled PDF/rasterizer
code path plus Ghostscript, which is sufficient for this skill's use case.

## What this skill actually runs on (recorded for reference)

The instance this skill was built and tested against: `k2pdfopt v2.55
(w/MuPDF,DjVuLibre,OCR)`, compiled `Dec 26 2023` with `Clang v17.0.6` for
`OS/X on ARM64` — i.e. a full-featured native Apple Silicon build obtained
via Option A (already on disk), not built from source. Its exact flag set
and device profile list are cached in `cli-reference.md`.
