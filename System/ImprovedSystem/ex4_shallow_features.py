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
from itertools import combinations
import math
import pandas as pd
import cPickle as pickle

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

#FEATURES LEFT OUT: ["reference-feat", ""pub-length-feat", "issue-feat", "volume-feat", "orgs-info"]
leave_out = [ "tfidf","year-feat", "language-feat",
             "reference-feat", 'orgs-feat', "keyword-feat", "month-feat",
             "volume-feat", "type-feat", "issue-feat", "pub-length-feat",
             "author-feat", "doc-type-feat", "subject-feat", "sub-header-feat",
              "header-feat", "LDA-abstract-feat", "title-feat",
             "tokens-title-feat", "tokens-abstract-feat"
             ]
feature_keys = helper.removeFeatureKeys(leave_out)
# NOTE: can also use helper.getFeatureKeys() and set list in getFeatureKeys() method.
# List of feature keys:
# WORKING = ["count-vect", "tfidf", "year-feat", "language-feat",
#           "reference-feat", 'orgs-feat', "keyword-feat", "month-feat",
#            "volume-feat", "type-feat", "issue-feat", "pub-length-feat",
#           "author-feat", "doc-type", "subject-feat", "sub-header-feat",
#           "header-feat", "LDA-abstract-feat", "title-feat"
#           ]
#print("Feature used (number = {}):\n{}".format(len(feature_keys), feature_keys))
#print("Features left out (number = {}):\n{}".format(len(leave_out), leave_out))

#l = ["tokens-abstract-feat", "tokens-title-feat", "LDA-abstract-feat", "title-feat"]
#l = ["language-feat", "reference-feat", "pub-length-feat", "month-feat", "volumne-feat"]
#l = ["subject-feat", "sub-header-feat", "header-feat", "type-feat", "doc-type-feat"]
#l = helper.removeFeatureKeys()
#feature_list = [['subject-feat', 'sub-header-feat', 'header-feat', 'type-feat', 'doc-type-feat', 'count-vect']]
feature_list = [['tokens-title-feat', 'LDA-abstract-feat', 'title-feat', 'count-vect']]

#del feature_list[0]
#feature_list = sum([map(list, combinations(l, i)) for i in range(len(l) + 1)], [])
#for sub in feature_list:
#    sub.append("count-vect")

#print("Number of options: {}".format(len(feature_list)))
# Adding LDA column
train_data, validate_data, test_data = helper.addLDA(train_data, validate_data, test_data)

# Lemmatize abstracts
use_lemming = 1
if use_lemming:
    print("Lemmatizing abstracts and replacing..")
    train_data, validate_data, test_data = helper.lemmatizeAbstracts(train_data, validate_data, test_data)


# Select classifiers to use
# noinspection PyUnboundLocalVariable
classifiers = [
    #LinearSVC(),
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    #MultinomialNB(),
    #SGDClassifier(),
    SVC(C=5.2, kernel='linear')
]

dev_score = []
val_score = []
# ***** TRAIN CLASSIFIERS   *****

print("Start crunching. Time used: {:.1f} minutes".format((time.time()-start_time)/60.0))
for idx, sub_feat_list in enumerate(feature_list):
    print("Crunching on features: {}\nTime used: {:.1f} minutes".format(sub_feat_list, (time.time()-start_time)/60.0))
    for clf in classifiers:
        print 80 * "="
        print clf
        print 80 * "="

        # Use optimized parameters from grid_search_improved
        pipeline = Pipeline([
            ('features', FeatureUnion(helper.getFeatures(sub_feat_list))),
            ('clf', clf)
        ])

        pred_stances = cross_val_predict(pipeline, train_data, train_data.Stance, cv=cv)

        print("Cross validated train score")
        print 80 * "="
        print classification_report(train_data.Stance, pred_stances, digits=4)

        macro_f = fbeta_score(train_data.Stance, pred_stances, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')

        print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score (NONE): {:.4f}\n\n'.format(macro_f)
        dev_score.append({idx: macro_f, "features": sub_feat_list})

        print("Start validation. Time used: {:.1f} minutes".format((time.time()-start_time)/60.0))
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
        val_score.append({idx: macro_f, "features": sub_feat_list})


#################################
#                               #
#       Testing procedure       #
#                               #
#################################
check_test = 1
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

