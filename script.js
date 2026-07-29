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
// Pages without a dark hero ship .is-solid in the markup and opt out entirely.
const updateHeader = () => {
  if (header?.classList.contains('is-solid')) return;
  header?.classList.toggle('is-scrolled', window.scrollY > 12);
};
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

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
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });

document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
