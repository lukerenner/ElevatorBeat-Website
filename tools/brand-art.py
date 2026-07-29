#!/usr/bin/env python3
"""Regenerate the two environmental images that carry the brand story.

The site's image sequence is one upward journey through one world, shot as if
by one camera:

    hero     ground-level arrival — the tower rises out of the top of frame
    ascent   a close view up the shaft, the car caught mid-rise  (this script)
    terrace  the view from the observation level, high above the valley

`assets/img/hero-*.webp` is the reference every other frame is matched to: it
already has the palette, lens, grain and finish the brand wants, so it is
passed to the model as an image input rather than described in words. The
earlier house-day / house-dusk art was generated against different references
and drifted into a separate look (flat pastel daylight, and a violet party
scene) — that mismatch is what this replaces.

Both prompts deliberately reserve the LEFT third of the frame for open sky.
Each image carries overlaid copy on that side, and composing the emptiness in
means the page needs only a light scrim rather than one heavy enough to flatten
the painting.

Pipeline mirrors tools/house-art.py: nano-banana generates, real-esrgan doubles
the resolution, ImageMagick emits the WebP srcset variants.

Usage:  python3 brand-art.py [--skip-generate] [--skip-upscale]
"""
import base64
import mimetypes
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img"
MASTERS = SITE / "Reference Images" / "Retrofuturism" / "_upscaled"

GEN_MODEL = "google/nano-banana"
UPSCALE_MODEL = ("nightmareai/real-esrgan:"
                 "f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa")

# Repeated verbatim in both prompts. The exclusions are as load-bearing as the
# description: earlier passes filled empty space with robots, rockets and party
# crowds, which is exactly the "visual spectacle" the brand is not.
STYLE = (
    "Retro-futurist cinematic matte painting. Match the reference image exactly "
    "for palette, lens, brush handling, grain and level of finish: deep blue "
    "sky with fine stars, warm amber architectural light, copper and desert-rust "
    "rock, restrained cyan glints in the glass, analog film grain, soft "
    "atmospheric haze, painted brushwork. Optimistic 1950s Palm Springs "
    "architecture relocated to a distant planet. Sophisticated, quiet, "
    "architectural. No text, no lettering, no signature, no watermark. "
    "No robots, no rockets, no spacecraft, no crowds, no party."
)

# The building, described identically everywhere so the model keeps rebuilding
# the same structure instead of inventing a new one per scene.
TOWER = (
    "the slender cylindrical glass elevator tower of the same building as the "
    "reference — a round mid-century glass pavilion with a low floating disc "
    "roof — the tower's lit glass car visible inside the shaft"
)

# name -> (prompt, reference images, aspect ratio, widths to emit)
JOBS = {
    # Brand-idea band: the middle frame of the journey. Reads as ascent.
    "ascent": (
        f"{STYLE} A low three-quarter view looking steeply UP {TOWER}, from "
        "close to its base. The lit glass car is caught mid-shaft on its way "
        "up, its warm amber interior glowing, a thin cyan light line running "
        "the full height of the shaft rails beside it. The tower's structural "
        "rings recede sharply upward into a deep blue starlit sky, strong "
        "vertical perspective and a clear sense of motion and ascent. Along "
        "the bottom edge: the pale concrete deck and the edge of the disc "
        "roof, a few date palms and copper boulders catching warm light. "
        "COMPOSITION: the tower stands in the RIGHT half of the frame; the "
        "LEFT third is open, empty, deep blue sky. No people.",
        ["hero-1400.webp"],
        "21:9", [900, 1400, 1920, 2400, 3000],
    ),
    # Closing band: the top of the journey — the view the ride bought you.
    "terrace": (
        f"{STYLE} The view FROM an open-air observation terrace high on {TOWER}, "
        "at golden hour. Foreground: a curved chrome-and-glass railing, a "
        "section of pale terrazzo deck, two low mid-century lounge chairs and "
        "a small round table, all lit warmly from the side. Two small distant "
        "figures stand at the railing seen from behind, tiny in the frame. "
        "Far below and beyond: a desert valley of scattered low modernist "
        "pavilions with warm lit windows, date palms, a turquoise pool, copper "
        "rock formations, and distant mountains fading into haze. Deep blue "
        "sky above with a warm amber band at the horizon. Calm, spacious, "
        "elevated. COMPOSITION: railing, chairs and detail sit in the RIGHT "
        "half; the LEFT third is open sky and distant valley haze, uncluttered.",
        ["hero-1400.webp", "about-1400.webp"],
        "16:9", [900, 1400, 1920, 2400],
    ),
}


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/webp"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def fetch(out) -> bytes:
    """replicate.run returns either a file-like object or a URL string."""
    if hasattr(out, "read"):
        return out.read()
    if isinstance(out, list):
        out = out[0]
    if hasattr(out, "read"):
        return out.read()
    return urllib.request.urlopen(str(out)).read()


def generate():
    import replicate
    MASTERS.mkdir(parents=True, exist_ok=True)
    for name, (prompt, refs, ratio, _widths) in JOBS.items():
        raw = MASTERS / f"{name}.raw.png"
        if raw.exists():
            print(f"  {name}: already generated, skipping")
            continue
        print(f"  {name}: generating …", flush=True)
        out = replicate.run(GEN_MODEL, input={
            "prompt": prompt,
            "image_input": [data_uri(OUT / r) for r in refs],
            "aspect_ratio": ratio,
            "output_format": "png",
        })
        raw.write_bytes(fetch(out))
        print(f"  {name}: wrote {raw.name}", flush=True)


def upscale():
    import replicate
    for name in JOBS:
        raw, master = MASTERS / f"{name}.raw.png", MASTERS / f"{name}.png"
        if master.exists():
            print(f"  {name}: master already present, skipping")
            continue
        if not raw.exists():
            print(f"  {name}: nothing to upscale")
            continue
        print(f"  {name}: upscaling …", flush=True)
        with open(raw, "rb") as fh:
            # face_enhance plasticizes the small painted figures — leave it off.
            out = replicate.run(UPSCALE_MODEL,
                                input={"image": fh, "scale": 2,
                                       "face_enhance": False})
        master.write_bytes(fetch(out))
        print(f"  {name}: wrote {master.name}", flush=True)


def render():
    for name, (_p, _r, _a, widths) in JOBS.items():
        master = MASTERS / f"{name}.png"
        if not master.exists():
            print(f"  {name}: no master, skipping")
            continue
        for w in widths:
            subprocess.run([
                "magick", str(master),
                "-filter", "Lanczos", "-resize", f"{w}x",
                "-unsharp", "0x0.6+0.35+0.02",
                "-define", "webp:method=6", "-quality", "78",
                str(OUT / f"{name}-{w}.webp"),
            ], check=True)
        print(f"  {name}: {len(widths)} variants", flush=True)


if __name__ == "__main__":
    if not os.environ.get("REPLICATE_API_TOKEN"):
        sys.exit("REPLICATE_API_TOKEN is not set.")
    if "--skip-generate" not in sys.argv:
        generate()
    if "--skip-upscale" not in sys.argv:
        upscale()
    render()
    print("Done.")
