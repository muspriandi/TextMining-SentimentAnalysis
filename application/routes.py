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
		if response != None:
			return response
		
		return redirect(url_for('preprocessing'))	# Memanggil fungsi 'preprocessing()' dengan method GET

# Tampil Data ke dalam tabel preprocessing
@app.route('/list_data_preprocessing', methods=['GET'])
def list_data_preprocessing():
	data_preprocessing = controller.select_dataPreprocessing()	# Memanggil fungsi 'select_dataPreprocessing()' menggunakan Instance 'controller'
	return { 'data': data_preprocessing }

# Tampil Halaman(VIEW) & Simpan Labeling Data ================================================
@app.route('/labeling', methods=['GET','POST'])
def labeling():
	if request.method == 'GET':
		return render_template('labeling.html')
	
	if request.method == 'POST':
		response = controller.add_dataLabeling()	# Memanggil fungsi 'add_dataLabeling()' menggunakan Instance 'controller'
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

# Modelling Data ================================================
@app.route('/modeling', methods=['GET','POST'])
def modeling():
	if request.method == 'GET':
		data_model = controller.select_dataModel()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller'
		return render_template('modeling.html', data_model=data_model)
	
	if request.method == 'POST':
		response = controller.create_dataModeling()	# Memanggil fungsi 'create_dataModeling()' menggunakan Instance 'controller'
		return response

# Pengujian Data ================================================
@app.route('/evaluation', methods=['GET','POST'])
def evaluation():
	if request.method == 'GET':
		data_tes = controller.count_dataTes()	# Memanggil fungsi 'count_dataTes()' menggunakan Instance 'controller'
		data_model = controller.select_dataModel()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller'
		return render_template('evaluation.html', data_model=data_model, data_tes=data_tes)
	
	if request.method == 'POST':
		response = controller.check_evaluation()	# Memanggil fungsi 'check_evaluation()' menggunakan Instance 'controller'
		return response


# Import file excel proses Slangword data ================================================
@app.route('/importSlangword', methods=['POST'])
def importSlangword():
	controller.import_fileExcelSlangword()
	return redirect(url_for('slangword'))	# Memanggil fungsi 'slangword()' dengan method GET

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

