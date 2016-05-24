# Fix path for use in terminal ###
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

import time
start_time = time.time()

import System.DataProcessing.process_data as ptd
import System.Utilities.helper_feature as helper
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

import pandas as pd
import sklearn



# ***** SETTINGS   *****
use_upsample = 0
use_downsample = 0

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
    train_data = ptd.getTrainingData()
    validate_data = ptd.getValidationData()
    test_data = ptd.getTestData()

if use_upsample:
    data = pd.concat([data, data[data.Stance == "AGAINST"]])

#train_data, validate_data, test_data = helper.lemmatizeAbstracts(train_data, validate_data, test_data)

cv = StratifiedKFold(train_data.Stance, n_folds=10, shuffle=True, random_state=1)

# Select classifiers to use
classifiers = [
    #LinearSVC(C=1.18),
    #SVC(C=0.1, kernel='linear')
    #MultinomialNB(alpha=0.1, fit_prior=True)
    #LogisticRegression(C=22.9, penalty='l2', solver='lbfgs')
    #SGDClassifier(alpha=0.0001, loss='squared_hinge')
    #BernoulliNB(alpha=0.1, fit_prior=True)
]

# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:


    # Use optimized parameters from grid_search_improved
    pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='char',
                                                  ngram_range=(2, 3),
                                                  stop_words=None,
                                                  max_features=50000)),
                         #('tfidf', TfidfTransformer(use_idf=True)),
                         ('clf', clf)])

    print 80 * "="
    print clf
    print pipeline
    print 80 * "="

    pred_stances = cross_val_predict(pipeline, train_data.Abstract, train_data.Stance, cv=cv, n_jobs=10)

    print classification_report(train_data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(train_data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'],
                          average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f)

    print 80 * "="
    print("Validation score")
    print 80 * "="

    pipeline.fit(train_data.Abstract, train_data.Stance)

    validate_preds = pipeline.predict(validate_data.Abstract)

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
        pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                      analyzer='word',
                                                      ngram_range=(1, 3),
                                                      stop_words='english',
                                                      max_features=50000)),
                             ('tfidf', TfidfTransformer(use_idf=True)),
                             ('clf', clf)]) \
            .fit(train_and_validation.Abstract, train_and_validation.Stance)

        test_preds = pipeline.predict(test_data.Abstract)
        print classification_report(test_data.Stance, test_preds, digits=4)

        macro_f = fbeta_score(test_data.Stance, test_preds, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')
        print("Test macro F-score: {:.4f}".format(macro_f))

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