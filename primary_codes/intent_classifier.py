# PENJELASAN FUNGSI LIBRARY
# pandas : penyedia fungsi operasi untuk mengelola data file menjadi data tabel (dataframe)
import pandas as pd
# read string sebagai file
from io import StringIO
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier


def read_data():
    df = pd.read_csv('data/eksyar_intent.csv')
    return df

# fungsi persiapan data
# y menampilkan hasil csv dan kode labels (+category id)
def prepare_data():
    # memanggil df (data jadi objek)
    y = read_data()
    # mengubah labels menjadi angka (0,1,2 - X) dan dimasukan ke array baru
    y['category_id'] = y['labels'].factorize()[0]
    # array nama labels dan category_idnya dimasukan ke variabel dataframe baru (sort untuk menuliskan susunan)
    category_id_df = y[['labels', 'category_id']].drop_duplicates().sort_values('category_id')
    # buat list { 'nama labels' : kode kelas } dimasukan ke variabel dataframe (values biar angka/ kodenya aja)
    category_to_id = dict(category_id_df.values)
    # kebalikan yang diatas wkwk
    id_to_category = dict(category_id_df[['category_id', 'labels']].values)
    return y

def supportvector():
    # memanggil stopword
    factory = StopWordRemoverFactory()
    stop_word_list = factory.get_stop_words()
    stop = stop_word_list + list(punctuation)
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2),
                            stop_words=stop)                          # ambil data + angka class
    df = prepare_data()
    # transform data question ke array (array multilable), seperti magical number [101]
    X_train, X_test, y_train, y_test = train_test_split(df['questions'], df['labels'], random_state=0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = OneVsRestClassifier(SVC(kernel='rbf', gamma='auto')).fit(X_train_tfidf, y_train)
    return clf, count_vect


#X_test.iloc[0]

def predict(question):
    clf, count_vect = supportvector()
    intent = clf.predict(count_vect.transform([question]))
    intent = str(intent).strip("['']")
    return intent

# independet code
# """
# question=input("Masukan pertanyaan")
# x=predict(question)
# intent=str(x).strip("['']")
# print(x)
# """

