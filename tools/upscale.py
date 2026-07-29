#!/usr/bin/env python3
"""Upscale the retro-futurist source paintings via Replicate (Real-ESRGAN),
then regenerate the site's WebP variants from the higher-resolution masters.

Only the five paintings used as large/full-bleed art are worth upscaling — the
Dragify and StraightPic product shots are already well above their display size.

Usage:  REPLICATE_API_TOKEN=... python3 upscale.py [--skip-upscale]
"""
import os
import subprocess
import sys
from pathlib import Path

# Resolved from this file's location rather than hardcoded, so renaming the
# project folder doesn't break it.
SITE = Path(__file__).resolve().parent.parent
RETRO = SITE / "Reference Images" / "Retrofuturism"
OUT = SITE / "assets" / "img"
MASTERS = RETRO / "_upscaled"
MODEL = "nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa"

# name -> (source painting, crop or None, widths to emit)
# Widths gain larger candidates now that the masters carry real detail.
JOBS = {
    # The hero master is cropped 4:3 -> 3:2, trimming the empty pool foreground
    # so the full-bleed cover crop doesn't have to eat the moon or the lounge.
    "hero":      ("FuturePlane10.png", "5792x3861+0+120", [900, 1400, 1920, 2400]),
    "band-mars": ("FuturePlane8.png",  None, [900, 1400, 1920, 2400, 3000]),
    "cta":       ("FuturePlane3.png",  None, [900, 1300, 1800, 2200, 2800]),
    "lounge":    ("FuturePlane2.png",  None, [640, 960, 1280, 1600]),
    "nextup":    ("FuturePlane9.png",  None, [700, 1000, 1400, 1800]),
}


def upscale_all():
    import replicate
    MASTERS.mkdir(parents=True, exist_ok=True)
    for name, (src, _crop, _widths) in JOBS.items():
        dest = MASTERS / f"{name}.png"
        if dest.exists():
            print(f"  {name}: master already present, skipping")
            continue
        print(f"  {name}: upscaling {src} …", flush=True)
        with open(RETRO / src, "rb") as fh:
            out = replicate.run(MODEL, input={"image": fh, "scale": 4,
                                              "face_enhance": False})
        data = out.read() if hasattr(out, "read") else None
        if data is None:                      # older client returns a URL string
            import urllib.request
            data = urllib.request.urlopen(str(out)).read()
        dest.write_bytes(data)
        print(f"  {name}: wrote {dest.name} ({len(data)/1e6:.1f} MB)")


def render():
    """Re-encode the WebP variants from the upscaled masters."""
    for name, (_src, crop, widths) in JOBS.items():
        master = MASTERS / f"{name}.png"
        if not master.exists():
            print(f"  {name}: no master, skipping")
            continue
        for w in widths:
            cmd = ["magick", str(master)]
            if crop:
                cmd += ["-crop", crop, "+repage"]
            cmd += ["-filter", "Lanczos", "-resize", f"{w}x",
                    "-unsharp", "0x0.6+0.35+0.02",
                    "-define", "webp:method=6", "-quality", "78",
                    str(OUT / f"{name}-{w}.webp")]
            subprocess.run(cmd, check=True)
        print(f"  {name}: {len(widths)} variants")


if __name__ == "__main__":
    if "--skip-upscale" not in sys.argv:
        if not os.environ.get("REPLICATE_API_TOKEN"):
            sys.exit("REPLICATE_API_TOKEN is not set")
        print("Upscaling masters via Replicate …")
        upscale_all()
    print("Rendering WebP variants …")
    render()
    print("Done. Bump the ?v= cache-bust in the four HTML files.")
