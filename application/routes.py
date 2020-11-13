from flask import render_template, request, redirect, url_for
from application import app
from application.controller import Controller

@app.route('/')
@app.route('/dashboard')
def index():
	return render_template('dashboard.html', title='dashboard')

controller = Controller()	# Menetapkan Instance dari Class Controller

# CRUD Data Slangword
@app.route('/slangword', methods=['GET','POST'])
def slangword():
	if request.method == "GET":
		data_slangword = controller.select_dataSlangword()	# Memanggil fungsi 'select_dataSlangword()' menggunakan Instance 'controller'
		return render_template('slangword.html', data_slangword=data_slangword)
	
	if request.method == "POST":
		controller.add_dataStopword()	# Memanggil fungsi 'add_dataStopword()' menggunakan Instance 'controller'
	
	return redirect(url_for('slangword'))	# Memanggil fungsi slangword() dengan method GET

@app.route('/slangword/ubah', methods=['POST'])
def ubah_dataSlangword():
	controller.update_dataStopword()	# Memanggil fungsi 'update_dataStopword()' menggunakan Instance 'controller'
	return redirect(url_for('slangword'))

@app.route('/slangword/hapus', methods=['POST'])
def hapus_dataSlangword():
	controller.delete_dataStopword()	# Memanggil fungsi 'delete_dataStopword()' menggunakan Instance 'controller'
	return redirect(url_for('slangword'))

# CRUD Data Crawling
@app.route('/crawling', methods=['GET','POST'])
def crawling():
	if request.method == "GET":
		data_crawling = controller.select_dataCrawling()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller'
		return render_template('crawling.html', data_crawling=data_crawling)
	
	if request.method == "POST":
		response = controller.add_dataCrawling()
		if response != None:
			return response
		
		return redirect(url_for('crawling'))	# Memanggil fungsi crawling() dengan method GET

# CRUD Data Preprocessing
@app.route('/preprocessing', methods=['GET','POST'])
def preprocessing():
	if request.method == "GET":
		data_preprocessing = controller.select_dataPreprocessing()	# Memanggil fungsi 'select_dataPreprocessing()' menggunakan Instance 'controller'
		return render_template('preprocessing.html', data_preprocessing=data_preprocessing)
	
	if request.method == "POST":
		response = controller.add_dataPreprocessing()
		return response

@app.route('/clustering')
def clustering():
	return render_template('clustering.html', title='clustering')