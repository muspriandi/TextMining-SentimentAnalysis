// FRONTEND
$(document).ready(function() {
	$('#myTable').DataTable();
	$('#myTable2').DataTable();
	$('#myTable3').DataTable();
	$('#myTable4').DataTable();
});

$('#menu-action').click(function() {
	$('.sidebar').toggleClass('active');
	$('.main').toggleClass('active');
	$(this).toggleClass('active');
	
	if ($('.sidebar').hasClass('active')) {
		$(this).find('i').addClass('fa-close');
		$(this).find('i').removeClass('fa-bars');
	} else {
		$(this).find('i').addClass('fa-bars');
		$(this).find('i').removeClass('fa-close');
		$('ul .collapse').collapse('hide');
	}
});

$('#menu-action').hover(function() {
	$('.sidebar').toggleClass('hovered');
});

$("a[data-toggle='collapse']").click(function() {
	if (!$('.sidebar').hasClass('active')) {
		$('#menu-action').click();
	}
});