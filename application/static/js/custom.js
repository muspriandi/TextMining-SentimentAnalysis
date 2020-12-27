// FRONTEND
$(document).ready(function() {
	// SET WAKTU GLOBAL UNTUK LIBRARY MOMENT.JS KE INDONESIA
	moment.locale('id');
	$('#myTable').DataTable();

	// if($(this).prop("value") == 'modalTweetAsli') {
	// 	$("#modalLihatTweetAsli").find("p[id='tweetAsli']").html(data['text']);
	// 	$("#modalLihatTweetAsli").find("p[id='tweetBersih']").html(data['clean_text']);
	// 	$('#modalLihatTweetAsli').modal('show');
	// }
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

$('#sample-positive, #sample-negative, #sample-netral').on("change paste keyup", function() {
	const value = parseInt($(this).val());
	const max = parseInt($(this).attr('max'));

	if(value > 0 && value <= max) {
		$('#sample-positive, #sample-negative, #sample-netral').val(value);
		$('#total_sample').html(value * 3);
	}
	else {
		$('#sample-positive, #sample-negative, #sample-netral').val(max);
		$('#total_sample').html(max * 3);
	}
});

function cariRasio(kode) {
	var jumlah_data = $('#jumlah_dataWithLabel').html();
	var rasio_hasil_testing = 0;
	var rasio_hasil_training = 0;

	if(kode == '2:8') {		// 2:8
		rasio_hasil_testing = Math.floor(jumlah_data * 0.2);
		rasio_hasil_training = Math.ceil(jumlah_data * 0.8);
		$('#rasio-satu-hasil').html('<i class="fa fa-arrow-right mr-3"></i>'+ rasio_hasil_testing +' Data Tes & '+ rasio_hasil_training +' Data Latih');
		$('#rasio-dua-hasil').empty();
	}
	else if(kode == '3:7') {	// 3:7
		rasio_hasil_testing = Math.floor(jumlah_data * 0.3);
		rasio_hasil_training = Math.ceil(jumlah_data * 0.7);
		$('#rasio-satu-hasil').empty();
		$('#rasio-dua-hasil').html('<i class="fa fa-arrow-right mr-3"></i>'+ rasio_hasil_testing +' Data Tes & '+ rasio_hasil_training +' Data Latih');
	}
}