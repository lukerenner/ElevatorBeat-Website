#!/usr/bin/env python3
"""Regenerate the site's full-bleed art so every painting shows the SAME house.

The site's visual premise is one building — a round mid-century glass pavilion
with a slender glass elevator tower — seen at different hours and from
different vantage points. `assets/img/about-*.webp` (night, interior, looking
out over the valley) is the reference the other views are matched to.

Pipeline mirrors tools/upscale.py: nano-banana generates, real-esrgan doubles
the resolution, ImageMagick emits the WebP srcset variants.

Usage:  python3 house-art.py [--skip-generate] [--skip-upscale]
"""
import base64
import mimetypes
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

# The house, described identically in every prompt so the model keeps building
# the same structure rather than a new one per scene.
HOUSE = ("a single round mid-century-modern glass pavilion house with a low "
         "floating disc roof, curved floor-to-ceiling glass walls, warm amber "
         "interior lighting, and a slender cylindrical glass elevator tower "
         "rising through one side with its lit glass car visible inside the shaft")

STYLE = ("Retro-futurist matte painting, 1960s space-age optimism, painted "
         "brushwork, fine detail, cinematic, no text, no signature. Match the "
         "palette, brush handling and level of finish of the reference image.")

# name -> (prompt, reference images, aspect ratio, widths to emit)
JOBS = {
    # Origin band: the house from outside, mid-morning — the daylight view.
    "house-day": (
        f"{STYLE} Ultra-wide daylight view of the SAME building as the "
        f"reference: {HOUSE}. Seen from across a Palm Springs desert valley in "
        "clear late-morning sun, the San Jacinto mountains rising behind it, "
        "date palms, agave, pale boulders and a turquoise pool around its base, "
        "a long pale concrete drive leading to it. Bright warm blue sky with "
        "high thin clouds. No moon, no rocket, no people, no vehicles.",
        ["about-1400.webp", "band-mars-1400.webp"],
        "21:9", [900, 1400, 1920, 2400, 3000],
    ),
    # Closing CTA: the house at sunset, from the pool deck, elevator prominent.
    "house-dusk": (
        f"{STYLE} Sunset view of the SAME building as the reference, seen from "
        f"its pool deck: {HOUSE}, the glass elevator tower prominent at the "
        "right and clearly glowing from within. Foreground: a warm, relaxed "
        "evening party around a turquoise pool. Two men in dinner jackets stand "
        "close together holding coupe glasses, one resting a hand on the "
        "other's back; beside them two women in tailored tuxedos laugh "
        "together; behind them a mixed crowd of friends of many ages and "
        "skin tones in 1960s evening wear. Chrome robots carry trays of "
        "cocktails. Palm trees, glowing globe lamps, low desert mountains, "
        "an orange-into-violet sunset sky with early stars.",
        ["cta-1300.webp", "about-1400.webp"],
        "4:3", [900, 1300, 1800, 2200, 2800],
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
        print(f"  {name}: wrote {raw.name}")


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
        print(f"  {name}: wrote {master.name}")


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
        print(f"  {name}: {len(widths)} variants")


if __name__ == "__main__":
    if "--skip-generate" not in sys.argv:
        generate()
    if "--skip-upscale" not in sys.argv:
        upscale()
    render()
    print("Done.")
