#!/usr/bin/env python3
"""Cut the homepage's architectural frames from the upscaled masters.

The retro-futurist paintings live at 3072-7664px in
`Reference Images/Retrofuturism/_upscaled/` (git-ignored, not deployed). Everything
this script emits is a derivative of those masters; the masters themselves are never
written to. Re-running is free and idempotent.

TWO THINGS THIS DOES THAT A PLAIN RESIZE DOES NOT
-------------------------------------------------
1. ART-DIRECTED CROPS, not `object-fit: cover` guesses. A 4:3 painting squeezed into a
   phone viewport by CSS loses whichever third of the composition happens to fall
   outside the box. Each mobile crop below was chosen against the actual subjects — the
   offsets are measured, not eyeballed defaults — and is served through `<picture>` so
   the browser fetches the right framing rather than cropping the wrong one.

2. A RESTRAINED SHARED GRADE. The collection spans cool blue night, pale daylight and
   deep copper dusk. `band-mars` and `cta` sit far enough into the reds that they read
   as a different world from `about` and `house-day`. GRADE pulls saturation back a
   few points on those frames only.

   This is deliberately a small global desaturation rather than a hue-targeted filter
   or a cyan wash. Those images are ~90% warm rock and sky, so scaling saturation
   lowers the orange almost exclusively, while skin, white architecture and desert rock
   keep their own colour. The goal is related images, not identical ones.

Heights are computed from each master's true ratio and every emitted size lands on
whole pixels, so a CSS `aspect-ratio` can never disagree with the file it is framing.

Usage:  python3 exhibit-art.py
"""
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img"
MASTERS = SITE / "Reference Images" / "Retrofuturism" / "_upscaled"

# name -> dict(master, crop, grade, widths)
#   crop  : (w, h, x, y) in master pixels, or None for the full frame
#   grade : saturation percentage, or None to leave the frame alone
JOBS = {
    # ---- ARRIVAL -------------------------------------------------------------
    # Desktop keeps the painting's own 3:2 (the master trimmed of its empty pool
    # foreground, matching what tools/upscale.py has always emitted).
    "hero": dict(master="hero.png", crop=(5792, 3861, 0, 120), grade=None,
                 widths=[900, 1400, 1920, 2400]),
    # Portrait arrival. 4:5 out of a 4:3 master throws away 40% of the width, so the
    # offset matters: +560 is the only window holding the moon (left), the rocket
    # trail, the lit observation deck and the tower together. Centring instead would
    # cut the moon in half, which is the one element the whole frame is composed
    # around.
    "hero-mobile": dict(master="hero.png", crop=(3475, 4344, 560, 0), grade=None,
                        widths=[560, 760, 1000, 1240]),

    # ---- THE LOUNGE ----------------------------------------------------------
    # Was capped at 1600px, which was soft the moment it went full-frame. Rebuilt from
    # the master. A light grade only: the amber interior lighting is the point of the
    # room, it just should not out-shout `about`.
    "lounge": dict(master="lounge.png", crop=None, grade=94,
                   widths=[960, 1400, 1920, 2400]),

    # ---- THE GROUNDS ---------------------------------------------------------
    "band-mars": dict(master="band-mars.png", crop=None, grade=92,
                      widths=[900, 1400, 1920, 2400, 3000]),
    # A 2.33:1 strip is 160px tall on a phone — too thin to read as a chapter break.
    # 16:9 at +1400 keeps the moon's edge, the full pavilion and elevator, and the
    # rocket trail that connects them.
    "band-mars-mobile": dict(master="band-mars.png", crop=(5838, 3284, 1400, 0),
                             grade=92, widths=[640, 960, 1280]),

    # ---- CLOSING -------------------------------------------------------------
    # No mobile crop on purpose. The people, robot, pool, building and rocket are all
    # part of this scene; on narrow viewports it stacks above the copy at its natural
    # 4:3 instead of being cropped down to whichever third fits.
    "cta": dict(master="cta.png", crop=None, grade=92,
                widths=[900, 1300, 1800, 2200, 2800]),
}


def identify(path):
    out = subprocess.run(
        ["magick", "identify", "-format", "%w %h", str(path)],
        check=True, capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])


def main():
    if not MASTERS.is_dir():
        sys.exit(f"masters not found: {MASTERS}\n"
                 "They are git-ignored — see README.md, 'Upscaled masters'.")

    for name, job in JOBS.items():
        master = MASTERS / job["master"]
        if not master.exists():
            print(f"  {name}: SKIP (no {job['master']})")
            continue

        if job["crop"]:
            cw, ch, cx, cy = job["crop"]
        else:
            cw, ch = identify(master)
            cx = cy = 0

        emitted = []
        for width in job["widths"]:
            if width > cw:
                continue
            # Derive height from the crop's true ratio, then hold the resize to that
            # exact pixel pair. No rounding drift, no 1px letterbox.
            height = round(width * ch / cw)
            args = ["magick", str(master)]
            if job["crop"]:
                args += ["-crop", f"{cw}x{ch}+{cx}+{cy}", "+repage"]
            if job["grade"]:
                args += ["-modulate", f"100,{job['grade']},100"]
            args += ["-filter", "Lanczos", "-resize", f"{width}x{height}!",
                     "-unsharp", "0x0.5+0.4+0.02",
                     "-quality", "78", "-define", "webp:method=6",
                     str(OUT / f"{name}-{width}.webp")]
            subprocess.run(args, check=True)
            emitted.append(f"{width}x{height}")

        grade = f" grade {job['grade']}" if job["grade"] else ""
        print(f"  {name:<18} {cw}x{ch}{grade} -> {', '.join(emitted)}")


if __name__ == "__main__":
    main()
