# ElevatorBeat — elevatorbeat.com

Marketing site for ElevatorBeat, a small app studio in Portland, Oregon. Currently Dragify
and StraightPic.

Positioning: *"A small app studio in Portland. We make focused iPhone apps."* The apps carry
the visual ambition, not the marketing copy around them. Dependency-free, hand-authored
HTML/CSS/JS — no build step.

## Run locally

```bash
python3 -m http.server 8642
```

Then open `http://localhost:8642`. `index.html` also opens directly in a browser with no
server, though relative links between pages work best served over HTTP.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Home page — the ten-beat shot list (see below) |
| `support.html` | App support (Dragify + StraightPic), links to contact |
| `privacy.html` | Privacy policy for the site and both apps |
| `terms.html` | Terms of use |
| `open-source.html` | Open source license notices for Dragify and StraightPic |
| `thanks.html` | Contact-form confirmation page — `noindex`, not in the sitemap |
| `styles.css` | All styling — dual-ground tokens in `:root` / `.on-dark`, the `.plate` image component, one button system |
| `script.js` | Before/after slider, transparent-until-scroll header, mobile nav, canonical-policy dialog, the rail, scroll reveals |
| `assets/` | Favicon (SVG), apple touch icon, OG/social share image |
| `assets/img/` | All site photography, WebP, multiple widths per image for `srcset` |
| `assets/video/` | Superseded hero animation — **no longer referenced**, kept on disk only |
| `tools/exhibit-art.py` | Cuts every architectural frame + art-directed mobile crops from the upscaled masters — dev only |
| `tools/dragify-looks.py` | Exports the curated Dragify exhibition from the app's pack data — dev only |
| `tools/straightpic-demo.py` | Builds the StraightPic before/after from `Tower.jpg` — dev only |
| `tools/upscale.py` | Regenerates the original retro art from upscaled masters — dev only |
| `tools/house-art.py`, `tools/house-dusk-refine.py` | Generate the `house-day` / `house-dusk` paintings — dev only |
| `tools/deprecated/` | Superseded generators, kept for provenance — see the Dragify note below |
| `robots.txt` | Allows crawling, points at sitemap |
| `sitemap.xml` | Lists all five indexable pages (thanks.html is deliberately excluded) |
| `CNAME` | Custom domain for GitHub Pages (`elevatorbeat.com`) |

## Design system — two grounds, one set of components

The page has two grounds, not one. **Warm white is the primary canvas** — where the work is
explained, catalogued and read. **Midnight is reserved for the architecture**, full-frame and
edge to edge.

Both are expressed through the *same* custom properties. `:root` carries the paper palette;
`.on-dark` overrides those properties in place. Every component — eyebrows, rules, captions,
buttons, plates, the rail — reads `var(--ground)` / `var(--text)` / `var(--accent)`, so it
works on either ground with no duplicate rulesets. **Adding a section means picking a ground,
not writing a second theme.**

Cyan is an annotation, not a brand wash: hairlines, ticks, the compare handle, the rail car,
focus rings. The solid button is the inverse of whatever it sits on (ink on paper, ivory on
midnight) — deliberately *not* cyan, because a large cyan rectangle over a photograph is the
generic CTA reflex this system exists to avoid. Copper comes off the elevator's amber lighting
and appears only as exhibition numerals.

Four display tiers (`.display-xl` / `-l` / `-m` / `-s`) are chosen by the job a headline is
doing, not by its heading level. The previous build ran every section at one `h2` size, which
is most of why it read as a template.

## The page — a shot list

Ten beats, cut like a film rather than assembled from a formula. There is no rule forcing
white and dark to alternate; sequence follows narrative continuity, contrast and pacing.

| # | Beat | Ground | Asset |
| --- | --- | --- | --- |
| 01 | Arrival — the front elevation | dark | `hero-*` / `hero-mobile-*` |
| 02 | The studio — one oversized statement | paper | — |
| 03 | The lounge — interior, straight after the exterior | dark | `lounge-*` |
| 04 | Exhibition 01, Dragify — wall label, then a full-bleed gallery | paper → dark | `assets/img/dragify/*` |
| 05 | The grounds — panoramic interlude, caption only | dark | `band-mars-*` |
| 06 | Morning — the one daylight frame | **paper over image** | `house-day-*` |
| 07 | Exhibition 02, StraightPic — geometric, annotated | paper | `straightpic-*` |
| 08 | The observation level — another room, another hour | dark | `about-*` |
| 09 | Closing — split editorial | paper + image | `cta-*` |

