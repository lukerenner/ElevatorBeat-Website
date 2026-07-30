#!/usr/bin/env python3
"""Export the curated Dragify exhibition from the app's own pack data.

WHY THIS EXISTS
---------------
The homepage used to show five Dragify "looks" cut out of
`assets/img/dragify-looks-2724.webp` by `tools/dragify-sheet.py`. That sheet is a
contact strip in which **every tile already has a rounded corner baked onto a white
ground**. Cutting a tile at its bounding box therefore shipped white corner pixels
inside the file, which then sat inside a second, differently-radiused CSS frame — the
white triangles visible on the old page. No CSS could fix it; the white was in the
JPEG data.

The real artwork was on disk all along. Dragify's backend carries five signed packs
with names, descriptions and ~90 full-bleed look images at 768–1024px:

    Apps/Dragify/Dragify 4.0/App/backend/data/packs/<pack_id>/

Those are full-bleed with no baked corners and no white ground, so they can be cropped
and framed freely. They are the canonical source for site imagery from now on.

THE EDIT
--------
Eighteen looks, chosen for visual quality, spread across all five collections, and
sequenced so that colour, silhouette and setting change from one frame to the next.
The homepage labels by COLLECTION only — the individual queen names stay in the app.

Eighteen and not fifteen because the homepage now shows the collection through a fixed
aperture — three columns of six, held still while the window travels over them — and a
wall that has to be taller than the viewport in both directions needs enough frames to
fill it without ever repeating one. Appending to EDIT is safe: the index comes from the
list order, so 01–15 keep the filenames they already ship under.

Every look is emitted at the SAME 2:3 ratio. That is deliberate: the brief asks for
shared cropping, margins and presentation so eighteen unrelated portraits read as one
exhibition — and with the mosaic now a single grid of one shape, that ratio is also the
only one on the page, so no frame is cropped away from what the app returns.

Sources are 768–1024px, so 1200 is the largest honest width. Nothing is upscaled.

Usage:  python3 dragify-looks.py
"""
import json
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img" / "dragify"
PACKS = Path(
    "/Users/luke/Library/CloudStorage/GoogleDrive-luke.renner@gmail.com/My Drive"
    "/Antigravity/Apps/Dragify/Dragify 4.0/App/backend/data/packs"
)

WIDTHS = [480, 800, 1200]
RATIO_W, RATIO_H = 2, 3

# slug -> (pack directory, display name, description)
# Names and descriptions are lifted verbatim from the packs' own index.json so the
# site can never drift from what the app actually ships.
COLLECTIONS = {
    "haute-haus":       ("haute_haus",       "Haute Haus",       "Intercontinental couture"),
    "afterglow":        ("afterglow",        "Afterglow",        "A black tie affair"),
    "euphoria-uv":      ("euphoria_uv",      "Euphoria // UV",   "Electric love and molly magnificence"),
    "canonical-queens": ("canonical_queens", "Canonical Queens", "Iconic looks that always cook"),
    "ground-control":   ("ground_control",   "Ground Control",   "Retro-futurist space drag"),
}

