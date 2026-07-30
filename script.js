document.documentElement.classList.add('js');

const header = document.querySelector('[data-header]');
const menuToggle = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-nav]');

// The header is transparent over the arrival image and goes solid once the
// page moves. Pages without a photographic arrival ship .is-solid in the
// markup and opt out.
const updateHeader = () => {
  if (header?.classList.contains('is-solid')) return;
  header?.classList.toggle('is-scrolled', window.scrollY > 12);
};

menuToggle?.addEventListener('click', () => {
  const isOpen = nav.classList.toggle('is-open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
});

nav?.addEventListener('click', (event) => {
  if (event.target.closest('a')) {
    nav.classList.remove('is-open');
    menuToggle?.setAttribute('aria-expanded', 'false');
  }
});

// ---------------------------------------------------------------------------
// Arrival parallax.
//
// The hero photograph drifts slower than the copy stacked over it, so the
// desert reads as depth behind the type rather than one flat plane scrolling
// as a unit. Only the image moves; the copy is ordinary in-flow content and
// needs no code of its own — it already scrolls at full speed.
//
// .parallax-media (see styles.css) overscans its box by 8% top and bottom for
// exactly this: the cap below stays inside that margin, so the translate can
// never pull a bare edge into view. Reduced-motion visitors get a static
// photograph — no transform is ever set.
// ---------------------------------------------------------------------------
const parallaxMedia = document.querySelector('[data-parallax-media]');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (parallaxMedia && !reduceMotion.matches) {
  const heroSection = parallaxMedia.closest('.chapter');
  const RATE = 0.3;
  let cap = 0;
  let ticking = false;

  const measure = () => {
    cap = heroSection.offsetHeight * 0.07;
  };

  const paintParallax = () => {
    ticking = false;
    // Past the hero, the section is clipped by scroll anyway; skip the work.
    if (window.scrollY > heroSection.offsetTop + heroSection.offsetHeight) return;
    const shift = Math.min(window.scrollY * RATE, cap);
    parallaxMedia.style.transform = `translateY(${shift}px)`;
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(paintParallax);
  };

  measure();
  paintParallax();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', measure);
}

// ---------------------------------------------------------------------------
// The rail — the page's elevator floor indicator.
//
// A hairline in the window's left gutter with a lit segment tracking scroll
// position, a tick at the top of each chapter, and a named stop at each of the
// four numbered floors: 01 STUDIO, 02 GALLERY, 03 OBSERVATION, GF GROUND FLOOR.
// It is decoration in the sense that it carries nothing you can't already see,
// which is why it is aria-hidden and why it is only built above 1100px, where
// there is gutter to spare.
//
// Both the ticks and the floor names are read off the sections themselves —
// data-floor / data-floor-name — rather than from a list kept here. Editing,
// reordering or renaming a section therefore cannot leave the panel pointing at
// a floor that no longer exists, and a room that shares a floor with another
// simply omits the attributes and gets a plain tick (StraightPic is the second
// room on the gallery floor, so Dragify's 02 covers them both).
//
// The page has two grounds and the rail is fixed, so it crosses both as you
// scroll. Rather than blend-mode tricks — which go wrong over photographs — it
// asks whether a dark band straddles a probe line. The cyan car reads on either
// ground and never changes.
// ---------------------------------------------------------------------------
const rail = document.querySelector('[data-rail]');
const railCar = rail?.querySelector('.rail-car');
const sections = [...document.querySelectorAll('[data-rail-section]')];

if (rail && railCar && sections.length) {
  const wide = window.matchMedia('(min-width: 1100px)');
  let marks = [];

  const buildTicks = () => {
    marks.forEach((mark) => mark.remove());
    marks = [];
    if (!wide.matches) return;
    const doc = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    const travel = window.innerHeight - 78;
    sections.forEach((section) => {
      // Chapters start at their own top; map that scroll offset onto the rail's
      // full-viewport height the same way the car is mapped, so a tick and the
      // car meet exactly when that chapter reaches the top of the window.
      const at = Math.min(section.offsetTop / doc, 1) * travel;
      const floor = section.dataset.floor;

      const tick = document.createElement('span');
      tick.className = floor ? 'rail-tick is-floor' : 'rail-tick';
      tick.style.top = `${at}px`;
      rail.appendChild(tick);
      marks.push(tick);

      if (!floor) return;

      // Numeral over name, as a floor plate reads. The name is a separate
      // element rather than a second line of text because the stylesheet drops
      // it on the widths where the gutter is too narrow to hold it without
      // running into the page grid — leaving the numeral, which always fits.
      const plate = document.createElement('span');
      plate.className = 'rail-floor';
      plate.style.top = `${at}px`;
      const num = document.createElement('b');
      num.textContent = floor;
      plate.appendChild(num);
      const name = section.dataset.floorName;
      if (name) {
        const label = document.createElement('span');
        label.textContent = name;
        plate.appendChild(label);
      }
      rail.appendChild(plate);
      marks.push(plate);
    });
  };

  // Which ground is the rail sitting on right now?
  //
  // Asking which SECTION is at the top of the viewport gets this wrong: the
  // Dragify exhibition is one section that opens on paper and then breaks
  // full-bleed onto midnight for its gallery, so a section-level answer leaves
  // an ink hairline drawn over a dark wall of photographs.
  //
  // So the question is asked of the dark BANDS instead of the sections: does
  // any .on-ground-dark region straddle the probe line? That covers a section
  // which changes ground partway through, needs no special case, and — unlike
  // elementFromPoint — is pure geometry, so it can't disagree with itself
  // depending on when in the frame it is called.
  //
  // The probe sits at y = 140, below the fixed header.
  const darkZones = [...document.querySelectorAll('.on-dark')];
  const PROBE_Y = 140;

  const paintGround = () => {
    const onDark = darkZones.some((zone) => {
      const box = zone.getBoundingClientRect();
      return box.top <= PROBE_Y && box.bottom > PROBE_Y;
    });
    rail.dataset.ground = onDark ? 'dark' : 'light';
  };

  const paintRail = () => {
    paintGround();
    if (!wide.matches) return;
    const doc = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    const progress = Math.min(Math.max(window.scrollY / doc, 0), 1);
    rail.style.setProperty('--rail-pos', `${progress * (window.innerHeight - 78)}px`);
  };

  const refresh = () => { buildTicks(); paintRail(); };
  refresh();
  window.addEventListener('resize', refresh);
  wide.addEventListener('change', refresh);
  // The chapters and gallery are lazy-loaded, so the document height keeps
  // changing after load; recompute once everything has settled.
  window.addEventListener('load', refresh);

  window.addEventListener('scroll', () => {
    updateHeader();
    paintRail();
  }, { passive: true });
} else {
  window.addEventListener('scroll', updateHeader, { passive: true });
}

updateHeader();

// Policies that are canonical on another domain (Dragify's live on
// dragifyapp.com) open in a dialog framing that page, so there is only ever one
// copy to keep current. The iframe src is set on open and cleared on close, so
// nothing is requested from the other origin unless the visitor asks for it.
// Without JS the links are ordinary external links and still work.
const legalDialog = document.querySelector('[data-legal-dialog]');
if (legalDialog && typeof legalDialog.showModal === 'function') {
  const frame = legalDialog.querySelector('[data-legal-dialog-frame]');
  const title = legalDialog.querySelector('[data-legal-dialog-title]');
  const openInTab = legalDialog.querySelector('[data-legal-dialog-link]');

  document.querySelectorAll('[data-legal-modal]').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const label = link.dataset.legalTitle || link.textContent.trim();
      title.textContent = label;
      frame.title = label;
      frame.src = link.href;
      openInTab.href = link.href;
      legalDialog.showModal();
    });
  });

  // Tearing the frame down is done here rather than in a 'close' listener:
  // some engines don't fire 'close' for a scripted dialog.close(), which would
  // leave the third-party page loaded and running behind a dismissed dialog.
  // Every dismissal route is therefore wired explicitly. The 'close' listener
  // stays as a backstop for any route that does fire it.
  const teardown = () => { frame.src = 'about:blank'; };
  const close = () => { teardown(); legalDialog.close(); };

  legalDialog.querySelector('[data-legal-dialog-close]')?.addEventListener('click', close);
  // Clicking the backdrop lands on the dialog element itself, not its contents.
  legalDialog.addEventListener('click', (event) => {
    if (event.target === legalDialog) close();
  });
  // Esc: 'cancel' fires before the browser closes the dialog itself.
  legalDialog.addEventListener('cancel', teardown);
  legalDialog.addEventListener('close', teardown);
}

