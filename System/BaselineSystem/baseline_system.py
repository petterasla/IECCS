# Fix path for use in terminal ###
import time
start_time = time.time()
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

import time
start_time = time.time()

import System.DataProcessing.process_data as ptd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.svm import LinearSVC


# ***** LOAD DATA   *****
# Retrieve abstracts
abstracts = ptd.getAbstractData()
# Retrieve labels in form of endorsement
endorsement_data = ptd.getEndorsementData()

# Convert endorsement to classes (FAVOR, AGAINST, NONE)
target_data = []
for endorse in endorsement_data.tolist():
    target_data.append(ptd.getAbstractStance('soft', endorse))

cv = StratifiedKFold(target_data, n_folds=10, shuffle=True, random_state=1)

# Select classifiers to use
classifiers = [
    DummyClassifier(strategy='stratified', random_state=None, constant=None),
    DummyClassifier(strategy='most_frequent', random_state=None, constant=None),
    #LinearSVC(C=1.0),
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    #MultinomialNB(alpha=0.5)
]

# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:
    print 80 * "="
    print clf
    print 80 * "="

    pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='word',
                                                  ngram_range=(1,3),
                                                  stop_words=None,
                                                  max_features=None)),
                         ('tfidf', TfidfTransformer(use_idf=True)),
                         ('clf', clf)])

    pred_stances = cross_val_predict(pipeline, abstracts,
                                     target_data, cv=cv, n_jobs=10)

    print classification_report(target_data, pred_stances, digits=4)

    macro_f = fbeta_score(target_data, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score (NONE): {:.4f}\n'.format(macro_f)

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f)

print("--- %s seconds ---" % (time.time() - start_time))

