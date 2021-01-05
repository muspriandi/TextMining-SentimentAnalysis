import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas
import random

instance_Stemming = StemmerFactory()
stemmer = instance_Stemming.create_stemmer()


# NORMALISASI DATA KATA NEGATIF

#data_frame = pandas.read_excel('tbl_lexicon_negative.xlsx')
# last_data = []
# for index, data in data_frame.iterrows():
# 	result_text = str(data['negative_word']).lower()
# 	result_text = (result_text.encode('ascii', 'ignore')).decode("utf-8")
# 	result_text = result_text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
# 	result_text = result_text.strip()
# 	result_text = re.sub('\s+', ' ', result_text)
# 	result_text = stemmer.stem(result_text)
# 	last_data.append(result_text)
# 	print(index)

# data_frame = pandas.DataFrame({'negative_word': last_data})
# data_frame.to_excel('tbl_lexicon_negative NORM.xlsx', index=False)	
# print('\n\nFile excel(.xlsx) berhasil dibuat\n\n')


# NORMALISASI STOWORD BEDASARKAN KAMUS KATA

# data_frame = pandas.read_excel('stopword.xlsx')
# last_data = []
# for index, data in data_frame.iterrows():

# 	result_text = data['stopword']
# 	data_frame2 = pandas.read_excel('tbl_lexicon_negative.xlsx')
# 	for index2, data2 in data_frame2.iterrows():
# 		if result_text == data2['negative_word']:
# 			result_text = '  '
# 	last_data.append(result_text)
# 	print(index)

# data_frame = pandas.DataFrame({'stopword': last_data})
# data_frame.to_excel('stopword NORM.xlsx', index=False)
# print('\n\nFile excel(.xlsx) berhasil dibuat\n\n')