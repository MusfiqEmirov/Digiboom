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
    $('.featured-projects-slider .owl-carousel').owlCarousel({
        center: true,
        loop: true,
        margin: 30,
        nav: false,
        dots: false,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: false,
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
            clearInterval(testimonialAutoplayTimer);
        }
        startAutoplay();
        $('.testimonial-slider-wrapper').on('mouseenter', stopAutoplay).on('mouseleave', startAutoplay);
    }


    // Count
    $('.count').each(function () {
		$(this).prop('Counter', 0).animate({
			Counter: $(this).text()
		}, {
			duration: 1000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});


    // ScrollToTop
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    const btn = document.getElementById("scrollToTopBtn");
    btn.addEventListener("click", scrollToTop);

    window.onscroll = function () {
        const btn = document.getElementById("scrollToTopBtn");
        if (document.documentElement.scrollTop > 100 || document.body.scrollTop > 100) {
            btn.style.display = "flex";
        } else {
            btn.style.display = "none";
        }
    };


    // Aos
	AOS.init({
		once: true,
	});

	// Bomb: səhifə yüklənəndə 3-2-1 sayım, sonra partlama (klik yoxdur)
	(function () {
		var countdownEl = document.querySelector('.bomb-countdown');
		var numEl = countdownEl ? countdownEl.querySelector('.bomb-num') : null;
		var explosionEl = document.querySelector('.bomb-explosion');
		var particlesEl = document.querySelector('.bomb-particles');
		if (!countdownEl || !numEl || !explosionEl || !particlesEl) return;

		var countdownMs = 520;

		function createParticles() {
			particlesEl.innerHTML = '';
			for (var i = 0; i < 12; i++) {
				var dot = document.createElement('span');
				dot.className = 'bomb-dot';
				particlesEl.appendChild(dot);
			}
		}

		function showNum(n, next) {
			numEl.textContent = n;
			numEl.style.animation = 'none';
			numEl.offsetHeight;
			numEl.style.animation = 'bomb-pop 0.45s ease-out';
			if (n > 1) {
				setTimeout(next, countdownMs);
			} else {
				setTimeout(fireExplosion, countdownMs);
			}
		}

		function fireExplosion() {
			countdownEl.classList.remove('is-active');
			countdownEl.setAttribute('aria-hidden', 'true');
			createParticles();
			explosionEl.classList.add('is-exploding');
			particlesEl.classList.add('is-exploding');
			setTimeout(function () {
				explosionEl.classList.remove('is-exploding');
				particlesEl.classList.remove('is-exploding');
			}, 680);
		}

		function startBomb() {
			countdownEl.classList.add('is-active');
			countdownEl.setAttribute('aria-hidden', 'false');
			showNum(3, function () {
				showNum(2, function () {
					showNum(1);
				});
			});
		}

		setTimeout(startBomb, 600);
	})();

	// Rəy bildir modal – form göndərildikdə səhifə yenilənmir, modal bağlanır (backend əlavə edəndə burada göndərmə yazılır)
	$('#reviewForm').on('submit', function (e) {
		e.preventDefault();
		var modal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
		if (modal) modal.hide();
		// TODO: form məlumatlarını serverə göndərmək
	});

});

