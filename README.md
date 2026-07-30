# ElevatorBeat — elevatorbeat.com

Marketing site for ElevatorBeat, a Portland art collective working in apps. Currently
Dragify and StraightPic.

Positioning: *"A Portland art collective working in apps."* The page is structured as a
building the collective works in: numbered floors, wall labels, two occupied rooms and a
directory on the ground floor. Dependency-free, hand-authored HTML/CSS/JS — no build step.

## Run locally

```bash
python3 -m http.server 8642
```

Then open `http://localhost:8642`. `index.html` also opens directly in a browser with no
server, though relative links between pages work best served over HTTP.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Home page — the seven-beat shot list (see below) |
| `support.html` | App support (Dragify + StraightPic), links to contact |
| `privacy.html` | Privacy policy for the site and both apps |
| `terms.html` | Terms of use |
| `open-source.html` | Open source license notices for Dragify and StraightPic |
| `thanks.html` | Contact-form confirmation page — `noindex`, not in the sitemap |
| `styles.css` | All styling — dual-ground tokens in `:root` / `.on-dark`, the `.plate` image component, one button system |
| `script.js` | Transparent-until-scroll header, mobile nav, canonical-policy dialog, the floor indicator, scroll reveals |
| `assets/` | Favicon (SVG), apple touch icon, OG/social share image |
| `assets/img/` | All site photography, WebP, multiple widths per image for `srcset` |
| `assets/video/` | Superseded hero animation — **no longer referenced**, kept on disk only |
| `tools/exhibit-art.py` | Cuts every architectural frame + art-directed mobile crops from the upscaled masters — dev only |
| `tools/dragify-looks.py` | Exports the curated Dragify exhibition from the app's pack data — dev only |
| `tools/straightpic-demo.py` | Builds the StraightPic before/after from `Tower.jpg` — dev only, **no longer used by any page** (see StraightPic below) |
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

Cyan is an annotation, not a brand wash: hairlines, ticks, tag glyphs, the plan drawing, the
floor indicator, focus rings. Copper comes off the elevator's amber lighting and appears only
as numerals — the floor plates in the gutter and the elevator core in the plan.

**Buttons are one system at three weights**, all tracked uppercase at one size, so an action
reads as building signage rather than as a web control:

| Weight | Where | Why |
| --- | --- | --- |
| Solid | The arrival, once | The inverse of its ground (ink on paper, ivory on midnight) — deliberately *not* cyan, because a large cyan rectangle over a photograph is the generic CTA reflex this system exists to avoid |
| Outline | Every room, the directory, the footer | A hairline box: the same annotation vocabulary as the rail and the plan |
| Quiet | Secondary text actions | A rule that brightens on hover |

An app that hasn't shipped keeps the **outline** — both rooms must be labelled on identical
terms — but goes soft and drops the hover brightening, because a phone has no hover and a
control that looks live for something undownloadable is the failure to avoid.

Four display tiers (`.display-xl` / `-l` / `-m` / `-s`) are chosen by the job a headline is
doing, not by its heading level. The previous build ran every section at one `h2` size, which
is most of why it read as a template.

## The page — a shot list

Seven beats. The page is a building: four **numbered floors** that the floor indicator names,
plus two unnumbered interludes between them. Sequence follows narrative continuity and
contrast — there is no rule forcing paper and midnight to alternate.

| Floor | Beat | Ground | Asset |
| --- | --- | --- | --- |
| — | Arrival — the front elevation, the whole window | dark | `hero-*` / `hero-mobile-*` |
| **01** | The studio — one passage, flanked by a photograph and a survey annotation | paper | `salon-*` |
| **02** | Room 01, Dragify — wall label and a wall of looks behind a moving aperture | dark | `assets/img/dragify/*` |
| — | Morning — the one daylight frame, and the one chapter with **ink type over a lifted scrim** | **paper over image** | `house-day-*` |
| **02** | Room 02, StraightPic — wall label and two real captures from the app | paper | `ui-straightpic-editor-*`, `ui-straightpic-result-*` |
| **03** | The observation level — the empty floors, said plainly | dark | `band-mars-*` |
| **GF** | Ground floor — the directory, then the footer bar | paper | — |

