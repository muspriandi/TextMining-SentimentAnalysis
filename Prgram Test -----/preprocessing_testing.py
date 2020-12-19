import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas
import random
from datetime import datetime

instance_Stopword = StopWordRemoverFactory()
stopword = instance_Stopword.create_stop_word_remover()
# Inisialisasi Konfigurasi Library Sastrawi untuk proses 7. Stemming
instance_Stemming = StemmerFactory()
stemmer = instance_Stemming.create_stemmer()

data_frame = pandas.read_excel('negative_word_InSet.xlsx')
		
last_data_slang = []
last_data_slang2 = []
for index, data in data_frame.iterrows():
	result_text = ''
	result_text = str(data['negative_word']).lower()
	result_text = re.sub(r'http\S+|@\S+|#\S+|\d+', '', result_text)
	result_text = (result_text.encode('ascii', 'ignore')).decode("utf-8")
	result_text = result_text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
	result_text = result_text.strip()
	result_text = re.sub('\s+', ' ', result_text)

	for word in result_text.split():
		data_frame2222 = pandas.read_excel('tbl_slangword.xlsx')
		for index22222, data22222 in data_frame2222.iterrows():
			if word == data22222['slangword']:
				result_text = result_text.replace(word, data22222['kata_asli'])

	result_text = stopword.remove(result_text)
	result_text = stemmer.stem(result_text)
	last_data_slang.append(result_text)
	last_data_slang2.append(str(data['negative_weight']))
	print(index)


data_frame = pandas.DataFrame({'negative_word': last_data_slang, 'negative_weight': last_data_slang2})
data_frame.to_excel('negative_word_InSet22222.xlsx', index=False)	
print('\n\nFile excel(.xlsx) berhasil dibuat\n\n')