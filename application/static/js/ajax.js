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
								<h4>Data <em>Crawling</em></h4>
								<p class="text-muted"><em>Crawling</em> Data dengan kata kunci <strong>`+ $('#kata_kunci').val() +`</strong>, dari tanggal <strong>`+ $('#tanggal_awal').val() +`</strong> s/d <strong>`+ $('#tanggal_akhir').val() +`</strong>.</p>
							</div>
							
							<div class="loaderDiv my-5 m-auto"></div>
						`;
						
			$('#content_crawling').html(content);
			$(".loaderDiv").show();
		},
		success     : function(response) {
			
			var total_dataDidapat = response.data_crawling.length;
			
			content +=	`
							<div class="col-md-6 offset-md-3 col-sm-12 text-center border border-success rounded shadow py-4">
								<label class="text-center d-inline-flex align-items-center mb-1">
									<h3 class="text-info mb-1">`+ total_dataDidapat +`</h3>
									<span class="ml-2 text-muted"> Data didapat</span>
								</label>
								<form action="/crawling" method="POST">									
									<input type="hidden" name="aksi" value="save_crawling" required readonly />
									<button type="submit" class="btn btn-primary w-75"><i class="fa fa-save"></i> Simpan Data</button>
								</form>
							</div>
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

			content += 	`
									</tbody>
								</table>
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
								<h4>Data <em>Preprocessing</em></h4>
								<p class="text-muted"><em>Preprocessing</em> <strong>`+ $('#jumlah_dataCrawling').html() +`</strong> data <em>crawling</em></p>
							</div>
							
							<div class="loaderDiv my-5 m-auto"></div>
						`;
						
			$('#content_preprocessing').html(content);
			$(".loaderDiv").show();
		},
		success     : function(response) {
			content +=	`
							<div class="col-md-6 offset-md-3 col-sm-12 text-center">
								<form action="/preprocessing" method="POST">
									<input type="hidden" name="aksi" value="save_preprocessing" required readonly />
									<button type="submit" class="btn btn-primary w-75"><i class="fa fa-save"></i> Simpan Data</button>
								</form>
							</div>
							<div class="table-responsive-sm">
								<table class="table table-bordered table-striped text-center" id="myTable">
									<thead>
										<tr>
											<th>No.</th>
											<th>Teks Bersih</th>
											<th>Pilihan</th>
										</tr>
									</thead>
									<tbody>
						`;
						
			$.each(response.last_data, function(index) {
				content +=	`
										<tr>
											<td>`+ ++index +`</td>
											<td class="text-left">`+ response.last_data[--index] +`</td>
											<td class="text-left"><button class="btn btn-outline-info" data-toggle="modal" data-target="#modalDetailPreprocessing`+ index +`"><i class="fa fa-search-plus"></i> Detail</button></td>
										</tr>
										
										<div class="modal fade" id="modalDetailPreprocessing`+ index +`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
											<div class="modal-dialog modal-lg">
												<div class="modal-content">
													<div class="modal-header">
														<h5 class="modal-title" id="exampleModalLabel">Detail <em>Preprocessing</em> Tweet</h5>
														<button type="button" class="close" data-dismiss="modal" aria-label="Close">
														<span aria-hidden="true">&times;</span>
														</button>
													</div>
													<div class="modal-body px-5">
														<div class="row">
															<div class="col-md-12 d-flex justify-content-start align-items-center">
																<div class="timeline">
																	<p><span>1. Tweet Awal</span><br />`+ response.first_data[index] +`</p>
																	<p><span>2. Case Folding</span><br />`+ response.case_folding[index]+`</p>
																	<p><span>3. Menghapus URL, Mention, Hastag, Angka, Unicode, Tanda Baca, Spasi (<em>Cleansing</em>)</span><br />`+ response.remove_non_character[index]+`</p>
																	<p><span>4. Menghapus <em>Stop Word</em></span><br />`+ response.remove_stop_word[index]+`</p>
																	<p><span>5. Mengubah kata ke bentuk kata dasar (<em>Stemming</em>)</span><br />`+ response.change_stemming[index]+`</p>
																	<p><span>6. Mengubah kata ke bentuk kata dasar (<em>Slang Word</em>)</span><br />`+ response.change_slang[index]+`</p>
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

// AJAX - LABELING DATA
$("select[name='label_data']").change(function() {
	id = $(this).attr('id');
	value = $(this).find(":selected").text();
	type = $(this).attr('tipe');
	
	$.ajax({
		url         : "/labeling",
		data		: {'id': id, 'value': value, 'type': type},
		type        : "POST",
		dataType	: "json",
		success     : function(response) {
			console.log(response);
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});

// AJAX - MODEELING DATA
$('#modeling_data').click(function() {
	
	var content =	"";
	
	$.ajax({
		url         : "/modeling",
		type        : "POST",
		beforeSend: function() {
			content +=	`	
							<br />
							<div class="modal-backdrop" style="background-color: rgba(0,0,0,0.3);"></div>
							<div class="loaderDiv my-5 m-auto"></div>
						`;
						
			$('#content_modeling').html(content);
			$(".loaderDiv").show();
		},
		success     : function(response) {
			content = 	`
							Model: <strong>`+ response.model_name +`</strong><br />
							Total Sentimen:  <strong>`+ response.sentiment_count +`</strong><br />
							&nbsp; &nbsp; Sentimen Positif:  <strong>`+ response.sentiment_positive +`</strong><br />
							&nbsp; &nbsp; Sentimen Negatif:  <strong>`+ response.sentiment_negative +`</strong><br />
							&nbsp; &nbsp; Sentimen Netral:  <strong>`+ parseInt(response.sentiment_count - response.sentiment_positive - response.sentiment_negative) +`</strong><br />
						
							`;
			
			$('#content_modeling').html(content);
			
			$(".loaderDiv").hide();
			
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});

// AJAX - PENGUJIAN DATA
$('#uji_data').click(function() {
	
	var content =	"";
	
	$.ajax({
		url         : "/evaluation",
		data		: $('form').serialize(),
		type        : "POST",
		dataType	: "json",
		beforeSend: function() {
			content +=	`	
							<br />
							<div class="modal-backdrop" style="background-color: rgba(0,0,0,0.3);"></div>
							<div class="loaderDiv my-5 m-auto"></div>
						`;
						
			$('#content_pengujian').html(content);
			$(".loaderDiv").show();
		},
		success     : function(response) {
			content +=	`
							<div class="table-responsive-sm">
								<table class="table table-bordered table-striped text-center" id="myTable">
									<thead>
										<tr>
											<th>No.</th>
											<th>Teks Bersih</th>
											<th>Sentimen (<em>Labeling</em>)</th>
											<th>Sentimen (Prediksi)</th>
										</tr>
									</thead>
									<tbody>
						`;
						
			$.each(response.teks_database, function(index) {
				content +=	`
										<tr>
											<td>`+ ++index +`</td>
											<td class="text-left">`+ response.teks_database[--index] +`</td>
											<td>`+ response.sentimen_database[index].toUpperCase() +`</td>
											<td><strong>`+ response.sentimen_prediksi[index].toUpperCase() +`</strong></td>
										</tr>
							`;
			});
			
			content +=	`			</tbody>
								</table>
							</div>
							<br />
							Akurasi: <strong>`+ response.akurasi +`</strong>
						`;
			
			$('#content_pengujian').html(content);
			
			$(".loaderDiv").hide();
			$('#myTable').DataTable();
			
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});


// FUNGSI MENTRIGGER MODAL UNTUK MELIHAT TWEET ASLI(HASIL CRAWLING) SECARA SATUAN -- DATATABLES
$('.modalLihatTweetAsli').click(function() {
	id = $(this).attr('key');

	$.ajax({
		url         : "/getTweetById",
		data		: {'id': id},
		type        : "POST",
		dataType	: "json",
		success     : function(response) {
			$('#tweetAsli').text(response.text);
			$('#tweetBersih').text(response.clean_text);
			$('#modalLihatTweetAsli').modal('show');
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});

// FUNGSI MENTRIGGER MODAL UNTUK MELIHAT TWEET ASLI(HASIL CRAWLING) SECARA SATUAN -- MODAL KE-2
$('.modalLihatTweetAsli2').click(function() {
	id = $(this).attr('key');
	type = $(this).attr('tipe');

	$.ajax({
		url         : "/getTweetById",
		data		: {'id': id, 'type': type},
		type        : "POST",
		dataType	: "json",
		success     : function(response) {
			$('#tweetBersih').text(response.clean_text);
			$('#tweetAsli').text(response.text);
			$('#modalLihatTweetAsli').modal('show');
			$('#modalLihatTweetAsli').css('background-color', 'rgba(0,0,0,0.3)');
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});

// FUNGSI MENTRIGGER BACKDROP MODAL KE-2
$('#modalLihatTweetAsli2').on('hidden.bs.modal', function () {
	$('body').addClass('modal-open');
});

// AUTO REFRESH PAGE SETELAH PROSES PELABELAN AJAX
$('#modalLabeling').on('hidden.bs.modal', function () {
	window.location.href = "/labeling";
});