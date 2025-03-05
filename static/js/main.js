(function($) {
    "use strict";
    
    // Preloader
    $(window).on('load', function() {
        if ($('#preloader').length) {
            $('#preloader').delay(100).fadeOut('slow', function() {
                $(this).remove();
            });
        }
    });
    
    // Back to top button
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('#backToTop').addClass('active');
        } else {
            $('#backToTop').removeClass('active');
        }
    });
    
    $('#backToTop').on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: 0
        }, 800);
        return false;
    });
    
    // Sticky Header
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.navbar').addClass('navbar-scrolled shadow-sm');
        } else {
            $('.navbar').removeClass('navbar-scrolled shadow-sm');
        }
    });
    
    // Mobile Navigation
    $('.navbar-toggler').on('click', function() {
        if (!$('#navbarMain').hasClass('show')) {
            $('body').addClass('mobile-nav-active');
        } else {
            $('body').removeClass('mobile-nav-active');
        }
    });
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });
    
    // Animate on scroll
    function animateOnScroll() {
        $('.animate-on-scroll').each(function() {
            var elementPos = $(this).offset().top;
            var topOfWindow = $(window).scrollTop();
            var windowHeight = $(window).height();
            var animationDelay = $(this).data('delay') || 0;
            
            if (elementPos < topOfWindow + windowHeight - 100) {
                setTimeout(function() {
                    $(this).addClass('animated');
                }.bind(this), animationDelay);
            }
        });
    }
    
    $(window).on('scroll', animateOnScroll);
    animateOnScroll();
    
    // Filter items on button click
    $('.filter-button-group').on('click', 'button', function() {
        var filterValue = $(this).attr('data-filter');
        $('.filter-container').isotope({ filter: filterValue });
        $('.filter-button-group button').removeClass('active');
        $(this).addClass('active');
    });
    
    // Newsletter form validation
    $('#newsletter-form').validate({
        rules: {
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            email: {
                required: "Please enter your email address",
                email: "Please enter a valid email address"
            }
        },
        errorElement: 'div',
        errorPlacement: function(error, element) {
            error.addClass('invalid-feedback');
            element.closest('.form-group').append(error);
        },
        highlight: function(element, errorClass, validClass) {
            $(element).addClass('is-invalid');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).removeClass('is-invalid');
        },
        submitHandler: function(form) {
            var $form = $(form);
            var $submitBtn = $form.find('button[type="submit"]');
            var submitBtnText = $submitBtn.html();
            
            $.ajax({
                type: $form.attr('method'),
                url: $form.attr('action'),
                data: $form.serialize(),
                beforeSend: function() {
                    $submitBtn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Sending...');
                    $submitBtn.prop('disabled', true);
                },
                success: function(response) {
                    if (response.status === 'success') {
                        $('.newsletter-response').html('<div class="alert alert-success mt-3">' + response.message + '</div>');
                        $form[0].reset();
                    } else {
                        $('.newsletter-response').html('<div class="alert alert-danger mt-3">' + response.message + '</div>');
                    }
                    $submitBtn.html(submitBtnText);
                    $submitBtn.prop('disabled', false);
                },
                error: function() {
                    $('.newsletter-response').html('<div class="alert alert-danger mt-3">An error occurred. Please try again later.</div>');
                    $submitBtn.html(submitBtnText);
                    $submitBtn.prop('disabled', false);
                }
            });
            
            return false;
        }
    });
    
    // Counter animation
    $('.counter').each(function() {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 2000,
            easing: 'swing',
            step: function(now) {
                $(this).text(Math.ceil(now));
            }
        });
    });
    
    // Testimonial carousel
    $('.testimonial-carousel').owlCarousel({
        loop: true,
        margin: 30,
        nav: false,
        dots: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            }
        }
    });
    
    // Partners carousel
    $('.partners-carousel').owlCarousel({
        loop: true,
        margin: 30,
        nav: false,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 2
            },
            576: {
                items: 3
            },
            768: {
                items: 4
            },
            992: {
                items: 5
            }
        }
    });
    
    // Gallery lightbox
    $('.gallery-lightbox').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        },
        zoom: {
            enabled: true,
            duration: 300,
            easing: 'ease-in-out'
        }
    });
    
    // Video lightbox
    $('.video-lightbox').magnificPopup({
        type: 'iframe',
        iframe: {
            patterns: {
                youtube: {
                    index: 'youtube.com/',
                    id: 'v=',
                    src: 'https://www.youtube.com/embed/%id%?autoplay=1'
                },
                vimeo: {
                    index: 'vimeo.com/',
                    id: '/',
                    src: 'https://player.vimeo.com/video/%id%?autoplay=1'
                }
            }
        }
    });
    
    // AOS initialization
    AOS.init({
        duration: 1000,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });
    
})(jQuery);