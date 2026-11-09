#!/usr/bin/env python3
"""Minify dashboard/app.js -> dashboard/app.min.js with terser.

Lighthouse audit "Minify JavaScript" flagged the readable source that
GitHub Pages serves. The source stays in the repo (and is what the
static unit tests read); the browser loads app.min.js. Regenerate
after every app.js edit:

    python3 scripts/minify_app_js.py

Terser is fetched via `npx --yes terser@5.51.2` (no repo dependency);
set TERSER_BIN to a local terser binary to skip the download.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "dashboard" / "app.js"
OUT = ROOT / "dashboard" / "app.min.js"
BANNER = (
    "/* app.min.js — minified from app.js by scripts/minify_app_js.py. "
    "Do not edit by hand; edit app.js and re-run the script. */"
)
TERSER_VERSION = "5.51.2"


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: {SRC} not found", file=sys.stderr)
        return 1
    terser = os.environ.get("TERSER_BIN") or shutil.which("terser")
    if terser:
        cmd = [terser]
    else:
        npx = shutil.which("npx")
        if not npx:
            print("ERROR: terser/npx not found. Install Node.js.", file=sys.stderr)
            return 1
        cmd = [npx, "--yes", f"terser@{TERSER_VERSION}"]
    with tempfile.NamedTemporaryFile(suffix=".js", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        cmd += [str(SRC), "--compress", "--mangle", "--output", tmp_path]
        print("+", " ".join(cmd))
        result = subprocess.run(cmd, cwd=ROOT, check=False)
        if result.returncode != 0:
            print("ERROR: terser failed", file=sys.stderr)
            return result.returncode
        body = pathlib.Path(tmp_path).read_text(encoding="utf-8")
        OUT.write_text(BANNER + "\n" + body + "\n", encoding="utf-8")
    finally:
        pathlib.Path(tmp_path).unlink(missing_ok=True)
    src_size = SRC.stat().st_size
    out_size = OUT.stat().st_size
    print(
        f"Wrote {OUT.relative_to(ROOT)} ({out_size / 1024:.1f} KiB, "
        f"was {src_size / 1024:.1f} KiB, saved {(src_size - out_size) / 1024:.1f} KiB)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
