var $clickable = $('#clickable');
$clickable.on('click', function(e) {
	var $pointer;

	$clickable.append('<div class="pointer" />');
  $pointer = $clickable.find('.pointer');

  $pointer.css({
  	top: event.pageY - $clickable.offset().top,
    left: event.pageX - $clickable.offset().left
  })

	e.preventDefault();
})