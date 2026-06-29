(function () {
  'use strict';

  /* Siyahı: səhifə başına 6 kurs */
  var grid = document.querySelector('[data-training-grid]');
  if (grid) {
    var allCards = Array.prototype.slice.call(grid.querySelectorAll('[data-training-card]'));
    var perPage = 6;
    var currentPage = 1;
    var activeFilter = 'all';
    var pagination = document.querySelector('[data-training-pagination]');
    var filterButtons = document.querySelectorAll('[data-training-filter]');

    function getVisibleCards() {
      if (activeFilter === 'all') return allCards.slice();
      return allCards.filter(function (card) {
        return card.getAttribute('data-training-category') === activeFilter;
      });
    }

    function getTotalPages() {
      return Math.max(1, Math.ceil(getVisibleCards().length / perPage));
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
        prev.className = 'training-pagination__btn';
        prev.textContent = '‹';
        prev.setAttribute('aria-label', 'Əvvəlki səhifə');
        prev.disabled = currentPage === 1;
        prev.addEventListener('click', function () { renderPage(currentPage - 1); });
        pagination.appendChild(prev);

        for (var i = 1; i <= totalPages; i++) {
          (function (num) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'training-pagination__btn' + (num === currentPage ? ' is-active' : '');
            btn.textContent = String(num);
            btn.setAttribute('aria-label', 'Səhifə ' + num);
            btn.setAttribute('aria-current', num === currentPage ? 'page' : 'false');
            btn.addEventListener('click', function () { renderPage(num); });
            pagination.appendChild(btn);
          })(i);
        }

        var next = document.createElement('button');
        next.type = 'button';
        next.className = 'training-pagination__btn';
        next.textContent = '›';
        next.setAttribute('aria-label', 'Növbəti səhifə');
        next.disabled = currentPage === totalPages;
        next.addEventListener('click', function () { renderPage(currentPage + 1); });
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
})();
