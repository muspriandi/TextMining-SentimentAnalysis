from application.models import Models
from flask import request, json
from sklearn.metrics import accuracy_score
import joblib

class EvaluationController:
	
	def select_dataModel(self):
		instance_Model = Models('SELECT * FROM tbl_model')
		data_model = instance_Model.select()
		return data_model
	
	def count_dataTes(self):
		# HITUNG JUMLAH data testing
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_testing WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL')
		data_testing = instance_Model.select()
		return data_testing[0]['jumlah']
	
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
		model = joblib.load('application/static/model_data/' + model_name)
		# Memprediksikan sentimen untuk data 'x_test'
		hasil = model.predict(x_test)

		# Membandingkan hasil prediksi (hasil) dengan sentimen yang sebenarnya (y_test)
		akurasi = accuracy_score(y_test, hasil)
		return json.dumps({ 'akurasi': akurasi, 'teks_database': x_test, 'sentimen_database': y_test, 'sentimen_prediksi': hasil.tolist() })
	
	def select_komposisiModel(self):
		model_name = request.form['model_name']
		instance_Model = Models("SELECT sentiment_count, sentiment_positive, sentiment_negative FROM tbl_model WHERE model_name = '"+ model_name +"'")
		komposisi_model = instance_Model.select()
		return komposisi_model
	
	
    