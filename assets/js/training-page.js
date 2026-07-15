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

  /* Detal: icmal video önizləməsi */
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
