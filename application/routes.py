from flask import render_template, request, redirect, url_for
from application import app
from application.controllers import Controllers

@app.route('/')
@app.route('/dashboard')
def index():
	return render_template('dashboard.html')

controller = Controllers()	# Menetapkan Instance dari Class Controllers

# Tampil Halaman(VIEW) & Simpan Data Slangword ================================================
@app.route('/slangword', methods=['GET','POST'])
def slangword():
	if request.method == 'GET':
		return render_template('slangword.html')	# Akses ke halaman/view slangword
	
	if request.method == 'POST':
		controller.add_dataSlangword()	# Memanggil fungsi 'add_dataSlangword()' menggunakan Instance 'controller'
	
	return redirect(url_for('slangword'))	# Memanggil fungsi slangword() dengan method GET# Tampil & Simpan Data Slangword

# Tampil Data ke dalam tabel Slangword
@app.route('/list_slangword', methods=['GET'])
def list_slangword():
	data_slangword = controller.select_dataSlangword()	# Memanggil fungsi 'select_dataSlangword()' menggunakan Instance 'controller'
	return { 'data': data_slangword }

# Ubah Data Slangword 
@app.route('/slangword/ubah', methods=['POST'])
def ubah_dataSlangword():
	controller.update_dataSlangword()	# Memanggil fungsi 'update_dataSlangword()' menggunakan Instance 'controller'
	return redirect(url_for('slangword'))

# Hapus Data Slangword
@app.route('/slangword/hapus', methods=['POST'])
def hapus_dataSlangword():
	controller.delete_dataSlangword()	# Memanggil fungsi 'delete_dataSlangword()' menggunakan Instance 'controller'
	return redirect(url_for('slangword'))

# Tampil Halaman(VIEW) & Simpan Data Stopword ================================================
@app.route('/stopword', methods=['GET','POST'])
def stopword():
	if request.method == 'GET':
		return render_template('stopword.html')	# Akses ke halaman/view stopword
	
	if request.method == 'POST':
		controller.add_dataStopword()	# Memanggil fungsi 'add_dataStopword()' menggunakan Instance 'controller'
	
	return redirect(url_for('stopword'))	# Memanggil fungsi stopword() dengan method GET# Tampil & Simpan Data Stopword

# Tampil Data ke dalam tabel Stopword
@app.route('/list_stopword', methods=['GET'])
def list_stopword():
	data_stopword = controller.select_dataStopword()	# Memanggil fungsi 'select_dataStopword()' menggunakan Instance 'controller'
	return { 'data': data_stopword }

# Ubah Data Stopword 
@app.route('/stopword/ubah', methods=['POST'])
def ubah_dataStopword():
	controller.update_dataStopword()	# Memanggil fungsi 'update_dataStopword()' menggunakan Instance 'controller'
	return redirect(url_for('stopword'))

# Hapus Data Stopword
@app.route('/stopword/hapus', methods=['POST'])
def hapus_dataStopword():
	controller.delete_dataStopword()	# Memanggil fungsi 'delete_dataStopword()' menggunakan Instance 'controller'
	return redirect(url_for('stopword'))

# Tampil Halaman(VIEW) & Simpan Data kata Positive ================================================
@app.route('/positive-word', methods=['GET','POST'])
def positive_word():
	if request.method == 'GET':
		return render_template('positive_word.html')	# Akses ke halaman/view positif_word
	
	if request.method == 'POST':
		controller.add_dataPositiveWord()	# Memanggil fungsi 'add_dataPositiveWord()' menggunakan Instance 'controller'
	
	return redirect(url_for('positive_word'))	# Memanggil fungsi positive_word() dengan method GET

# Tampil Data ke dalam tabel kata Positive
@app.route('/list_positive_word', methods=['GET'])
def list_positive_word():
	data_positive_word = controller.select_dataPositiveWord()	# Memanggil fungsi 'select_dataPositiveWord()' menggunakan Instance 'controller'
	return { 'data': data_positive_word }

# Ubah Data kata Positive
@app.route('/positive-word/ubah', methods=['POST'])
def ubah_positive_word():
	controller.update_dataPositiveWord()	# Memanggil fungsi 'update_dataPositiveWord()' menggunakan Instance 'controller'
	return redirect(url_for('positive_word'))

# Hapus Data kata Positive
@app.route('/positive-word/hapus', methods=['POST'])
def hapus_positive_word():
	controller.delete_dataPositiveWord()	# Memanggil fungsi 'delete_dataPositiveWord()' menggunakan Instance 'controller'
	return redirect(url_for('positive_word'))

