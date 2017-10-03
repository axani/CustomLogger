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
});