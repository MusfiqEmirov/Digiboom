(function () {
  'use strict';

  var root = document.getElementById('heroBannerBomb');
  if (!root) return;

  var STEP_MS = 1400;
  var COUNTS = [3, 2, 1];
  var BURN_MS = STEP_MS * (COUNTS.length + 1);

  var numEl = root.querySelector('.hero-banner-bomb__num');
  var burstEl = root.querySelector('.hero-banner-bomb__burst');
  var sparksEl = root.querySelector('.hero-banner-bomb__sparks');

  root.style.setProperty('--hero-bomb-step-ms', STEP_MS + 'ms');
  root.style.setProperty('--hero-bomb-burn-ms', BURN_MS + 'ms');

  root.classList.add('is-burning');

  function popNumber(value) {
    if (!numEl) return;
    numEl.textContent = String(value);
    numEl.classList.remove('is-popping');
    void numEl.offsetWidth;
    numEl.classList.add('is-popping');
  }

  function buildSparks() {
    if (!sparksEl) return;
    sparksEl.innerHTML = '';
    for (var i = 0; i < 9; i++) {
      var spark = document.createElement('span');
      spark.className = 'hero-banner-bomb__spark';
      sparksEl.appendChild(spark);
    }
  }

  function runExplosion(done) {
    root.classList.remove('is-burning');
    root.classList.add('is-exploding');

    if (numEl) {
      numEl.classList.remove('is-popping');
      numEl.style.opacity = '0';
    }

    buildSparks();
    if (burstEl) burstEl.classList.add('is-exploding');
    if (sparksEl) sparksEl.classList.add('is-exploding');

    setTimeout(done, 780);
  }

  function finish() {
    root.classList.add('is-finished');
    root.setAttribute('aria-hidden', 'true');
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
        setTimeout(finish, 260);
      });
    }, STEP_MS);
  }

  requestAnimationFrame(function () {
    setTimeout(function () {
      runCountdown(0);
    }, 500);
  });
})();