// ---------------------------------------------------------------------------
// Reveals.
//
// Two behaviours share one observer. Copy blocks rise into place; full-frame
// chapters settle their photograph from 1.03 to 1, which is the only motion on
// the page that touches an image. Both are one-shot: once seen, unobserved.
//
// Within a section, order is expressed as a --delay in the markup — the wall
// label, then its evidence. There is no per-frame stagger inside the mosaic on
// purpose: the six looks arrive as one wall, the way a gallery lights a
// wall rather than a picture at a time.
// ---------------------------------------------------------------------------
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-visible');
    observer.unobserve(entry.target);
  });
}, { threshold: 0.08, rootMargin: '0px 0px -5% 0px' });

document.querySelectorAll('.reveal, .chapter').forEach((element) => observer.observe(element));

// ---------------------------------------------------------------------------
// The aperture — Dragify's wall of looks, and the window that climbs it.
//
// The gallery is a fixed-height window cut in the page with a wall of six
// portraits behind it. The wall is pinned to the VIEWPORT: as the page scrolls,
// the window travels up over a set of frames that do not move at all. It is not
// a parallax layer moving at a fraction of scroll speed — the fraction is zero.
//
// WHY THE ANCHOR IS THE WINDOW'S OWN BOX, NOT window.scrollY. Everything is
// derived from one `getBoundingClientRect()` each frame, so the wall re-pins
// itself to whatever the window's real position turns out to be. That is what
// makes it survive the reveal transition on the same element, a lazy image
// resolving above it, a phone's URL bar collapsing mid-scroll and an anchor
// jump — none of which a scroll offset accumulated on this side would see.
//
// THE ANCHOR ITSELF: hold the wall's top one window-height above the top of the
// viewport. That is the only constant that keeps the wall covering the window at
// both ends of the pass, because the window's box sweeps from y = 100vh down to
// y = -height, and the union of everywhere it has been is exactly that band.
//
// THE CLAMP is the honest failure mode. If a viewport is tall enough that the
// band outruns the wall — which at six frames it always does — the wall stops at
// the page for the last pixels of the pass, rather than sliding past and
// showing the midnight ground through a window that is supposed to be a wall.
//
// ALL OF THE ABOVE IS THE FALLBACK NOW. Recomputing that anchor every scroll
// event is main-thread work, and any frame the main thread is late, the wall's
// transform is still the previous frame's while the window has already moved
// on — a beat of desync that shows up as old-wall-through-new-window, i.e. the
// jitter and the fold. Where the browser supports it, styles.css drives the
// same sweep off a view() timeline instead, which the compositor evaluates
// every frame without asking this thread — no beat to miss. This code then
// only supplies --mosaic-start, computed once per load/resize/image-load, and
// never touches a scroll event.
// ---------------------------------------------------------------------------
const aperture = document.querySelector('[data-mosaic]');
const wall = document.querySelector('[data-mosaic-plane]');

