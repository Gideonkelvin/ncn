// Activates the correct Jazzmin "horizontal_tabs" tab from the URL hash.
// This prevents needing a manual refresh when opening /change/#<tab-id>.
(function () {
  'use strict';

  function showTabByHash() {
    const hash = window.location.hash;
    if (!hash) return;

    const tabsUl = document.querySelector('#content-main form #jazzy-tabs');
    if (!tabsUl) return;

    // Prefer the first tab containing the first error (matches Jazzmin's intention).
    const firstError = document.querySelector('.change-form .errorlist li');
    let targetHref = null;
    if (firstError) {
      const pane = firstError.closest('.tab-pane');
      const paneId = pane && pane.id;
      if (paneId) targetHref = '#' + paneId;
    }

    const hrefToUse = targetHref || hash;
    const link =
      tabsUl.querySelector('a.nav-link[href="' + hrefToUse + '"]') ||
      tabsUl.querySelector('a[href="' + hrefToUse + '"]');
    if (!link) return;

    // Bootstrap 5 Tab API
    if (window.bootstrap && window.bootstrap.Tab && window.bootstrap.Tab.getOrCreateInstance) {
      window.bootstrap.Tab.getOrCreateInstance(link).show();
      return;
    }

    // Fallback: do a minimal class toggle (best-effort)
    const tabPanes = document.querySelectorAll('#content-main form .tab-content .tab-pane');
    tabsUl.querySelectorAll('a.nav-link').forEach((a) => a.classList.remove('active'));
    link.classList.add('active');
    tabPanes.forEach((pane) => {
      const isActive = '#' + pane.id === hrefToUse;
      if (isActive) {
        pane.classList.add('active', 'show');
      } else {
        pane.classList.remove('active', 'show');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Run immediately and again shortly after to handle any late tab rendering.
    showTabByHash();
    setTimeout(showTabByHash, 0);
    setTimeout(showTabByHash, 50);
  });
})();

