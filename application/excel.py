import pandas
import random
from datetime import datetime

class Excel:
	def __init__(self):
		self.file_excelCrawling = 'application/static/excel_data/data_crawling('+ datetime.today().strftime('%d-%m-%Y') +').xlsx'
		self.file_excelPreprocessing = 'application/static/excel_data/data_preprocessing('+ datetime.today().strftime('%d-%m-%Y') +').xlsx'
	
	# Fungsi untuk menyimpan data_crawling ke dalam file excel(.xlsx)
	def save_excel_crawling(self, tweets):
		id = []
		text = []
		username = []
		created_at = []
		
		for tweet in tweets:
			id.append(tweet['id'])
			text.append(str(tweet['full_text']))
			username.append(str(tweet['user']['screen_name']))
			created_at.append(str(tweet['created_at']))
		
		data_frame = pandas.DataFrame({'id': id, 'text': text, 'username': username, 'created_at': created_at})
		data_frame.to_excel(self.file_excelCrawling, index=False)
		
		print('\n\nFile excel(.xlsx) berhasil dibuat.\nLokasi: /:root_project/'+ self.file_excelCrawling +'\n\n')
		return None
	
	# Fungsi untuk menyimpan data hasil preprocessing ke dalam file excel(.xlsx)
	def save_excel_preprocessing(self, result_data):
		id = []
		text = []
		username = []
		created_at = []
		data_type = []
		
		for data in result_data:
			id.append(data['id'])
			text.append(str(data['text']))
			username.append(str(data['username']))
			created_at.append(str(data['created_at']))
			data_type.append(data['data_type'])
		
		data_frame = pandas.DataFrame({'id': id, 'text': text, 'username': username, 'created_at': created_at, 'data_type': data_type})
		data_frame.to_excel(self.file_excelPreprocessing, index=False)
		
		print('\n\nFile excel(.xlsx) berhasil dibuat.\nLokasi: /:root_project/'+ self.file_excelPreprocessing +'\n\n')
		return None
	
	# Fungsi untuk menambahkan kolom baru(data_type) untuk menyimpan informasi jenis data(0 | 1)
	# 0 = data berjenis data tes	;	1 = data berjenis data latih
	def split_data(self, data_tes, data_latih):
		# Membuat list(data_type) dengan value 0 sebanyak jumlah data_tes
		data_type = [0 for i in range(int(data_tes))]
		# Perulangan untuk memasukkan value 1 ke dalam list(data_type) pada index random sebanyak jumlah data_latih
		for _ in range(int(data_latih)):
			data_type.insert(random.randint(0, len(data_type)), 1)
		
		data_frame = pandas.read_excel(self.file_excelCrawling)
		# Menyisipkan kolom dan isian data_type ke dalam excel
		data_frame['data_type'] = data_type
		# Menyimpan kembali file excel (replace)
		data_frame.to_excel(self.file_excelCrawling, index=False)
		return None
	
	# Fungsi untuk membuat tuple dari data excel crawling yang ada
	def make_tuples_crawling(self):
		tweets_container = []
		data_frame = pandas.read_excel(self.file_excelCrawling)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(datetime.strftime(datetime.strptime(row['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')),str(row['data_type']))
			tweets_container.append(tweet_tuple)
		return tweets_container
		
	# Fungsi untuk membuat tuple dari data excel preprocessing yang ada
	def make_tuples_preprocessing(self):
		tweets_container_testing = []
		tweets_container_training = []
		data_frame = pandas.read_excel(self.file_excelPreprocessing)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(row['created_at']))
			if row['data_type'] == 0:
				tweets_container_testing.append(tweet_tuple)
			else:
				tweets_container_training.append(tweet_tuple)
		return tweets_container_testing, tweets_container_training

	# Fungsi untuk membuat tuple dari import excel
	def make_tuples_import(self, excel_file):
		tweets_container = []
		data_frame = pandas.read_excel(excel_file)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(row['created_at']), str(row['data_type']))
			tweets_container.append(tweet_tuple)
		return tweets_container