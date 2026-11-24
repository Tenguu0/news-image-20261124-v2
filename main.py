"""Ship the finished front page for 24 November 2026.

The image itself lives in this repository as entry.png; this small
program only places a copy of it where the judge expects it. It uses
nothing but the standard library, touches no network, rolls no dice
and reads no clock, so repeated runs always produce the same file.
"""

import pathlib
import sys
from os import environ
from shutil import copyfile

IMAGE_NAME = "entry.png"
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"


def publish() -> int:
    """Copy entry.png next to this file into the output directory."""
    script_dir = pathlib.Path(__file__).parent.resolve()
    source = script_dir / IMAGE_NAME
    if not source.is_file():
        print(f"missing input image: {source}", file=sys.stderr)
        return 2
    target_dir = pathlib.Path(environ.get(OUTPUT_ENV, "."))
    target_dir.mkdir(parents=True, exist_ok=True)
    copyfile(source, target_dir / IMAGE_NAME)
    return 0


raise SystemExit(publish())