# (slug, source filename, alt text). Order IS the gallery order.
#
# The sequence opens on Haute Haus — full-length couture shot against raw concrete,
# which is the closest the collection comes to the site's own architecture — and closes
# on Ground Control, whose retro-futurism is the same world the rest of the page is set
# in. Between them the ground changes every frame: concrete, jewel-lit interior, neon,
# flat saturated seamless.
EDIT = [
    ("haute-haus", "11. Nadja Evangelique.jpg",
     "A Haute Haus look: a copper satin mermaid gown with opera gloves, photographed "
     "in a raw concrete colonnade."),
    ("afterglow", "3. Maribel Kensington.jpg",
     "An Afterglow look: an emerald sequinned gown and matching fur, lit by teal "
     "chandeliers in a grand salon."),
    ("euphoria-uv", "9. Sasha Velvet.jpg",
     "A Euphoria // UV look: a purple sequinned bodice and dark bouffant framed by a "
     "red neon rectangle."),
    ("canonical-queens", "6. Hannah Nevada.jpg",
     "A Canonical Queens look: a tall blue updo and a monochrome zebra gown against a "
     "flat cyan ground."),
    ("haute-haus", "2. Isolde Versachi.jpg",
     "A Haute Haus look: a tiered teal tulle ball gown with sheer sleeves, shot in a "
     "concrete courtyard."),
    ("afterglow", "8. Octavia Sterling.jpg",
     "An Afterglow look: a white feathered gown beside a lit pool under a full moon, "
     "holding a sparkler."),
    ("ground-control", "3. Gigi Stardust.jpg",
     "A Ground Control look: a silver and mint flight suit with a rocket headdress and "
     "a smoking ray gun."),
    ("euphoria-uv", "15. Kitty Caliente.jpg",
     "A Euphoria // UV look: candyfloss curls and a liquid silver dress cut through by "
     "a blue neon beam."),
    ("haute-haus", "9. Tatiana von Runvay.jpg",
     "A Haute Haus look: a cream feathered gown with a ruffled train against pale "
     "concrete."),
    ("canonical-queens", "14. Imani Obscura.jpg",
     "A Canonical Queens look: a black strapless gown with a long train and a full "
     "afro, on a flat green ground."),
    ("afterglow", "11. Lorelei Whitaker.jpg",
     "An Afterglow look: an embroidered emerald suit and finger waves in a red-lit "
     "drawing room."),
    ("euphoria-uv", "12. Stella Sorrento.jpg",
     "A Euphoria // UV look: a teal bob and a zipped leather dress in front of hot pink "
     "neon rings."),
    ("haute-haus", "12. Madame San Laurent.jpg",
     "A Haute Haus look: an enormous black tulle ball gown with a beaded bodice, shot "
     "against concrete."),
    ("afterglow", "1. Lucinda Biltmore.jpg",
     "An Afterglow look: a crimson beaded gown and auburn waves in a red velvet salon."),
    ("ground-control", "10. Major Climax.jpg",
     "A Ground Control look: a lilac flight suit and an antenna bouffant, holding a "
     "prop scanner."),
    # 16–18 extend the wall to eighteen. They are appended rather than interleaved so
    # the first fifteen keep their stems, and they still land the sequence on Ground
    # Control: saturated seamless, then neon, then the retro-futurism the page is set
    # in.
    ("canonical-queens", "1. Lola Luxeon.jpg",
     "A Canonical Queens look: a lilac bouffant and a scarlet blazer over a red mini "
     "dress, against a hot pink ground."),
    ("euphoria-uv", "19. Roxy Riviera.jpg",
     "A Euphoria // UV look: platinum waves and a black latex dress with opera gloves, "
     "under a pink neon heart."),
    ("ground-control", "12. Glimmer Rocketblaster.jpg",
     "A Ground Control look: a silver flight suit and a bubble helmet over a platinum "
     "bouffant, ray gun in hand."),
]


def identify(path):
    out = subprocess.run(
        ["magick", "identify", "-format", "%w %h", str(path)],
        check=True, capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []

    for index, (slug, filename, alt) in enumerate(EDIT, start=1):
        pack_dir, name, description = COLLECTIONS[slug]
        source = PACKS / pack_dir / "assets" / filename
        if not source.exists():
            sys.exit(f"missing source: {source}")

        w, h = identify(source)
        # Crop to 2:3 by trimming the LONGER axis only, so nothing is ever stretched
        # and the figure keeps its proportions.
        if w * RATIO_H > h * RATIO_W:
            crop_w, crop_h = round(h * RATIO_W / RATIO_H), h
        else:
            crop_w, crop_h = w, round(w * RATIO_H / RATIO_W)

        # Never upscale. Where a source is too small for the next rung on the ladder
        # (the Haute Haus frames are square, so a 2:3 crop is only ~683px wide), emit
        # the source's own maximum instead of silently dropping the large candidate —
        # otherwise those looks would have nothing above 480px to serve a wide slot.
        widths = [w for w in WIDTHS if w <= crop_w]
        if crop_w - (widths[-1] if widths else 0) >= 64:
            widths.append(crop_w - crop_w % 2)

        stem = f"{slug}-{index:02d}"
        for width in widths:
            height = round(width * RATIO_H / RATIO_W)
            subprocess.run([
                "magick", str(source),
                "-gravity", "center", "-crop", f"{crop_w}x{crop_h}+0+0", "+repage",
                "-filter", "Lanczos", "-resize", f"{width}x{height}!",
                "-unsharp", "0x0.6+0.5+0.02",
                "-quality", "82", "-define", "webp:method=6",
                str(OUT / f"{stem}-{width}.webp"),
            ], check=True)

        emitted = sorted(int(p.stem.rsplit("-", 1)[1]) for p in OUT.glob(f"{stem}-*.webp"))
        manifest.append({
            "index": index, "collection": slug, "collection_name": name,
            "collection_description": description, "stem": stem,
            "widths": emitted, "source": filename, "alt": alt,
        })
        print(f"  {stem:<22} {w}x{h} -> 2:3 {emitted}")

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"\n{len(manifest)} looks across {len({m['collection'] for m in manifest})} collections")


if __name__ == "__main__":
    main()
