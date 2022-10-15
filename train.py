import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from string import punctuation
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import warnings
warnings.filterwarnings('ignore')

def get_data():
    df = pd.read_csv('data/eksyar_intent.csv')
    return df


def data_prepare():
    col = ['labels', 'questions']
    y = get_data()
    y = y[col]
    y = y[pd.notnull(y['questions'])]
    y.columns = ['labels', 'questions']
    y['category_id'] = y['labels'].factorize()[0]
    category_id_df = y[['labels', 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['category_id', 'labels']].values)
    return y


from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

supportvector =   OneVsRestClassifier(SVC(kernel='rbf', gamma=0.8))
factory = StopWordRemoverFactory()
stop_word_list = factory.get_stop_words()

# stopwords added
stopwords = stop_word_list + list(punctuation)
#create vectorizer
vect = TfidfVectorizer(sublinear_tf=True, min_df=3, norm='l2', encoding='id', ngram_range=(1, 2),stop_words=stopwords)
#create data
df = data_prepare()
features = vect.fit_transform(df.questions).toarray()
labels = df.category_id
# cross validation technique
X_train, X_test, y_train, y_test = train_test_split(df['questions'], df['labels'], random_state=0, test_size=0.5)



# fit and transform X_train into X_train_dtm
X_train_dtm = vect.fit_transform(X_train)
#X_train_dtm.shape


print("X_train")
for i in range(50):
    print(str([i])+" "+str(X_train.iloc[i]))
	
print("X_test")
for i in range(50):
    print(str([i])+" "+str(X_train.iloc[i]))

# transform X_test into X_test_dtm
X_test_dtm = vect.transform(X_test)
#X_test_dtm.shape

# for prec
Y_train_dtm = vect.fit_transform(y_train)
#Y_train_dtm.shape

y_test_dtm = vect.transform(y_test)
#y_test_dtm.shape

# train the model using X_train_dtm
supportvector.fit(X_train_dtm, y_train)

# make class predictions for X_test_dtm
y_pred_class = supportvector.predict(X_test_dtm)

# calculate accuracy of class predictions
from sklearn import metrics
print("\nAccuracy score :")
print(metrics.accuracy_score(y_test, y_pred_class ))

y_test.value_counts()

#print the numbers of data
print("Trained : {0}".format(X_train.shape))
print("Tested: {0}".format(X_test.shape))

#print report
print("Report")
print(metrics.classification_report(y_test, y_pred_class))


# print the confusion matrix
print("Confusion Matrix")
print(metrics.confusion_matrix(y_test, y_pred_class))