if (aperture && wall && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // Where the browser can drive the sweep off a view() timeline (styles.css),
  // the compositor owns every frame and this script only ever supplies the
  // pass's starting offset — the one number CSS can't work out for itself,
  // because it depends on the wall's real rendered height. Recomputing it on
  // scroll would put the main thread straight back into the loop it was just
  // taken out of, so only the events that can actually change it touch it.
  const usesViewTimeline = CSS.supports('animation-timeline', 'view()');

  // Where the wall stands as the window starts its pass. It is the same
  // `-height - top` as the loop below, evaluated at the one moment the range
  // begins — top = one viewport down — and held to the same floor, so a
  // viewport tall enough to outrun the wall starts flush with the
  // wall's bottom edge instead of past it.
  const setStart = () => {
    const height = aperture.getBoundingClientRect().height;
    const floor = height - wall.offsetHeight;
    const start = Math.min(Math.max(-height - window.innerHeight, floor), 0);
    wall.style.setProperty('--mosaic-start', `${start}px`);
  };

  if (usesViewTimeline) {
    setStart();
    window.addEventListener('resize', setStart);
    window.addEventListener('load', setStart);
    wall.querySelectorAll('img').forEach((img) => {
      if (!img.complete) img.addEventListener('load', setStart, { once: true });
    });
  } else {
    // The fallback for browsers without view(): the same rAF-throttled
    // scroll loop as before.
    let pending = 0;

    const pinWall = () => {
      pending = 0;
      const box = aperture.getBoundingClientRect();
      // Not rounded: a fractional offset renders still, and a rounded one
      // steps by a pixel every time the page crosses a boundary — visible
      // as jitter on something whose whole point is that it is motionless.
      const shift = -box.height - box.top;
      const floor = box.height - wall.offsetHeight;
      wall.style.transform = `translate3d(0, ${Math.min(Math.max(shift, floor), 0)}px, 0)`;
    };

    const schedule = () => { pending ||= requestAnimationFrame(pinWall); };

    pinWall();
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    window.addEventListener('load', schedule);
    wall.querySelectorAll('img').forEach((img) => {
      if (!img.complete) img.addEventListener('load', schedule, { once: true });
    });
  }
}
