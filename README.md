# Elevator Beat — elevatorbeat.com

Marketing site for Elevator Beat, an independent creative app studio in Portland, Oregon
(apps: Dragify, StraightPic). Dependency-free, hand-authored HTML/CSS/JS — no build step.

## Run locally

```bash
python3 -m http.server 8642
```

Then open `http://localhost:8642`. `index.html` also opens directly in a browser with no
server, though relative links between pages work best served over HTTP.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Home page — hero, apps, studio story, support, closing CTA, footer |
| `support.html` | App support (Dragify + StraightPic), links to contact |
| `privacy.html` | Privacy policy for the site and both apps |
| `terms.html` | Terms of use |
| `styles.css` | All styling — design tokens in `:root`, mobile-first responsive rules |
| `script.js` | Sticky header state, mobile nav toggle, scroll-reveal animations |
| `assets/` | Favicon (SVG), apple touch icon, OG/social share image |
| `robots.txt` | Allows crawling, points at sitemap |
| `sitemap.xml` | Lists all four indexable pages |
| `CNAME` | Custom domain for GitHub Pages (`elevatorbeat.com`) |

## Placeholder visuals

Every navy/orange/blue rounded block on the site (`[role="img"]` elements) is a **CSS
gradient placeholder** standing in for a future photo or app screenshot, per Luke's note
that solid color areas will be replaced with real images later. To swap one in:

1. Replace the `role="img"` div with an `<img>` (or add a `background-image` to the
   existing div) using a descriptive `alt` (or update `aria-label` if you keep the div).
2. Below-the-fold images should get `loading="lazy" decoding="async"` plus explicit
   `width`/`height`.
3. If a swapped-in image becomes the largest above-the-fold visual (the hero art), give it
   `fetchpriority="high"` and preload it — see the lukerenner.co 2.0 build for the pattern.

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

There is no contact form — `mailto:hello@elevatorbeat.com` is used directly for "Contact
Elevator Beat" and the support/policy pages. Update that address once a real inbox exists.

## Legal pages

`privacy.html` and `terms.html` are drafted from the app descriptions on this site and are
a reasonable starting point, not a substitute for review by counsel — especially before
Dragify/StraightPic process real user photos at scale or collect payment data directly.

## Cache-busting

CSS/JS are loaded with a version query string (`styles.css?v=20260728`). Bump the date on
any meaningful change so browsers don't serve a stale cached copy.
