#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Fix path for use in terminal ###
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

import time
start_time = time.time()

import System.DataProcessing.process_data as ptd
import System.DataProcessing.process_meta_data as meta
import System.Utilities.helper_feature as helper

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.preprocessing import FunctionTransformer
import math
import pandas as pd

# ***** SETTINGS   *****
use_upsample = 0
use_downsample = 0

downsample_rate_favor = 0.3
downsample_rate_none  = 0.3

strength = 'soft'

# ***** LOAD DATA   *****
if use_downsample:
    data = ptd.getTrainingData()
    sub_none = ptd.getDownsample2_0(data, "NONE", strength, downsample_rate_none)
    sub_favor = ptd.getDownsample2_0(data, "FAVOR", strength, downsample_rate_favor)
    against = data[data.Stance == "AGAINST"]

    data = pd.concat([sub_favor, sub_none, against])

else:
    train_data = ptd.getTrainingDataWithMeta()
    validate_data = ptd.getValidationDataWithMeta()
    test_data = ptd.getTestDataWithMeta()



if use_upsample:
    data = pd.concat([data, data[data.Stance == "AGAINST"]])

#print "None: ", len(data[data.Stance == "NONE"])
#print "Against: ", len(data[data.Stance == "AGAINST"])
#print "FAVOR: ", len(data[data.Stance == "FAVOR"])

cv = StratifiedKFold(train_data.Stance, n_folds=10, shuffle=True, random_state=1)


# List of feature keys:
# ["id-idf", "count-vect", "year-feat", "category-feat", "language-feat"]

feature_keys = ['sub-header-feat']
# NOTE: can also use helper.getFeatureKeys() and set list in getFeatureKeys() method.
# WORKING = ["count-vect", "tfidf", "year-feat", "language-feat",
#           "reference-feat", 'orgs-feat', "keyword-feat", "month-feat",
#            "volume-feat", "type-feat", "issue-feat", "pub-length-feat",
#           "author-feat", "doc-type", "subject-feat", "sub-header-feat",
#           "header-feat"
#           ]
# NOT WORKING = []
# Select classifiers to use

classifiers = [
    #LinearSVC(C=0.00017782794100389227),
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    MultinomialNB(alpha=0.1, fit_prior=False)
]

# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:
    print 80 * "="
    print clf
    print 80 * "="

    # Use optimized parameters from grid_search_improved
    pipeline = Pipeline([
        ('features', FeatureUnion(helper.getFeatures(feature_keys))),
        ('clf', clf)
    ])

    pred_stances = cross_val_predict(pipeline, train_data, train_data.Stance, cv=cv)

    print("Cross validated train score")
    print 80 * "="
    print classification_report(train_data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(train_data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score (NONE): {:.4f}\n\n'.format(macro_f)

    print 80 * "="
    print("Validation score")
    print 80 * "="

    validate_preds = pipeline\
        .fit(train_data, train_data.Stance)\
        .predict(validate_data)

    print classification_report(validate_data.Stance, validate_preds, digits=4)

    macro_f = fbeta_score(validate_data.Stance, validate_preds, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')
    print("Validation macro F-score: {:.4f}\n\n".format(macro_f))


#################################
#                               #
#       Testing procedure       #
#                               #
#################################
check_test = 0
if check_test:
    train_and_validation = pd.concat([train_data, validate_data])
    for clf in classifiers:
        print 80 * "="
        print "TEST RESULTS FOR"
        print clf
        print 80 * "="
        pipeline = Pipeline([
                ('features', FeatureUnion(helper.getFeatures(feature_keys))),
                ('clf', clf)
        ]).fit(train_and_validation, train_and_validation.Stance)

        test_preds = pipeline.predict(test_data)
        print classification_report(test_data.Stance, test_preds, digits=4)

        macro_f = fbeta_score(test_data.Stance, test_preds, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')
        print("Test macro F-score: {:.4f}".format(macro_f))

print("Time used {:.1f} in minutes ".format((time.time()-start_time)/60.0))

