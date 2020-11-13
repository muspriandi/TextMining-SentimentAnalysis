// FRONTEND
$(document).ready(function() {
	$('#myTable').DataTable();
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
	}
});

$('#menu-action').hover(function() {
    $('.sidebar').toggleClass('hovered');
});

// AJAX - GET AND READ DATA SCRAPING
$('#crawling_data').click(function() {
	
	var content =	"";
	
	$.ajax({
		url         : "/crawling",
		data		: $('form').serialize(),
		type        : "POST",
		dataType	: "json",
		beforeSend: function() {
			content +=	`
							<div class="bs-callout bs-callout-primary mt-0">
								<h4>Data Crawling</h4>
								<p class="text-muted">Crawling Data dengan kata kunci <strong>`+ $('#kata_kunci').val() +`</strong>, dari tanggal <strong>`+ $('#tanggal_awal').val() +`</strong> s/d <strong>`+ $('#tanggal_akhir').val() +`</strong>.</p>
							</div>
							
							<div class="loaderDiv my-5 m-auto"></div>
						`;
						
			$('#content_crawling').html(content);
			$(".loaderDiv").show();
		},
		success     : function(response) {
			content +=	`
							<div class="table-responsive-sm">
								<table class="table table-bordered table-striped text-center" id="myTable">
									<thead>
										<tr>
											<th>No.</th>
											<th>ID</th>
											<th>Teks</th>
											<th>Pengguna</th>
											<th>Dibuat pada</th>
										</tr>
									</thead>
									<tbody>
						`;
						
			$.each(response.data_crawling, function(index, data) {
				content +=	`
										<tr>
											<td>`+ ++index +`</td>
											<td>`+ data.id +`</td>
											<td class="text-left">`+ data.full_text +`</td>
											<td>`+ data.user.screen_name +`</td>
											<td>`+ data.created_at +`</td>
											
										</tr>
							`;
			});
			
			var total_dataDidapat = response.data_crawling.length;
			var data_tes =  parseInt(total_dataDidapat / 4);
			var data_latih = parseInt(total_dataDidapat - data_tes);
			
			content +=	`			</tbody>
								</table>
							</div>
							<br />
							<div class="col-md-6 offset-md-3 col-sm-12 text-center mb-3">
								<label class="border border-info rounded p-2 mb-3 w-75"> <strong>`+ total_dataDidapat +`</strong> Data didapat</label>
								<form action="/crawling" method="POST">
									<div class="row mb-3">
										<div class="col">
											<label>Data Tes</label>
											<input type="number" id="data_tes" name="data_tes" min="0" value="`+ data_tes +`" class="form-control">
										</div>
										<div class="col">
											<label>Data Latih</label>
											<input type="number" id="data_latih" name="data_latih" min="0" value="`+ data_latih +`" class="form-control">
										</div>
									</div>
									
									<input type="hidden" name="aksi" value="save_crawling" required readonly />
									<button type="submit" class="btn btn-primary w-75"><i class="fa fa-save"></i> Simpan Data</button>
								</form>
							</div>
						`;
			
			$('#content_crawling').html(content);
			$(".loaderDiv").hide();
			$('#myTable').DataTable();
			
			$('#modalCrawling').modal('toggle');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			
			$('#data_tes').on("keyup keypress change", function () {
				if($(this).val() > total_dataDidapat) {
					$(this).val(total_dataDidapat);
				}
				$('#data_latih').val(total_dataDidapat - $(this).val());
			});
			
			$('#data_latih').on("keyup keypress change", function () {
				if($(this).val() > total_dataDidapat) {
					$(this).val(total_dataDidapat);
				}
				$('#data_tes').val(total_dataDidapat - $(this).val());
			});
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});

// AJAX - PROCESS AND READ DATA PREROCESSING
$('#preprocessing_data').click(function() {
	
	$.ajax({
		url         : "/preprocessing",
		data		: $('form').serialize(),
		type        : "POST",
		dataType	: "json",
		beforeSend: function() {
			var content =	"";
			
			label_tampil = "";
			label_tampil += ($('#data-tes').is(':checked')) ? "<strong>Data Tes</strong>":"";
			label_tampil += ($('#data-tes').is(':checked') && $('#data-latih').is(':checked')) ? " dan ":"";
			label_tampil += ($('#data-latih').is(':checked')) ? "<strong>Data Latih</strong>":"";
			
			content +=	`
							<div class="bs-callout bs-callout-primary mt-0">
								<h4>Data Preprocessing</h4>
								<p class="text-muted">Preprocessing `+ label_tampil +`.</p>
							</div>
							
							<div class="loaderDiv my-5 m-auto"></div>
						`;
						
			$('#content_preprocessing').html(content);
			$(".loaderDiv").show();
		},
		success     : function() {
			$(".loaderDiv").hide();
			
			$('#modalCrawling').modal('toggle');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			
			//location.href = "/preprocessing";
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});