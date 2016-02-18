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
#use_upsample = 1
#use_downsample = 1

#perform_test_on_unused_data = 1

#downsample_rate_favor = 3
#downsample_rate_none  = 10



strength = 'soft'

# ***** LOAD DATA   *****
# if use_downsample:
#     abstracts_none, labels_none, test_none, test_none_labels        = ptd.getDownsample("NONE", strength, downsample_rate_none)
#     abstracts_favor, labels_favor, test_favor, test_favor_labels    = ptd.getDownsample("FAVOR", strength, downsample_rate_none)
#     abstracts_against, labels_against                               = ptd.getAgainstAbstracts(strength)
#
#     abstracts = pd.concat([abstracts_none, abstracts_favor, abstracts_against])
#     test_abstracts = pd.concat([test_none, test_favor], axis=0)
#
#     target_data = []
#     target_data.extend(labels_none)
#     target_data.extend(labels_favor)
#     target_data.extend(labels_against)
#
#     test_labels = []
#     test_labels.extend(test_none_labels)
#     test_labels.extend(test_favor_labels)
#
# else:

# Retrieve abstracts
abstracts = ptd.getAbstractData()
# Retrieve labels in form of endorsement
endorsement_data = ptd.getEndorsementData()

# Convert endorsement to classes (FAVOR, AGAINST, NONE)
#target_data = []
#for endorse in endorsement_data.tolist():
#    target_data.append(ptd.getAbstractStance(strength, endorse))

binaryStances = []
for endorse in endorsement_data.tolist():
    binaryStances.append(ptd.getAbstractStanceVsNoStance(strength, endorse))

# if use_upsample:
#     againstAbstracts, againstLabels = ptd.getAgainstAbstracts(strength)
#     abstracts = pd.concat([abstracts, againstAbstracts], axis=0)
#     target_data.extend(againstLabels)



cv = StratifiedKFold(binaryStances, n_folds=10, shuffle=True, random_state=1)

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

    pred_stances = cross_val_predict(pipeline, abstracts, binaryStances, cv=cv, n_jobs=10)

    print classification_report(binaryStances, pred_stances, digits=4)

    macro_f = fbeta_score(binaryStances, pred_stances, 1.0,
                          labels=['STANCE', 'NONE'],
                          pos_label='STANCE',
                          average='macro')

    print 'macro-average of F-score(STANCE) and F-score(NONE): {:.4f}\n'.format(macro_f)


print "time = " , time.time()-start_time

# if use_downsample and perform_test_on_unused_data:
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
#    print 'macro-average of F-score(FAVOR), and F-score(NONE): {:.4f}\n'.format(macro_f)