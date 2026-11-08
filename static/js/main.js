(function ($) {
    "use strict";

    if ("scrollRestoration" in history) {
        history.scrollRestoration = "manual";
    }

    var isHomePage = document.body.classList.contains("page-home");

    function scrollPageToTop() {
        window.scrollTo(0, 0);
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
    }

    function lockHomePageToHero() {
        if (!isHomePage) {
            return;
        }
        scrollPageToTop();
    }

    function scheduleHomeScrollLock() {
        if (!isHomePage) {
            return;
        }
        lockHomePageToHero();
        requestAnimationFrame(function () {
            lockHomePageToHero();
            requestAnimationFrame(lockHomePageToHero);
        });
        [0, 50, 150, 300, 500, 800, 1200, 1800].forEach(function (delay) {
            window.setTimeout(lockHomePageToHero, delay);
        });
    }

    function releaseHomeScrollLock() {
        if (!isHomePage) {
            return;
        }
        document.documentElement.classList.remove("home-scroll-lock");
        document.body.style.position = "";
        document.body.style.width = "";
        document.body.style.left = "";
        document.body.style.right = "";
        lockHomePageToHero();
    }

    function resetHeroCarousel() {
        var $headerCarousel = $(".header-carousel");
        if (!$headerCarousel.length) {
            return;
        }
        var carousel = $headerCarousel.data("owl.carousel");
        if (!carousel) {
            return;
        }
        $headerCarousel.trigger("to.owl.carousel", [0, 0, true]);
    }

    if (isHomePage) {
        document.documentElement.classList.add("home-scroll-lock");
        lockHomePageToHero();
    } else {
        scrollPageToTop();
        if (typeof WOW !== "undefined") {
            new WOW().init();
        }
    }

    // Mobile drawer
    var mobileNavDrawer = document.getElementById("mobileNavDrawer");
    if (mobileNavDrawer) {
        mobileNavDrawer.querySelectorAll(".mobile-nav-dropdown").forEach(function (item) {
            item.classList.add("is-open");
            var toggle = item.querySelector(".dropdown-toggle");
            if (!toggle) {
                return;
            }
            toggle.setAttribute("aria-expanded", "true");
            toggle.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                item.classList.toggle("is-open");
                toggle.setAttribute("aria-expanded", item.classList.contains("is-open") ? "true" : "false");
            });
        });

        mobileNavDrawer.querySelectorAll("a.dropdown-item, a.nav-link:not(.dropdown-toggle)").forEach(function (link) {
            link.addEventListener("click", function () {
                var instance = bootstrap.Offcanvas.getInstance(mobileNavDrawer);
                if (instance) {
                    instance.hide();
                }
            });
        });
    }

    function syncNavbarHeight() {
        var nav = document.querySelector(".site-navbar");
        if (!nav) {
            return;
        }
        document.documentElement.style.setProperty("--site-navbar-height", nav.offsetHeight + "px");
    }

    syncNavbarHeight();
    $(window).on("resize load", syncNavbarHeight);

    function updateFixedNavbar() {
        var $nav = $(".site-navbar");
        if ($(window).scrollTop() > 20) {
            $nav.addClass("shadow-sm");
        } else {
            $nav.removeClass("shadow-sm");
        }
    }

    $(window).on("scroll", updateFixedNavbar);
    updateFixedNavbar();

    $("#navbarCollapse .dropdown-toggle").on("click", function (e) {
        e.preventDefault();
    });

    $("[data-toggle=\"counter-up\"]").counterUp({
        delay: 10,
        time: 2000,
    });

    $(".date").datetimepicker({
        format: "L",
    });
    $(".time").datetimepicker({
        format: "LT",
    });

    var $headerCarousel = $(".header-carousel");
    var heroSlideCount = $headerCarousel.find(".owl-carousel-item").length;
    var heroHasMultiple = heroSlideCount > 1;

    if ($headerCarousel.length) {
        $headerCarousel.owlCarousel({
            autoplay: heroHasMultiple,
            autoplayTimeout: 5000,
            autoplaySpeed: 800,
            smartSpeed: 800,
            loop: false,
            rewind: heroHasMultiple,
            nav: false,
            dots: false,
            items: 1,
            mouseDrag: heroHasMultiple,
            touchDrag: heroHasMultiple,
        });

        $headerCarousel.on("initialized.owl.carousel", function () {
            resetHeroCarousel();
            if (isHomePage) {
                scheduleHomeScrollLock();
            }
        });
    }

    $(window).on("load", function () {
        syncNavbarHeight();
        if (isHomePage) {
            scheduleHomeScrollLock();
            window.setTimeout(releaseHomeScrollLock, 200);
            window.setTimeout(lockHomePageToHero, 400);
        } else {
            scrollPageToTop();
        }
        if ($headerCarousel.length) {
            resetHeroCarousel();
            if (isHomePage) {
                scheduleHomeScrollLock();
            }
        }
    });

    window.addEventListener("pageshow", function () {
        if (isHomePage) {
            document.documentElement.classList.add("home-scroll-lock");
            scheduleHomeScrollLock();
            window.setTimeout(releaseHomeScrollLock, 200);
        } else {
            scrollPageToTop();
        }
        resetHeroCarousel();
    });

    $(function () {
        if (isHomePage) {
            lockHomePageToHero();
        }
    });

    var $testimonialCarousel = $(".testimonial-carousel");
    if ($testimonialCarousel.length) {
        $testimonialCarousel.owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            loop: true,
            nav: false,
            dots: true,
            items: 1,
            dotsData: true,
        });
    }

    var $eventsCarousel = $(".events-carousel");
    if ($eventsCarousel.length) {
        var eventsBreakpoint = 992;
        function eventsUseAutoplay() {
            return $(window).width() < eventsBreakpoint;
        }
        $eventsCarousel.owlCarousel({
            loop: true,
            margin: 24,
            nav: false,
            dots: true,
            autoplay: eventsUseAutoplay(),
            autoplayTimeout: 4500,
            autoplayHoverPause: true,
            smartSpeed: 650,
            responsive: {
                0: {
                    items: 1,
                    dots: true,
                },
                992: {
                    items: 3,
                    dots: false,
                },
            },
        });
        $(window).on("resize.eventsCarousel orientationchange.eventsCarousel", function () {
            if (eventsUseAutoplay()) {
                $eventsCarousel.trigger("play.owl.autoplay", [4500]);
            } else {
                $eventsCarousel.trigger("stop.owl.autoplay");
            }
        });
    }
})(jQuery);
