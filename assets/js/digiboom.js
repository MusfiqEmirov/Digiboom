(function () {
  'use strict';

  /* =====================================================
     HERO BANNER SLIDER
     ===================================================== */
  var heroMedia = document.querySelector('.hero-banner-media');
  if (heroMedia) {
    var slides = Array.from(heroMedia.querySelectorAll('.hero-banner-slide'));
    var prevBtn = document.querySelector('.hero-banner-nav--prev');
    var nextBtn = document.querySelector('.hero-banner-nav--next');
    var current = 0;

    function goTo(idx) {
      slides[current].classList.remove('is-active');
      // Pause video on old slide
      var oldVid = slides[current].querySelector('video');
      if (oldVid) oldVid.pause();

      current = (idx + slides.length) % slides.length;
      slides[current].classList.add('is-active');

      // Play video on new slide
      var newVid = slides[current].querySelector('video');
      if (newVid) {
        newVid.currentTime = 0;
        newVid.play().catch(function () {});
      }

      updateBtns();
    }

    function updateBtns() {
      if (!prevBtn || !nextBtn) return;
      var isVideo = !!slides[current].querySelector('video');

      if (isVideo) {
        prevBtn.classList.add('hero-banner-nav--hidden');
        prevBtn.classList.add('hero-banner-nav--disabled');
        prevBtn.setAttribute('aria-disabled', 'true');
        prevBtn.setAttribute('aria-hidden', 'true');
        prevBtn.setAttribute('tabindex', '-1');
      } else {
        prevBtn.classList.remove('hero-banner-nav--hidden');
        prevBtn.classList.remove('hero-banner-nav--disabled');
        prevBtn.removeAttribute('aria-disabled');
        prevBtn.removeAttribute('aria-hidden');
        prevBtn.removeAttribute('tabindex');
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        if (prevBtn.classList.contains('hero-banner-nav--hidden')) return;
        goTo(current - 1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        goTo(current + 1);
      });
    }

    // Initial state
    updateBtns();
  }

  /* =====================================================
     ABOUT IMAGE CAROUSEL
     ===================================================== */
  var aboutTrack = document.querySelector('.about-image-carousel-track');
  if (aboutTrack) {
    var aboutSlides = Array.from(aboutTrack.querySelectorAll('.about-image-carousel-slide'));
    var aboutPrev = document.querySelector('.about-carousel-nav--prev');
    var aboutNext = document.querySelector('.about-carousel-nav--next');
    var aboutCurrent = 0;
    var total = aboutSlides.length;

    function aboutGoTo(idx) {
      aboutCurrent = (idx + total) % total;
      aboutTrack.style.transform = 'translateX(-' + (aboutCurrent * 100) + '%)';
    }

    if (aboutPrev) {
      aboutPrev.addEventListener('click', function () { aboutGoTo(aboutCurrent - 1); });
    }
    if (aboutNext) {
      aboutNext.addEventListener('click', function () { aboutGoTo(aboutCurrent + 1); });
    }
  }

  /* =====================================================
     SCROLL-TO-TOP WIDGET
     ===================================================== */
  var scrollTopBtn = document.getElementById('scrollToTopBtn');
  if (scrollTopBtn) {
    window.addEventListener('scroll', function () {
      var scrolled = document.documentElement.scrollTop || document.body.scrollTop;
      scrollTopBtn.classList.toggle('is-visible', scrolled > 200);
    }, { passive: true });

    scrollTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

})();
