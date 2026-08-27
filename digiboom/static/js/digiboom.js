(function () {
  'use strict';

  /* =====================================================
     HERO BANNER SLIDER
     - Both arrows always visible (when >1 slide)
     - Auto: image ~3.5s → next; video → next when ended
     ===================================================== */
  var heroMedia = document.querySelector('.hero-banner-media');
  if (heroMedia) {
    var slides = Array.from(heroMedia.querySelectorAll('.hero-banner-slide'));
    var prevBtn = document.querySelector('.hero-banner-nav--prev');
    var nextBtn = document.querySelector('.hero-banner-nav--next');
    var current = 0;
    var heroTransitionMs = 850;
    var heroTransitioning = false;
    var imageDwellMs = 3500;
    var autoTimer = null;
    var videoEndedHandler = null;

    function clearAutoAdvance() {
      if (autoTimer) {
        clearTimeout(autoTimer);
        autoTimer = null;
      }
      if (videoEndedHandler) {
        slides.forEach(function (slide) {
          var vid = slide.querySelector('video');
          if (vid) vid.removeEventListener('ended', videoEndedHandler);
        });
        videoEndedHandler = null;
      }
    }

    function scheduleAutoAdvance() {
      clearAutoAdvance();
      if (slides.length <= 1) return;

      var slide = slides[current];
      var vid = slide.querySelector('video');

      if (vid) {
        videoEndedHandler = function () {
          goTo(current + 1);
        };
        vid.addEventListener('ended', videoEndedHandler);
        // If metadata already ended / short clip already finished
        if (vid.ended) {
          autoTimer = setTimeout(function () {
            goTo(current + 1);
          }, 200);
        }
      } else {
        autoTimer = setTimeout(function () {
          goTo(current + 1);
        }, imageDwellMs);
      }
    }

    function goTo(idx) {
      if (heroTransitioning) return;
      if (slides.length <= 1) return;
      var next = (idx + slides.length) % slides.length;
      if (next === current) return;

      clearAutoAdvance();
      heroTransitioning = true;
      var oldSlide = slides[current];
      var oldVid = oldSlide.querySelector('video');

      oldSlide.classList.remove('is-active');
      current = next;
      slides[current].classList.add('is-active');

      var newVid = slides[current].querySelector('video');
      if (newVid) {
        try {
          newVid.currentTime = 0;
        } catch (e) { /* ignore */ }
        newVid.play().catch(function () {});
      }

      setTimeout(function () {
        if (oldVid) {
          oldVid.pause();
          try {
            oldVid.currentTime = 0;
          } catch (e) { /* ignore */ }
        }
        heroTransitioning = false;
        scheduleAutoAdvance();
      }, heroTransitionMs);
    }

    if (prevBtn) {
      prevBtn.classList.remove('hero-banner-nav--hidden', 'hero-banner-nav--disabled');
      prevBtn.removeAttribute('aria-disabled');
      prevBtn.removeAttribute('aria-hidden');
      prevBtn.removeAttribute('tabindex');
      prevBtn.addEventListener('click', function () {
        goTo(current - 1);
      });
    }
    if (nextBtn) {
      nextBtn.classList.remove('hero-banner-nav--hidden', 'hero-banner-nav--disabled');
      nextBtn.removeAttribute('aria-disabled');
      nextBtn.removeAttribute('aria-hidden');
      nextBtn.removeAttribute('tabindex');
      nextBtn.addEventListener('click', function () {
        goTo(current + 1);
      });
    }

    // Start autoplay for the initial slide
    var firstVid = slides[current] && slides[current].querySelector('video');
    if (firstVid) {
      firstVid.play().catch(function () {});
    }
    scheduleAutoAdvance();
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
      video.muted = false;
      video.play().catch(function () {
        video.muted = true;
        video.play().then(hideOverlay).catch(function () {
          showOverlay();
        });
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

  var contactSuccessTimer = null;

  function getCsrfToken() {
    var cookie = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    if (cookie) return decodeURIComponent(cookie[1]);
    var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return input ? input.value : '';
  }

  window.digiboomGetCsrfToken = getCsrfToken;

  function showContactSuccessAlert() {
    var alertEl = document.getElementById('contactSuccessAlert');
    if (!alertEl) return;
    if (contactSuccessTimer) clearTimeout(contactSuccessTimer);
    alertEl.hidden = false;
    requestAnimationFrame(function () {
      alertEl.classList.add('is-visible');
    });
    contactSuccessTimer = setTimeout(function () {
      alertEl.classList.remove('is-visible');
      setTimeout(function () {
        alertEl.hidden = true;
      }, 320);
    }, 2800);
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
        var endpoint = form.getAttribute('action') || '/api/appeal/';
        var formData = new FormData(form);
        var csrf = getCsrfToken();

        if (submitBtn) submitBtn.classList.add('is-loading');
        showFormStatus(form, '', '');

        fetch(endpoint, {
          method: 'POST',
          body: formData,
          credentials: 'same-origin',
          headers: {
            Accept: 'application/json',
            'X-CSRFToken': csrf
          }
        })
          .then(function (res) {
            return res.json().catch(function () {
              return { ok: false, message: 'Xəta baş verdi.' };
            }).then(function (data) {
              data._httpOk = res.ok;
              return data;
            });
          })
          .catch(function () {
            return { ok: false, message: 'Şəbəkə xətası.' };
          })
          .then(function (data) {
            if (!data || !data.ok) {
              showFormStatus(form, (data && data.message) || 'Göndərilmədi. Yenidən cəhd edin.', 'error');
              return;
            }
            showFormStatus(form, '', '');
            form.reset();
            var contactModalEl = document.getElementById('contactModal');
            if (contactModalEl && window.bootstrap && window.bootstrap.Modal) {
              var contactModal = window.bootstrap.Modal.getInstance(contactModalEl);
              if (contactModal) contactModal.hide();
            }
            showContactSuccessAlert();
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
