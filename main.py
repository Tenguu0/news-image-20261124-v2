#!/usr/bin/env python3
"""news-image-20261124-v2 entry: write the day's world news image.

The front-page image (entry.png) was composed in this repo by
build_page.py and is held in the repo. This program copies it to the
output directory. Python 3.12+, standard library only. No network,
no randomness, no clock, so every run writes the same bytes.

Run: MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "."))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