# Tampil Halaman(VIEW) & Simpan Data kata Negative ================================================
@app.route('/negative-word', methods=['GET','POST'])
def negative_word():
	if request.method == 'GET':
		return render_template('negative_word.html')	# Akses ke halaman/view negative_word
	
	if request.method == 'POST':
		controller.add_dataNegativeWord()	# Memanggil fungsi 'add_dataNegativeWord()' menggunakan Instance 'controller'
	
	return redirect(url_for('negative_word'))	# Memanggil fungsi positive_word() dengan method GET

# Tampil Data ke dalam tabel kata Negative
@app.route('/list_negative_word', methods=['GET'])
def list_negative_word():
	data_negative_word = controller.select_dataNegativeWord()	# Memanggil fungsi 'select_dataNegativeWord()' menggunakan Instance 'controller'
	return { 'data': data_negative_word }

# Ubah Data kata Negative
@app.route('/negative-word/ubah', methods=['POST'])
def ubah_negative_word():
	controller.update_dataNegativeWord()	# Memanggil fungsi 'update_dataNegativeWord()' menggunakan Instance 'controller'
	return redirect(url_for('negative_word'))

# Hapus Data kata Negative
@app.route('/negative-word/hapus', methods=['POST'])
def hapus_negative_word():
	controller.delete_dataNegativeWord()	# Memanggil fungsi 'delete_dataNegativeWord()' menggunakan Instance 'controller'
	return redirect(url_for('negative_word'))

# Tampil Halaman(VIEW) & Simpan Data Crawling ================================================
@app.route('/crawling', methods=['GET','POST'])
def crawling():
	if request.method == 'GET':
		return render_template('crawling.html')
	
	if request.method == 'POST':
		response = controller.add_dataCrawling()	# Memanggil fungsi 'add_dataCrawling()' menggunakan Instance 'controller'
		if response != None:
			return response
		
		return redirect(url_for('crawling'))	# Memanggil fungsi 'crawling()' dengan method GET

# Tampil Data ke dalam tabel Crawling
@app.route('/list_data_crawling', methods=['GET'])
def list_data_crawling():
	data_crawling = controller.select_dataCrawling()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller'
	return { 'data': data_crawling }

# Tampil Halaman(VIEW) & Simpan Data Preprocessing ================================================
@app.route('/preprocessing', methods=['GET','POST'])
def preprocessing():
	if request.method == 'GET':
		count_data_crawling = controller.count_dataCrawling()	# Memanggil fungsi 'count_dataCrawling()' menggunakan Instance 'controller'
		return render_template('preprocessing.html', count_data_crawling=count_data_crawling)
	
	if request.method == 'POST':
		response = controller.add_dataPreprocessing()	# Memanggil fungsi 'add_dataPreprocessing()' menggunakan Instance 'controller'
		return response

# Tampil Data ke dalam tabel preprocessing
@app.route('/list_data_preprocessing', methods=['GET'])
def list_data_preprocessing():
	data_preprocessing = controller.select_dataPreprocessing()	# Memanggil fungsi 'select_dataPreprocessing()' menggunakan Instance 'controller'
	return { 'data': data_preprocessing }

# Tampil Halaman(VIEW) & Simpan Labeling Data ================================================
@app.route('/labeling', methods=['GET','POST'])
def labeling():
	if request.method == 'GET':
		count_data_no_label = controller.count_dataNoLabel()	# Memanggil fungsi 'count_dataNoLabel()' menggunakan Instance 'controller'
		return render_template('labeling.html', count_data_no_label=count_data_no_label)
	
	if request.method == 'POST':
		response = controller.add_dataLabeling()	# Memanggil fungsi 'add_dataLabeling()' menggunakan Instance 'controller'
		return response

# Labeling dengan Kamus sentimen
@app.route('/labeling_kamus', methods=['POST'])
def labeling_kamus():
	response = controller.add_dataLabelingKamus()	# Memanggil fungsi 'add_dataLabelingKamus()' menggunakan Instance 'controller'
	return response

# Tampil Data BERLABEL ke dalam tabel labeling
@app.route('/list_data_with_label', methods=['GET'])
def list_data_with_label():
	data_with_label = controller.select_dataWithLabel()	# Memanggil fungsi 'select_dataWithLabel()' menggunakan Instance 'controller'
	return { 'data': data_with_label }

# Tampil Data NO-LABEL ke dalam tabel labeling
@app.route('/list_data_no_label', methods=['GET'])
def list_data_no_label():
	data_no_label = controller.select_dataNoLabel()	# Memanggil fungsi 'select_dataNoLabel()' menggunakan Instance 'controller'
	return { 'data': data_no_label }

# Tampil Halaman(VIEW) & Simpan Split Data ================================================
@app.route('/split', methods=['GET','POST'])
def split():
	if request.method == 'GET':
		count_data_with_label = controller.count_dataWithLabel()	# Memanggil fungsi 'count_dataWithLabel()' menggunakan Instance 'controller'
		return render_template('split.html', count_data_with_label=count_data_with_label)
	
	if request.method == 'POST':
		response = controller.add_dataSplit()	# Memanggil fungsi 'add_dataSplit()' menggunakan Instance 'controller'
		return response

