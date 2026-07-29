#!/usr/bin/env python3
"""Build the StraightPic before/after pair from a real photograph.

WHY THIS EXISTS
---------------
The old demonstration was a square slate tile photographed on a wooden table. It read
as a debugging fixture rather than as something a photographer would care about
protecting, which undersold what the app is for.

The replacement is `Apps/StraightPic/Reference Photos/Tower.jpg` — a 4284x5712 phone
photograph of a brick smokestack between a concrete block and a Victorian brick
warehouse. It is architecture, it has strong converging verticals, and it is a picture
worth keeping. That is the whole argument: the photograph was already good, and the
correction only makes it ready to share.

The source is already exactly 3:4 (4284/5712), so both frames keep the photographer's
full composition and neither is cropped to flatter the other.

WHAT THE CORRECTION IS
----------------------
A keystone: the camera was tilted up, so verticals lean inward toward the top of the
frame. Mapping the narrower top span out to the full width pushes them upright. This
reproduces the transform StraightPic applies; it is a demonstration built from the raw
photograph, not a screen recording of the app.

INSET is in source pixels and was chosen by eye against the concrete building's left
edge and the warehouse's window mullions, which are the two strongest true verticals in
the frame.

The guide lines and corner handles are NOT baked in here. They are drawn as an SVG
overlay in the page, so they stay crisp at any pixel density and the photographs remain
swappable without redoing the artwork.

Usage:  python3 straightpic-demo.py
"""
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img"
SOURCE = Path(
    "/Users/luke/Library/CloudStorage/GoogleDrive-luke.renner@gmail.com/My Drive"
    "/Antigravity/Apps/StraightPic/Reference Photos/Tower.jpg"
)

# Width -> height, held to the source's native 3:4 so every rendered size lands on
# whole pixels and the CSS aspect-ratio can never disagree with the file.
SIZES = [(600, 800), (900, 1200), (1200, 1600)]

INSET = 760  # source pixels trimmed from each top corner


def identify(path):
    out = subprocess.run(
        ["magick", "identify", "-format", "%w %h", str(path)],
        check=True, capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])


def emit(pipeline, stem):
    for width, height in SIZES:
        subprocess.run(
            ["magick", *pipeline,
             "-filter", "Lanczos", "-resize", f"{width}x{height}!",
             "-unsharp", "0x0.6+0.5+0.02",
             "-quality", "84", "-define", "webp:method=6",
             str(OUT / f"{stem}-{width}.webp")],
            check=True)
    print(f"  {stem}: {[w for w, _ in SIZES]}")


def main():
    if not SOURCE.exists():
        sys.exit(f"missing source: {SOURCE}")
    w, h = identify(SOURCE)
    print(f"source {w}x{h} ({w / h:.4f}, want 0.75)")

    # BEFORE — the photograph as shot.
    emit([str(SOURCE)], "straightpic-before")

    # AFTER — keystone corrected. `-virtual-pixel none` leaves anything pulled in from
    # outside the source transparent; the flatten below fills those with the frame's
    # own dark edge tone rather than white, so a stray sub-pixel at the border can
    # never read as a bright seam against the page.
    emit([
        str(SOURCE), "-virtual-pixel", "none",
        "-distort", "Perspective",
        f"{INSET},0 0,0  {w - INSET},0 {w},0  0,{h} 0,{h}  {w},{h} {w},{h}",
        "-background", "#1b1c20", "-alpha", "remove", "-alpha", "off",
    ], "straightpic-after")


if __name__ == "__main__":
    main()
