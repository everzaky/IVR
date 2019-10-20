
var $clickable = $('.clickable');

var $pointer = $('.pointer');

$clickable.dblclick( function(e) {
   e.stopPropagation();
   $(this).append('<div class="pointer" />');
  var $pointerr = $(this).find('.pointer:last-child');
  $pointerr.css({
  	top: event.pageY- $(this).offset().top,
    left: event.pageX  - $(this).offset().left
  });
  $pointer = $('.pointer');
  $pointer.click(function(){
  $(this).remove();
    });
});

$pointer.click(function () {
   $(this).remove();
});

var $button = $('.button');
$button.click(function () {
   $.ajax({

   })
});


