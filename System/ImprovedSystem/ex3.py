# Fix path for use in terminal ###
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

import time
start_time = time.time()

import System.DataProcessing.process_data as ptd

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.svm import LinearSVC
from sklearn.preprocessing import FunctionTransformer

import pandas as pd

# ***** SETTINGS   *****
use_upsample = 1
use_downsample = 0

downsample_rate_favor = 0.3
downsample_rate_none  = 0.3

strength = 'soft'

# ***** LOAD DATA   *****
if use_downsample:
    data = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
    sub_none = ptd.getDownsample2_0(data, "NONE", strength, downsample_rate_none)
    sub_favor = ptd.getDownsample2_0(data, "FAVOR", strength, downsample_rate_favor)
    against = data[data.Stance == "AGAINST"]

    data = pd.concat([sub_favor, sub_none, against])

else:
    data = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')

if use_upsample:
    data = pd.concat([data, data[data.Stance == "AGAINST"]])


print "None: ", len(data[data.Stance == "NONE"])
print "Against: ", len(data[data.Stance == "AGAINST"])
print "FAVOR: ", len(data[data.Stance == "FAVOR"])

cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)


# Select classifiers to use
classifiers = [
    LinearSVC(C=0.00017782794100389227),
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    #MultinomialNB(alpha=0.5)
]

# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:
    print 80 * "="
    print clf
    print 80 * "="

    # Use optimized parameters from grid_search_improved
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('unigram_word', Pipeline([
                ('vect', CountVectorizer(decode_error='ignore',
                                         analyzer='word',
                                         ngram_range=(1,3),
                                         stop_words=None,
                                         max_features=50000))
            ])),
            ('td-idf', Pipeline([
                ('vect', CountVectorizer(decode_error='ignore',
                                         analyzer='word',
                                         ngram_range=(1,3),
                                         stop_words=None,
                                         max_features=50000)),
                ('tfidf', TfidfTransformer(use_idf=True))
            ])),
            ('year', Pipeline([
                ('year-feat', FunctionTransformer(ptd.yearFeature, validate=False))
            ]))
        ])),
        ('clf', clf)])



    pred_stances = cross_val_predict(pipeline, data.Abstract, data.Stance, cv=cv, n_jobs=10)

    print classification_report(data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'],
                          average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f)


print "time = " , time.time()-start_time

