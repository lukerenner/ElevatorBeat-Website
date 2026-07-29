#!/usr/bin/env python3
"""Re-cut only the foreground figures of the closing-CTA painting.

The first pass got the architecture right — same house as the hero, glass
elevator tower lit and prominent — but rendered the foreground pair as a man
and a woman. This edits that pass rather than regenerating from scratch, so
the building, lighting and palette stay identical.

Usage:  python3 house-dusk-refine.py
"""
import base64
import subprocess
import urllib.request
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img"
MASTERS = SITE / "Reference Images" / "Retrofuturism" / "_upscaled"
WIDTHS = [900, 1300, 1800, 2200, 2800]

PROMPT = (
    "Edit this retro-futurist matte painting. Keep the architecture, the glass "
    "elevator tower, the pool, the palms, the sunset sky, the lighting and the "
    "palette exactly as they are. Change only the people. "
    "In the left foreground, replace the couple with TWO MEN — both clearly "
    "male, both in 1960s dinner jackets and bow ties, one Black and one white, "
    "standing close together and smiling at each other, one with his arm around "
    "the other's waist, each holding a cocktail. "
    "In the right foreground, replace the figures with TWO WOMEN in tailored "
    "tuxedos, holding hands and laughing together. "
    "In the crowd behind, make the visible pairs same-sex couples — men with "
    "men, women with women — of many ages and skin tones. No man-and-woman "
    "couples anywhere in the picture. Keep the chrome robot waiters. "
    "Painted brushwork, fine detail, no text."
)


def fetch(out) -> bytes:
    if isinstance(out, list):
        out = out[0]
    if hasattr(out, "read"):
        return out.read()
    return urllib.request.urlopen(str(out)).read()


def main():
    import replicate
    src = MASTERS / "house-dusk.raw.png"
    edited = MASTERS / "house-dusk.edit.png"
    master = MASTERS / "house-dusk.png"

    print("editing foreground figures …", flush=True)
    uri = "data:image/png;base64," + base64.b64encode(src.read_bytes()).decode()
    out = replicate.run("google/nano-banana", input={
        "prompt": PROMPT,
        "image_input": [uri],
        "aspect_ratio": "4:3",
        "output_format": "png",
    })
    edited.write_bytes(fetch(out))

    print("upscaling …", flush=True)
    with open(edited, "rb") as fh:
        up = replicate.run(
            "nightmareai/real-esrgan:"
            "f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
            input={"image": fh, "scale": 2, "face_enhance": False})
    master.write_bytes(fetch(up))

    for w in WIDTHS:
        subprocess.run([
            "magick", str(master),
            "-filter", "Lanczos", "-resize", f"{w}x",
            "-unsharp", "0x0.6+0.35+0.02",
            "-define", "webp:method=6", "-quality", "78",
            str(OUT / f"house-dusk-{w}.webp"),
        ], check=True)
    print(f"wrote {len(WIDTHS)} variants")


if __name__ == "__main__":
    main()