# Tampil Data TRAINING ke dalam tabel split
@app.route('/list_data_training', methods=['GET'])
def list_data_training():
	data_training = controller.select_dataTraining()	# Memanggil fungsi 'select_dataTraining()' menggunakan Instance 'controller'
	return { 'data': data_training }

# Tampil Data TESTING ke dalam tabel split
@app.route('/list_data_testing', methods=['GET'])
def list_data_testing():
	data_testing = controller.select_dataTesting()	# Memanggil fungsi 'select_dataTesting()' menggunakan Instance 'controller'
	return { 'data': data_testing }

# Modelling Data ================================================
@app.route('/modeling', methods=['GET','POST'])
def modeling():
	if request.method == 'GET':
		data_model = controller.select_dataModel()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller'
		count_data_training = controller.count_dataTraining()	# Memanggil fungsi 'count_dataTraining()' menggunakan Instance 'controller'
		max_sample_sentiment, total_sample_sentiment = controller.count_sampleSentiment()	# Memanggil fungsi 'count_sampleSentiment()' menggunakan Instance 'controller'
		return render_template('modeling.html', data_model=data_model, count_data_training=count_data_training, max_sample_sentiment=max_sample_sentiment, total_sample_sentiment=total_sample_sentiment)
	
	if request.method == 'POST':
		response = controller.create_dataModeling()	# Memanggil fungsi 'create_dataModeling()' menggunakan Instance 'controller'
		return response

# Hapus Data Model
@app.route('/modeling/hapus', methods=['POST'])
def hapus_dataModelling():
	controller.delete_dataModelling()	# Memanggil fungsi 'delete_dataModelling()' menggunakan Instance 'controller'
	return redirect(url_for('modeling'))


# Pengujian Data ================================================
@app.route('/evaluation', methods=['GET','POST'])
def evaluation():
	if request.method == 'GET':
		count_data_testing = controller.count_dataTes()	# Memanggil fungsi 'count_dataTes()' menggunakan Instance 'controller'
		data_model = controller.select_dataModel()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller'
		return render_template('evaluation.html', data_model=data_model, count_data_testing=count_data_testing)
	
	if request.method == 'POST':
		response = controller.check_evaluation()	# Memanggil fungsi 'check_evaluation()' menggunakan Instance 'controller'
		return response

# Tampil KOMPOSISI model
@app.route('/komposisi_model', methods=['POST'])
def komposisi_model():
	komposisi_model = controller.select_komposisiModel()	# Memanggil fungsi 'select_komposisiModel()' menggunakan Instance 'controller'
	return { 'data': komposisi_model }

# Visualisasi Data ================================================
@app.route('/visualization', methods=['GET'])
def visualization():
	jumlah_tweets, jumlah_p, jumlah_n, persentase_p, persentase_n, waktu = controller.get_visualisasiHasil()	# Memanggil fungsi 'get_visualisasiHasil()' menggunakan Instance 'controller'
	return render_template('visualization.html', jumlah_tweets=jumlah_tweets, jumlah_p=jumlah_p,jumlah_n=jumlah_n, persentase_p=persentase_p, persentase_n=persentase_n, waktu=waktu)

# Import file excel proses Slangword data ================================================
@app.route('/importSlangword', methods=['POST'])
def importSlangword():
	controller.import_fileExcelSlangword()
	return redirect(url_for('slangword'))	# Memanggil fungsi 'slangword()' dengan method GET

# Import file excel proses Stopword data ================================================
@app.route('/importStopword', methods=['POST'])
def importStopword():
	controller.import_fileExcelStopword()
	return redirect(url_for('stopword'))	# Memanggil fungsi 'stopword()' dengan method GET

# Import file excel proses data kata positif ================================================
@app.route('/importPositive_word', methods=['POST'])
def importPositive_word():
	controller.import_fileExcelPositiveWord()
	return redirect(url_for('positive_word'))	# Memanggil fungsi 'positive_word()' dengan method GET

# Import file excel proses data kata positif ================================================
@app.route('/importNegative_word', methods=['POST'])
def importNegative_word():
	controller.import_fileExcelNegativeWord()
	return redirect(url_for('negative_word'))	# Memanggil fungsi 'negative_word()' dengan method GET

# Import file excel proses Crawling data ================================================
@app.route('/importCrawling', methods=['POST'])
def importCrawling():
	controller.import_fileExcelCrawling()
	return redirect(url_for('crawling'))	# Memanggil fungsi 'crawling()' dengan method GET
