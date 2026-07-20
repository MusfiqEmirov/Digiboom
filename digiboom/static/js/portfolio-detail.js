(function () {
  'use strict';

  /* — Layihə adı + xidmətlər (URL-dən; detail-də hamısı göstərilir) — */
  if (window.DigiBoomProjects) {
    var slug = DigiBoomProjects.getProjectSlugFromUrl();
    var project = DigiBoomProjects.getProject(slug);
    var nameEl = document.getElementById('projectDetailName');
    if (nameEl) nameEl.textContent = project.name;
    document.title = 'DigiBoom — ' + project.name;

    var tagsList = document.querySelector('.project-detail-tags');
    if (tagsList && project.services && project.services.length) {
      tagsList.innerHTML = '';
      project.services.forEach(function (serviceName) {
        var href = window.DigiBoomServices
          ? DigiBoomServices.serviceDetailUrl(serviceName)
          : '/services/detail/';
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.className = 'project-detail-tags__item';
        a.href = href;
        a.setAttribute('aria-label', serviceName + ' xidmətinin ətraflı səhifəsi');
        var icon = document.createElement('iconify-icon');
        icon.setAttribute('icon', DigiBoomProjects.getServiceIcon(serviceName));
        icon.setAttribute('aria-hidden', 'true');
        var span = document.createElement('span');
        span.textContent = serviceName;
        a.appendChild(icon);
        a.appendChild(span);
        li.appendChild(a);
        tagsList.appendChild(li);
      });
    }
  }

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

  /* — Tək sətir qalereya karuseli — */
  function initProjectGallery() {
    var galleryRoot = document.getElementById('projectGallery');
    var track = galleryRoot ? galleryRoot.querySelector('.project-gallery-marquee__track') : null;
    var viewport = galleryRoot ? galleryRoot.querySelector('.project-gallery-marquee') : null;
    var row = galleryRoot ? galleryRoot.querySelector('.project-gallery-carousel__row') : null;

    if (!galleryRoot || !track || !viewport) return;

    var speed = 1.05;
    var visible = true;
    var draggingLane = null;
    var dragStartX = 0;
    var dragStartOffset = 0;
    var dragMoved = false;
    var animating = false;
    var animRaf = null;
    var resizeT = null;

    var lane = { track: track, viewport: viewport, flow: 'left', offset: 0, loopWidth: 0, paused: false };

    var origChildren = Array.from(lane.track.children);
    origChildren.forEach(function (child) {
      var clone = child.cloneNode(true);
      clone.setAttribute('data-clone', 'true');
      lane.track.appendChild(clone);
    });
    lane.track.style.animation = 'none';

    function easeOutQuart(t) {
      return 1 - Math.pow(1 - t, 4);
    }

    function normalize(v, loopWidth) {
      if (loopWidth <= 0) return v;
      return ((v % loopWidth) + loopWidth) % loopWidth;
    }

    function setLaneTransform() {
      var x = lane.loopWidth > 0 ? normalize(lane.offset, lane.loopWidth) : lane.offset;
      lane.track.style.transform = 'translate3d(' + (-x) + 'px,0,0)';
    }

    function measure() {
      lane.loopWidth = lane.track.scrollWidth / 2;
      lane.offset = normalize(lane.offset, lane.loopWidth);
      setLaneTransform();
    }

    function getStep() {
      var first = lane.track.firstElementChild;
      if (!first) return 300;
      var style = getComputedStyle(lane.track);
      var gap = parseFloat(style.columnGap || style.gap || 0) || 0;
      return first.offsetWidth + gap;
    }

    function animateNudge(delta) {
      if (animating || lane.loopWidth <= 0) return;
      if (animRaf) cancelAnimationFrame(animRaf);
      animating = true;

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
        setLaneTransform();
        if (p < 1) {
          animRaf = requestAnimationFrame(frame);
        } else {
          lane.offset = normalize(end, lane.loopWidth);
          setLaneTransform();
          animating = false;
        }
      }
      animRaf = requestAnimationFrame(frame);
    }

    function tick() {
      if (visible && !draggingLane && !animating) {
        if (!lane.paused && lane.loopWidth > 0) {
          lane.offset += speed;
          lane.offset = normalize(lane.offset, lane.loopWidth);
          setLaneTransform();
        }
      }
      requestAnimationFrame(tick);
    }

    measure();
    tick();

    window.addEventListener('resize', function () {
      clearTimeout(resizeT);
      resizeT = setTimeout(measure, 200);
    });

    galleryRoot.querySelectorAll('.project-gallery-carousel__nav--prev').forEach(function (btn) {
      btn.addEventListener('click', function () {
        animateNudge(-getStep());
      });
    });

    galleryRoot.querySelectorAll('.project-gallery-carousel__nav--next').forEach(function (btn) {
      btn.addEventListener('click', function () {
        animateNudge(getStep());
      });
    });

    if (row) {
      row.addEventListener('mouseenter', function () { lane.paused = true; });
      row.addEventListener('mouseleave', function () {
        lane.paused = false;
        if (draggingLane) {
          draggingLane = null;
          viewport.classList.remove('is-dragging');
        }
      });
    }

    viewport.addEventListener('mousedown', function (e) {
      if (e.button !== 0) return;
      e.preventDefault();
      draggingLane = lane;
      dragMoved = false;
      dragStartX = e.clientX;
      dragStartOffset = normalize(lane.offset, lane.loopWidth);
      viewport.classList.add('is-dragging');
    });

    viewport.addEventListener('touchstart', function (e) {
      if (!e.touches.length) return;
      draggingLane = lane;
      dragMoved = false;
      dragStartX = e.touches[0].clientX;
      dragStartOffset = normalize(lane.offset, lane.loopWidth);
    }, { passive: true });

    viewport.addEventListener('touchmove', function (e) {
      if (draggingLane !== lane || !e.touches.length) return;
      var delta = e.touches[0].clientX - dragStartX;
      if (Math.abs(delta) > 4) dragMoved = true;
      lane.offset = normalize(dragStartOffset - delta, lane.loopWidth);
      setLaneTransform();
    }, { passive: true });

    viewport.addEventListener('touchend', function () {
      if (draggingLane === lane) {
        draggingLane = null;
        viewport.classList.remove('is-dragging');
      }
    });
    viewport.addEventListener('touchcancel', function () {
      if (draggingLane === lane) {
        draggingLane = null;
        viewport.classList.remove('is-dragging');
      }
    });

    track.addEventListener('click', function (e) {
      if (dragMoved) {
        e.preventDefault();
        e.stopPropagation();
        dragMoved = false;
      }
    }, true);

    window.addEventListener('mousemove', function (e) {
      if (!draggingLane) return;
      var delta = e.clientX - dragStartX;
      if (Math.abs(delta) > 4) dragMoved = true;
      draggingLane.offset = normalize(dragStartOffset - delta, draggingLane.loopWidth);
      setLaneTransform();
    });
    window.addEventListener('mouseup', function () {
      if (!draggingLane) return;
      viewport.classList.remove('is-dragging');
      draggingLane = null;
    });

    galleryRoot.addEventListener('click', function () {
      if (dragMoved) dragMoved = false;
    }, true);
  }

  initProjectGallery();

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
      var item = gallery.querySelector('.project-gallery-marquee__item[data-gallery-index="' + i + '"]:not([data-clone])');
      if (!item) {
        item = gallery.querySelector('.project-gallery-marquee__item[data-gallery-index="' + i + '"]');
      }
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

    var closeBtn = modalEl.querySelector('.project-gallery-modal__close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        getModal().hide();
      });
    }

    modalEl.addEventListener('keydown', function (e) {
      if (!modalEl.classList.contains('show')) return;
      if (e.key === 'Escape') {
        getModal().hide();
        return;
      }
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
