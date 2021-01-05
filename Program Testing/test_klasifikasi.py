import pandas
from sklearn.neighbors import KNeighborsClassifier

# data_frame = pandas.read_excel('test_vectorizer.xlsx')

# array_df = data_frame.to_numpy()

# corpus_train = array_df[0:5]
# sent_train = ['positif','negatif','positif','positif','positif']
# corpus_tes = array_df[5:]
# sent_tes = ['negatif']

X = [[0], [1], [2], [3]]
y = [0, 0, 1, 1]

# print(len(corpus_train), len(corpus_tes))


klasifikasi = KNeighborsClassifier(n_neighbors=3, metric='manhattan', p=1)
klasifikasi.fit(X, y)
# print(klasifikasi.effective_metric_)

X = klasifikasi.predict_proba([[0.6]])
Y = klasifikasi.kneighbors_graph([[1.6]])
print(Y)

# print(klasifikasi.classes_)
print(X)
print(klasifikasi.predict([[1.6]]))

# data_frame = pandas.DataFrame(data_frame.to_numpy())
# data_frame.to_excel('test_klasifikasi.xlsx', index=False, header=False)

# print(data_frame)