from flask import request, json
from application.models import Models
from application.api import Api
from application.excel import Excel
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Controllers:
	
	# ================================================================== CRUD - SLANGWORD ==================================================================
	def select_dataSlangword(self):
		instance_Model = Models('SELECT * FROM tbl_slangword')
		data_slangword = instance_Model.select()
		return data_slangword
	
	def add_dataSlangword(self):
		slangword = request.form['slangword']
		kata_asli = request.form['kata_asli']
	
		data_tambah = (slangword, kata_asli)
	
		instance_Model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s,%s)')
		instance_Model.query_sql(data_tambah)
		
	def update_dataSlangword(self):
		id = request.form['id']
		slangword = request.form['slangword']
		kata_asli = request.form['kata_asli']
	
		data_ubah = (slangword, kata_asli, id)
	
		instance_Model = Models('UPDATE tbl_slangword SET slangword=%s, kata_asli=%s WHERE id_slangword = %s')
		instance_Model.query_sql(data_ubah)
	
	def delete_dataSlangword(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_slangword WHERE id_slangword = %s')
		instance_Model.query_sql(id)
		
	# ================================================================== CRUD - CRAWLING ==================================================================
	def select_dataCrawling(self):
		instance_Model = Models('SELECT * FROM tbl_tweet_search')
		data_crawling = instance_Model.select()
		return data_crawling
	
	def add_dataCrawling(self):
		aksi = request.form['aksi']
		
		instance_Api = Api()
		instance_Excel = Excel()
		
		# Fungsi CARI TWEET(crawling) : Ambil data menggunakan API Twitter ==> Simpan(data) ke Excel & Tampilkan(data) ke layar
		if aksi == 'crawling':
			kata_kunci = request.form['kata_kunci']
			tanggal_awal = request.form['tanggal_awal']
			tanggal_akhir = request.form['tanggal_akhir']
			
			# Ambil data menggunakan API Twitter (Tweepy)
			data_crawling = instance_Api.get_search(kata_kunci +' -filter:retweets', tanggal_awal, tanggal_akhir)
			# Fungsi[1] : Simpan data_crawling ke dalam file Excel
			instance_Excel.save_excel_crawling(data_crawling)
			# Menampilkan data_crawling ke layar
			return json.dumps({ 'data_crawling': data_crawling })
		
		# Fungsi SIMPAN TWEET(crawling) : Ambil data dari excel(yang telah disimpan[1]) ==> Tambahkan Tipe Data (0/1) ==> Simpan ke Database
		if aksi == 'save_crawling':
			data_tes = request.form['data_tes']
			data_latih = request.form['data_latih']
			
			# Fungsi[2] : Split data excel[1] menjadi x% data tes dan x% data latih berdasarkan request form (data_tes & data_latih)
			instance_Excel.split_data(data_tes, data_latih)
			# Fungsi[3] : Membuat tuple dari file excel (dari data yang telah memiliki kolom data_type[2])
			tuples_excel = instance_Excel.make_tuples('crawling')
			
			# Simpan ke Database dengan VALUES berupa tuple dari Fungsi[3]
			instance_Model = Models('REPLACE INTO tbl_tweet_search(id, text, user, created_at, data_type) VALUES (%s, %s, %s, %s, %s)')
			instance_Model.insert_multiple(tuples_excel)
			return None
	
	# ================================================================== CRUD - PREPROCESSING ==================================================================
	def select_dataPreprocessing(self):
		instance_Model = Models('SELECT * FROM tbl_tweet_preprocessing')
		data_preprocessing = instance_Model.select()
		return data_preprocessing
	
	def add_dataPreprocessing(self):
		aksi = request.form['aksi']
		
		instance_Excel = Excel()
		
		# Fungsi PREPROCESSING : Data Tweet dari database ==> PREPROCESSING ==> Tweet Bersih ==> Simpan(data) ke Excel & Tampilkan(data) ke layar
		if aksi == 'preprocessing':
			tipe_data = request.form.getlist('tipe_data[]')
			
			# Menampilkan data berdasarkan request form (tipe_data)
			if len(tipe_data) == 1:
				instance_Model = Models("SELECT * FROM tbl_tweet_search WHERE data_type='"+ tipe_data[0] +"'")
				data_preprocessing = instance_Model.select()
			else:
				instance_Model = Models('SELECT * FROM tbl_tweet_search')
				data_preprocessing = instance_Model.select()
			
			result_data = []
			# Inisialisasi Konfigurasi Library Sastrawi untuk proses 6. Remove Stop Word
			instance_Stopword = StopWordRemoverFactory()
			stopword = instance_Stopword.create_stop_word_remover()
			# Inisialisasi Konfigurasi Library Sastrawi untuk proses 7. Stemming
			instance_Stemming = StemmerFactory()
			stemmer = instance_Stemming.create_stemmer()
			# Inisialisasi untuk proses 8. Change Slang Word
			instance_Model = Models('SELECT slangword,kata_asli FROM tbl_slangword')
			slangword = instance_Model.select()
			
			for index, data in enumerate(data_preprocessing):
				
				# 1. Case Folding : Mengubah huruf menjadi huruf kecil
				result_text = data['text'].lower()
				
				# 2. Remove URL, Mention, Hastag & Number  : Menghilangkan kata yang diawali dengan kata 'http', '@', '#' atau angka[0-9]
				result_text = re.sub(r'http\S+|@\S+|#\S+|\d+', '', result_text)
				
				# 3. Remove Unicode : Menghilangkan pengkodean karakter
				result_text = (result_text.encode('ascii', 'ignore')).decode("utf-8")
				
				# 4. Remove Punctuation : Menghilangkan tanda baca kalimat
				result_text = result_text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
				
				# 5. Remove Whitespace : Menghilangkan spasi/tab/baris yang kosong
				result_text = result_text.strip()
				result_text = re.sub('\s+', ' ', result_text)
				
				# 6. Remove Stop Word : Menghilangkan kata yang dianggap tidak memiliki makna
				result_text = stopword.remove(result_text)
				
				# 7. Stemming : Menghilangkan infleksi kata ke bentuk dasarnya
				result_text = stemmer.stem(result_text)
				
				# 8. Change Slang Word : Merubah kata 'gaul' ke kata aslinya
				for slang in slangword:
					if slang['slangword'] in result_text:
						result_text = re.sub(r''+ slang['slangword'] +'', ''+ slang['kata_asli'] +'', result_text)
				
				# 9. Tokenizing
				#---
				
				result_data.append({'id': data['id'], 'text': result_text, 'username': data['user'], 'created_at': data['created_at'], 'data_type': data['data_type']})
			
			# Fungsi[4] : Simpan result_data ke dalam file Excel
			instance_Excel.save_excel_preprocessing(result_data)
			# Menampilkan result_data ke layar
			return json.dumps({ 'result_data': result_data, 'data_preprocessing': data_preprocessing })
		
		# Fungsi SIMPAN TWEET(PREPROCESSING) : Ambil data dari excel(yang telah disimpan[4]) ==> Simpan ke Database
		if aksi == 'save_preprocessing':
			# Fungsi[5] : Membuat tuple dari file excel (dari data yang telah memiliki kolom data_type[2])
			tuples_excel = instance_Excel.make_tuples('preprocessing')
			
			# Simpan ke Database dengan VALUES berupa tuple dari Fungsi[5]
			instance_Model = Models('INSERT INTO tbl_tweet_preprocessing(id, text, user, created_at, data_type) VALUES (%s, %s, %s, %s, %s)')
			instance_Model.insert_multiple(tuples_excel)
			return None
	
	# ================================================================== CRUD - PREPROCESSING ==================================================================
	
	