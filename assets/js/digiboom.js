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
    var heroTransitionMs = 850;
    var heroTransitioning = false;

    function goTo(idx) {
      if (heroTransitioning) return;
      var next = (idx + slides.length) % slides.length;
      if (next === current) return;

      heroTransitioning = true;
      var oldSlide = slides[current];
      var oldVid = oldSlide.querySelector('video');

      oldSlide.classList.remove('is-active');
      current = next;
      slides[current].classList.add('is-active');

      var newVid = slides[current].querySelector('video');
      if (newVid) {
        newVid.play().catch(function () {});
      }

      updateBtns();

      setTimeout(function () {
        if (oldVid) oldVid.pause();
        heroTransitioning = false;
      }, heroTransitionMs);
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
    var aboutWrap = aboutTrack.closest('.about-image-carousel-wrap');
    var aboutSlides = Array.from(aboutTrack.querySelectorAll('.about-image-carousel-slide'));
    var aboutPrev = document.querySelector('.about-carousel-nav--prev');
    var aboutNext = document.querySelector('.about-carousel-nav--next');
    var aboutCurrent = 0;
    var total = aboutSlides.length;
    var aboutAutoplayTimer = null;
    var aboutAutoplayDelay = 3800;

    function aboutGoTo(idx) {
      if (total <= 1) return;
      var next = (idx + total) % total;
      if (next === aboutCurrent) return;

      aboutSlides[aboutCurrent].classList.remove('is-active');
      aboutCurrent = next;
      aboutSlides[aboutCurrent].classList.add('is-active');
    }

    function aboutGoNext() {
      aboutGoTo(aboutCurrent + 1);
    }

    function startAboutAutoplay() {
      if (total <= 1) return;
      stopAboutAutoplay();
      aboutAutoplayTimer = setInterval(aboutGoNext, aboutAutoplayDelay);
    }

    function stopAboutAutoplay() {
      if (aboutAutoplayTimer) {
        clearInterval(aboutAutoplayTimer);
        aboutAutoplayTimer = null;
      }
    }

    function restartAboutAutoplay() {
      stopAboutAutoplay();
      startAboutAutoplay();
    }

    if (aboutPrev) {
      aboutPrev.addEventListener('click', function () {
        aboutGoTo(aboutCurrent - 1);
        restartAboutAutoplay();
      });
    }
    if (aboutNext) {
      aboutNext.addEventListener('click', function () {
        aboutGoTo(aboutCurrent + 1);
        restartAboutAutoplay();
      });
    }

    if (aboutWrap) {
      aboutWrap.addEventListener('mouseenter', stopAboutAutoplay);
      aboutWrap.addEventListener('mouseleave', startAboutAutoplay);
    }

    startAboutAutoplay();
  }

  /* =====================================================
     CARD IMAGE LINKS — yalnız Ətraflı düyməsi keçid edir
     ===================================================== */

  /* =====================================================
     ABOUT PROMO VIDEO — custom play overlay
     ===================================================== */
  document.querySelectorAll('.about-promo-video__player[data-video-type="html5"]').forEach(function (player) {
    var video = player.querySelector('.about-promo-video__el');
    var playBtn = player.querySelector('.about-promo-video__play');
    if (!video || !playBtn) return;

    function showOverlay() {
      player.classList.remove('is-playing');
      video.removeAttribute('controls');
    }

    function hideOverlay() {
      player.classList.add('is-playing');
      video.setAttribute('controls', '');
    }

    playBtn.addEventListener('click', function () {
      hideOverlay();
      video.play().catch(function () {
        showOverlay();
      });
    });

    video.addEventListener('ended', function () {
      video.currentTime = 0;
      showOverlay();
    });
  });

  /* =====================================================
     SCROLL-TO-TOP WIDGET
     ===================================================== */
  var scrollTopBtn = document.getElementById('scrollToTopBtn');
  if (scrollTopBtn) {
    var showAfter = 220;
    var hideBefore = 60;
    var scrollingToTop = false;

    function updateScrollTopBtn() {
      var scrolled = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
      var isVisible = scrollTopBtn.classList.contains('is-visible');

      if (scrolled <= 0) {
        scrollingToTop = false;
      }

      if (scrollingToTop) {
        if (isVisible) scrollTopBtn.classList.remove('is-visible');
        return;
      }

      if (!isVisible && scrolled > showAfter) {
        scrollTopBtn.classList.add('is-visible');
      } else if (isVisible && scrolled < hideBefore) {
        scrollTopBtn.classList.remove('is-visible');
      }
    }

    window.addEventListener('scroll', updateScrollTopBtn, { passive: true });
    updateScrollTopBtn();

    scrollTopBtn.addEventListener('click', function () {
      scrollingToTop = true;
      scrollTopBtn.classList.remove('is-visible');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* =====================================================
     ƏLAQƏ FORMU — SMTP API göndərişi
     ===================================================== */
  function showFormStatus(form, message, type) {
    var statusEl = form.querySelector('[data-form-status]');
    if (!statusEl) return;

    statusEl.textContent = message;
    statusEl.hidden = !message;
    statusEl.classList.remove('contact-form-modern__status--success', 'contact-form-modern__status--error');
    if (type) statusEl.classList.add('contact-form-modern__status--' + type);
  }

  function bindSmtpContactForms() {
    document.querySelectorAll('form[data-smtp-form]').forEach(function (form) {
      if (form.dataset.smtpBound === 'true') return;
      form.dataset.smtpBound = 'true';

      form.addEventListener('submit', function (event) {
        event.preventDefault();

        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }

        var submitBtn = form.querySelector('[type="submit"]');
        var endpoint = form.getAttribute('action') || '/api/contact';
        var formData = new FormData(form);

        if (submitBtn) submitBtn.classList.add('is-loading');
        showFormStatus(form, '', '');

        fetch(endpoint, {
          method: 'POST',
          body: formData,
          headers: { Accept: 'application/json' }
        })
          .then(function (res) {
            if (!res.ok) {
              return res.json().catch(function () {
                return { message: 'Mesaj göndərilmədi. Zəhmət olmasa bir az sonra yenidən cəhd edin.' };
              }).then(function (data) {
                throw new Error(data.message || 'Mesaj göndərilmədi.');
              });
            }
            return res.json().catch(function () {
              return { ok: true };
            });
          })
          .then(function () {
            showFormStatus(form, 'Mesajınız uğurla göndərildi. Tezliklə sizinlə əlaqə saxlayacağıq.', 'success');
            form.reset();
          })
          .catch(function (err) {
            showFormStatus(form, err.message || 'Xəta baş verdi. Birbaşa info@digiboom.az ünvanına yazın.', 'error');
          })
          .finally(function () {
            if (submitBtn) submitBtn.classList.remove('is-loading');
          });
      });
    });
  }

  document.addEventListener('digiboom:includes-ready', bindSmtpContactForms);
  if (document.readyState !== 'loading') {
    bindSmtpContactForms();
  }

})();
