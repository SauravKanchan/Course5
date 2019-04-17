import pandas as pd
import ast
import time
import re

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import string
import nltk
from nltk.stem import WordNetLemmatizer

import string
import nltk
from nltk.stem import WordNetLemmatizer

filename = 'reviews.csv'
df = pd.read_csv(filename)
df.drop_duplicates(subset=None, inplace=True)
X_train, X_test, y_train, y_test = train_test_split(df['comment'],
                                                    df['stars'],
                                                    test_size=.2, random_state=1)
# instantiate the vectorizer
vect = CountVectorizer()

# tokenize train and test text data
X_train_dtm = vect.fit_transform(X_train)
print(("number words in training corpus:", len(vect.get_feature_names())))

X_test_dtm = vect.transform(X_test)


# nb = MultinomialNB()
# nb.fit(X_train_dtm, y_train)
#
# MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
# y_pred = nb.predict(X_test_dtm)
#
# #calculate accuracy, precision, recall, and F-measure of class predictions
def eval_predictions(y_test, y_pred):
    print('accuracy:', metrics.accuracy_score(y_test, y_pred))


#    print('precision:', metrics.precision_score(y_test, y_pred, average='weighted'))
#    print('recall:', metrics.recall_score(y_test, y_pred, average='weighted'))
#    print('F-measure:', metrics.f1_score(y_test, y_pred, average='weighted'))


def no_punctuation_unicode(text):
    '''.translate only takes str. Therefore, to use .translate in the
    tokenizer in TfidfVectorizer I need to write a function that converts
    unicode -> string, applies .translate, and then converts it back'''
    str_text = str(text)
    no_punctuation = str_text.translate(None, string.punctuation)
    unicode_text = no_punctuation.decode('utf-8')
    return unicode_text


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


stoplist = ['money', 'battery', 'sound', 'fingerprint']

wnl = WordNetLemmatizer()


def prep_review(review):
    lower_case = review.lower()
    no_punct = no_punctuation_unicode(lower_case)
    tokens = nltk.word_tokenize(no_punct)  # weird to tokenize within the vectorizer,
    # but not sure how else to apply functions to each token
    has_letters = [t for t in tokens if re.search('[a-zA-Z]', t)]
    drop_numbers = [t for t in has_letters if not hasNumbers(t)]
    drop_stops = [t for t in drop_numbers if not t in stoplist]
    lemmed = [wnl.lemmatize(word) for word in drop_stops]
    return lemmed


# tokenize train and test text data
# vect = CountVectorizer(tokenizer=prep_review)
# X_train_dtm = vect.fit_transform(X_train)
# X_test_dtm = vect.transform(X_test)
# instantiate and train model
nb = MultinomialNB()
nb.fit(X_train_dtm, y_train)

# evaluate model
y_pred = nb.predict(X_test_dtm)
eval_predictions(y_test, y_pred)

# tfidf_vectorizer_2 = TfidfVectorizer(tokenizer=prep_review, min_df=5, max_df=0.8)


svm_rbf = svm.SVC(kernel='linear', random_state=1)
svm_rbf.fit(X_train_dtm, y_train)
y_pred_2 = svm_rbf.predict(X_test_dtm)

eval_predictions(y_test, y_pred_2)
