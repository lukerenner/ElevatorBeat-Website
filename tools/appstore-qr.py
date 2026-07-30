#!/usr/bin/env python3
"""Render assets/img/qr-dragify.svg — the desktop "scan to install" code.

A committed SVG rather than a runtime QR library or a Google Charts URL: the
code only changes when the App Store listing does, so generating it on every
page load would spend a script (or a third-party request, and the tracking that
comes with it) on a value that is constant.

Two deliberate choices in the output:

  * The modules are ink on a paper plate baked INTO the svg, not currentColor.
    The Dragify room is an .on-dark section, and an ivory-on-midnight QR is an
    inverted code — iOS Camera reads those, but enough scanners do not that an
    install CTA should not gamble on it. Fixed contrast means the same file
    scans on either ground.
  * border=4 is the spec quiet zone, and it is part of the plate rather than
    left to CSS padding, so the code cannot be cropped by a layout change.

Usage:  python3 appstore-qr.py
"""
import sys
from pathlib import Path

try:
    import segno
except ImportError:
    sys.exit("segno not installed — run: pip3 install segno")

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img" / "qr-dragify.svg"

# Apple's short form, not the descriptive URL the anchors carry. It 301s to
# exactly that URL, and at 39 characters instead of 71 it drops the symbol from
# version 5 to version 3 — 29 modules instead of 37. That is the whole ballgame
# for a code displayed on a monitor: at the ~148px the room gives it, fewer
# modules means each one is 4px instead of 2.7px, which is the difference
# between scanning from across a desk and having to lean in.
URL = "https://apps.apple.com/app/id6756401226"

INK = "#08131F"     # --ink, the midnight ground
PAPER = "#F7F3EC"   # --ground, the warm white canvas


def main() -> None:
    # 'M' recovers 15% — plenty for a screen-displayed code, and it keeps the
    # module count (and so the printed size of each module) low enough to scan
    # comfortably at the ~150px the layout gives it.
    qr = segno.make(URL, error="m")

    # omitsize writes a viewBox in place of width/height, so the file scales
    # from CSS alone and stays resolution-free at any size the layout picks.
    qr.save(OUT, kind="svg", border=4, dark=INK, light=PAPER,
            omitsize=True, svgversion=1.1, xmldecl=False)

    size = qr.symbol_size(border=4)[0]
    print(f"{OUT.relative_to(SITE)} — version {qr.version}, "
          f"{size}×{size} modules, {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
