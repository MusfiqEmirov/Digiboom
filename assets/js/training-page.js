(function () {
  'use strict';

  /* Siyahı: səhifə başına 6 kurs — layihələr səhifəsi kimi 12 səhifə pəncərəsi */
  var grid = document.querySelector('[data-training-grid]');
  if (grid) {
    var originals = Array.prototype.slice.call(grid.querySelectorAll('[data-training-card]'));
    var perPage = 6;
    var targetTotal = perPage * 12;
    var currentPage = 1;
    var activeFilter = 'all';
    var pagination = document.querySelector('[data-training-pagination]');
    var filterButtons = document.querySelectorAll('[data-training-filter]');

    while (grid.querySelectorAll('[data-training-card]').length < targetTotal && originals.length) {
      var nextIndex = grid.querySelectorAll('[data-training-card]').length % originals.length;
      grid.appendChild(originals[nextIndex].cloneNode(true));
    }

    var allCards = Array.prototype.slice.call(grid.querySelectorAll('[data-training-card]'));

    function getVisibleCards() {
      if (activeFilter === 'all') return allCards.slice();
      return allCards.filter(function (card) {
        return card.getAttribute('data-training-category') === activeFilter;
      });
    }

    function getTotalPages() {
      return Math.max(1, Math.ceil(getVisibleCards().length / perPage));
    }

    function getPageWindow(page, totalPages) {
      var windowSize = 3;
      var start = page;

      if (page > totalPages - windowSize) {
        start = Math.max(1, page - windowSize + 1);
      }

      var end = Math.min(start + windowSize - 1, totalPages);

      if (end - start + 1 < windowSize) {
        start = Math.max(1, end - windowSize + 1);
      }

      return { start: start, end: end, size: windowSize };
    }

    function appendPageBtn(num, page) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'training-pagination__btn' + (num === page ? ' is-active' : '');
      btn.textContent = String(num);
      btn.setAttribute('aria-label', 'Səhifə ' + num);
      btn.setAttribute('aria-current', num === page ? 'page' : 'false');
      btn.addEventListener('click', function () { renderPage(num); });
      pagination.appendChild(btn);
    }

    function appendDots() {
      var dots = document.createElement('span');
      dots.className = 'training-pagination__dots';
      dots.setAttribute('aria-hidden', 'true');
      dots.textContent = '...';
      pagination.appendChild(dots);
    }

    function renderPage(page) {
      var visible = getVisibleCards();
      var totalPages = getTotalPages();
      currentPage = Math.max(1, Math.min(page, totalPages));

      allCards.forEach(function (card) {
        card.classList.add('is-hidden');
      });

      var start = (currentPage - 1) * perPage;
      var end = start + perPage;
      visible.slice(start, end).forEach(function (card) {
        card.classList.remove('is-hidden');
      });

      if (pagination) {
        pagination.innerHTML = '';
        if (totalPages <= 1) return;

        var prev = document.createElement('button');
        prev.type = 'button';
        prev.className = 'training-pagination__btn' + (currentPage === 1 ? ' is-disabled' : '');
        prev.textContent = '‹';
        prev.setAttribute('aria-label', 'Əvvəlki səhifə');
        prev.setAttribute('aria-disabled', currentPage === 1 ? 'true' : 'false');
        prev.addEventListener('click', function () {
          if (currentPage === 1) return;
          renderPage(currentPage - 1);
        });
        pagination.appendChild(prev);

        var win = getPageWindow(currentPage, totalPages);
        var winStart = win.start;
        var winEnd = win.end;
        var i;

        if (winStart > 1 && currentPage > win.size) {
          appendPageBtn(1, currentPage);
          if (winStart > 2) appendDots();
        }

        for (i = winStart; i <= winEnd; i++) {
          appendPageBtn(i, currentPage);
        }

        if (winEnd < totalPages) {
          appendDots();
          appendPageBtn(totalPages, currentPage);
        }

        var next = document.createElement('button');
        next.type = 'button';
        next.className = 'training-pagination__btn' + (currentPage === totalPages ? ' is-disabled' : '');
        next.textContent = '›';
        next.setAttribute('aria-label', 'Növbəti səhifə');
        next.setAttribute('aria-disabled', currentPage === totalPages ? 'true' : 'false');
        next.addEventListener('click', function () {
          if (currentPage === totalPages) return;
          renderPage(currentPage + 1);
        });
        pagination.appendChild(next);
      }
    }

    filterButtons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeFilter = btn.getAttribute('data-training-filter') || 'all';
        filterButtons.forEach(function (b) {
          b.classList.toggle('is-active', b === btn);
        });
        renderPage(1);
      });
    });

    renderPage(1);
  }

  /* Detal: icmal video müddəti + önizləmə */
  function formatVideoDuration(seconds) {
    if (!isFinite(seconds) || seconds < 0) return '';
    var total = Math.round(seconds);
    var mins = Math.floor(total / 60);
    var secs = total % 60;
    return mins + ':' + (secs < 10 ? '0' : '') + secs;
  }

  function fillCurriculumDurations() {
    var thumbs = document.querySelectorAll('[data-training-preview]');
    if (!thumbs.length) return;

    thumbs.forEach(function (btn) {
      var src = btn.getAttribute('data-video-src');
      var durationEl = btn.querySelector('.training-curriculum__duration');
      if (!src || !durationEl) return;

      durationEl.textContent = '';
      durationEl.setAttribute('aria-hidden', 'true');

      var probe = document.createElement('video');
      probe.preload = 'metadata';
      probe.muted = true;
      probe.setAttribute('playsinline', '');

      function applyDuration() {
        var text = formatVideoDuration(probe.duration);
        if (!text) return;
        durationEl.textContent = text;
        durationEl.removeAttribute('aria-hidden');
      }

      probe.addEventListener('loadedmetadata', applyDuration);
      probe.addEventListener('error', function () {
        durationEl.textContent = '';
        durationEl.setAttribute('aria-hidden', 'true');
      });

      probe.src = src;
    });
  }

  fillCurriculumDurations();

  /* Detal: Təlimdən kadrlar lightbox */
  var trainingGallery = document.getElementById('trainingGallery');
  var trainingModalEl = document.getElementById('trainingImageModal');
  var trainingModalImg = document.getElementById('trainingModalImage');
  var trainingCounterEl = document.getElementById('trainingGalleryCounter');
  var trainingPrevBtn = document.getElementById('trainingGalleryPrev');
  var trainingNextBtn = document.getElementById('trainingGalleryNext');

  if (trainingGallery && trainingModalEl && trainingModalImg) {
    var galleryItems = Array.prototype.slice.call(
      trainingGallery.querySelectorAll('.training-detail__gallery-item[data-gallery-index]')
    );
    var galleryImages = galleryItems.map(function (item) {
      var img = item.querySelector('img');
      return {
        src: img ? img.src : '',
        alt: img ? img.alt : ''
      };
    });

    var galleryIndex = 0;
    var trainingGalleryModal = null;

    function getTrainingGalleryModal() {
      if (!trainingGalleryModal) {
        trainingGalleryModal = new bootstrap.Modal(trainingModalEl);
      }
      return trainingGalleryModal;
    }

    function showTrainingGalleryImage(index) {
      if (!galleryImages.length) return;
      galleryIndex = (index + galleryImages.length) % galleryImages.length;
      var current = galleryImages[galleryIndex];
      trainingModalImg.src = current.src;
      trainingModalImg.alt = current.alt;
      if (trainingCounterEl) {
        trainingCounterEl.textContent = (galleryIndex + 1) + ' / ' + galleryImages.length;
      }
      trainingModalImg.style.animation = 'none';
      void trainingModalImg.offsetWidth;
      trainingModalImg.style.animation = 'serviceGalleryImgIn 0.45s cubic-bezier(0.22, 1, 0.36, 1)';
    }

    trainingGallery.addEventListener('click', function (e) {
      var item = e.target.closest('.training-detail__gallery-item');
      if (!item || !trainingGallery.contains(item)) return;
      var idx = parseInt(item.getAttribute('data-gallery-index'), 10);
      if (isNaN(idx)) return;
      showTrainingGalleryImage(idx);
      getTrainingGalleryModal().show();
    });

    if (trainingPrevBtn) {
      trainingPrevBtn.addEventListener('click', function () {
        showTrainingGalleryImage(galleryIndex - 1);
      });
    }

    if (trainingNextBtn) {
      trainingNextBtn.addEventListener('click', function () {
        showTrainingGalleryImage(galleryIndex + 1);
      });
    }

    var trainingCloseBtn = trainingModalEl.querySelector('.service-gallery-modal__close');
    if (trainingCloseBtn) {
      trainingCloseBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        getTrainingGalleryModal().hide();
      });
    }

    trainingModalEl.addEventListener('keydown', function (e) {
      if (!trainingModalEl.classList.contains('show')) return;
      if (e.key === 'Escape') {
        getTrainingGalleryModal().hide();
        return;
      }
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        showTrainingGalleryImage(galleryIndex - 1);
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        showTrainingGalleryImage(galleryIndex + 1);
      }
    });
  }

  var previewModal = document.getElementById('trainingPreviewModal');
  var previewVideo = document.getElementById('trainingPreviewVideo');
  if (previewModal && previewVideo) {
    document.querySelectorAll('[data-training-preview]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var src = btn.getAttribute('data-video-src');
        var title = btn.getAttribute('data-video-title') || 'Video önizləmə';
        if (!src) return;
        previewVideo.src = src;
        previewVideo.setAttribute('title', title);
        previewModal.querySelector('.modal-title').textContent = title;
        var modal = bootstrap.Modal.getOrCreateInstance(previewModal);
        modal.show();
      });
    });
    previewModal.addEventListener('hidden.bs.modal', function () {
      previewVideo.pause();
      previewVideo.removeAttribute('src');
      previewVideo.load();
    });
  }

  /* Detal: sifariş modalı */
  var orderModal = document.getElementById('trainingOrderModal');
  var orderForm = document.getElementById('trainingOrderForm');
  if (orderModal && orderForm) {
    var courseInput = document.getElementById('trainingOrderCourse');
    var nameInput = document.getElementById('trainingOrderName');
    var phoneInput = document.getElementById('trainingOrderPhone');
    var gmailInput = document.getElementById('trainingOrderGmail');
    var gmailError = document.getElementById('trainingOrderGmailError');
    var orderStatus = document.getElementById('trainingOrderStatus');
    var gmailPattern = /^[a-zA-Z0-9._%+-]+@gmail\.com$/i;

    function fillTrainingName() {
      var titleEl = document.querySelector('.training-detail__title');
      if (courseInput && titleEl) {
        courseInput.value = (titleEl.textContent || '').trim();
      }
    }

    function setGmailValid(isValid) {
      if (!gmailInput) return;
      gmailInput.classList.toggle('is-invalid', !isValid);
      if (gmailError) gmailError.hidden = isValid;
    }

    function isGmailValid() {
      var value = (gmailInput.value || '').trim();
      return value.length > 0 && gmailPattern.test(value);
    }

    orderModal.addEventListener('show.bs.modal', function () {
      fillTrainingName();
      if (orderStatus) {
        orderStatus.hidden = true;
        orderStatus.textContent = '';
        orderStatus.classList.remove('training-order-form__status--ok');
      }
      setGmailValid(true);
    });

    if (gmailInput) {
      gmailInput.addEventListener('input', function () {
        if (!(gmailInput.value || '').trim()) {
          setGmailValid(true);
          return;
        }
        setGmailValid(isGmailValid());
      });
      gmailInput.addEventListener('blur', function () {
        if ((gmailInput.value || '').trim()) setGmailValid(isGmailValid());
      });
    }

    orderForm.addEventListener('submit', function (e) {
      e.preventDefault();

      var name = (nameInput && nameInput.value || '').trim();
      var phone = (phoneInput && phoneInput.value || '').trim();
      var gmailOk = isGmailValid();

      setGmailValid(gmailOk);

      if (!name) {
        if (nameInput) nameInput.focus();
        return;
      }
      if (!phone) {
        if (phoneInput) phoneInput.focus();
        return;
      }
      if (!gmailOk) {
        if (gmailInput) gmailInput.focus();
        return;
      }

      /* Ödəniş inteqrasiyası sonra əlavə olunacaq */
      if (orderStatus) {
        orderStatus.hidden = false;
        orderStatus.classList.add('training-order-form__status--ok');
        orderStatus.textContent = 'Məlumatlar qəbul olundu. Ödəniş inteqrasiyası tezliklə aktivləşəcək.';
      }
    });
  }
})();
