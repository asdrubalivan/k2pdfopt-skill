#!/usr/bin/env python3
"""Generate (or refresh) the local k2pdfopt CLI reference cache.

k2pdfopt's own help output is the ground truth for exact flag names and
defaults on the user's installed version -- more reliable than any
hand-written flag list, and versions do drift. This script captures that
output once and caches it to reference/cli-reference.md so later runs don't
re-spend tokens re-reading it, and regenerates it when the binary path or
mtime changes.

Interaction note (k2pdfopt v2.55 behavior, confirmed empirically): the
binary's help is an interactive pager ("Press <ENTER> to continue (q to
quit)"). Running it with stdin redirected from an already-exhausted source
(EOF) makes it read EOF as "continue" at every prompt, which pages straight
through to the end instead of blocking -- so no keystrokes need to be fed
in. `-longhelp` is not a real flag on this build; the full flag-by-flag
reference comes from plain `-?` paged through in this way.

Usage:
  generate_cli_reference.py <binary_path> <out_file>
"""
import re
import subprocess
import sys
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def capture(binary: str, flags: list[str]) -> str:
    try:
        proc = subprocess.run(
            [binary, *flags],
            stdin=subprocess.DEVNULL,  # EOF -> pager auto-advances instead of blocking
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"(failed to run `{binary} {' '.join(flags)}`: {exc})"
    out = (proc.stdout or "") + (proc.stderr or "")
    return ANSI_RE.sub("", out).strip()


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    binary, out_file = sys.argv[1], Path(sys.argv[2])

    full_help = capture(binary, ["-?"])
    device_list = capture(binary, ["-dev", "?"])

    if not full_help or len(full_help) < 200:
        print(f"'-?' produced suspiciously little output from {binary} -- aborting", file=sys.stderr)
        print(full_help, file=sys.stderr)
        return 1

    binary_path = Path(binary).resolve()
    mtime = binary_path.stat().st_mtime if binary_path.exists() else 0
    version_line = full_help.splitlines()[0] if full_help else "unknown"

    lines = [
        "# k2pdfopt CLI reference (auto-generated)",
        "",
        f"<!-- source_binary: {binary_path} -->",
        f"<!-- source_mtime: {mtime} -->",
        "",
        f"Captured from: `{version_line}`",
        "",
        "This file is generated directly from the installed k2pdfopt binary's own",
        "help output -- it is the source of truth for exact flag names, current",
        "defaults, and which device profiles this specific build ships with. Do",
        "not hand-edit; SKILL.md regenerates it automatically when",
        "`source_mtime` above no longer matches the resolved binary.",
        "",
        "## Device profiles (`-dev ?`)",
        "",
        "Prefer an exact alias below over manual `-w`/`-h`/`-dpi` geometry.",
        "If the user's exact device isn't listed, pick the closest resolution",
        "match, or fall back to manual geometry using the device's real panel",
        "spec -- see `decision-guide.md`.",
        "",
        "```",
        device_list or "(no output captured)",
        "```",
        "",
        "## Full flag reference (`-?`)",
        "",
        "```",
        full_help,
        "```",
    ]

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(lines) + "\n")
    print(f"wrote {out_file} ({len(full_help)} chars of flag help, {len(device_list)} chars of device list)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
