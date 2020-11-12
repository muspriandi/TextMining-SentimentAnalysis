import pandas
import random
from datetime import datetime

class Excel:
	def __init__(self):
		self.file_excelCrawling = 'application/static/excel_data/data_crawling('+ datetime.today().strftime('%d-%m-%Y') +').xlsx'
	
	# Fungsi untuk menyimpan data_crawling ke dalam file excel(.xlsx)
	def save_excel(self, tweets):
		id = []
		text = []
		username = []
		created_at = []
		
		for tweet in tweets:
			id.append(tweet['id'])
			text.append(str(tweet['full_text']))
			username.append(str(tweet['user']['screen_name']))
			created_at.append(str(tweet['created_at']))
		
		data_frame = pandas.DataFrame({ 'id': id, 'text': text, 'username': username, 'created_at': created_at })
		data_frame.to_excel(self.file_excelCrawling, index=False)
		
		print('\n\nFile excel(.xlsx) berhasil dibuat.\nLokasi: /:root_project/'+ self.file_excelCrawling +'\n\n')
		return None
	
	# Fungsi untuk menambahkan kolom baru(data_type) untuk menyimpan informasi jenis data(0 | 1)
	# 0 = data berjenis data tes	;	1 = data berjenis data latih
	def split_data(self, data_tes, data_latih):
		data_type = [0 for i in range(int(data_tes))]	# Membuat list(data_type) dengan value 0 sebanyak jumlah data_tes
		
		for _ in range(int(data_latih)):	# Perulangan untuk memasukkan value 1 ke dalam list(data_type) pada index random sebanyak jumlah data_latih
			data_type.insert(random.randint(0, len(data_type)), 1)
		
		data_frame = pandas.read_excel(self.file_excelCrawling)
		data_frame['data_type'] = data_type
		data_frame.to_excel(self.file_excelCrawling, index=False)
		return None
	
	# Fungsi untuk membuat tuple dari data excel yang ada
	def make_tuples(self):
		tweets_container = []
		data_frame = pandas.read_excel(self.file_excelCrawling)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(datetime.strftime(datetime.strptime(row['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')),str(row['data_type']))
			tweets_container.append(tweet_tuple)
		return tweets_container
	