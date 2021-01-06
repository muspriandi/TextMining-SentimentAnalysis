from application.models import Models
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import operator

class VisualizationController:
	
	def get_visualisasiHasil(self):
		# HISTOGRAM DISTRIBUSI WAKTU [START]
		instance_Model = Models('SELECT DATE(created_at) as tanggal FROM tbl_tweet_clean WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL')
		data_distribusi_waktuTweet = instance_Model.select()

		# membuat list tanggal
		list_tanggal = [str(data['tanggal']) for data in data_distribusi_waktuTweet]
		
		# set ukuran figure
		plt.subplots(figsize=(25, 10))
		plt.hist(list_tanggal, bins=125)
		# mengatur label
		plt.ylabel('Jumlah Tweet', fontsize=18)
		plt.xlabel('Tanggal Perolehan', fontsize=18)
		plt.xticks(rotation=45)
		# memunculkan garis pada figure
		plt.grid()
		plt.savefig('application/static/matplotlib/hist_distribusi_waktu('+ datetime.today().strftime('%d-%m-%Y') +').png')
		# reset setting matplotlib menjadi default
		plt.cla()
		plt.clf()
		# HISTOGRAM DISTRIBUSI WAKTU [END]

		# PIE CHART SENTIMEN [START]
		instance_Model = Models("SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE clean_text IS NOT NULL AND sentiment_type = 'positif'")
		data_sentimentPositif = instance_Model.select()
		instance_Model = Models("SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE clean_text IS NOT NULL AND sentiment_type = 'negatif'")
		data_sentimentNegatif = instance_Model.select()

		data_P = int(data_sentimentPositif[0]['jumlah'])
		data_N = int(data_sentimentNegatif[0]['jumlah'])

		# membuat persentase data
		jumlah_data = data_P + data_N
		persentase_P = (data_P / jumlah_data) * 100
		persentase_N = (data_N / jumlah_data) * 100
		# membulatkan menjadi 2 desimal di belakang titik (.)
		persentase_P = round(persentase_P, 2)
		persentase_N = round(persentase_N, 2)

		list_countSentiment =[persentase_P, persentase_N]

		# set ukuran figure
		plt.subplots(figsize=(10, 10))
		plt.pie(list_countSentiment, labels=['Positif ('+ str(persentase_P) +' %)', 'Negatif ('+ str(persentase_N) +' %)'], colors=['#00c853', '#ff1744'], startangle = 90)
		plt.legend(title = " Tipe Sentimen ")
		plt.savefig('application/static/matplotlib/pie_sentiment('+ datetime.today().strftime('%d-%m-%Y') +').png')
		# reset setting matplotlib menjadi default
		plt.cla()
		plt.clf()
		# PIE CHART SENTIMEN [END]
		
		# WORDCLOUD SENTIMEN [START]
		instance_Model = Models("SELECT clean_text FROM tbl_tweet_clean WHERE clean_text IS NOT NULL AND sentiment_type = 'positif'")
		data_sentimentPositif = instance_Model.select()
		instance_Model = Models("SELECT clean_text FROM tbl_tweet_clean WHERE clean_text IS NOT NULL AND sentiment_type = 'negatif'")
		data_sentimentNegatif = instance_Model.select()
		
		string_dataPositif = ""
		for data in data_sentimentPositif:
			string_dataPositif += str(data['clean_text'])+ " "
		string_dataNegatif = ""
		for data in data_sentimentNegatif:
			string_dataNegatif += str(data['clean_text'])+ " "

		wordcloud = WordCloud(width = 800, height = 400, background_color='black', collocations=False).generate(string_dataPositif)
		wordcloud.to_file('application/static/wordcloud/wordcloud_visualisasiPositive('+ datetime.today().strftime('%d-%m-%Y') +').png')
		wordcloud = WordCloud(width =  800, height = 400, background_color='black', collocations=False).generate(string_dataNegatif)
		wordcloud.to_file('application/static/wordcloud/wordcloud_visualisasiNegative('+ datetime.today().strftime('%d-%m-%Y') +').png')
		# WORDCLOUD SENTIMEN [END]
		
		counts = {}
		for word in string_dataPositif.split():
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1
		frekuensi_P = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))
		
		counts = {}
		for word in string_dataNegatif.split():
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1
		frekuensi_N = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))

		# set data yang akan dikembalikan
		data = {'jumlah_tweets': len(list_tanggal), 'jumlah_p': data_P, 'jumlah_n': data_N, 'persentase_p': persentase_P, 'persentase_n': persentase_N, 'frekuensi_p': list(frekuensi_P.items())[:10], 'frekuensi_n': list(frekuensi_N.items())[:10], 'waktu': datetime.today().strftime('%d-%m-%Y')}
		
		return data
    