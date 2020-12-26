from flask import request, json
from application.models import Models
from application.api import Api
from application.excel import Excel
import re
import string
import math
import random
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline
import joblib
from joblib import load
from datetime import datetime
from sklearn.metrics import accuracy_score

class Controllers:
	
	# ================================================================== SLANGWORD ==================================================================
	def select_dataSlangword(self):
		instance_Model = Models('SELECT * FROM tbl_slangword')
		data_slangword = instance_Model.select()
		return data_slangword
	
	def add_dataSlangword(self):
		slangword = request.form['slangword']
		kata_asli = request.form['kata_asli']
	
		data_tambah = (slangword.lower(), kata_asli.lower())	# Membuat tupple dari form data masukan
	
		instance_Model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s,%s)')
		instance_Model.query_sql(data_tambah)
	
	def update_dataSlangword(self):
		id = request.form['id']
		slangword = request.form['slangword']
		kata_asli = request.form['kata_asli']
	
		data_ubah = (slangword.lower(), kata_asli.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_slangword SET slangword=%s, kata_asli=%s WHERE id_slangword = %s')
		instance_Model.query_sql(data_ubah)
	
	def delete_dataSlangword(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_slangword WHERE id_slangword = %s')
		instance_Model.query_sql(id)
			
	# ================================================================== STOPWORD ==================================================================
	def select_dataStopword(self):
		instance_Model = Models('SELECT * FROM tbl_stopword')
		data_stopword = instance_Model.select()
		return data_stopword
	
	def add_dataStopword(self):
		stopword = request.form['stopword']
	
		instance_Model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
		instance_Model.query_sql(stopword.lower())
	
	def update_dataStopword(self):
		id = request.form['id']
		stopword = request.form['stopword']
	
		data_ubah = (stopword.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_stopword SET stopword=%s WHERE id_stopword = %s')
		instance_Model.query_sql(data_ubah)
	
	def delete_dataStopword(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_stopword WHERE id_stopword = %s')
		instance_Model.query_sql(id)
		
	# ================================================================== POSITIVE WORD ==================================================================
	def select_dataPositiveWord(self):
		instance_Model = Models('SELECT * FROM tbl_lexicon_positive')
		data_positive_word = instance_Model.select()
		return data_positive_word
	
	def add_dataPositiveWord(self):
		kata_positif = request.form['kata_positif']

		instance_Model = Models('INSERT INTO tbl_lexicon_positive(positive_word) VALUES (%s)')
		instance_Model.query_sql(kata_positif.lower())
	
	def update_dataPositiveWord(self):
		id = request.form['id']
		kata_positif = request.form['kata_positif']
	
		data_ubah = (kata_positif.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_lexicon_positive SET positive_word=%s WHERE id_positive = %s')
		instance_Model.query_sql(data_ubah)
	
	def delete_dataPositiveWord(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_lexicon_positive WHERE id_positive = %s')
		instance_Model.query_sql(id)
			
	# ================================================================== NEGATIVE WORD ==================================================================
	def select_dataNegativeWord(self):
		instance_Model = Models('SELECT * FROM tbl_lexicon_negative')
		data_negative_word = instance_Model.select()
		return data_negative_word
	
	def add_dataNegativeWord(self):
		kata_negatif = request.form['kata_negatif']

		instance_Model = Models('INSERT INTO tbl_lexicon_negative(negative_word) VALUES (%s)')
		instance_Model.query_sql(kata_negatif.lower())
	
	def update_dataNegativeWord(self):
		id = request.form['id']
		kata_negatif = request.form['kata_negatif']
	
		data_ubah = (kata_negatif.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_lexicon_negative SET negative_word=%s WHERE id_negative = %s')
		instance_Model.query_sql(data_ubah)
	
	def delete_dataNegativeWord(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_lexicon_negative WHERE id_negative = %s')
		instance_Model.query_sql(id)
	
	# ==============================================================  CRAWLING ==============================================================
	def select_dataCrawling(self):
		instance_Model = Models('SELECT * FROM tbl_tweet_crawling')
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
		
		# Fungsi SIMPAN TWEET(crawling) : Ambil data dari excel(yang telah disimpan[1]) ==> Simpan ke Database
		if aksi == 'save_crawling':
			# Fungsi[2] : Membuat tuple dari file excel
			tuples_excel = instance_Excel.make_tuples_crawling()
			
			# Simpan ke Database dengan VALUES berupa tuple dari Fungsi[2]
			instance_Model = Models('REPLACE INTO tbl_tweet_crawling(id, text, user, created_at) VALUES (%s, %s, %s, %s)')
			instance_Model.insert_multiple(tuples_excel)
			return None

	def count_dataCrawling(self):
		# SELECT jumlah data crawling
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
		data_crawling = instance_Model.select()
		return data_crawling[0]['jumlah']
	
	# ============================================================== PREPROCESSING ==============================================================
	def select_dataPreprocessing(self):
		# SELECT data preprocessing
		instance_Model = Models('SELECT * FROM tbl_tweet_clean')
		data_preprocessing = instance_Model.select()
		return data_preprocessing
	
	def add_dataPreprocessing(self):
		aksi = request.form['aksi']
		
		instance_Excel = Excel()
		
		# Fungsi PREPROCESSING : Data Tweet dari database ==> PREPROCESSING ==> Tweet Bersih ==> Simpan(data) ke Excel & Tampilkan(data) ke layar
		if aksi == 'preprocessing':
			instance_Model = Models('SELECT * FROM tbl_tweet_crawling')
			data_preprocessing = instance_Model.select()
			
			first_data = []
			last_data = []
			case_folding = []
			remove_non_character = []
			remove_stop_word = []
			change_stemming = []
			change_slang = []

			# Inisialisasi untuk proses 7. Change Slang Word
			instance_Model = Models('SELECT slangword,kata_asli FROM tbl_slangword')
			slangwords = instance_Model.select()
			# Inisialisasi Konfigurasi Library Sastrawi untuk proses 8. Remove Stop Word
			instance_Model = Models('SELECT stopword FROM tbl_stopword')
			stopwords = instance_Model.select()
			# Inisialisasi Konfigurasi Library Sastrawi untuk proses 9. Stemming
			instance_Stemming = StemmerFactory()
			stemmer = instance_Stemming.create_stemmer()

			print('\n-- PROSES '+ str(len(data_preprocessing)) +' DATA --')	# PRINT KE CMD
			for index, data in enumerate(data_preprocessing):
				first_data.append(data['text'])
				
				# 1. Case Folding : Mengubah huruf menjadi huruf kecil
				result_text = data['text'].lower()
				case_folding.append(result_text)
				
				# 2. Remove URL, Mention, Hastag & Number  : Menghilangkan kata yang diawali dengan kata 'http', '@', '#' atau angka[0-9]
				result_text = re.sub(r'http\S+|@\S+|#\S+|\d+', '', result_text)
				
				# 3. Remove Unicode : Menghilangkan pengkodean karakter
				result_text = (result_text.encode('ascii', 'ignore')).decode("utf-8")
				
				# 4. Remove Punctuation : Menghilangkan tanda baca kalimat
				result_text = result_text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
				
				# 5. Remove Whitespace : Menghilangkan spasi/tab/baris yang kosong
				result_text = result_text.strip()
				result_text = re.sub('\s+', ' ', result_text)
				remove_non_character.append(result_text)

				for slang in slangwords:
					if slang['slangword'] in result_text:
						result_text = re.sub(r'\b{}\b'.format(slang['slangword']), slang['kata_asli'], result_text)
				change_slang.append(result_text)

				for stop in stopwords:
					if stop['stopword'] in result_text:
						result_text = re.sub(r'\b{}\b'.format(stop['stopword']), '', result_text)
				remove_stop_word.append(result_text)
				
				# 9. Stemming : Menghilangkan infleksi/kata berimbuhan kata ke bentuk dasarnya
				result_text = stemmer.stem(result_text)
				change_stemming.append(result_text)

				last_data.append(result_text)

				# SIMPAN DATA
				try:
					data_simpan = (data['id'], data['text'], result_text, data['user'], data['created_at']) # Membuat tuple sebagai isian untuk kueri INSERT
					
					# Menyimpan data hasil preprocessing dengan kueri INSERT IGNORE, dengan memperbarui record yang duplikat berdasarkan PK
					instance_Model = Models('INSERT IGNORE tbl_tweet_clean(id, text, clean_text, user, created_at) VALUES (%s, %s, %s, %s, %s)')
					instance_Model.query_sql(data_simpan)
				except:
					print('\nGagal Menyimpan Data '+ str(data['id']) +'\n')
				print(index+1, end=" ")	# PRINT KE CMD
			print('\n-- SELESAI --\n')	# PRINT KE CMD
			# Menampilkan data ke layar
			return json.dumps({'first_data': first_data, 'case_folding': case_folding, 'remove_non_character': remove_non_character, 'change_slang': change_slang, 'remove_stop_word': remove_stop_word, 'change_stemming': change_stemming, 'last_data': last_data})
	
	def count_dataNoLabel(self):
		# SELECT jumlah clean data yang tidak memiliki label
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NULL')
		data_crawling = instance_Model.select()
		return data_crawling[0]['jumlah']

	def count_dataWithLabel(self):
		# SELECT jumlah clean data yang telah memiliki label
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
		data_labeling = instance_Model.select()
		return data_labeling[0]['jumlah']
	
	# ============================================================== LABELING ==================================================================
	def select_dataWithLabel(self):
		# SELECT data tweet yang TELAH diberi label
		instance_Model = Models('SELECT * FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
		data_withLabel = instance_Model.select()
		return data_withLabel
	
	def select_dataNoLabel(self):
		# SELECT data tweet yang BELUM diberi label
		instance_Model = Models('SELECT id, text, clean_text FROM tbl_tweet_clean WHERE sentiment_type IS NULL')
		data_noLabel = instance_Model.select()
		return data_noLabel
	
	def add_dataLabeling(self):
		id = request.form['id']
		value = request.form['value']
		
		data_ubah = (value, id)
		instance_Model = Models('UPDATE tbl_tweet_clean SET sentiment_type=%s WHERE id=%s')
		instance_Model.query_sql(data_ubah)
		return 'Berhasil Melabeli Data!'
		
	def add_dataLabelingKamus(self):
		aksi = request.form['aksi']

		# FUNGSI LABELING DENGAN KAMUS : Data teks bersih ==> Hitung Skor(Sentimen) ==> Pemberian Kelas Sentimen ==> Update ==> Tampilkan(data) ke layar
		if aksi == 'labelingKamus':
			# SELECT data tanpa label dari database
			instance_Model = Models('SELECT id, clean_text FROM tbl_tweet_clean WHERE sentiment_type IS NULL')
			data_noLabel = instance_Model.select()

			# SELECT data kata-kata & bobot positif dari database
			instance_Model = Models('SELECT positive_word FROM tbl_lexicon_positive')
			data_positive = instance_Model.select()

			# SELECT data kata-kata & bobot negative dari database
			instance_Model = Models('SELECT negative_word FROM tbl_lexicon_negative')
			data_negative = instance_Model.select()
			
			teks_data = []
			skor_data = []
			for data_nL in data_noLabel:	# loop data tweet yang belum memiliki label
				skor = 0

				# Menghitung jumlah skor pada teks bersih dengan kamus
				for clean_text in data_nL['clean_text'].split(): # Tokenizing
					for data_p in data_positive:	# loop data kata positif
						if clean_text == data_p['positive_word']:
							skor += 1
					for data_n in data_negative:	# loop data kata negatif
						if clean_text == data_n['negative_word']:
							skor -= 1
				
				# Klasifikasi sentimen berdasarkan skor
				if skor > 0:
					sentimen = 'positif'
				elif skor == 0:
					sentimen = 'netral'
				else:
					sentimen = 'negatif'

				try:
					data_ubah = (sentimen, data_nL['id']) # Membuat tuple sebagai isian untuk kueri UPDATE
					
					# Menyimpan sentimen hasil dengan kueri UPDATE
					instance_Model = Models('UPDATE tbl_tweet_clean SET sentiment_type=%s WHERE id = %s')
					instance_Model.query_sql(data_ubah)
					
					# Simpan data ke list
					teks_data.append(data_nL['clean_text'])
					skor_data.append(skor)
				except:
					print('\nGagal Mengubah Data '+ str(data['id']) +'\n')
					return None
			# Menampilkan data ke layar
			return json.dumps({ 'teks_data': teks_data, 'skor_data': skor_data })

	# ============================================================== SPLIT ==============================================================
	
	def add_dataSplit(self):
		rasio = request.form['rasio']
		jumlah_data = float(request.form['jumlah_data'])
		
		if rasio == '2:8':
			jumlah_dataTes = math.floor(jumlah_data * 0.2) # Membagi data sebanyak 20% sebagai data tes(dengan pembulatan ke bawah)
			jumlah_dataLatih = math.ceil(jumlah_data * 0.8) # Membagi data sebanyak 80% sebagai data latih(dengan pembulatan ke atas)
		elif rasio == '3:7':
			jumlah_dataTes = math.floor(jumlah_data * 0.3) # Membagi data sebanyak 20% sebagai data tes(dengan pembulatan ke bawah)
			jumlah_dataLatih = math.ceil(jumlah_data * 0.7) # Membagi data sebanyak 80% sebagai data latih(dengan pembulatan ke atas)
		
		# value 0 = data tes	|	value1 = data latih
		# Membuat list(data_type) dengan value 0 sebanyak jumlah variabel 'jumlah_dataTes'
		data_type = [0 for i in range(int(jumlah_dataTes))]
		# Perulangan untuk mengisi value 1 ke dalam list(data_type) pada index random sebanyak jumlah variabel 'jumlah_dataLatih'
		for _ in range(int(jumlah_dataLatih)):
			data_type.insert(random.randint(0, len(data_type)), 1)
		
		# SELECT data tweet yang TELAH diberi label untuk diproses
		instance_Model = Models('SELECT * FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
		data_withLabel = instance_Model.select()

		# Menyimpan data(yang telah diSELECT) ke tabel yang berbeda berdasarkan value dari variabel 'data_type'
		for index, data in enumerate(data_withLabel):
			if data_type[index] == 0: # Jika value 'data_type' bernilai 0 maka akan di INSERT kedalam tabel TESTING
				# SIMPAN DATA
				try:
					data_simpan = (data['id'], data['text'], data['clean_text'], data['user'], data['created_at'], data['sentiment_type']) # Membuat tuple sebagai isian untuk kueri INSERT
					
					# Menyimpan data dengan kueri INSERT IGNORE, dengan memperbarui record yang duplikat berdasarkan PK
					instance_Model = Models('INSERT IGNORE tbl_tweet_testing(id, text, clean_text, user, created_at, sentiment_type) VALUES (%s, %s, %s, %s, %s, %s)')
					instance_Model.query_sql(data_simpan)
				except:
					print('\nGagal Menyimpan Data '+ str(data['id']) +'\n')
			else: # Jika value 'data_type' tidak bernilai 0  INSERT kedalam tabel TRAINING
				# SIMPAN DATA
				try:
					data_simpan = (data['id'], data['text'], data['clean_text'], data['user'], data['created_at'], data['sentiment_type']) # Membuat tuple sebagai isian untuk kueri INSERT
					
					# Menyimpan data dengan kueri INSERT IGNORE, dengan memperbarui record yang duplikat berdasarkan PK
					instance_Model = Models('INSERT IGNORE tbl_tweet_training(id, text, clean_text, user, created_at, sentiment_type) VALUES (%s, %s, %s, %s, %s, %s)')
					instance_Model.query_sql(data_simpan)
				except:
					print('\nGagal Menyimpan Data '+ str(data['id']) +'\n')
		
		return None
	
	def select_dataTraining(self):
		# SELECT data tweet TRAINING
		instance_Model = Models('SELECT * FROM tbl_tweet_training')
		data_training = instance_Model.select()
		return data_training
	
	def select_dataTesting(self):
		# SELECT data tweet TESTING
		instance_Model = Models('SELECT * FROM tbl_tweet_testing')
		data_testing = instance_Model.select()
		return data_testing

	def count_dataTraining(self):
		# SELECT data training
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL')
		data_training = instance_Model.select()
		return data_training[0]['jumlah']

	# ============================================================== MODELING ==============================================================
	def select_dataModel(self):
		instance_Model = Models('SELECT * FROM tbl_model')
		data_model = instance_Model.select()
		return data_model
	
	def create_dataModeling(self):
		# Select data dari tbl_tweet_training yang telah diberi label
		instance_Model = Models('SELECT clean_text, sentiment_type FROM tbl_tweet_training WHERE sentiment_type IS NOT NULL')
		tweet_training_label = instance_Model.select()
		
		x_train = []
		y_train = []
		sentiment_positive = 0
		sentiment_negative = 0
		for tweet in tweet_training_label:
			x_train.append(tweet['clean_text'])
			y_train.append(tweet['sentiment_type'])
			if tweet['sentiment_type'] == 'positif':
				sentiment_positive += 1
			elif tweet['sentiment_type'] == 'negatif':
				sentiment_negative += 1
		
		# Inisialisasi jenis vectorizer dan algoritme yang akan digunakan untuk membuat model
		instance_Vectorizer = TfidfVectorizer()
		instance_Classification = BernoulliNB()

		# Konfigurasi model dengan vectorizer dan algoritme
		model = Pipeline([('vectorizer', instance_Vectorizer), ('classifier', instance_Classification)])
		# Membuat model dengan data latih
		model.fit(x_train, y_train)

		# Menyimpan model kedalam bentuk .joblib agar dapat digunakan kembali (untuk proses Evaluasi & Prediksi)
		model_name = 'sentiment_model('+ datetime.today().strftime('%d-%m-%Y') +').joblib'
		joblib.dump(model, 'application/static/model_data/'+ model_name)

		# Insert model ke dalam database
		instance_Model = Models('REPLACE INTO tbl_model(model_name, sentiment_count, sentiment_positive, sentiment_negative) VALUES (%s, %s, %s, %s)')
		# Menjadikan tuple sebagai argumen untuk method query_sql
		instance_Model.query_sql((model_name, len(y_train), sentiment_positive, sentiment_negative))

		return { 'model_name': model_name, 'sentiment_count': len(y_train), 'sentiment_positive': sentiment_positive, 'sentiment_negative': sentiment_negative }
	
	def count_sampleSentiment(self):
		# SELECT jumlah data training berdasarkan jenis sentimen
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL GROUP BY sentiment_type')
		data_max_sentiment = instance_Model.select()

		min = 999999	# asumsi jumlah minimal sentimen tidak lebih dari 999999
		# mencari jumlah minimal sentimen
		for data in data_max_sentiment:
			if data['jumlah'] < min:
				min = data['jumlah']
		
		# nilai variable 'min' digunakan sebagai batas atas sample sentimen & nilai 'min*3' digunakan untuk mengetahui jumlah kuota sample
		return min, min*3
	
	# ============================================================== EVALUASI ==============================================================
	def count_dataTes(self):
		# HITUNG JUMLAH data training
		instance_Model = Models("SELECT count(id) as jumlah FROM tbl_tweet_testing WHERE sentiment_type IS NOT NULL")
		count_tweet_testing = instance_Model.select()
		return count_tweet_testing[0]
	
	def check_evaluation(self):
		model_name = request.form['model_name']
		# Select data dari tbl_tweet_testing yang telah diberi label
		instance_Model = Models('SELECT clean_text, sentiment_type FROM tbl_tweet_testing WHERE sentiment_type IS NOT NULL')
		tweet_testing_label = instance_Model.select()
		
		x_test = []
		y_test = []
		for tweet in tweet_testing_label:
			x_test.append(tweet['clean_text'])
			y_test.append(tweet['sentiment_type'])
		
		# Memuat kembali model yang telah dibuat pada proses Pemodelan
		model = load('application/static/model_data/' + model_name)
		# Memprediksikan sentimen untuk data 'x_test'
		hasil = model.predict(x_test)

		# Membandingkan hasil prediksi (hasil) dengan sentimen yang sebenarnya (y_test)
		akurasi = accuracy_score(y_test, hasil)
		return json.dumps({ 'akurasi': akurasi, 'teks_database': x_test, 'sentimen_database': y_test, 'sentimen_prediksi': hasil.tolist() })
	
	# ============================================================== IMPORT EXCEL ==============================================================
	
	# IMPORT EXCEL SLANGWORD
	def import_fileExcelSlangword(self):
		excel_file = request.files['excel_file']

		instance_Excel = Excel()
		tuples_excel = instance_Excel.make_tuples_slangword(excel_file)
		# Simpan ke Database dengan VALUES berupa tuple
		instance_Model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s, %s)')
		instance_Model.insert_multiple(tuples_excel)
		return None		# IMPORT EXCEL SLANGWORD
	
	# IMPORT EXCEL STOPWORD
	def import_fileExcelStopword(self):
		excel_file = request.files['excel_file']

		instance_Excel = Excel()
		tuples_excel = instance_Excel.make_tuples_stopword(excel_file)
		# Simpan ke Database dengan VALUES berupa tuple
		instance_Model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
		instance_Model.insert_multiple(tuples_excel)
		return None	
	
	# IMPORT EXCEL POSITIVE WORD
	def import_fileExcelPositiveWord(self):
		excel_file = request.files['excel_file']

		instance_Excel = Excel()
		tuples_excel = instance_Excel.make_tuples_positive_word(excel_file)
		# Simpan ke Database dengan VALUES berupa tuple
		instance_Model = Models('INSERT INTO tbl_lexicon_positive(positive_word) VALUES (%s)')
		instance_Model.insert_multiple(tuples_excel)
		return None	# IMPORT EXCEL POSITIVE WORD
	
	# IMPORT EXCEL NEGATIVE WORD
	def import_fileExcelNegativeWord(self):
		excel_file = request.files['excel_file']

		instance_Excel = Excel()
		tuples_excel = instance_Excel.make_tuples_negative_word(excel_file)
		# Simpan ke Database dengan VALUES berupa tuple
		instance_Model = Models('INSERT INTO tbl_lexicon_negative(negative_word) VALUES (%s)')
		instance_Model.insert_multiple(tuples_excel)
		return None

	# IMPORT EXCEL CRAWLING
	def import_fileExcelCrawling(self):
		excel_file = request.files['excel_file']

		instance_Excel = Excel()
		tuples_excel = instance_Excel.make_tuples_crawling(excel_file)
		# Simpan ke Database dengan VALUES berupa tuple
		instance_Model = Models('REPLACE INTO tbl_tweet_crawling(id, text, user, created_at) VALUES (%s, %s, %s, %s)')
		instance_Model.insert_multiple(tuples_excel)
		return None