Both rooms sit on floor **02**: they are two rooms on one gallery floor, so StraightPic omits
`data-floor` and takes a plain tick. That is the mechanism, not a special case — see the floor
indicator below.

The morning beat is the one chapter that does **not** carry `.on-dark`. Darkening a pale
morning sky enough to hold ivory type would turn the morning into another dusk — the "every
image becomes the same dark scene" failure. Its type is near-black and its scrim *lifts* the
sky instead (`.scrim-lift`). Same component, inverted ground. Its stops are the weakest lift
that still clears WCAG AA against the actual pixels of `house-day`, measured at each element's
own measure rather than across the whole band: **eyebrow 4.86:1, body 5.34:1, headline
13.8:1**. Lifting harder passes by more and costs the sky. Re-measure before changing them.

Held back deliberately, for interior pages and OG artwork: `lounge-*` (the full frame — the
homepage now uses the figure-free `salon-*` crop of it), `terrace-*`, `ascent-*`,
`house-dusk-*`, `cta-*`, `nextup-*`.

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
| `lounge-*` | `_upscaled/lounge.png` — studio interior (full frame; unused on the homepage) |
| `salon-*` | the same master, right-hand 3258px — the only crop of that painting with **no figures in it**, for the studio passage's arch-topped plate |
| `band-mars-*`, `band-mars-mobile-*` | `_upscaled/band-mars.png` — the grounds; 16:9 crop for phones |
| `house-day-*` | the daylight frame |
| `about-*` | the observation level |
| `cta-*` | the closing scene |
| `assets/img/dragify/*` | Dragify's own pack data — see below |
| `straightpic-before/after-*` | `Apps/StraightPic/Reference Photos/Tower.jpg` — **unused**, kept on disk |
| `ui-straightpic-editor-*`, `ui-straightpic-result-*` | two real captures from one session in the app |
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

Eighteen looks ship, chosen for visual quality, spread across all five collections, and
sequenced so colour, silhouette and setting change frame to frame — down the columns and across
the rows both. The homepage labels nothing by name — the collection and queen names stay in the
app. `EDIT` in the script is appended to, never reordered: the index comes from list order, so
adding a look cannot rename the fifteen already deployed.

**The wall does not scroll.** `.mosaic` is a fixed-height window cut in the page; the
`.mosaic-plane` behind it is pinned to the *viewport* by `script.js`. As the page rises the
window climbs the wall and not one queen travels a pixel — the opposite of a parallax layer,
which moves slower than the page rather than not at all. Frames are cut hard by the window's
edge on purpose: an opening in a wall, not a carousel.

Three rules keep it honest:

1. **The anchor is the window's own box, never `scrollY`.** Everything comes from one
   `getBoundingClientRect()` per frame, so the wall re-pins to wherever the window actually is.
   That survives a lazy image resolving above it, a phone's URL bar collapsing mid-scroll and an
   anchor jump — none of which an offset accumulated on the JS side would see. Hold the wall's
   top one window-height above the top of the viewport and it is motionless for the whole pass;
   measured, the error is **0.00px** at every stop.
2. **The wall has to outrun the window's travel.** Between entering at the bottom of the
   viewport and leaving at the top, the window sweeps a band of `100vh + 2 × its own height`.
   Six frames a column clears that at every viewport the page is read on. Past that the script
   clamps rather than let a gap open, and the wall creeps for the last pixels of the pass.
3. **The aperture is the one reveal that fades without rising.** A transition fires no scroll
   events, so a window that slid 12px into place would carry the wall with it and only find its
   anchor again on the visitor's next scroll.

**One ratio now.** The old mosaic mixed 3:2 and 5:4 into the 2:3 so three columns of different
widths would finish level. Behind an aperture nothing has to finish level, so every frame is
back at the single ratio the app exports: no look is cropped at all, and `--focus` is gone.

