$(function() {
    $('.menu_link').on('click', function() {
        event.preventDefault();
        var $this_item = $(this);
        var target_id = $(this).attr('href');
        $('.menu_target, .menu_item').removeClass('active');
        console.log($('[href="'+target_id+'"]'));
        $('[href="'+target_id+'"]').parent('.menu_item').addClass('active');
        $(target_id).addClass('active');
    });

    $('[data-action="js_toggle"]').on('click', function() {
        $(this).parent('.ui_toggle_container').toggleClass('ui_toggle_show');
    });
});