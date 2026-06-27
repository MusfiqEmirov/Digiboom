(function () {
  'use strict';

  var SPLASH_KEY = 'digiboom_session_started';
  var STEP_MS = 900;
  var COUNTS = [3, 2, 1];

  var splashEl = document.getElementById('siteSplash');
  if (!splashEl) return;

  var html = document.documentElement;

  function unlockPage() {
    html.classList.remove('is-splash-loading');
    html.classList.add('splash-done');
    document.body.classList.remove('site-splash-active');
  }

  function markSessionDone() {
    try {
      sessionStorage.setItem(SPLASH_KEY, '1');
    } catch (e) {}
  }

  function skipSplash() {
    splashEl.classList.add('is-hidden');
    splashEl.setAttribute('aria-hidden', 'true');
    splashEl.remove();
    unlockPage();
  }

  if (sessionStorage.getItem(SPLASH_KEY)) {
    skipSplash();
    return;
  }

  html.classList.add('is-splash-loading');
  document.body.classList.add('site-splash-active');

  var countdownEl = splashEl.querySelector('.bomb-countdown');
  var numEl = splashEl.querySelector('.bomb-num');
  var explosionEl = splashEl.querySelector('.bomb-explosion');
  var particlesEl = splashEl.querySelector('.bomb-particles');

  function popNumber(value) {
    if (!numEl) return;
    numEl.textContent = String(value);
    numEl.classList.remove('is-popping');
    void numEl.offsetWidth;
    numEl.classList.add('is-popping');
  }

  function buildParticles() {
    if (!particlesEl) return;
    particlesEl.innerHTML = '';
    for (var i = 0; i < 12; i++) {
      var dot = document.createElement('span');
      dot.className = 'bomb-dot';
      particlesEl.appendChild(dot);
    }
  }

  function runExplosion(done) {
    if (countdownEl) countdownEl.classList.remove('is-active');
    if (numEl) numEl.style.visibility = 'hidden';

    buildParticles();
    if (explosionEl) explosionEl.classList.add('is-exploding');
    if (particlesEl) particlesEl.classList.add('is-exploding');

    setTimeout(done, 780);
  }

  function hideSplash() {
    splashEl.classList.add('is-hidden');
    splashEl.setAttribute('aria-hidden', 'true');

    var removed = false;
    function removeSplash() {
      if (removed) return;
      removed = true;
      splashEl.remove();
      markSessionDone();
      unlockPage();
    }

    splashEl.addEventListener('transitionend', removeSplash, { once: true });
    setTimeout(removeSplash, 500);
  }

  function runCountdown(step) {
    popNumber(COUNTS[step]);

    if (step < COUNTS.length - 1) {
      setTimeout(function () {
        runCountdown(step + 1);
      }, STEP_MS);
      return;
    }

    setTimeout(function () {
      runExplosion(function () {
        setTimeout(hideSplash, 180);
      });
    }, STEP_MS);
  }

  requestAnimationFrame(function () {
    setTimeout(function () {
      runCountdown(0);
    }, 200);
  });
})();
