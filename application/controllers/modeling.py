from application.models import Models
from flask import request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
import joblib
from datetime import datetime
from wordcloud import WordCloud

class ModelingController:
	
	def count_dataTraining(self):
		# SELECT data training
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL')
		data_training = instance_Model.select()
		return data_training[0]['jumlah']
	
	def select_dataModel(self):
		instance_Model = Models('SELECT * FROM tbl_model')
		data_model = instance_Model.select()
		return data_model
	
	def create_dataModeling(self):
		sample_positive = request.form['sample_positive']
		sample_negative = request.form['sample_negative']
		# sample_netral = request.form['sample_netral']
		jumlah_sample = int(sample_positive) + int(sample_negative)
		# jumlah_sample = int(sample_positive) + int(sample_negative) + int(sample_netral)

		# if sample_positive == sample_negative == sample_netral:
		if sample_positive == sample_negative:
			list_data = [] # wadah untuk menyimpan data yang diperoleh dari database

			# Select data positif dari tbl_tweet_training sebanyak n record (berdasarkan variabel sample)
			instance_Model = Models("SELECT clean_text, sentiment_type FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type = 'positif' ORDER BY RAND() LIMIT "+ sample_positive)
			list_data.append(instance_Model.select())
			# Select data negatif dari tbl_tweet_training sebanyak n record (berdasarkan variabel sample)
			instance_Model = Models("SELECT clean_text, sentiment_type FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type = 'negatif' ORDER BY RAND() LIMIT "+ sample_negative)
			list_data.append(instance_Model.select())
			# Select data netral dari tbl_tweet_training sebanyak n record (berdasarkan variabel sample)
			# instance_Model = Models("SELECT clean_text, sentiment_type FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type = 'netral' ORDER BY RAND() LIMIT "+ sample_netral)
			# list_data.append(instance_Model.select())

			x_train = [] # wadah untuk tweet (clean_text) yang akan dijadikan sebagai model latih
			y_train = [] # wadah untuk sentimen (sentiment_type) yang akan dijadikan sebagai model latih

			tweet_positive = [] # wadah untuk menampung data clean_text positif guna visualisasi word clound
			tweet_negative = [] # wadah untuk menampung data clean_text negatif guna visualisasi word clound
			# tweet_netral = [] # wadah untuk menampung data clean_text netral guna visualisasi word clound

			# set data untuk x_train dan y_train menggunakan data yang telah diambil dari database
			# for index_luar in range(3):
			for index_luar in range(2):
				for index_dalam in range(len(list_data[index_luar])):
					clean_text = list_data[index_luar][index_dalam]['clean_text']
					sentiment_type = list_data[index_luar][index_dalam]['sentiment_type']

					x_train.append(clean_text)
					y_train.append(sentiment_type)

					if sentiment_type == 'positif':
						tweet_positive.append(clean_text)
					elif sentiment_type == 'negatif':
						tweet_negative.append(clean_text)
					# else:
					# 	tweet_netral.append(clean_text)
			
			# Membuat wordcloud menggunakan list tweet positif
			wordcloud = WordCloud(width = 800, height = 400, background_color='black', collocations=False).generate((" ").join(tweet_positive))
			wordcloud.to_file('application/static/wordcloud/wordcloud_modelingPositive.png')
			# Membuat wordcloud menggunakan list tweet negatif
			wordcloud = WordCloud(width = 800, height = 400, background_color='black', collocations=False).generate((" ").join(tweet_negative))
			wordcloud.to_file('application/static/wordcloud/wordcloud_modelingNegative.png')
			# Membuat wordcloud menggunakan list tweet netral
			# wordcloud = WordCloud(width = 1000, height = 600, background_color='black', collocations=False).generate((" ").join(tweet_netral))
			# wordcloud.to_file('application/static/wordcloud/wordcloud_netral.png')
			
			# Inisialisasi jenis vectorizer dan algoritme yang akan digunakan untuk membuat model
			instance_Vectorizer = CountVectorizer()
			instance_Classification = KNeighborsClassifier(n_neighbors=3, algorithm='brute', metric='euclidean')

			# Konfigurasi model dengan vectorizer dan algoritme
			model = Pipeline([('vectorizer', instance_Vectorizer), ('classifier', instance_Classification)])
			
			# Membuat model dengan data latih
			model.fit(x_train, y_train)

			# Menyimpan model kedalam bentuk .joblib agar dapat digunakan kembali (untuk proses Evaluasi & Prediksi)
			model_name = 'sentiment_model('+ datetime.today().strftime('%d-%m-%Y') +').pkl'
			joblib.dump(model, 'application/static/model_data/'+ model_name)

			# Membuat tuple untuk simpan data
			data_simpan = (model_name, jumlah_sample, sample_positive, sample_negative)

			# Insert model ke dalam database
			instance_Model = Models('REPLACE INTO tbl_model(model_name, sentiment_count, sentiment_positive, sentiment_negative) VALUES (%s, %s, %s, %s)')
			# Menjadikan tuple sebagai argumen untuk method query_sql
			instance_Model.query_sql(data_simpan)

			return { 'model_name': model_name, 'sentiment_count': jumlah_sample, 'sentiment_positive': sample_positive, 'sentiment_negative': sample_negative }
		return  { 'error': 'Gagal Membuat Model Latih' }
	
	def delete_dataModelling(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_model WHERE model_name = %s')
		instance_Model.query_sql(id)
	
	def count_sampleSentiment(self):
		# SELECT jumlah data training berdasarkan jenis sentimen
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL GROUP BY sentiment_type')
		data_max_sentiment = instance_Model.select()

		min = 999999	# asumsi jumlah minimal sentimen tidak lebih dari 999999
		# mencari jumlah minimal sentimen
		for data in data_max_sentiment:
			if data['jumlah'] < min:
				min = data['jumlah']
		
		if min == 999999:
			min = 0
		
		# nilai variable 'min' digunakan sebagai batas atas sample sentimen & nilai 'min*2' digunakan untuk mengetahui jumlah kuota sample
		return min, min*2
    