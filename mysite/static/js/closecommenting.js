
$(document).ready(function() {
    $('.collapse').toggle(function(e) {
        e.preventDefault();
        $('.comment-block', $(this).parents()[1]).css('display', 'block');
        $('#add-comment', $(this).parents()[1]).css('display', 'block');
    }, function(e) {
        e.preventDefault();
        $('.comment-block', $(this).parents()[1]).css('display', 'none');
        $('#add-comment', $(this).parents()[1]).css('display', 'none');
    });
});