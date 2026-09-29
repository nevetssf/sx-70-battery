#!/usr/bin/env python3
"""Render every enclosure variant from the OpenSCAD source.

Usage:  python scripts/build_stl.py [--openscad /path/to/openscad]
Output: hardware/enclosure/stl/<option>_<part>.stl
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "hardware" / "enclosure" / "sx70_power_pack.scad"
OUT = SRC.parent / "stl"

OPTIONS = ("lipo", "aaa4")
PARTS = ("base", "lid")


def render(openscad: str, option: str, part: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{option}_{part}.stl"
    cmd = [
        openscad,
        "-D", f'battery_option="{option}"',
        "-D", f'part="{part}"',
        "-o", str(target),
        str(SRC),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}\n{proc.stderr}")
    for line in proc.stderr.splitlines():
        if "WARNING" in line:
            print(f"  {line}", file=sys.stderr)
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--openscad", default=shutil.which("openscad") or "openscad")
    args = ap.parse_args()

    if not shutil.which(args.openscad):
        print("openscad not found; install it or pass --openscad", file=sys.stderr)
        return 1

    for option, part in product(OPTIONS, PARTS):
        path = render(args.openscad, option, part)
        print(f"{path.relative_to(ROOT)}  ({path.stat().st_size // 1024} kB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
