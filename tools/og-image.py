#!/usr/bin/env python3
"""Render assets/og-image.jpg — the social preview card.

Rendered through headless Chrome from a real HTML card rather than composited
with ImageMagick, so the card uses the same self-hosted display face, the same
palette and the same cyan tick as the site. A hand-composited version drifts
from the brand the moment either changes.

The previous card set the wordmark as two words ("Elevator Beat") and described
the studio as a "creative app studio". Both are wrong: the mark is one word, and
the studio is an independent app studio. Since this image is what gets pasted
into Slack, iMessage and every social card, it is the single most-copied place
to get the name wrong — hence a generator instead of a one-off export.

Usage:  python3 og-image.py
"""
import base64
import subprocess
import sys
import tempfile
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

WIDTH, HEIGHT = 1200, 630


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def build_html() -> str:
    hero = data_uri(SITE / "assets/img/hero-1400.webp", "image/webp")
    serif = data_uri(SITE / "assets/fonts/instrument-serif-latin.woff2", "font/woff2")
    return f"""<!doctype html><meta charset="utf-8"><style>
  @font-face {{ font-family: "Instrument Serif"; src: url({serif}) format("woff2"); }}
  * {{ margin: 0; box-sizing: border-box; }}
  body {{ width: {WIDTH}px; height: {HEIGHT}px; overflow: hidden; position: relative;
          background: #08131F; font-family: -apple-system, "Helvetica Neue", sans-serif; }}
  img {{ position: absolute; inset: 0; width: 100%; height: 100%;
         object-fit: cover; object-position: 62% 52%; }}
  .scrim {{ position: absolute; inset: 0; background: linear-gradient(to right,
      rgba(5,12,21,.93) 0%, rgba(5,12,21,.80) 34%, rgba(5,12,21,.32) 64%, rgba(5,12,21,0) 92%); }}
  .card {{ position: absolute; inset: 0; padding: 72px 80px;
           display: flex; flex-direction: column; justify-content: center; }}
  .eyebrow {{ display: flex; align-items: center; gap: 14px; margin-bottom: 26px;
              font-size: 17px; font-weight: 600; letter-spacing: .085em;
              text-transform: uppercase; color: #00D8ED; }}
  .eyebrow::before {{ content: ""; width: 34px; height: 2px; background: currentColor; }}
  h1 {{ font-family: "Instrument Serif", serif; font-weight: 400; font-size: 78px;
        line-height: 1.04; letter-spacing: -.018em; color: #F3ECE1; max-width: 13ch; }}
  p {{ margin-top: 26px; font-size: 25px; line-height: 1.45;
       color: rgba(243,236,225,.82); max-width: 30ch; }}
</style>
<img src="{hero}" alt=""><div class="scrim"></div>
<div class="card">
  <div class="eyebrow">ElevatorBeat &middot; Portland, Oregon</div>
  <h1>Small apps that take your work higher.</h1>
  <p>An independent app studio.</p>
</div>"""


def main():
    if not Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "og.html"
        html.write_text(build_html())
        png = Path(tmp) / "og.png"
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
            f"--screenshot={png}", f"--window-size={WIDTH},{HEIGHT}",
            "--virtual-time-budget=5000", html.as_uri(),
        ], check=True, capture_output=True)
        if not png.exists():
            sys.exit("Chrome produced no screenshot")
        out = SITE / "assets" / "og-image.jpg"
        subprocess.run(["magick", str(png), "-quality", "88", str(out)], check=True)
        print(f"  wrote {out.relative_to(SITE)} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
