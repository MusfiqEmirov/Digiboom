(function () {
  'use strict';

  var splashEl = document.getElementById('siteSplash');
  if (!splashEl) return;

  var html = document.documentElement;
  var hidden = false;
  var pageLoaded = false;
  var includesReady = !document.querySelector('[data-include]');

  html.classList.add('is-splash-loading');
  document.body.classList.add('site-splash-active');

  function unlockPage() {
    html.classList.remove('is-splash-loading');
    html.classList.add('splash-done');
    document.body.classList.remove('site-splash-active');
  }

  function hideSplash() {
    if (hidden) return;
    hidden = true;

    unlockPage();
    splashEl.setAttribute('aria-hidden', 'true');

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        splashEl.remove();
      });
    });
  }

  function tryHideSplash() {
    if (!pageLoaded || !includesReady || hidden) return;
    hideSplash();
  }

  document.addEventListener('digiboom:includes-ready', function () {
    includesReady = true;
    tryHideSplash();
  }, { once: true });

  if (document.readyState === 'complete') {
    pageLoaded = true;
    tryHideSplash();
  } else {
    window.addEventListener('load', function () {
      pageLoaded = true;
      tryHideSplash();
    }, { once: true });
  }

  setTimeout(function () {
    if (!includesReady) {
      includesReady = true;
      tryHideSplash();
    }
  }, 4000);
})();
