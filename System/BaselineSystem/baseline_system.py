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
from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
import pandas as pd


# ***** LOAD DATA   *****
train_data = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
validate_data = pd.read_csv('../TextFiles/data/tcp_validate.csv', sep='\t')
test_data = pd.read_csv('../TextFiles/data/tcp_test.csv', sep='\t')


cv = StratifiedKFold(train_data.Stance, n_folds=10, shuffle=True, random_state=1)

# Select classifiers to use
classifiers = [
    #DummyClassifier(strategy='stratified', random_state=None, constant=None),
    #DummyClassifier(strategy='most_frequent', random_state=None, constant=None),
    #LinearSVC(),
    #SVC(kernel='linear'),
    #MultinomialNB(),
    #BernoulliNB(),
    LogisticRegression(),
    SGDClassifier()
]

print("Running...")
# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:
    print 80 * "="
    print clf
    print 80 * "="

    pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='word',
                                                  ngram_range=(1,1),
                                                  stop_words=None,
                                                  max_features=None)),
                         #('tfidf', TfidfTransformer(use_idf=True)),
                         ('clf', clf)])

    pred_stances = cross_val_predict(pipeline, train_data.Abstract,
                                     train_data.Stance, cv=cv)

    print("Cross validated train score")
    print 80 * "="
    print classification_report(train_data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(train_data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score (NONE): {:.4f}\n\n'.format(macro_f)

    print 80 * "="
    print("Validation score")
    print 80 * "="
    validate_preds = cross_val_predict(pipeline, validate_data.Abstract,
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
check_test = 1
if check_test:
    train_and_validation = pd.concat([train_data, validate_data])
    for clf in classifiers:
        print 80 * "="
        print "TEST RESULTS FOR"
        print clf
        print 80 * "="
        pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                      analyzer='word',
                                                      ngram_range=(1,1),
                                                      stop_words=None,
                                                      max_features=None)),
                             #('tfidf', TfidfTransformer(use_idf=True)),
                             ('clf', clf)])\
            .fit(train_and_validation.Abstract, train_and_validation.Stance)

        test_preds = pipeline.predict(test_data.Abstract)
        print classification_report(test_data.Stance, test_preds, digits=4)

        macro_f = fbeta_score(test_data.Stance, test_preds, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'], average='macro')
        print("Test macro F-score: {:.4f}".format(macro_f))
print("--- %s seconds ---" % (time.time() - start_time))

