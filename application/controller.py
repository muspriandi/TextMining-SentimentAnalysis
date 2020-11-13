from flask import request, json
from application.models import Models
from application.api import Api
from application.excel import Excel

class Controller:
	
	# CRUD - Slangword
	def select_dataSlangword(self):
		instance_Model = Models('SELECT * FROM tbl_slangword')
		data_slangword = instance_Model.select()
		return data_slangword
	
	def add_dataStopword(self):
		slangword = request.form['slangword']
		kata_asli = request.form['kata_asli']
	
		data_tambah = (slangword, kata_asli)
	
		instance_Model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s,%s)')
		instance_Model.query_sql(data_tambah)
		
	def update_dataStopword(self):
		id = request.form['id']
		slangword = request.form['slangword']
		kata_asli = request.form['kata_asli']
	
		data_ubah = (slangword, kata_asli, id)
	
		instance_Model = Models('UPDATE tbl_slangword SET slangword=%s, kata_asli=%s WHERE id_slangword = %s')
		instance_Model.query_sql(data_ubah)
	
	def delete_dataStopword(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_slangword WHERE id_slangword = %s')
		instance_Model.query_sql(id)
		
	# CRUD - Crawling
	def select_dataCrawling(self):
		instance_Model = Models('SELECT * FROM tbl_tweet_search')
		data_crawling = instance_Model.select()
		return data_crawling
	
	def add_dataCrawling(self):
		aksi = request.form['aksi']
		
		instance_Api = Api()
		instance_Excel = Excel()
		
		if aksi == "crawling":
			kata_kunci = request.form['kata_kunci']
			tanggal_awal = request.form['tanggal_awal']
			tanggal_akhir = request.form['tanggal_akhir']
			
			data_crawling = instance_Api.get_search(kata_kunci +' -filter:retweets', tanggal_awal, tanggal_akhir)
			instance_Excel.save_excel(data_crawling)
			return json.dumps({ 'kata_kunci': kata_kunci, 'tanggal_awal': tanggal_awal, 'tanggal_akhir': tanggal_akhir, 'data_crawling': data_crawling })
		
		if aksi == "save_crawling":
			data_tes = request.form['data_tes']
			data_latih = request.form['data_latih']
			
			instance_Excel.split_data(data_tes, data_latih)
			tuples_excel = instance_Excel.make_tuples()
			
			instance_Model = Models('REPLACE INTO tbl_tweet_search(id, text, user, created_at, data_type) VALUES (%s, %s, %s, %s, %s)')
			instance_Model.insert_multiple(tuples_excel)
			return None
	
	# CRUD - Preprocessing
	def select_dataPreprocessing(self):
		instance_Model = Models('SELECT * FROM tbl_tweet_preprocessing')
		data_preprocessing = instance_Model.select()
		return data_preprocessing
	
	def add_dataPreprocessing(self):
		tipe_data = request.form.getlist('tipe_data[]')
		
		if len(tipe_data) == 1:
			instance_Model = Models("SELECT text FROM tbl_tweet_search WHERE data_type='"+ tipe_data[0] +"'")
			data_preprocessing = instance_Model.select()
		else:
			instance_Model = Models("SELECT text FROM tbl_tweet_search")
			data_preprocessing = instance_Model.select()
		
		# FUNGSI PREPROCESSING - BESOK!!
		#print("\n\n\n ====================================================== \n\n\n")
		return json.dumps(0)
	