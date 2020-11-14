from flask import render_template, request, redirect, url_for
from application import app
from application.controllers import Controllers

@app.route('/')
@app.route('/dashboard')
def index():
	return render_template('dashboard.html', title='dashboard')

controller = Controllers()	# Menetapkan Instance dari Class Controllers

# CRUD Data Slangword
@app.route('/slangword', methods=['GET','POST'])
def slangword():
	if request.method == 'GET':
		data_slangword = controller.select_dataSlangword()	# Memanggil fungsi 'select_dataSlangword()' menggunakan Instance 'controller'
		return render_template('slangword.html', data_slangword=data_slangword)
	
	if request.method == 'POST':
		controller.add_dataSlangword()	# Memanggil fungsi 'add_dataSlangword()' menggunakan Instance 'controller'
	
	return redirect(url_for('slangword'))	# Memanggil fungsi slangword() dengan method GET

@app.route('/slangword/ubah', methods=['POST'])
def ubah_dataSlangword():
	controller.update_dataSlangword()	# Memanggil fungsi 'update_dataSlangword()' menggunakan Instance 'controller'
	return redirect(url_for('slangword'))

@app.route('/slangword/hapus', methods=['POST'])
def hapus_dataSlangword():
	controller.delete_dataSlangword()	# Memanggil fungsi 'delete_dataSlangword()' menggunakan Instance 'controller'
	return redirect(url_for('slangword'))

# CRUD Data Crawling
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

# CRUD Data Preprocessing
@app.route('/preprocessing', methods=['GET','POST'])
def preprocessing():
	if request.method == 'GET':
		data_preprocessing = controller.select_dataPreprocessing()	# Memanggil fungsi 'select_dataPreprocessing()' menggunakan Instance 'controller'
		return render_template('preprocessing.html', data_preprocessing=data_preprocessing)
	
	if request.method == 'POST':
		response = controller.add_dataPreprocessing()	# Memanggil fungsi 'add_dataPreprocessing()' menggunakan Instance 'controller'
		if response != None:
			return response
		
		return redirect(url_for('preprocessing'))	# Memanggil fungsi 'preprocessing()' dengan method GET

@app.route('/labeling')
def labeling():
	return render_template('labeling.html', title='labeling')