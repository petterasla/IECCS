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

downsample_rate_favor = 0.5
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
                          labels=['AGAINST', 'FAVOR', 'NONE'],
                          average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f)


print "time = " , time.time()-start_time

# if use_downsample and perform_test_on_unused_data:
#     ## Noe buggy her!!
#     print "Testing with unused data: "
#
#     pipeline.fit(abstracts, target_data)
#
#     pred_stances_test = pipeline.predict(test_abstracts)
#
#     print classification_report(test_labels, pred_stances_test, digits=4)
#
#     macro_f = fbeta_score(test_labels, pred_stances_test, 1.0,
#                           labels=['FAVOR', 'NONE'],
#                           average='macro')
#
#     print 'macro-average of F-score(FAVOR), and F-score(NONE): {:.4f}\n'.format(macro_f)