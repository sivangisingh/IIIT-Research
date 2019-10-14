jQuery(document).ready(function() {
    // for hover dropdown menu
    
    /* slick slider call */
    //Check to see if the window is top if not then display button
    jQuery(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });
    //Click event to scroll to top
    $('.scrollToTop').click(function() {
        $('html, body').animate({
            scrollTop: 0
        }, 800);
        return false;
    });
    $(".search_icon").click(function() {
        $('.search_bar').fadeOut();
        // $("i", this).toggleClass("fa-search fa-close");
    });
    // $(document).on('click', '.fa-close', function() {
    //     $('.search_bar').fadeIn();
    // });
});



jQuery(window).load(function() { // makes sure the whole site is loaded
    $('#status').fadeOut(); // will first fade out the loading animation
    $('#preloader').delay(100).fadeOut('slow'); // will fade out the white DIV that covers the website.
    $('body').delay(100).css({
        'overflow': 'visible'
    });
})