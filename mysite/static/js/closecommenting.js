
$(document).ready(function() {
    // Hide metadata at loading
    var elt = $("#metadata dl:first");
    elt.hide();
    $("#metadata p:first").click(function () {
        elt.slideToggle('fast');
    });
    
    // If add-comment form, then comment-block is visible
    if ($('#add-comment', $(this).parents()[1]).css('display') == 'block') {
        $('.comment-block', $(this).parents()[1]).css('display', 'block');
        $('.collapse-block').text('⬆');
    }
    // Show/Hide a comment-block
    $('.collapse-block').click(function(e) {
        e.preventDefault();
        if ($('.comment-block', $(this).parents()[1]).css('display') == 'block') {
            $('.comment-block', $(this).parents()[1]).css('display', 'none');
            $(this).text('⬇');
        } else {
            $('.comment-block', $(this).parents()[1]).css('display', 'block');
            $(this).text('⬆');
        }
    });

    // Truncate single comment
    $('.collapse-one').toggle(function(e) {
        e.preventDefault();
        $('.comment-text', $(this).parents()[1]).css('height', '0.8em');
        $(this).text('⬇');
    }, function(e) {
        e.preventDefault();
        $('.comment-text', $(this).parents()[1]).css('height', 'auto');
        $(this).text('⬆');
    });
    
    // Truncate all single comments
    $('.preview-all').toggle(function(e) {
        e.preventDefault();
        $('.comment-text', $(this).parents()[1]).css('height', '0.8em');
        $(this).text('collapse all');
    }, function(e) {
        e.preventDefault();
        $('.comment-text', $(this).parents()[1]).css('height', 'auto');
        $(this).text('uncollapse all');
    });
        
});