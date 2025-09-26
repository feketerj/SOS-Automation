#!/usr/bin/env python3
"""Simple helper to copy web assets into dist."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "web"
DST = ROOT / "dist"


def build() -> None:
    if not SRC.exists():
        raise SystemExit(f"Source directory not found: {SRC}")
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    print(f"Copied {SRC} -> {DST}")


if __name__ == "__main__":
    build()
