$(function () {

    // Header Scroll
    $(window).scroll(function () {
        if ($(window).scrollTop() >= 60) {
            $("header").addClass("fixed-header");
        } else {
            $("header").removeClass("fixed-header");
        }
    });


    // Featured Owl Carousel
    var $featuredProjectsCarousel = $('.featured-projects-slider .owl-carousel');
    if ($featuredProjectsCarousel.length) {
        $featuredProjectsCarousel.owlCarousel({
            center: true,
            loop: true,
            margin: 30,
            nav: false,
            dots: false,
            autoplay: true,
            autoplayTimeout: 5000,
            autoplayHoverPause: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
        $(window).on('resize', function () {
            clearTimeout(window._featuredProjectsResizeT);
            window._featuredProjectsResizeT = setTimeout(function () {
                if ($featuredProjectsCarousel.data('owl.carousel')) {
                    $featuredProjectsCarousel.trigger('refresh.owl.carousel');
                }
            }, 200);
        });
    }
    $('.featured-projects-carousel-wrap').on('mouseenter', function () {
        $(this).find('.owl-carousel').trigger('stop.owl.autoplay');
    }).on('mouseleave', function () {
        $(this).find('.owl-carousel').trigger('play.owl.autoplay');
    });
    // Gördüyümüz işlər – mobil/tablet sol/sağ ox (ana səhifə, haqqımızda)
    $('.featured-projects-nav-prev').on('click', function () {
        $(this).closest('.featured-projects-carousel-wrap').find('.owl-carousel').trigger('prev.owl.carousel', [350]);
    });
    $('.featured-projects-nav-next').on('click', function () {
        $(this).closest('.featured-projects-carousel-wrap').find('.owl-carousel').trigger('next.owl.carousel', [350]);
    });

    // Ana səhifə – Xidmətlər carousel: mobil/tablet (<992) 1 kart/sətir, ox+autoplay 1-1; desktop (≥992) 3 kart, 3-3
    // Qeyd: Owl-un next() 1 addım atır; desktop üçün carousel.to(relative ± step) istifadə olunur.
    var $servicesSlider = $('.services-slider');
    if ($servicesSlider.length) {
        function servicesIsDesktop() {
            return $(window).width() >= 992;
        }
        function servicesGoRelative(deltaPages) {
            var carousel = $servicesSlider.data('owl.carousel');
            if (!carousel) return;
            if (servicesIsDesktop()) {
                var step = 3 * deltaPages;
                var rel = carousel.relative(carousel.current());
                carousel.to(rel + step, 550);
            } else {
                $servicesSlider.trigger(deltaPages > 0 ? 'next.owl.carousel' : 'prev.owl.carousel', [400]);
            }
        }
        $servicesSlider.owlCarousel({
            loop: true,
            margin: 16,
            nav: false,
            dots: true,
            slideBy: 'page',
            autoplay: false,
            smartSpeed: 450,
            checkVisibility: false,
            responsive: {
                0: { items: 1, margin: 14 },
                992: { items: 3, margin: 24 }
            }
        });
        $('.services-nav-prev').on('click', function () {
            servicesGoRelative(-1);
        });
        $('.services-nav-next').on('click', function () {
            servicesGoRelative(1);
        });
        var servicesAutoplayTimer = null;
        function startServicesAutoplay() {
            stopServicesAutoplay();
            servicesAutoplayTimer = setInterval(function () {
                try {
                    servicesGoRelative(1);
                } catch (err) {
                    /* eslint no-console: off */
                    if (window.console && console.warn) console.warn('services autoplay', err);
                }
            }, 3000);
        }
        function stopServicesAutoplay() {
            if (servicesAutoplayTimer) {
                clearInterval(servicesAutoplayTimer);
                servicesAutoplayTimer = null;
            }
        }
        startServicesAutoplay();
        $('.services-carousel-shell').on('mouseenter', stopServicesAutoplay).on('mouseleave', startServicesAutoplay);
        $(window).on('resize', function () {
            clearTimeout(window._servicesResizeT);
            window._servicesResizeT = setTimeout(function () {
                if ($servicesSlider.data('owl.carousel')) {
                    stopServicesAutoplay();
                    startServicesAutoplay();
                }
            }, 250);
        });
    }

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

	// Rəy bildir modal – form göndərildikdə səhifə yenilənmir, modal bağlanır (backend əlavə edəndə burada göndərmə yazılır)
	$('#reviewForm').on('submit', function (e) {
		e.preventDefault();
		var modal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
		if (modal) modal.hide();
		// TODO: form məlumatlarını serverə göndərmək
	});

});

