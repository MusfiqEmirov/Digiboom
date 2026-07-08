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
        stepCards: 1,
        prev: '.services-nav-prev',
        next: '.services-nav-next'
    });

    // Testimonial: hər klikdə bir rəy
    var $testimonialSlider = $('.testimonial-slider');
    if ($testimonialSlider.length) {
        var testimonialAutoplayTimer;

        function buildTestimonialStarsHtml(rating) {
            var count = Math.max(1, Math.min(5, parseInt(rating, 10) || 5));
            var html = '<div class="testimonial-stars" aria-label="' + count + ' ulduzdan 5">';
            for (var i = 1; i <= 5; i++) {
                html += '<iconify-icon icon="lucide:star"' + (i <= count ? ' class="is-filled"' : '') + ' aria-hidden="true"></iconify-icon>';
            }
            return html + '</div>';
        }

        function initTestimonialStars(root) {
            $(root || document).find('.testimonial-card').each(function () {
                var $card = $(this);
                var $body = $card.find('.card-body').first();
                if (!$body.length || $body.find('.testimonial-stars').length) return;
                var rating = parseInt($card.attr('data-rating'), 10) || 5;
                $body.prepend(buildTestimonialStarsHtml(rating));
            });
        }

        initTestimonialStars();

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

        function goTestimonialNext() {
            $testimonialSlider.trigger('next.owl.carousel', [300]);
        }

        function goTestimonialPrev() {
            $testimonialSlider.trigger('prev.owl.carousel', [300]);
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

        window.addSubmittedTestimonial = function (data) {
            var rating = Math.max(1, Math.min(5, parseInt(data.rating, 10) || 5));
            var categoryLabel = data.categoryLabel || data.category || '';
            var company = data.company || 'Müştəri';
            var text = data.text || '';
            var initial = company.trim().charAt(0).toUpperCase() || 'D';
            var $item = $(
                '<div class="item d-flex align-items-stretch">' +
                '<div class="testimonial-card testimonial-card--light w-100 h-100" data-rating="' + rating + '">' +
                '<div class="card-body d-flex flex-column gap-5 justify-content-between">' +
                buildTestimonialStarsHtml(rating) +
                '<p class="testimonial-quote mb-0"></p>' +
                '<div class="testimonial-author hstack gap-3">' +
                '<div class="testimonial-author__avatar" aria-hidden="true">' + initial + '</div>' +
                '<div><h5 class="mb-1 fw-semibold"></h5><p class="mb-0 text-muted small"></p></div>' +
                '</div></div></div></div>'
            );
            $item.find('.testimonial-quote').text(text);
            $item.find('h5').text(company);
            $item.find('.text-muted').text(categoryLabel);
            $testimonialSlider.trigger('add.owl.carousel', [$item, 0]);
            $testimonialSlider.trigger('refresh.owl.carousel');
            $testimonialSlider.trigger('to.owl.carousel', [0, 300]);
        };
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

	// Rəy bildir modal – dropdown, ulduz, fayl və göndərmə
	var $reviewForm = $('#reviewForm');
	var $reviewModal = $('#reviewModal');
	var reviewSuccessTimer = null;
	var reviewDropdownCloseTimer = null;
	var REVIEW_CATEGORY_LABELS = {
		paketler: 'Paketlər',
		telim: 'Təlim',
		elaqe: 'Əlaqə',
		qiymetler: 'Qiymətlər',
		layiheler: 'Layihələr',
		diger: 'Digər'
	};

	function showReviewSuccessAlert() {
		var alertEl = document.getElementById('reviewSuccessAlert');
		if (!alertEl) return;
		if (reviewSuccessTimer) clearTimeout(reviewSuccessTimer);
		alertEl.hidden = false;
		requestAnimationFrame(function () {
			alertEl.classList.add('is-visible');
		});
		reviewSuccessTimer = setTimeout(function () {
			alertEl.classList.remove('is-visible');
			setTimeout(function () {
				alertEl.hidden = true;
			}, 320);
		}, 2000);
	}

	function resetReviewDropdown() {
		var $dropdown = $('#reviewCategoryDropdown');
		if (!$dropdown.length) return;
		$dropdown.removeClass('is-open');
		$dropdown.find('.review-dropdown__toggle').attr('aria-expanded', 'false');
		$dropdown.find('.review-dropdown__option').removeClass('is-active').attr('aria-selected', 'false');
		$('#reviewCategory').val('');
		$dropdown.find('.review-dropdown__label').text('Bölmə seçin');
		$dropdown.find('.review-dropdown__lead-icon').attr('icon', 'lucide:layers');
	}

	function openReviewDropdown() {
		var $dropdown = $('#reviewCategoryDropdown');
		if (!$dropdown.length) return;
		if (reviewDropdownCloseTimer) {
			clearTimeout(reviewDropdownCloseTimer);
			reviewDropdownCloseTimer = null;
		}
		$dropdown.addClass('is-open');
		$dropdown.find('.review-dropdown__toggle').attr('aria-expanded', 'true');
	}

	function closeReviewDropdown(delay) {
		if (reviewDropdownCloseTimer) clearTimeout(reviewDropdownCloseTimer);
		reviewDropdownCloseTimer = setTimeout(function () {
			var $dropdown = $('#reviewCategoryDropdown');
			$dropdown.removeClass('is-open');
			$dropdown.find('.review-dropdown__toggle').attr('aria-expanded', 'false');
		}, delay || 120);
	}

	function selectReviewDropdownOption($option) {
		var value = $option.data('value');
		var label = $option.find('span').text();
		var icon = $option.data('icon') || 'lucide:layers';
		var $dropdown = $('#reviewCategoryDropdown');
		$('#reviewCategory').val(value);
		$dropdown.find('.review-dropdown__label').text(label);
		$dropdown.find('.review-dropdown__lead-icon').attr('icon', icon);
		$dropdown.find('.review-dropdown__option').removeClass('is-active').attr('aria-selected', 'false');
		$option.addClass('is-active').attr('aria-selected', 'true');
		closeReviewDropdown(0);
	}

	function syncReviewStars($group, highlight) {
		var active = highlight;
		if (active == null) {
			var $checked = $group.find('input:checked');
			active = $checked.length ? parseInt($checked.val(), 10) : 0;
		}
		$group.find('.review-star').each(function (index) {
			var filled = index < active;
			$(this).find('iconify-icon').toggleClass('is-filled', filled);
			$(this).toggleClass('is-active', filled && $(this).find('input').is(':checked'));
		});
	}

	var $reviewDropdown = $('#reviewCategoryDropdown');
	if ($reviewDropdown.length) {
		$reviewDropdown.on('mouseenter', function () {
			openReviewDropdown();
		});
		$reviewDropdown.on('mouseleave', function () {
			closeReviewDropdown();
		});
		$reviewDropdown.on('click', '.review-dropdown__toggle', function (e) {
			e.preventDefault();
			if ($reviewDropdown.hasClass('is-open')) {
				closeReviewDropdown(0);
			} else {
				openReviewDropdown();
			}
		});
		$reviewDropdown.on('click', '.review-dropdown__option', function (e) {
			e.preventDefault();
			selectReviewDropdownOption($(this));
		});
	}

	$reviewForm.on('mouseenter', '.review-star', function () {
		var index = $(this).index() + 1;
		syncReviewStars($(this).closest('.review-stars'), index);
	});
	$reviewForm.on('mouseleave', '.review-stars', function () {
		syncReviewStars($(this));
	});
	$reviewForm.on('change', '.review-star input', function () {
		syncReviewStars($(this).closest('.review-stars'));
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
		resetReviewDropdown();
		syncReviewStars($reviewForm.find('.review-stars'));
		$reviewForm.find('.review-file-upload').removeClass('has-file');
		$reviewForm.find('.review-file-name').text('');
	});

	$reviewForm.on('submit', function (e) {
		e.preventDefault();
		if (!$('#reviewCategory').val()) {
			openReviewDropdown();
			return;
		}
		var category = $('#reviewCategory').val();
		var payload = {
			company: $('#reviewCompany').val(),
			category: category,
			categoryLabel: REVIEW_CATEGORY_LABELS[category] || category,
			rating: $reviewForm.find('input[name="rating"]:checked').val(),
			text: $('#reviewText').val()
		};
		if (typeof window.addSubmittedTestimonial === 'function') {
			window.addSubmittedTestimonial(payload);
		}
		var modal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
		if (modal) modal.hide();
		showReviewSuccessAlert();
	});

	function openReviewModalFromHash() {
		if (window.location.hash !== '#rey') return;
		var modalEl = document.getElementById('reviewModal');
		if (!modalEl || !window.bootstrap || !window.bootstrap.Modal) return;
		window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
	}

	openReviewModalFromHash();
	window.addEventListener('hashchange', openReviewModalFromHash);

});

