#!/usr/bin/env python3
"""Build the two real app-interface frames used on the homepage.

Both sources are real screenshots living with the apps themselves, outside this
repo. Nothing here is illustration: the Dragify frame is the pack drawer as it
ships, cropped out of the App Store screenshot that composites it over marketing
type, and the StraightPic frame is an unretouched capture of the editor with the
four perspective handles placed on the same Tower.jpg the before/after below it
is built from.

Run from the repo root:  python3 tools/ui-shots.py
"""

import subprocess
from pathlib import Path

APPS = Path(
    "/Users/luke/Library/CloudStorage/GoogleDrive-luke.renner@gmail.com/"
    "My Drive/Antigravity/Apps"
)
OUT = Path(__file__).resolve().parent.parent / "assets" / "img"

# (stem, source, crop or None, widths)
# The Dragify crop isolates the phone screen from the marketing composite: the
# island row above and the clipped fourth card below both come off, leaving three
# whole pack cards and none of the purple backdrop the device sits on.
JOBS = [
    (
        "ui-dragify-packs",
        APPS / "Dragify/Dragify 4.0/Marketing/App Store Images/2.0/3.jpg",
        "1001x1651+104+905",
        (420, 640, 840),
    ),
    (
        "ui-straightpic-editor",
        APPS / "StraightPic/Reference Photos/3 (rainbow editor).PNG",
        None,
        (420, 640, 840),
    ),
    # The same session, one screen later: the corrected frame with the transform
    # applied. Paired with the editor it tells the whole story in two real
    # captures, which is why the homepage no longer needs the drag-to-compare
    # slider it used to carry underneath.
    (
        "ui-straightpic-result",
        APPS / "StraightPic/Reference Photos/4 (rainbow result).PNG",
        None,
        (420, 640, 840),
    ),
]


def main() -> None:
    for stem, src, crop, widths in JOBS:
        if not src.exists():
            raise SystemExit(f"missing source: {src}")
        for w in widths:
            dest = OUT / f"{stem}-{w}.webp"
            cmd = ["magick", str(src)]
            if crop:
                cmd += ["-crop", crop, "+repage"]
            cmd += [
                "-resize", f"{w}x",
                "-quality", "82",
                "-define", "webp:method=6",
                str(dest),
            ]
            subprocess.run(cmd, check=True)
            size = dest.stat().st_size / 1024
            out = subprocess.run(
                ["identify", "-format", "%wx%h", str(dest)],
                capture_output=True, text=True, check=True,
            ).stdout
            print(f"{dest.name:34} {out:>10}  {size:6.1f} KB")


if __name__ == "__main__":
    main()
