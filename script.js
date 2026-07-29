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

// The header is transparent over the hero and goes solid once the page moves.
// Pages without a photographic hero ship .is-solid in the markup and opt out.
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
// The rail — the page's elevator position indicator.
//
// A hairline in the window's left gutter with a lit segment tracking scroll
// position and a tick at the top of each section. It is decoration in the sense
// that it carries nothing you can't already see, which is why it is aria-hidden
// and why it is only built above 1100px, where there is gutter to spare. The
// tick positions come from the sections themselves rather than hard-coded
// offsets, so editing the page can't leave them pointing at nothing.
// ---------------------------------------------------------------------------
const rail = document.querySelector('[data-rail]');
const railCar = rail?.querySelector('.rail-car');

if (rail && railCar) {
  const sections = [...document.querySelectorAll('[data-rail-section]')];
  const wide = window.matchMedia('(min-width: 1100px)');
  let ticks = [];

  const buildTicks = () => {
    ticks.forEach((tick) => tick.remove());
    ticks = [];
    if (!wide.matches) return;
    const doc = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    sections.forEach((section) => {
      // Sections start at their own top; map that scroll offset onto the rail's
      // full-viewport height the same way the car is mapped, so a tick and the
      // car meet exactly when that section reaches the top of the window.
      const at = Math.min(section.offsetTop / doc, 1);
      const tick = document.createElement('span');
      tick.className = 'rail-tick';
      tick.style.top = `${at * (window.innerHeight - 78)}px`;
      rail.appendChild(tick);
      ticks.push(tick);
    });
  };

  const paintRail = () => {
    if (!wide.matches) return;
    const doc = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    const progress = Math.min(Math.max(window.scrollY / doc, 0), 1);
    rail.style.setProperty('--rail-pos', `${progress * (window.innerHeight - 78)}px`);
  };

  const refresh = () => { buildTicks(); paintRail(); };
  refresh();
  window.addEventListener('resize', refresh);
  wide.addEventListener('change', refresh);
  // The scenes and product shots are lazy-loaded, so the document height keeps
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

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -5% 0px' });

document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
