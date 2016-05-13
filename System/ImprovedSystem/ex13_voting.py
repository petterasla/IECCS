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
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier

import pandas as pd

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


cv = StratifiedKFold(train_data.Stance, n_folds=10, shuffle=True, random_state=1)

# Select classifiers to use
classifiers = [
    LinearSVC(C=1.178),
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    MultinomialNB(alpha=0.1, fit_prior=False)
    #LogisticRegression()
]

# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:
    print 80 * "="
    print clf
    print 80 * "="

    # Use optimized parameters from grid_search_improved
    svm_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='word',
                                                  ngram_range=(1, 2),
                                                  stop_words=None,
                                                  max_features=None)),
                         ('clf', LinearSVC(C=1.178))])
    mnb_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                 analyzer='word',
                                                 ngram_range=(2, 3),
                                                 stop_words='english',
                                                 max_features=50000)),
                        ('tf-idf', TfidfTransformer(use_idf=True)),
                        ('clf', MultinomialNB(alpha=0.1, fit_prior=False))])

    vot_clf = VotingClassifier(estimators=[('svm', svm_clf),
                                           ('mnb', mnb_clf)],
                               voting='soft',
                               weights=[1, 1])

    pred_stances = cross_val_predict(vot_clf, train_data.Abstract, train_data.Stance, cv=cv, n_jobs=10)

    print classification_report(train_data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(train_data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'],
                          average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f)

    print 80 * "="
    print("Validation score")
    print 80 * "="
    validate_preds = cross_val_predict(vot_clf, validate_data.Abstract,
                                       validate_data.Stance)
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
        svm_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                     analyzer='word',
                                                     ngram_range=(1, 2),
                                                     stop_words=None,
                                                     max_features=None)),
                            ('clf', LinearSVC(C=1.178))])
        mnb_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                 analyzer='word',
                                                 ngram_range=(2, 3),
                                                 stop_words='english',
                                                 max_features=50000)),
                        ('tf-idf', TfidfTransformer(use_idf=True)),
                        ('clf', MultinomialNB(alpha=0.1, fit_prior=False))])

        vot_clf = VotingClassifier(estimators=[('svm', svm_clf),
                                           ('mnb', mnb_clf)],
                               voting='soft',
                               weights=[1, 1]).fit(train_and_validation.Abstract)

        preds = vot_clf.predict(test_data.Abstract)

        print classification_report(test_data.Stance, vot_clf, digits=4)

        macro_f = fbeta_score(test_data.Stance, vot_clf, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')
        print("Test macro F-score: {:.4f}".format(macro_f))

print "time = " , time.time()-start_time
