(function () {
  'use strict';

  var root = document.getElementById('heroBannerBomb');
  if (!root) return;

  var STEP_MS = 1300;
  var COUNTS = [3, 2, 1];
  var BURN_MS = STEP_MS * (COUNTS.length + 1);

  var numEl = root.querySelector('.hero-banner-bomb__num');
  var sparksEl = root.querySelector('.hero-banner-bomb__sparks');
  var debrisEl = root.querySelector('.hero-banner-bomb__debris');
  var wordEl = root.querySelector('.hero-banner-bomb__word');

  var SPARK_COLORS = ['#fff4c0', '#ff9040', '#ed4f24', '#ffffff', '#c084fc', '#37075b'];

  root.style.setProperty('--hero-bomb-step-ms', STEP_MS + 'ms');
  root.style.setProperty('--hero-bomb-burn-ms', BURN_MS + 'ms');
  root.classList.add('is-burning');

  function popNumber(value, boom) {
    if (!numEl) return;
    numEl.textContent = String(value);
    numEl.classList.remove('is-popping', 'is-boom-num');
    numEl.style.opacity = '';
    void numEl.offsetWidth;
    numEl.classList.add(boom ? 'is-boom-num' : 'is-popping');
  }

  function buildParticles() {
    if (sparksEl) {
      sparksEl.innerHTML = '';
      for (var i = 0; i < 28; i++) {
        var spark = document.createElement('span');
        spark.className = 'hero-banner-bomb__spark';
        spark.style.setProperty('--hero-bomb-a', (i * (360 / 28)) + 'deg');
        spark.style.setProperty('--hero-bomb-spark-dist', (7 + (i % 5) * 1.4) + 'rem');
        spark.style.setProperty('--hero-bomb-spark-size', (5 + (i % 4) * 2) + 'px');
        spark.style.setProperty('--hero-bomb-spark-color', SPARK_COLORS[i % SPARK_COLORS.length]);
        spark.style.animationDelay = (i % 6) * 0.02 + 's';
        sparksEl.appendChild(spark);
      }
    }

    if (debrisEl) {
      debrisEl.innerHTML = '';
      for (var j = 0; j < 14; j++) {
        var bit = document.createElement('span');
        bit.className = 'hero-banner-bomb__bit';
        bit.style.setProperty('--hero-bomb-a', (j * (360 / 14) + 12) + 'deg');
        bit.style.setProperty('--hero-bomb-spark-dist', (5.5 + (j % 4) * 1.1) + 'rem');
        bit.style.setProperty('--hero-bomb-bit-w', (6 + (j % 3) * 3) + 'px');
        bit.style.setProperty('--hero-bomb-bit-h', (3 + (j % 2) * 2) + 'px');
        bit.style.animationDelay = (j % 5) * 0.015 + 's';
        debrisEl.appendChild(bit);
      }
    }
  }

  function runExplosion(done) {
    root.classList.remove('is-burning');
    popNumber(1, true);

    setTimeout(function () {
      root.classList.add('is-exploding');

      if (numEl) {
        numEl.classList.remove('is-popping', 'is-boom-num');
        numEl.style.opacity = '0';
      }

      buildParticles();
      if (sparksEl) sparksEl.classList.add('is-exploding');
      if (debrisEl) debrisEl.classList.add('is-exploding');
      if (wordEl) wordEl.classList.add('is-show');

      setTimeout(done, 1180);
    }, 280);
  }

  function finish() {
    root.classList.add('is-finished');
    root.setAttribute('aria-hidden', 'true');
  }

  function runCountdown(step) {
    popNumber(COUNTS[step], false);

    if (step < COUNTS.length - 1) {
      setTimeout(function () {
        runCountdown(step + 1);
      }, STEP_MS);
      return;
    }

    setTimeout(function () {
      runExplosion(function () {
        setTimeout(finish, 320);
      });
    }, STEP_MS);
  }

  requestAnimationFrame(function () {
    setTimeout(function () {
      runCountdown(0);
    }, 450);
  });
})();
