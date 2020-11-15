// FRONTEND
$(document).ready(function() {
	$('#myTable').DataTable();
	$('#myTable2').DataTable();
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
	
	var content =	"";
	
	$.ajax({
		url         : "/preprocessing",
		data		: $('form').serialize(),
		type        : "POST",
		dataType	: "json",
		beforeSend: function() {
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
		success     : function(response) {
			
			content +=	`
							<div class="table-responsive-sm">
								<table class="table table-bordered table-striped text-center" id="myTable">
									<thead>
										<tr>
											<th>No.</th>
											<th>ID</th>
											<th>Teks Bersih</th>
											<th>Pilihan</th>
										</tr>
									</thead>
									<tbody>
						`;
						
			$.each(response.result_data, function(index, data) {
				content +=	`
										<tr>
											<td>`+ ++index +`</td>
											<td>`+ data.id +`</td>
											<td class="text-left">`+ data.text +`</td>
											<td class="text-left"><button class="btn btn-outline-info" data-toggle="modal" data-target="#modalDetailPreprocessing`+ data.id +`"><i class="fa fa-search-plus"></i> Detail</button></td>
										</tr>
										
										<div class="modal fade" id="modalDetailPreprocessing`+ data.id +`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
											<div class="modal-dialog modal-lg">
												<div class="modal-content">
													<div class="modal-header">
														<h5 class="modal-title" id="exampleModalLabel">Detail Preprocessing Tweet</h5>
														<button type="button" class="close" data-dismiss="modal" aria-label="Close">
														<span aria-hidden="true">&times;</span>
														</button>
													</div>
													<div class="modal-body px-5">
														<div class="row">
															<div class="col-md-12 d-flex justify-content-start align-items-center">
																<div class="timeline">
																	<p><span>1. Tweet Awal</span><br />`+ response.first_data[--index] +`</p>
																	<p><span>2. Case Folding</span><br />`+ response.case_folding[index]+`</p>
																	<p><span>3. Menghapus URL, Mention, Hastag, Angka, Unicode, Tanda Baca & Spasi</span><br />`+ response.remove_non_character[index]+`</p>
																	<p><span>4. Menghapus Stop Word</span><br />`+ response.remove_stop_word[index]+`</p>
																	<p><span>5. Mengubah kata ke bentuk kata dasar (Stemming)</span><br />`+ response.change_stemming[index]+`</p>
																	<p><span>6. Mengubah kata ke bentuk kata dasar (Slang Word)</span><br />`+ response.change_slang[index]+`</p>
																</div>
															</div>
														</div>
													</div>
												</div>
											</div>
										</div>
							`;
			});
			
			content +=	`			</tbody>
								</table>
							</div>
							<br />
							<div class="col-md-6 offset-md-3 col-sm-12 text-center mb-3">
								<form action="/preprocessing" method="POST">
									<input type="hidden" name="aksi" value="save_preprocessing" required readonly />
									<button type="submit" class="btn btn-primary w-75"><i class="fa fa-save"></i> Simpan Data</button>
								</form>
							</div>
						`;
			
			$('#content_preprocessing').html(content);
			
			$(".loaderDiv").hide();
			$('#myTable').DataTable();
			
			$('#modalPreprocessing').modal('toggle');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});