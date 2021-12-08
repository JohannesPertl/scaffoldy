(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function (event) {

        // Validate next button
        if ($(this).hasClass('next-btn')) {
            const section = $(this).closest('section');
            let isInvalid = false;
            $('input', section).each(function () {
                let valid = $(this)[0].reportValidity();
                if (!valid) {
                    isInvalid = true;
                    return false;
                }
            })
            if (isInvalid) {
                return false;
            }
        }
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            let target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top + 20
                }, 1000, "easeInOutExpo");
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function () {
        $('.navbar-collapse').collapse('hide');
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
        target: '#mainNav',
        offset: 250
    });

})(jQuery); // End of use strict
