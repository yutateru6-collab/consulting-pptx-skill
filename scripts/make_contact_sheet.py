#!/usr/bin/env python3
"""Create a readable contact sheet from rendered slide PNGs."""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def natural_key(path: Path):
    import re
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", path.name)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--columns", type=int, default=3)
    ap.add_argument("--thumb-width", type=int, default=640)
    args = ap.parse_args()

    paths = sorted(args.input_dir.glob("*.png"), key=natural_key)
    if not paths:
        raise SystemExit(f"no PNGs found in {args.input_dir}")

    cols = max(1, args.columns)
    first = Image.open(paths[0]).convert("RGB")
    ratio = first.height / first.width
    tw = args.thumb_width
    th = round(tw * ratio)
    label_h = 38
    gap = 18
    rows = math.ceil(len(paths) / cols)
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * (th + label_h) + (rows + 1) * gap), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGB")
        im.thumbnail((tw, th), Image.Resampling.LANCZOS)
        x = gap + (i % cols) * (tw + gap)
        y = gap + (i // cols) * (th + label_h + gap)
        sheet.paste(im, (x, y))
        draw.text((x + 4, y + th + 8), f"Slide {i + 1}  {path.name}", fill="black", font=font)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, quality=92)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
