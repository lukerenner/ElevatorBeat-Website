document.documentElement.classList.add('js');

// Before/after comparison sliders. The range input is the only control; this
// just mirrors its value onto --split, which drives both the clip on the
// "before" image and the handle position. Pointer dragging and keyboard arrows
// therefore both work with no extra event handling.
document.querySelectorAll('[data-compare]').forEach((compare) => {
  const range = compare.querySelector('.compare-range');
  if (!range) return;
  const paint = () => compare.style.setProperty('--split', `${range.value}%`);
  range.addEventListener('input', paint);
  paint();
});

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
// The rail — the page's elevator position indicator.
//
// A hairline in the window's left gutter with a lit segment tracking scroll
// position and a tick at the top of each chapter. It is decoration in the sense
// that it carries nothing you can't already see, which is why it is aria-hidden
// and why it is only built above 1100px, where there is gutter to spare. The
// tick positions come from the chapters themselves rather than hard-coded
// offsets, so editing the page can't leave them pointing at nothing.
//
// The page has two grounds and the rail is fixed, so it crosses both as you
// scroll. Rather than blend-mode tricks — which go wrong over photographs — it
// asks which chapter currently occupies the top of the viewport and takes that
// chapter's ground. The cyan car reads on either and never changes.
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

      const tick = document.createElement('span');
      tick.className = 'rail-tick';
      tick.style.top = `${at}px`;
      rail.appendChild(tick);
      marks.push(tick);

      const label = section.dataset.railNum;
      if (label) {
        const num = document.createElement('span');
        num.className = 'rail-num';
        num.textContent = label;
        num.style.top = `${at}px`;
        rail.appendChild(num);
        marks.push(num);
      }
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
// the page that touches an image.
//
// Gallery frames are staggered by their position in their own row rather than
// by their index in the list, so a wide row doesn't run a long cascade while a
// narrow one finishes instantly. Both are one-shot: once seen, unobserved.
// ---------------------------------------------------------------------------
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-visible');
    observer.unobserve(entry.target);
  });
}, { threshold: 0.08, rootMargin: '0px 0px -5% 0px' });

document.querySelectorAll('.reveal, .chapter').forEach((element) => observer.observe(element));

// Stagger within each gallery row. Reading offsetTop rather than nth-child is
// what keeps the cascade correct after the grid reflows at a breakpoint — the
// rows are different at every width, and a hard-coded delay would be wrong at
// two of the three.
const stagger = () => {
  document.querySelectorAll('.gallery-grid').forEach((grid) => {
    let rowTop = null;
    let position = 0;
    [...grid.children].forEach((item) => {
      if (getComputedStyle(item).display === 'none') return;
      const top = item.offsetTop;
      if (rowTop === null || Math.abs(top - rowTop) > 80) {
        rowTop = top;
        position = 0;
      }
      item.style.setProperty('--delay', `${position * 90}ms`);
      position += 1;
    });
  });
};
stagger();
window.addEventListener('load', stagger);
