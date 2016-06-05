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
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

import pandas as pd
import sklearn



strength = 'soft'

# ***** LOAD DATA   *****
train_data = ptd.getTrainingData()
validate_data = ptd.getValidationData()
test_data = ptd.getTestData()

cv = StratifiedKFold(train_data.Stance, n_folds=10, shuffle=True, random_state=1)

# Select classifiers to use
classifiers = [
    LinearSVC(C=2.3988329190194899, multi_class='crammer_singer'),
    #SVC(C=5.2, kernel='linear')
    #MultinomialNB(alpha=0.63, fit_prior=True)
    #LogisticRegression(C=22.759, penalty='l2', solver='lbfgs')
    #SGDClassifier(alpha=0.0001, loss='squared_hinge')
    #BernoulliNB(alpha=0.1, fit_prior=True)
]

# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:


    # Use optimized parameters from grid_search_improved
    pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='word',
                                                  ngram_range=(1, 1),
                                                  stop_words='english',
                                                  max_features=None)),
                         ('tfidf', TfidfTransformer(use_idf=False)),
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

    validate_preds = pipeline.predict(validate_data.Abstract)#cross_val_predict(pipeline, validate_data.Abstract,
                     #                  validate_data.Stance)
    print classification_report(validate_data.Stance, validate_preds, digits=4)

    macro_f = fbeta_score(validate_data.Stance, validate_preds, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')
    print("Validation macro F-score: {:.4f}\n\n".format(macro_f))

#################################
#                               #
#       Testing procedure       #
#                               #
#################################
# check_test = 0
# if check_test:
#     train_and_validation = pd.concat([train_data, validate_data])
#     for clf in classifiers:
#         print 80 * "="
#         print "TEST RESULTS FOR"
#         print clf
#         print 80 * "="
#         pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
#                                                       analyzer='word',
#                                                       ngram_range=(1, 1),
#                                                       stop_words= None,
#                                                       max_features=10000)),
#                              #('tfidf', TfidfTransformer(use_idf=True)),
#                              ('clf', clf)]) \
#             .fit(train_and_validation.Abstract, train_and_validation.Stance)
#
#         test_preds = pipeline.predict(test_data.Abstract)
#         print classification_report(test_data.Stance, test_preds, digits=4)
#
#         macro_f = fbeta_score(test_data.Stance, test_preds, 1.0,
#                               labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')
#         print("Test macro F-score: {:.4f}".format(macro_f))

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