from flask import render_template, request, redirect, url_for
from application import app
from application.controllers import Controllers

@app.route('/')
@app.route('/dashboard')
def index():
	return render_template('dashboard.html')

controller = Controllers()	# Menetapkan Instance dari Class Controllers

# Tampil & Simpan Data Slangword
@app.route('/slangword', methods=['GET','POST'])
def slangword():
	if request.method == 'GET':
		data_slangword = controller.select_dataSlangword()	# Memanggil fungsi 'select_dataSlangword()' menggunakan Instance 'controller'
		return render_template('slangword.html', data_slangword=data_slangword)
	
	if request.method == 'POST':
		controller.add_dataSlangword()	# Memanggil fungsi 'add_dataSlangword()' menggunakan Instance 'controller'
	
	return redirect(url_for('slangword'))	# Memanggil fungsi slangword() dengan method GET

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

# Tampil & Simpan Data Crawling
@app.route('/crawling', methods=['GET','POST'])
def crawling():
	if request.method == 'GET':
		data_crawling = controller.select_dataCrawling()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller'
		return render_template('crawling.html', data_crawling=data_crawling)
	
	if request.method == 'POST':
		response = controller.add_dataCrawling()	# Memanggil fungsi 'add_dataCrawling()' menggunakan Instance 'controller'
		if response != None:
			return response
		
		return redirect(url_for('crawling'))	# Memanggil fungsi 'crawling()' dengan method GET

# Tampil & Simpan Data Preprocessing
@app.route('/preprocessing', methods=['GET','POST'])
def preprocessing():
	if request.method == 'GET':
		count_tweet_testing, count_tweet_training = controller.count_dataPreprocessing()	# Memanggil fungsi 'count_dataPreprocessing()' menggunakan Instance 'controller'
		data_preprocessing = controller.select_dataPreprocessing()	# Memanggil fungsi 'select_dataPreprocessing()' menggunakan Instance 'controller'
		return render_template('preprocessing.html', data_preprocessing=data_preprocessing, count_tweet_testing=count_tweet_testing, count_tweet_training=count_tweet_training)
	
	if request.method == 'POST':
		response = controller.add_dataPreprocessing()	# Memanggil fungsi 'add_dataPreprocessing()' menggunakan Instance 'controller'
		if response != None:
			return response
		
		return redirect(url_for('preprocessing'))	# Memanggil fungsi 'preprocessing()' dengan method GET

# Tampil & Labeling Data Preprocessing
@app.route('/labeling', methods=['GET','POST'])
def labeling():
	if request.method == 'GET':
		tweet_testing_label, tweet_testing_nolabel = controller.select_dataTesting()	# Memanggil fungsi 'select_dataTesting()' menggunakan Instance 'controller'
		tweet_training_label, tweet_training_nolabel = controller.select_dataTraining()	# Memanggil fungsi 'select_dataTraining()' menggunakan Instance 'controller'
		return render_template('labeling.html', tweet_testing_label=tweet_testing_label, tweet_testing_nolabel=tweet_testing_nolabel, tweet_training_label=tweet_training_label, tweet_training_nolabel=tweet_training_nolabel)
	
	if request.method == 'POST':
		response = controller.add_dataLabeling()	# Memanggil fungsi 'add_dataLabeling()' menggunakan Instance 'controller'
		return response

# Modelling Data
@app.route('/modeling', methods=['GET','POST'])
def modeling():
	if request.method == 'GET':
		return render_template('modeling.html')
	
	if request.method == 'POST':
		response = controller.create_dataModeling()	# Memanggil fungsi 'create_dataModeling()' menggunakan Instance 'controller'
		return response

# Pengujian Data
@app.route('/evaluation', methods=['GET','POST'])
def evaluation():
	if request.method == 'GET':
		return render_template('evaluation.html')
	
	if request.method == 'POST':
		response = controller.check_evaluation()	# Memanggil fungsi 'create_dataModeling()' menggunakan Instance 'controller'
		return response

# Prediksi Sentimen Data
@app.route('/prediction', methods=['GET','POST'])
def prediction():
	if request.method == 'GET':
		return render_template('prediction.html')
	
	if request.method == 'POST':
		response = controller.predict_tweet()	# Memanggil fungsi 'predict_tweet()' menggunakan Instance 'controller'
		return response


# Import File Excel
@app.route('/import', methods=['POST'])
def import_excel():
	controller.import_fileExcel()
	return redirect(url_for('crawling'))	# Memanggil fungsi 'crawling()' dengan method GET

# Tampil Data Crawling berdasarkan ID
@app.route('/getTweetById', methods=['POST'])
def getTweetById():
	response = controller.getTweetById()	# Memanggil fungsi 'getTweetById()' menggunakan Instance 'controller'
	return response
