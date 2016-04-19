# Fix path for use in terminal ###
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

import time
start_time = time.time()

import System.DataProcessing.process_data as ptd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.svm import LinearSVC

import pandas as pd

# ***** SETTINGS   *****
use_upsample = 1
use_downsample = 1

#perform_test_on_unused_data = 1

downsample_rate_favor = 0.3
#downsample_rate_none  = 10

strength = 'soft'


if use_downsample:
    data = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
    sub_favor = ptd.getDownsample2_0(data, "FAVOR", strength, downsample_rate_favor)
    against = data[data.Stance == "AGAINST"]

    data = pd.concat([sub_favor, against])

else:
    data = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
    data = pd.concat([data[data.Stance == "FAVOR"], data[data.Stance == "AGAINST"]])

if use_upsample:
    data = pd.concat([data, data[data.Stance == "AGAINST"]])

cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)

# Select classifiers to use
classifiers = [
    LinearSVC(C=0.56234132519034907),
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    #MultinomialNB(alpha=0.5)
]

# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:
    print 80 * "="
    print clf
    print 80 * "="

    # Use optimized parameters from grid_search_improved
    pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='word',
                                                  ngram_range=(1,3),
                                                  stop_words=None,
                                                  max_features=None)),
                         ('tfidf', TfidfTransformer(use_idf=False)),
                         ('clf', clf)])

    pred_stances = cross_val_predict(pipeline, data.Abstract, data.Stance, cv=cv, n_jobs=10)

    print classification_report(data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(data.Stance, pred_stances, 1.0,
                          labels=['FAVOR', 'AGAINST'],
                          pos_label='FAVOR',
                          average='binary')

    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)


print "time = " , time.time()-start_time
