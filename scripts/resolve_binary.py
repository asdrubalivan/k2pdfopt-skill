#!/usr/bin/env python3
"""Resolve, validate, and (optionally) persist the path to the k2pdfopt binary.

Resolution order:
  1. $K2PDFOPT_BIN environment variable
  2. ~/.config/k2pdfopt-skill/config.json -> {"binary_path": "..."}

Usage:
  resolve_binary.py                  # print the resolved path (JSON) or exit 1
  resolve_binary.py --set /path/bin  # validate and persist a new path
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

CONFIG_DIR = Path.home() / ".config" / "k2pdfopt-skill"
CONFIG_FILE = CONFIG_DIR / "config.json"


def is_executable(path: str) -> bool:
    return bool(path) and os.path.isfile(path) and os.access(path, os.X_OK)


def read_config_path() -> str | None:
    if not CONFIG_FILE.exists():
        return None
    try:
        data = json.loads(CONFIG_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    return data.get("binary_path")


def resolve() -> str | None:
    env_path = os.environ.get("K2PDFOPT_BIN")
    if env_path and is_executable(env_path):
        return env_path
    # Also accept a bare command name found on PATH via the env var.
    if env_path:
        found = shutil.which(env_path)
        if found:
            return found
    cfg_path = read_config_path()
    if cfg_path and is_executable(cfg_path):
        return cfg_path
    # Last resort: a k2pdfopt on PATH.
    found = shutil.which("k2pdfopt")
    if found:
        return found
    return None


def set_path(new_path: str) -> int:
    candidate = new_path
    if not is_executable(candidate):
        found = shutil.which(candidate)
        if found:
            candidate = found
        else:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": f"'{new_path}' is not an executable file and is not on PATH.",
                    }
                )
            )
            return 1
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"binary_path": candidate}, indent=2) + "\n")
    version = probe_version(candidate)
    print(json.dumps({"ok": True, "binary_path": candidate, "version": version}))
    return 0


def probe_version(path: str) -> str | None:
    for flags in (["-v"], ["-?"], []):
        try:
            proc = subprocess.run(
                [path, *flags],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        text = _ANSI_RE.sub("", (proc.stdout or "") + (proc.stderr or ""))
        first_line = text.strip().splitlines()[0] if text.strip() else None
        if first_line:
            return first_line
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set", metavar="PATH", help="Validate and persist a binary path")
    args = parser.parse_args()

    if args.set:
        return set_path(args.set)

    path = resolve()
    if not path:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": (
                        "k2pdfopt binary not found. Set $K2PDFOPT_BIN, or run "
                        "resolve_binary.py --set /path/to/k2pdfopt"
                    ),
                    "checked": {
                        "env": os.environ.get("K2PDFOPT_BIN"),
                        "config_file": str(CONFIG_FILE),
                    },
                }
            )
        )
        return 1
    print(json.dumps({"ok": True, "binary_path": path, "version": probe_version(path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
