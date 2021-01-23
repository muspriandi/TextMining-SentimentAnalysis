import pandas
from sklearn.feature_extraction.text import CountVectorizer

data_frame = pandas.read_excel('sample_data.xlsx')

corpus = []
for index, row in data_frame.iterrows():
    if index < 5:
        corpus.append(row['clean_text'])

# print(corpus)

# corpus = [
#     'This is the first document.',
#     'This document is the second document.',
#     'And this is the third one.',
#     'Is this the first document?',
# ]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(corpus)

# print(corpus)
# print(vectorizer.get_feature_names())
# print(X.shape)

data_frame = pandas.DataFrame(X.toarray(), columns =vectorizer.get_feature_names())
data_frame.to_excel('test_vectorizer.xlsx', index=False)

print(data_frame)