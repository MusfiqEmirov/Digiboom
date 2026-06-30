(function () {
  'use strict';

  /* — Video oynatma — */
  var player = document.getElementById('projectVideoPlayer');
  var video = document.getElementById('projectDetailVideo');
  var playBtn = document.getElementById('projectVideoPlay');

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

  /* — Sinxron qalereya karuselləri — */
  function initSyncedProjectGalleries() {
    var galleryRoot = document.getElementById('projectGallery');
    var topTrack = document.querySelector('.project-gallery-marquee--top .project-gallery-marquee__track');
    var bottomTrack = document.querySelector('.project-gallery-marquee--bottom .project-gallery-marquee__track');
    var topViewport = document.querySelector('.project-gallery-marquee--top');
    var bottomViewport = document.querySelector('.project-gallery-marquee--bottom');

    if (!galleryRoot || !topTrack || !bottomTrack) return;

    var speed = 1.05;
    var visible = true;
    var draggingLane = null;
    var dragStartX = 0;
    var dragStartOffset = 0;
    var dragMoved = false;
    var animatingLane = null;
    var animRaf = null;
    var resizeT = null;

    var topRow = document.querySelector('.project-gallery-carousel__row--top');
    var bottomRow = document.querySelector('.project-gallery-carousel__row--bottom');

    var lanes = [
      { track: topTrack, viewport: topViewport, flow: 'left', offset: 0, loopWidth: 0, paused: false },
      { track: bottomTrack, viewport: bottomViewport, flow: 'right', offset: 0, loopWidth: 0, paused: false }
    ];

    lanes.forEach(function (lane) {
      var origChildren = Array.from(lane.track.children);
      origChildren.forEach(function (child) {
        var clone = child.cloneNode(true);
        clone.setAttribute('data-clone', 'true');
        lane.track.appendChild(clone);
      });
      lane.track.style.animation = 'none';
    });

    function easeOutQuart(t) {
      return 1 - Math.pow(1 - t, 4);
    }

    function normalize(v, loopWidth) {
      if (loopWidth <= 0) return v;
      return ((v % loopWidth) + loopWidth) % loopWidth;
    }

    function setLaneTransform(lane) {
      var x = lane.loopWidth > 0 ? normalize(lane.offset, lane.loopWidth) : lane.offset;
      lane.track.style.transform = 'translate3d(' + (-x) + 'px,0,0)';
    }

    function measureAll() {
      lanes.forEach(function (lane) {
        lane.loopWidth = lane.track.scrollWidth / 2;
        if (lane.flow === 'right' && lane.offset === 0) {
          lane.offset = lane.loopWidth * 0.5;
        }
        lane.offset = normalize(lane.offset, lane.loopWidth);
        setLaneTransform(lane);
      });
    }

    function getStep(lane) {
      var first = lane.track.firstElementChild;
      if (!first) return 300;
      var style = getComputedStyle(lane.track);
      var gap = parseFloat(style.columnGap || style.gap || 0) || 0;
      return first.offsetWidth + gap;
    }

    function animateNudge(lane, delta) {
      if (animatingLane || lane.loopWidth <= 0) return;
      if (animRaf) cancelAnimationFrame(animRaf);
      animatingLane = lane;

      var start = normalize(lane.offset, lane.loopWidth);
      var end = start + delta;
      if (end >= lane.loopWidth) start -= lane.loopWidth;
      if (end < 0) start += lane.loopWidth;
      end = start + delta;

      var duration = 380;
      var t0 = null;

      function frame(now) {
        if (!t0) t0 = now;
        var p = Math.min((now - t0) / duration, 1);
        var cur = start + (end - start) * easeOutQuart(p);
        lane.offset = cur;
        setLaneTransform(lane);
        if (p < 1) {
          animRaf = requestAnimationFrame(frame);
        } else {
          lane.offset = normalize(end, lane.loopWidth);
          setLaneTransform(lane);
          animatingLane = null;
        }
      }
      animRaf = requestAnimationFrame(frame);
    }

    function tick() {
      if (visible && !draggingLane && !animatingLane) {
        lanes.forEach(function (lane) {
          if (lane.paused || lane.loopWidth <= 0) return;
          lane.offset += lane.flow === 'right' ? -speed : speed;
          lane.offset = normalize(lane.offset, lane.loopWidth);
          setLaneTransform(lane);
        });
      }
      requestAnimationFrame(tick);
    }

    measureAll();
    tick();

    window.addEventListener('resize', function () {
      clearTimeout(resizeT);
      resizeT = setTimeout(measureAll, 200);
    });

    function bindNav(selector, lane, direction) {
      document.querySelectorAll(selector).forEach(function (btn) {
        btn.addEventListener('click', function () {
          var delta = direction * getStep(lane);
          if (lane.flow === 'right') delta = -delta;
          animateNudge(lane, delta);
        });
      });
    }

    bindNav('.project-gallery-carousel__nav--top-prev', lanes[0], -1);
    bindNav('.project-gallery-carousel__nav--top-next', lanes[0], 1);
    bindNav('.project-gallery-carousel__nav--bottom-prev', lanes[1], -1);
    bindNav('.project-gallery-carousel__nav--bottom-next', lanes[1], 1);

    if (topRow) {
      topRow.addEventListener('mouseenter', function () { lanes[0].paused = true; });
      topRow.addEventListener('mouseleave', function () {
        lanes[0].paused = false;
        if (draggingLane === lanes[0]) {
          draggingLane = null;
          if (lanes[0].viewport) lanes[0].viewport.classList.remove('is-dragging');
        }
      });
    }
    if (bottomRow) {
      bottomRow.addEventListener('mouseenter', function () { lanes[1].paused = true; });
      bottomRow.addEventListener('mouseleave', function () {
        lanes[1].paused = false;
        if (draggingLane === lanes[1]) {
          draggingLane = null;
          if (lanes[1].viewport) lanes[1].viewport.classList.remove('is-dragging');
        }
      });
    }

    lanes.forEach(function (lane) {
      if (!lane.viewport) return;

      lane.viewport.addEventListener('mousedown', function (e) {
        if (e.button !== 0) return;
        e.preventDefault();
        draggingLane = lane;
        dragMoved = false;
        dragStartX = e.clientX;
        dragStartOffset = normalize(lane.offset, lane.loopWidth);
        lane.viewport.classList.add('is-dragging');
      });

      lane.viewport.addEventListener('touchstart', function (e) {
        if (!e.touches.length) return;
        draggingLane = lane;
        dragMoved = false;
        dragStartX = e.touches[0].clientX;
        dragStartOffset = normalize(lane.offset, lane.loopWidth);
      }, { passive: true });

      lane.viewport.addEventListener('touchmove', function (e) {
        if (draggingLane !== lane || !e.touches.length) return;
        var delta = e.touches[0].clientX - dragStartX;
        if (Math.abs(delta) > 4) dragMoved = true;
        lane.offset = normalize(dragStartOffset - delta, lane.loopWidth);
        setLaneTransform(lane);
      }, { passive: true });

      lane.viewport.addEventListener('touchend', function () {
        if (draggingLane === lane) {
          draggingLane = null;
          lane.viewport.classList.remove('is-dragging');
        }
      });
      lane.viewport.addEventListener('touchcancel', function () {
        if (draggingLane === lane) {
          draggingLane = null;
          lane.viewport.classList.remove('is-dragging');
        }
      });

      lane.track.addEventListener('click', function (e) {
        if (dragMoved) {
          e.preventDefault();
          e.stopPropagation();
          dragMoved = false;
        }
      }, true);
    });

    window.addEventListener('mousemove', function (e) {
      if (!draggingLane) return;
      var delta = e.clientX - dragStartX;
      if (Math.abs(delta) > 4) dragMoved = true;
      draggingLane.offset = normalize(dragStartOffset - delta, draggingLane.loopWidth);
      setLaneTransform(draggingLane);
    });
    window.addEventListener('mouseup', function () {
      if (!draggingLane) return;
      if (draggingLane.viewport) draggingLane.viewport.classList.remove('is-dragging');
      draggingLane = null;
    });

    galleryRoot.addEventListener('click', function (e) {
      if (dragMoved) {
        dragMoved = false;
      }
    }, true);
  }

  initSyncedProjectGalleries();

  /* — Qalereya lightbox — */
  var gallery = document.getElementById('projectGallery');
  var modalEl = document.getElementById('projectImageModal');
  var modalImg = document.getElementById('projectModalImage');
  var counterEl = document.getElementById('projectGalleryCounter');
  var prevBtn = document.getElementById('projectGalleryPrev');
  var nextBtn = document.getElementById('projectGalleryNext');

  if (gallery && modalEl && modalImg) {
    var images = [];
    var i;
    for (i = 0; i < 8; i++) {
      var item = gallery.querySelector('.project-gallery-marquee__item[data-gallery-index="' + i + '"]');
      if (!item) continue;
      var img = item.querySelector('img');
      images.push({
        src: img ? img.src : '',
        alt: img ? img.alt : ''
      });
    }

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
      modalImg.style.animation = 'projectGalleryImgIn 0.45s cubic-bezier(0.22, 1, 0.36, 1)';
    }

    gallery.addEventListener('click', function (e) {
      var item = e.target.closest('.project-gallery-marquee__item');
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

  /* — Checklist stagger animasiyası — */
  var checklist = document.querySelector('.project-detail-checklist');
  if (checklist && 'IntersectionObserver' in window) {
    var listItems = checklist.querySelectorAll('li');
    listItems.forEach(function (li, idx) {
      li.style.setProperty('--check-delay', (idx * 0.07) + 's');
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          checklist.classList.add('is-visible');
          observer.disconnect();
        }
      });
    }, { threshold: 0.2 });

    observer.observe(checklist);
  }
})();
