(function () {
  'use strict';

  /* Language change is server-side (POST set_language + reload).
     This script only keeps desktop dropdown hover / width UX. */

  function syncDropdownWidths() {
    document.querySelectorAll('.lang-switcher').forEach(function (switcher) {
      var toggle = switcher.querySelector('.lang-switcher__toggle');
      if (!toggle) return;
      var width = toggle.getBoundingClientRect().width;
      switcher.style.setProperty('--lang-switcher-width', width + 'px');
    });
  }

  function bindDesktopLangHover() {
    if (!window.bootstrap || !window.bootstrap.Dropdown) return;

    document.querySelectorAll('.lang-switcher-host--desktop .lang-switcher').forEach(function (switcher) {
      if (switcher.dataset.hoverBound === '1') return;

      var toggle = switcher.querySelector('.lang-switcher__toggle');
      if (!toggle) return;

      switcher.dataset.hoverBound = '1';
      var instance = window.bootstrap.Dropdown.getOrCreateInstance(toggle);
      var closeTimer = null;

      switcher.addEventListener('mouseenter', function () {
        if (closeTimer) {
          clearTimeout(closeTimer);
          closeTimer = null;
        }
        instance.show();
      });

      switcher.addEventListener('mouseleave', function () {
        closeTimer = setTimeout(function () {
          instance.hide();
        }, 120);
      });
    });
  }

  function init() {
    document.documentElement.lang =
      document.documentElement.getAttribute('lang') || 'az';
    bindDesktopLangHover();
    syncDropdownWidths();
    window.addEventListener('resize', syncDropdownWidths);
  }

  document.addEventListener('show.bs.dropdown', function (e) {
    if (e.target.closest('.lang-switcher')) syncDropdownWidths();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('digiboom:includes-ready', init);
})();