Beat 06 is the one chapter that does **not** carry `.on-dark`. Darkening a pale morning sky
enough to hold ivory type would turn the morning into another dusk — the "every image becomes
the same dark scene" failure. Its type is near-black and its scrim *lifts* the sky instead
(`.scrim-lift`). Same component, inverted ground.

Held back deliberately, for interior pages and OG artwork: `terrace-*` (duplicates
`house-day`'s landscape role), `ascent-*` (too close to the hero to sit on the same page),
`house-dusk-*` (duplicates `cta`), `nextup-*`.

## The plate — the one image component

Every photograph goes through `.plate`. The rules are not stylistic preferences; each closes a
specific way a rounded image leaks white pixels at its corners:

- The radius and `overflow: hidden` are on the **same element**. Split across a wrapper and a
  child, the child's square corners poke out of the parent's round ones.
- **No border.** A 1px stroke plus a radius is exactly where a corner seam comes from — the
  stroke and the clip antialias on different subpixel boundaries. Separation comes from the
  ground.
- The background is `var(--ground)`, so a sub-pixel of wrapper showing through is invisible
  rather than a bright triangle — and it is never white on a dark section, because `--ground`
  follows `.on-dark`.
- `aspect-ratio` on the plate, so its height always agrees with the file inside it.
- Full-bleed cinematic images set `--plate-radius: 0`. Editorial photography is not a card.

Grid widths are fractional at fluid breakpoints. That is fine and is *not* worth chasing: the
clip and the image are the same element, so they antialias together, and the ground behind
them matches.

`<picture>` must be told to fill: it is an inline wrapper by default, so an `<img>` inside it
resolving `height: 100%` measures against the picture's own content height, not the chapter.
`.chapter-media picture { display: block; height: 100% }` exists for exactly that reason.

## Imagery

Two sources. The retro-futurist paintings come from `Reference Images/Retrofuturism/`
(git-ignored, not deployed). The product imagery is pulled from the actual apps.

| Asset | Source |
| --- | --- |
| `hero-*`, `hero-mobile-*` | `_upscaled/hero.png` — arrival, plus an art-directed 4:5 portrait crop |
| `lounge-*` | `_upscaled/lounge.png` — studio interior |
| `band-mars-*`, `band-mars-mobile-*` | `_upscaled/band-mars.png` — the grounds; 16:9 crop for phones |
| `house-day-*` | the daylight frame |
| `about-*` | the observation level |
| `cta-*` | the closing scene |
| `assets/img/dragify/*` | Dragify's own pack data — see below |
| `straightpic-before/after-*` | `Apps/StraightPic/Reference Photos/Tower.jpg` |
| `icon-dragify-*`, `icon-straightpic-*` | the apps' `AppIcon` assets |

**Upscaled masters.** The paintings were only ~1448px wide natively. The ones used as large
art were run through Replicate (`nightmareai/real-esrgan`, `face_enhance=False` — it
plasticizes the small painted figures) and live as ~3000–7700px masters in
`Reference Images/Retrofuturism/_upscaled/`, git-ignored but kept on disk so a re-render never
pays for the upscale again.

**`tools/exhibit-art.py`** cuts every architectural frame from those masters. It does two
things a plain resize does not:

1. **Art-directed crops, not `object-fit: cover` guesses.** Each mobile crop was chosen
   against the actual subjects — the offsets are measured, not defaults — and is served
   through `<picture>`.
2. **A restrained shared grade.** `band-mars` and `cta` sit far enough into the reds that they
   read as a different world from `about` and `house-day`. A few points of desaturation on
   those frames only. Deliberately a small global desaturation rather than a hue-targeted
   filter or a cyan wash: those images are ~90% warm rock and sky, so it lowers the orange
   almost exclusively while skin, white architecture and desert rock keep their own colour.
   The goal is related images, not identical ones.

Heights are computed from each master's true ratio, so every emitted size lands on whole
pixels and a CSS `aspect-ratio` can never disagree with the file it frames.

### Dragify — the exhibition

`tools/dragify-looks.py` exports the gallery straight from Dragify's backend pack data
(`Dragify 4.0/App/backend/data/packs/`), which carries five signed collections and ~90
full-bleed look images at 768–1024px:

| Collection | Description |
| --- | --- |
| Canonical Queens | Iconic looks that always cook |
| Euphoria // UV | Electric love and molly magnificence |
| Afterglow | A black tie affair |
| Haute Haus | Intercontinental couture |
| Ground Control | Retro-futurist space drag |

Fifteen looks ship, chosen for visual quality, spread across all five collections, and
sequenced so colour, silhouette and setting change frame to frame. Twelve show at tablet
width, eight on a phone — abundance is the strength of the edit, not the count. The homepage
labels by **collection only**; the individual queen names stay in the app.

Every look is emitted at the same **2:3**. That is deliberate: shared cropping and presentation
are what make fifteen unrelated portraits read as one exhibition. Rhythm comes from how many
grid columns a frame spans and how far it is dropped, authored in `styles.css` (`.look:nth-child`)
rather than in the markup — so the whole edit can be re-timed in one place.

> **Deprecated: `assets/img/deprecated/`, `tools/deprecated/dragify-sheet.py`.**
> `dragify-looks-*.webp` is a fourteen-up contact sheet in which **every tile already has a
> rounded corner baked onto a white ground**. The old `dragify-sheet.py` cut tiles at their
> bounding box, so that white shipped inside the files, and inside a second differently-radiused
> CSS frame it showed as white triangles in the corner of every thumbnail. It was never a CSS
> bug — the white was in the image data. Nothing references those files; do not reintroduce them.

### StraightPic — the demonstration

`tools/straightpic-demo.py` builds the before/after from
`Apps/StraightPic/Reference Photos/Tower.jpg`, a 4284×5712 phone photograph of a brick
smokestack. It is architecture, it has strong converging verticals, and it is a picture worth
keeping — which is the whole argument. The source is already exactly 3:4, so both frames keep
the photographer's full composition.

The correction is a keystone reproducing the transform the app applies. **It is a
demonstration built from the raw photograph, not a screen recording of the app.**

The guide lines and corner handles are **not baked into the pixels** — they are an SVG overlay
in `index.html`, so they stay crisp at any density and the photographs underneath can be
swapped without redoing the artwork. The plate is 3:4 and so is the photograph, so with
`preserveAspectRatio="none"` the viewBox units map straight onto the picture at any size.

Better before/after photographs are welcome: drop them in at the same
`straightpic-before-*` / `straightpic-after-*` filenames and nothing else needs to change.

## The rail

A fixed hairline in the left gutter with a lit cyan segment tracking scroll position, a tick
at the top of every chapter, and two-digit chapter numerals above 1400px. It carries nothing
you cannot already see, which is why it is `aria-hidden`, and it is only built above 1100px
where there is gutter to spare. Tick positions come from the chapters themselves, so editing
the page cannot leave them pointing at nothing.

Because it is `position: fixed` it crosses both grounds. `script.js` therefore asks whether any
`.on-dark` band straddles a probe line 140px down the viewport, and colours the hairline to
match. Asking which *section* is at the top gets this wrong — the Dragify exhibition is one
section that opens on paper and then breaks full-bleed onto midnight for its gallery. Pure
geometry rather than `elementFromPoint`, so it cannot disagree with itself depending on when
in the frame it runs.

## Header

The header is transparent and absolutely positioned over the arrival image, then switches to a
solid paper bar once the page scrolls past 12px.

Pages with no photographic arrival (`support`, `contact`, `privacy`, `terms`, `open-source`,
`thanks`) ship `class="site-header is-solid"` in the markup. That starts them in the solid
appearance and makes `script.js` skip the scroll toggle entirely. **If you add a page,
remember the `is-solid`.**

## Canonical policy dialog

Dragify's terms and privacy policy are maintained on **dragifyapp.com**, and that copy stays
canonical — this site must never hold a second copy to keep in sync. The Dragify feature's
"Terms of Service" and "Privacy Policy" links therefore carry `data-legal-modal` and open a
native `<dialog>` that frames the live page, with an "open in a new tab" link alongside.

Notes for anyone touching this:

- The iframe `src` is set on open and reset to `about:blank` on close, so nothing is requested
  from dragifyapp.com unless a visitor actually asks for it.
- Teardown is wired to the close button, the backdrop click and the `cancel` (Esc) event —
  **not** to the `close` event alone. Some engines never fire `close` for a scripted
  `dialog.close()`, which left the third-party page loaded behind a dismissed dialog.
- Without JS the links are ordinary external links and still work.
- dragifyapp.com currently sends no `X-Frame-Options` or `frame-ancestors` CSP. If that ever
  changes the frame will go blank, and the "open in a new tab" link becomes the fallback.

StraightPic's links point at this site's own `terms.html` / `privacy.html`, which are single
documents covering both apps — hence no per-app fragment.

## Before/after slider

The Dragify mechanism uses a drag-to-compare slider. The control is a real
`<input type="range">` stretched invisibly over the whole frame, so pointer dragging *and*
keyboard arrows work without reimplementing either. `script.js` only mirrors its value onto a
`--split` custom property, which drives both the `clip-path` on the "before" image and the
handle position. Because the input is transparent, its focus ring is drawn on the frame via
`.compare:has(.compare-range:focus-visible)`.

It sits **inside** the Dragify exhibition, below the gallery and at a fraction of its size:
it demonstrates the mechanism, but the collection is the product. Both images are exported at
exactly 3:4 to match the plate, so `object-fit: cover` has nothing to crop.

StraightPic uses a static two-up installation instead of a slider — a different exhibition,
deliberately given a different form.

## Deploying to elevatorbeat.com (GitHub Pages)

1. Push this repo to GitHub (e.g. `elevatorbeat/website`).
2. In the repo's **Settings → Pages**, set the source to the `main` branch, root folder.
3. The `CNAME` file already in this repo tells GitHub Pages to serve the custom domain.
4. At your DNS provider, point `elevatorbeat.com` at GitHub Pages:
   - Apex domain (`elevatorbeat.com`): four `A` records to
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www.elevatorbeat.com` (optional): `CNAME` record to `<your-github-username>.github.io`
5. Back in **Settings → Pages**, enter `elevatorbeat.com` as the custom domain and enable
   **Enforce HTTPS** once the certificate provisions (can take up to ~24 hours after DNS
   propagates).

## Forms / contact

`contact.html` carries the contact form, posting to
[FormSubmit](https://formsubmit.co) at `hello@elevatorbeat.com` — no backend to run. It uses
a hidden `_honey` honeypot field with `_captcha` disabled, and `_next` redirects to
`thanks.html` on success. The homepage closes on a decision, not a five-field form — the form
lives where somebody who has already decided to write goes looking for it.

**Two things to do before launch:**

1. **`hello@elevatorbeat.com` does not exist yet** — the `elevatorbeat.com` domain still needs
   to be wired into Google Workspace. Until that inbox is live, submissions have nowhere to
   land.
2. **FormSubmit requires a one-time activation.** The very first submission triggers a
   confirmation email to that address; someone has to click the link in it before FormSubmit
   starts forwarding. Until that happens the form looks broken but isn't.

`thanks.html` is `noindex`, `Disallow`ed in `robots.txt`, and deliberately absent from
`sitemap.xml` — it should never be a search landing page.

## Legal pages

`privacy.html` and `terms.html` are drafted from the app descriptions on this site and are
a reasonable starting point, not a substitute for review by counsel — especially before
Dragify/StraightPic process real user photos at scale or collect payment data directly.

`open-source.html` carries both apps' notices. The Dragify list is a copy of the one on
dragifyapp.com/open-source/. The StraightPic section says the app has **no** third-party
open source components — that is checked, not assumed: its Xcode project has no Swift Package
or CocoaPods dependencies, and every framework it imports (SwiftUI, Core Image, Core Graphics,
Metal, ImageIO, Photos, AVFoundation, StoreKit) is Apple's own. Re-check that before shipping
StraightPic, and list anything new that gets added.

## Cache-busting

CSS/JS are loaded with a version query string (`styles.css?v=20260729e`). Bump it on any
meaningful change so browsers don't serve a stale cached copy — and bump it in all six
HTML files together, not just `index.html`.
