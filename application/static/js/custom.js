// FRONTEND
$(document).ready(function() {
	// TAMPIL TABEL DATA SLANGWORD [START]
	var table_dataSlangword = $('#table_dataSlangword').DataTable({
  		"deferRender": true,
		"ajax": "/list_slangword",
		"columns": [
			{
				data: null, 
				"render": function (data, type, full, meta) {
					return  meta.row + 1;
				}
			},
			{ data: 'slangword' },
			{ data: 'kata_asli' },
			{ data: null },
		],
		"columnDefs": [{
            "targets": 3,
			"data": null,
			"defaultContent": `
				<button type="button" value="update" class="btn btn-warning mb-1"><i class="fa fa-pencil text-white"></i></button>
				<button type="button" value="delete" class="btn btn-danger mb-1"><i class="fa fa-trash"></i></button>								
			`
		}],
	});
	// AKSI UPDATE DAN DELETE SLANGWORD DENGAN MODAL
	$('#table_dataSlangword tbody').on( 'click', 'button', function () {
		var data = table_dataSlangword.row($(this).parents('tr')).data();
		if($(this).prop("value") == 'update') {
			$("#slangwordEditModal").find("input[name='slangword']").val(data['slangword']);
			$("#slangwordEditModal").find("input[name='kata_asli']").val(data['kata_asli']);
			$("#slangwordEditModal").find("input[name='id']").val(data['id_slangword']);
			$('#slangwordEditModal').modal('show');
		}
		else if($(this).prop("value") == 'delete') {
			$("#slangwordDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
			$("#slangwordDeleteModal").find("input[name='id']").val(data['id_slangword']);
			$('#slangwordDeleteModal').modal('show');
		}
	});
	// TAMPIL TABEL DATA SLANGWORD [END]


	// TAMPIL DATA KATA POSITIF [START]
	var table_dataPositiveWord = $('#table_dataPositiveWord').DataTable({
  		"deferRender": true,
		"ajax": "/list_positive_word",
		"columns": [
			{
				data: null, 
				"render": function (data, type, full, meta) {
					return  meta.row + 1;
				}
			},
			{ data: 'positive_word' },
			{ data: 'positive_weight' },
			{ data: null },
		],
		"columnDefs": [{
            "targets": 3,
			"data": null,
			"defaultContent": `
				<button type="button" value="update" class="btn btn-warning mb-1"><i class="fa fa-pencil text-white"></i></button>
				<button type="button" value="delete" class="btn btn-danger mb-1"><i class="fa fa-trash"></i></button>								
			`
		}],
	});
	// AKSI UPDATE DAN DELETE KATA POSITIF DENGAN MODAL
	$('#table_dataPositiveWord tbody').on( 'click', 'button', function () {
		var data = table_dataPositiveWord.row($(this).parents('tr')).data();
		if($(this).prop("value") == 'update') {
			$("#positive_wordEditModal").find("input[name='kata_positif']").val(data['positive_word']);
			$("#positive_wordEditModal").find("input[name='nilai_positif']").val(data['positive_weight']);
			$("#positive_wordEditModal").find("input[name='id']").val(data['id_positive']);
			$('#positive_wordEditModal').modal('show');
		}
		else if($(this).prop("value") == 'delete') {
			$("#positive_wordDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
			$("#positive_wordDeleteModal").find("input[name='id']").val(data['id_positive']);
			$('#positive_wordDeleteModal').modal('show');
		}
	});
	// TAMPIL DATA KATA POSITIF [END]


	// TAMPIL DATA KATA NEGATIF [START]
	var table_dataNegativeWord = $('#table_dataNegativeWord').DataTable({
  		"deferRender": true,
		"ajax": "/list_negative_word",
		"columns": [
			{
				data: null, 
				"render": function (data, type, full, meta) {
					return  meta.row + 1;
				}
			},
			{ data: 'negative_word' },
			{ data: 'negative_weight' },
			{ data: null },
		],
		"columnDefs": [{
            "targets": 3,
			"data": null,
			"defaultContent": `
				<button type="button" value="update" class="btn btn-warning mb-1"><i class="fa fa-pencil text-white"></i></button>
				<button type="button" value="delete" class="btn btn-danger mb-1"><i class="fa fa-trash"></i></button>								
			`
		}],
	});
	// AKSI UPDATE DAN DELETE KATA NEGATIF DENGAN MODAL
	$('#table_dataNegativeWord tbody').on( 'click', 'button', function () {
		var data = table_dataNegativeWord.row($(this).parents('tr')).data();
		if($(this).prop("value") == 'update') {
			$("#negative_wordEditModal").find("input[name='kata_negatif']").val(data['negative_word']);
			$("#negative_wordEditModal").find("input[name='nilai_negatif']").val(parseInt(data['negative_weight']) * (-1));
			$("#negative_wordEditModal").find("input[name='id']").val(data['id_negative']);
			$('#negative_wordEditModal').modal('show');
		}
		else if($(this).prop("value") == 'delete') {
			$("#negative_wordDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
			$("#negative_wordDeleteModal").find("input[name='id']").val(data['id_negative']);
			$('#negative_wordDeleteModal').modal('show');
		}
	});
	// TAMPIL DATA KATA NEGATIF [END]

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