On a phone the column wrappers step out of the way with `display: contents` and all eighteen
flow two-up — three columns at a phone's measure is a 110px-wide thumbnail of a queen, not a
look.

Where the window cannot travel — **no JS, or `prefers-reduced-motion`** — the same markup is an
ordinary static wall, cut to its first twelve frames so the section stays the length of a
section.

> **Deprecated: `assets/img/deprecated/`, `tools/deprecated/dragify-sheet.py`.**
> `dragify-looks-*.webp` is a fourteen-up contact sheet in which **every tile already has a
> rounded corner baked onto a white ground**. The old `dragify-sheet.py` cut tiles at their
> bounding box, so that white shipped inside the files, and inside a second differently-radiused
> CSS frame it showed as white triangles in the corner of every thumbnail. It was never a CSS
> bug — the white was in the image data. Nothing references those files; do not reintroduce them.

### StraightPic — the demonstration

**Two real captures from one session in the app**, not a built demonstration: the editor with
the four perspective handles placed on the brick face, and the corrected frame that came back.
`tools/ui-shots.py` cuts both from `Apps/StraightPic/Reference Photos/`.

They sit side by side, the second dropped half a step, so the pair reads as a sequence rather
than as a comparison table — and because two phone screens whose bezels line up exactly look
like an App Store submission. On a phone they stay side by side: the two shapes read at a
glance, and the captions carry what the shrunken tool labels no longer can.

> **Superseded: the drag-to-compare slider.** Earlier builds rebuilt the correction from the
> raw 4284x5712 `Tower.jpg` (`tools/straightpic-demo.py`) and handed the visitor a divider to
> drag, with the four corner handles as an SVG overlay. Real screenshots of the shipping app
> are better evidence than a keystone the site computed for itself, so the slider, its CSS
> (`.compare`, `.guides`, `.frame-label`) and its JS are all gone. `straightpic-before/after-*`
> and the generator are still on disk; nothing references them.

## The floor indicator

A fixed hairline in the left gutter with a lit cyan segment tracking scroll position, a tick at
the top of every chapter, and — where there is room — the four numbered floors named:
**01 STUDIO, 02 GALLERY, 03 OBSERVATION, GF GROUND FLOOR**. Luke has asked for this through
every iteration of the site; it is the one thing that survives every rebuild.

Both the ticks and the names are read off the sections themselves — `data-floor` and
`data-floor-name` — rather than from a list kept in `script.js`. Editing, reordering or
renaming a section therefore cannot leave the panel pointing at a floor that no longer exists,
and **a room that shares a floor with another simply omits the attributes and gets a plain
tick**. That is how both apps sit on floor 02.

The stops are in **page order, top to bottom, not building order**. A real panel would put the
top floor at the top, but this one has a car on it that tracks scroll, and a car that runs
backwards up a panel while the reader scrolls down is an indicator that lies.

It carries nothing you cannot already see, which is why it is `aria-hidden`. Three widths:

| Viewport | What shows | Why |
| --- | --- | --- |
| < 1100px | nothing | no gutter to spare |
| 1100–1399px | hairline + ticks | a numeral would be drawn under the first words of every line |
| 1400–1575px | + numerals and names | the container **stops centring** and takes a fixed 168px left inset to give the panel a column of its own (`.container` override in the responsive section). Full-bleed photography is untouched — the panel overlays it, which is the point of a fixed indicator |
| ≥ 1576px | + numerals and names | a centred 1240px container clears the panel on its own; nothing is shifted |

Because it is `position: fixed` it crosses both grounds. `script.js` therefore asks whether any
`.on-dark` band straddles a probe line 140px down the viewport, and colours the hairline to
match. Asking which *section* is at the top gets this wrong — a section can open on one ground
and change partway through. Pure geometry rather than `elementFromPoint`, so it cannot disagree
with itself depending on when in the frame it runs.

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

CSS/JS are loaded with a version query string (`styles.css?v=20260729h`). Bump it on any
meaningful change so browsers don't serve a stale cached copy — and bump it in all seven
HTML files together, not just `index.html`.
