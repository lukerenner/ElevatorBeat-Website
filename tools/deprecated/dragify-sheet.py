#!/usr/bin/env python3
"""Cut a restrained contact sheet out of the Dragify looks collage.

`assets/img/dragify-looks-*.webp` is a 14-up grid on a white ground. Run
full-bleed it fought the site: white ground against a midnight page, fourteen
competing subjects, and a colour range (candy pink, mint, lemon) that read as a
second, unrelated palette.

This picks FIVE looks and emits them as individual 3:4 tiles, so the page can
frame them the same way it frames everything else instead of dropping in a
foreign strip. The five are chosen for deep, saturated, cinematic grounds —
champagne, teal, purple, blue, gold — which sit with the navy framing; the
pastel tiles are deliberately left out.

Tile geometry was measured off the 2724px master by thresholding the white
background, so the spans below are the real cut lines, not eyeballed ones.

Usage:  python3 dragify-sheet.py
"""
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img"
SOURCE = OUT / "dragify-looks-2724.webp"

# (x, y0, y1) of each chosen tile in the 2724x1123 master. Tiles are 422 wide.
# Row 1 spans y 0-551, row 2 spans y 582-1123.
TILES = [
    ("champagne", 257, 0, 551),
    ("teal", 718, 0, 551),
    ("purple", 1640, 0, 551),
    ("blue", 1042, 582, 1123),
    ("gold", 1965, 582, 1123),
]
TILE_W = 422
# Rendered at ~200px in a five-up row, so 480 covers 2x displays.
WIDTHS = [240, 480]


def main():
    master = Image.open(SOURCE).convert("RGB")
    for index, (name, x, y0, y1) in enumerate(TILES, start=1):
        height = y1 - y0
        # Trim width rather than height to reach 3:4 — the tiles are already
        # shorter than 3:4, and cropping height would take the hair or the hem,
        # which is the whole point of the look.
        width = round(height * 3 / 4)
        left = x + (TILE_W - width) // 2
        tile = master.crop((left, y0, left + width, y1))
        for w in WIDTHS:
            resized = tile.resize((w, round(w * 4 / 3)), Image.LANCZOS)
            path = OUT / f"dragify-look-{index}-{w}.webp"
            resized.save(path, "WEBP", quality=80, method=6)
        print(f"  look-{index} ({name}): {len(WIDTHS)} variants")


if __name__ == "__main__":
    main()
