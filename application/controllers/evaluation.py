from application.models import Models
from application.vectorizer import Vectorizer
from application.knearestneighbors import KNearestNeighbors
from flask import request, json
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
		nilai_k = int(request.form['nilai_k'])
		model_name = request.form['model_name']
		# Select data dari tbl_tweet_testing yang telah diberi label
		instance_Model = Models('SELECT clean_text, sentiment_type FROM tbl_tweet_testing WHERE sentiment_type IS NOT NULL')
		tweet_testing_label = instance_Model.select()
		
		teks_list = []
		label_list = []
		for tweet in tweet_testing_label:
			teks_list.append(tweet['clean_text'])
			label_list.append(tweet['sentiment_type'])
		
		# Memuat kembali model yang telah dibuat pada proses Pemodelan
		model = json.load(open('application/static/model_data/' +model_name))
		
		# akses ke kelas Vectorizer
		instance_Vectorizer = Vectorizer(teks_list, label_list)
		# membuat vektor berdasarkan model latih
		vector_list = instance_Vectorizer.test_vectorList(model)

		# akses ke kelas KNearestNeighbors
		instance_Klasification = KNearestNeighbors(nilai_k, model)
		data_dict = instance_Klasification.predict_labelList(vector_list)

		confusion_matrix = self.confusion_matrix(label_list, data_dict['label_prediction'])

		# Membandingkan hasil prediksi (hasil) dengan sentimen yang sebenarnya (label_list)
		return json.dumps({ 'teks_database': teks_list, 'sentimen_database': label_list, 'data_dict': data_dict, 'confusion_matrix': confusion_matrix })
	
	def select_komposisiModel(self):
		model_name = request.form['model_name']
		instance_Model = Models("SELECT sentiment_count, sentiment_positive, sentiment_negative FROM tbl_model WHERE model_name = '"+ model_name +"'")
		komposisi_model = instance_Model.select()
		return komposisi_model
	
	def confusion_matrix(self, label_aktual, label_prediksi):
		true_positif = 0
		true_negatif = 0
		false_positif = 0
		false_negatif = 0

		# mencari nilai TP,TN,FP,FN sehingga memperoleh confusion matrix
		for i in range(len(label_aktual)):
			if label_aktual[i] == 'positif':	# label aktual bernilai positif
				if label_aktual[i] == label_prediksi[i]:	# jika sama-sama positif
					true_positif += 1
				else:	# jika label aktual bernilai positif prediksi bernilai negatif
					false_negatif += 1
			else:	# label aktual bernilai negatif
				if label_aktual[i] == label_prediksi[i]:	# jika sama-sama negatif
					true_negatif += 1
				else:	# jika label aktual bernilai negatif prediksi bernilai positif
					false_positif += 1
		
		accuration = (true_positif+true_negatif) / (true_positif+true_negatif+false_positif+false_negatif)
		precision = true_positif / (true_positif+false_positif)
		recall = true_positif / (true_positif+false_negatif)

		return {
			'tp': true_positif,
			'tn': true_negatif,
			'fp': false_positif,
			'fn': false_negatif,
			'accuration': round(accuration, 2),
			'precision': round(precision, 2),
			'recall': round(recall, 2)
		}
	
	
    