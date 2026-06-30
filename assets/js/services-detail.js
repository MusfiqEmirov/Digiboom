(function () {
  'use strict';

  /* — Video oynatma — */
  var player = document.getElementById('serviceVideoPlayer');
  var video = document.getElementById('serviceDetailVideo');
  var playBtn = document.getElementById('serviceVideoPlay');

  if (player && video && playBtn) {
    function playVideo() {
      video.muted = false;
      video.play().then(function () {
        player.classList.add('is-playing');
      }).catch(function () {
        video.muted = true;
        video.play().then(function () {
          player.classList.add('is-playing');
        });
      });
    }

    playBtn.addEventListener('click', playVideo);

    video.addEventListener('click', function () {
      if (video.paused) {
        playVideo();
      } else {
        video.pause();
        player.classList.remove('is-playing');
      }
    });

    video.addEventListener('ended', function () {
      player.classList.remove('is-playing');
    });
  }

  /* — Checklist stagger animasiyası — */
  var checklist = document.querySelector('.service-detail-checklist');
  if (checklist && 'IntersectionObserver' in window) {
    checklist.querySelectorAll('li').forEach(function (li, idx) {
      li.style.setProperty('--check-delay', (idx * 0.06) + 's');
    });

    var checklistObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          checklist.classList.add('is-visible');
          checklistObserver.disconnect();
        }
      });
    }, { threshold: 0.15 });

    checklistObserver.observe(checklist);
  }

  /* — Bento qalereya lightbox — */
  var gallery = document.getElementById('serviceGallery');
  var modalEl = document.getElementById('serviceImageModal');
  var modalImg = document.getElementById('serviceModalImage');
  var counterEl = document.getElementById('serviceGalleryCounter');
  var prevBtn = document.getElementById('serviceGalleryPrev');
  var nextBtn = document.getElementById('serviceGalleryNext');

  if (gallery && modalEl && modalImg) {
    var items = Array.from(gallery.querySelectorAll('.service-detail-bento__item[data-gallery-index]'));
    var images = items.map(function (item) {
      var img = item.querySelector('img');
      return {
        src: img ? img.src : '',
        alt: img ? img.alt : ''
      };
    });

    var currentIndex = 0;
    var modalInstance = null;

    function getModal() {
      if (!modalInstance) {
        modalInstance = new bootstrap.Modal(modalEl);
      }
      return modalInstance;
    }

    function showImage(index) {
      if (!images.length) return;
      currentIndex = (index + images.length) % images.length;
      var current = images[currentIndex];
      modalImg.src = current.src;
      modalImg.alt = current.alt;
      if (counterEl) {
        counterEl.textContent = (currentIndex + 1) + ' / ' + images.length;
      }
      modalImg.style.animation = 'none';
      void modalImg.offsetWidth;
      modalImg.style.animation = 'serviceGalleryImgIn 0.45s cubic-bezier(0.22, 1, 0.36, 1)';
    }

    gallery.addEventListener('click', function (e) {
      var item = e.target.closest('.service-detail-bento__item');
      if (!item) return;
      var idx = parseInt(item.getAttribute('data-gallery-index'), 10);
      if (isNaN(idx)) return;
      showImage(idx);
      getModal().show();
    });

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        showImage(currentIndex - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        showImage(currentIndex + 1);
      });
    }

    modalEl.addEventListener('keydown', function (e) {
      if (!modalEl.classList.contains('show')) return;
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        showImage(currentIndex - 1);
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        showImage(currentIndex + 1);
      }
    });
  }
})();
