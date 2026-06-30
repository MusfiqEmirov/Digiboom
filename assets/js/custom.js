$(function () {

    // Header Scroll
    $(window).scroll(function () {
        if ($(window).scrollTop() >= 60) {
            $("header").addClass("fixed-header");
        } else {
            $("header").removeClass("fixed-header");
        }
    });


    // İnteraktiv marquee
    function initInteractiveMarquee(config) {
        var trackEl = document.querySelector(config.track);
        if (!trackEl) return;
        var viewportEl = trackEl.closest(config.viewport);
        if (!viewportEl) return;

        var flow      = config.flow || 'left';
        var speed     = config.speed || 0.45;
        var loopWidth = 0;
        var offset    = 0;
        var paused    = false;
        var visible   = true;
        var dragging  = false;
        var dragStartX = 0;
        var dragStartOffset = 0;
        var dragMoved = false;
        var animating = false;
        var animRaf   = null;

        // Klonla: sonsuz loop üçün 1 əlavə nüsxə
        var origChildren = Array.from(trackEl.children);
        origChildren.forEach(function (child) {
            trackEl.appendChild(child.cloneNode(true));
        });
        trackEl.style.animation = 'none';

        function easeOutQuart(t) {
            return 1 - Math.pow(1 - t, 4);
        }

        function normalize(v) {
            if (loopWidth <= 0) return v;
            return ((v % loopWidth) + loopWidth) % loopWidth;
        }

        // transform həmişə normalize edilmiş dəyərlə — animasiya bitişindəki sıçrayış yoxdur
        function setTransform(raw) {
            var x = loopWidth > 0 ? normalize(raw) : raw;
            trackEl.style.transform = 'translate3d(' + (-x) + 'px,0,0)';
        }

        function measure() {
            loopWidth = trackEl.scrollWidth / 2;
            // sağ axış: ikinci kopyanın ortasından başla
            if (flow === 'right' && offset === 0) {
                offset = loopWidth * 0.5;
            }
            offset = normalize(offset);
            setTransform(offset);
        }

        function getItemWidth() {
            var first = trackEl.firstElementChild;
            if (!first) return 320;
            var style = getComputedStyle(trackEl);
            var gap = parseFloat(style.columnGap || style.gap || 0) || 0;
            return first.offsetWidth + gap;
        }

        function getStep() {
            return getItemWidth() * (config.stepCards || 1);
        }

        function getAnimDuration() {
            var n = config.stepCards || 1;
            return Math.min(300 + n * 180, 900);
        }

        function animateNudge(delta) {
            if (animating || loopWidth <= 0) return;
            if (animRaf) cancelAnimationFrame(animRaf);
            animating = true;

            // Normalize başlanğıc nöqtəsini
            var start = normalize(offset);
            var end   = start + delta;

            // Animasiya boyunca hər iki tərəf eyni "kopya"da qalsın — wrap baş verməsin
            // Əgər end bütöv dövrü keçirsə, start-ı uyğunlaşdırırıq
            if (end >= loopWidth)  start = start - loopWidth;
            if (end < 0)           start = start + loopWidth;
            end = start + delta;

            var duration = getAnimDuration();
            var t0 = null;

            function frame(now) {
                if (!t0) t0 = now;
                var p = Math.min((now - t0) / duration, 1);
                var cur = start + (end - start) * easeOutQuart(p);
                setTransform(cur);
                if (p < 1) {
                    animRaf = requestAnimationFrame(frame);
                } else {
                    offset = normalize(end);
                    setTransform(offset);
                    animating = false;
                }
            }
            animRaf = requestAnimationFrame(frame);
        }

        function tick() {
            if (visible && !paused && !dragging && !animating && loopWidth > 0) {
                offset += flow === 'right' ? -speed : speed;
                offset = normalize(offset);
                setTransform(offset);
            }
            requestAnimationFrame(tick);
        }

        // IntersectionObserver: görünmədikdə CPU-nu boş yükləmirik
        if ('IntersectionObserver' in window) {
            var io = new IntersectionObserver(function (entries) {
                visible = entries[0].isIntersecting;
            }, { threshold: 0 });
            io.observe(viewportEl);
        }

        measure();
        tick();

        window.addEventListener('resize', function () {
            clearTimeout(config._resizeT);
            config._resizeT = setTimeout(measure, 200);
        });

        // Ox düymələri
        if (config.prev) {
            document.querySelectorAll(config.prev).forEach(function (btn) {
                btn.addEventListener('click', function () {
                    animateNudge(flow === 'right' ? getStep() : -getStep());
                });
            });
        }
        if (config.next) {
            document.querySelectorAll(config.next).forEach(function (btn) {
                btn.addEventListener('click', function () {
                    animateNudge(flow === 'right' ? -getStep() : getStep());
                });
            });
        }

        // Hover — dur
        viewportEl.addEventListener('mouseenter', function () { paused = true; });
        viewportEl.addEventListener('mouseleave', function () {
            paused = false;
            if (dragging) {
                dragging = false;
                viewportEl.classList.remove('is-dragging');
            }
        });

        // Mouse drag
        viewportEl.addEventListener('mousedown', function (e) {
            if (e.button !== 0) return;
            e.preventDefault();
            dragging   = true;
            dragMoved  = false;
            dragStartX = e.clientX;
            dragStartOffset = normalize(offset);
            viewportEl.classList.add('is-dragging');
        });
        window.addEventListener('mousemove', function (e) {
            if (!dragging) return;
            var delta = e.clientX - dragStartX;
            if (Math.abs(delta) > 4) dragMoved = true;
            offset = normalize(dragStartOffset - delta);
            setTransform(offset);
        });
        window.addEventListener('mouseup', function () {
            if (!dragging) return;
            dragging = false;
            viewportEl.classList.remove('is-dragging');
        });

        // Touch drag (passive: true → scroll-u bloklamır)
        viewportEl.addEventListener('touchstart', function (e) {
            if (!e.touches.length) return;
            dragging   = true;
            dragMoved  = false;
            dragStartX = e.touches[0].clientX;
            dragStartOffset = normalize(offset);
        }, { passive: true });
        viewportEl.addEventListener('touchmove', function (e) {
            if (!dragging || !e.touches.length) return;
            var delta = e.touches[0].clientX - dragStartX;
            if (Math.abs(delta) > 4) dragMoved = true;
            offset = normalize(dragStartOffset - delta);
            setTransform(offset);
        }, { passive: true });
        viewportEl.addEventListener('touchend',    function () { dragging = false; });
        viewportEl.addEventListener('touchcancel', function () { dragging = false; });

        // Drag zamanı linklərə kliku bloklayırıq
        trackEl.addEventListener('click', function (e) {
            if (dragMoved) {
                e.preventDefault();
                e.stopPropagation();
                dragMoved = false;
            }
        }, true);
    }

    initInteractiveMarquee({
        id: 'featured',
        track: '.featured-projects-marquee__track',
        viewport: '.featured-projects-marquee',
        flow: 'right',
        speed: 0.45,
        stepCards: 1,
        prev: '.featured-projects-nav-prev',
        next: '.featured-projects-nav-next'
    });

    initInteractiveMarquee({
        id: 'services',
        track: '.services-marquee__track',
        viewport: '.services-marquee',
        flow: 'left',
        speed: 0.45,
        stepCards: 4,
        prev: '.services-nav-prev',
        next: '.services-nav-next'
    });

    // Testimonial: desktop 1,2,3 → 4,5,6 → 7,8,9 (icon 3-3), mobil 1-1
    var $testimonialSlider = $('.testimonial-slider');
    if ($testimonialSlider.length) {
        var testimonialAutoplayTimer;
        var desktopPage = 0; // 0 = 1,2,3  1 = 4,5,6  2 = 7,8,9

        $testimonialSlider.owlCarousel({
            loop: true,
            margin: 24,
            nav: false,
            dots: false,
            autoplay: false,
            startPosition: 0,
            responsive: {
                0: { items: 1 },
                992: { items: 3 }
            }
        });

        function isDesktop() {
            return $(window).width() >= 992;
        }

        function goTestimonialNext() {
            if (isDesktop()) {
                desktopPage = (desktopPage + 1) % 3;
                $testimonialSlider.trigger('to.owl.carousel', [desktopPage * 3, 300]);
            } else {
                $testimonialSlider.trigger('next.owl.carousel', [300]);
            }
        }

        function goTestimonialPrev() {
            if (isDesktop()) {
                desktopPage = (desktopPage - 1 + 3) % 3;
                $testimonialSlider.trigger('to.owl.carousel', [desktopPage * 3, 300]);
            } else {
                $testimonialSlider.trigger('prev.owl.carousel', [300]);
            }
        }

        $('.testimonial-nav-prev').on('click', goTestimonialPrev);
        $('.testimonial-nav-next').on('click', goTestimonialNext);

        function startAutoplay() {
            testimonialAutoplayTimer = setInterval(goTestimonialNext, 5000);
        }
        function stopAutoplay() {
            if (testimonialAutoplayTimer) {
                clearInterval(testimonialAutoplayTimer);
                testimonialAutoplayTimer = null;
            }
        }
        startAutoplay();
        $('.testimonial-slider-wrapper').on('mouseenter', stopAutoplay).on('mouseleave', startAutoplay);
    }


    // Stats count-up (ana səhifə & haqqımızda)
    function animateStatCount($el) {
        if ($el.data('counted')) return;
        $el.data('counted', true);

        var target = parseInt($el.attr('data-target'), 10);
        if (isNaN(target)) {
            target = parseInt($el.text(), 10) || 0;
        }

        $el.text('0');
        $({ value: 0 }).animate({ value: target }, {
            duration: 1800,
            easing: 'swing',
            step: function (now) {
                $el.text(Math.floor(now));
            },
            complete: function () {
                $el.text(target);
            }
        });
    }

    var $statCounts = $('.about-stats .count');
    $statCounts.each(function () {
        $(this).text('0');
    });

    if ($statCounts.length && 'IntersectionObserver' in window) {
        var statsObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                $(entry.target).find('.count').each(function () {
                    animateStatCount($(this));
                });
                statsObserver.unobserve(entry.target);
            });
        }, { threshold: 0.35, rootMargin: '0px 0px -40px 0px' });

        $('.about-stats__cards').each(function () {
            statsObserver.observe(this);
        });

        $('.about-stats').each(function () {
            if (!this.querySelector('.about-stats__cards')) {
                var cardsRow = this.querySelector('.stats-card');
                if (cardsRow) {
                    statsObserver.observe(cardsRow.closest('.row'));
                }
            }
        });
    } else {
        $statCounts.each(function () {
            animateStatCount($(this));
        });
    }


    // Aos
	AOS.init({
		once: true,
	});

	// Rəy bildir modal – xidmət çipləri və fayl adı
	var $reviewForm = $('#reviewForm');
	var $reviewModal = $('#reviewModal');

	function syncReviewServiceChip($chip) {
		$chip.closest('.review-service-grid').find('.review-service-chip').removeClass('is-selected');
		$chip.addClass('is-selected');
	}

	$reviewForm.on('change', '.review-service-chip input[type="radio"]', function () {
		syncReviewServiceChip($(this).closest('.review-service-chip'));
	});

	$reviewForm.on('change', '#reviewImage', function () {
		var file = this.files && this.files[0];
		var $name = $reviewForm.find('.review-file-name');
		var $upload = $reviewForm.find('.review-file-upload');
		if (file) {
			$name.text(file.name);
			$upload.addClass('has-file');
		} else {
			$name.text('');
			$upload.removeClass('has-file');
		}
	});

	$reviewModal.on('hidden.bs.modal', function () {
		$reviewForm[0].reset();
		$reviewForm.find('.review-service-chip').removeClass('is-selected');
		$reviewForm.find('.review-file-upload').removeClass('has-file');
		$reviewForm.find('.review-file-name').text('');
	});

	$reviewForm.on('submit', function (e) {
		e.preventDefault();
		var modal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
		if (modal) modal.hide();
		// TODO: form məlumatlarını serverə göndərmək
	});

});

