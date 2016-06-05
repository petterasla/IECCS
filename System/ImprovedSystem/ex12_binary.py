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
from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import MultinomialNB

import pandas as pd

# ***** SETTINGS   *****
strength = 'soft'
validate = 1
if validate:
    print("Validating")
else:
    print("Training")

# ***** LOAD DATA STANCE VS NO STANCE   *****

data = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')

binaryStances = []
for endorse in data.Endorse.tolist():
    binaryStances.append(ptd.getAbstractStanceVsNoStance(strength, endorse))

if validate:
    dataVal = pd.read_csv('../TextFiles/data/tcp_validate.csv', sep='\t')
    binaryStancesVal = []
    for endorseVal in dataVal.Endorse.tolist():
        binaryStancesVal.append(ptd.getAbstractStanceVsNoStance(strength, endorseVal))


cv = StratifiedKFold(binaryStances, n_folds=10, shuffle=True, random_state=1)

# ***** CLASSIFIER  *****
clf = SVC(C=0.1, kernel='linear')
#clf = LinearSVC(C=1.9306977288832496)
#clf = MultinomialNB(alpha=0.1, fit_prior=False)


# Use optimized parameters from grid_search_improved
pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                              analyzer='word',
                                              ngram_range=(1, 1),
                                              stop_words=None,
                                              max_features=None)),
                     ('tfidf', TfidfTransformer(use_idf=True)),
                     ('clf', clf)])


if validate:
    # ***** TRAIN CLASSIFIERS   *****
    print 80 * "="
    print "VALIDATE: STANCE VS NO STANCE"
    print 80 * "="
    print pipeline.named_steps
    print 80 * "="
    pipeline.fit(data.Abstract, binaryStances)
    pred_stances = pipeline.predict(dataVal.Abstract)

    print classification_report(binaryStancesVal, pred_stances, digits=4)

    #macro_f = fbeta_score(binaryStancesVal, pred_stances, 1.0,
    #                      labels=['STANCE', 'NONE'],
    #                      pos_label='STANCE',
    #                      average='macro')

    precision, recall, fscore, support = precision_recall_fscore_support(binaryStancesVal, pred_stances, average=None)
    fscore_none = fscore[0]
    print 'macro-average of F-score(STANCE) and F-score(NONE): {:.4f}\n'.format(sum(fscore)/len(fscore))
else:
    # ***** TRAIN CLASSIFIERS   *****
    print 80 * "="
    print "TRAIN: STANCE VS NO STANCE"
    print 80 * "="
    print pipeline.named_steps
    print 80 * "="


    pred_stances = cross_val_predict(pipeline, data.Abstract, binaryStances, cv=cv, n_jobs=10)

    print classification_report(binaryStances, pred_stances, digits=4)

    #macro_f = fbeta_score(binaryStances, pred_stances, 1.0,
    #                      labels=['STANCE', 'NONE'],
    #                      pos_label='STANCE',
    #                      average='binary')

    precision, recall, fscore, support = precision_recall_fscore_support(binaryStances, pred_stances, average=None)
    fscore_none = fscore[0]
    print 'macro-average of F-score(STANCE) and F-score(NONE): {:.4f}\n'.format(sum(fscore)/len(fscore))

print 80 * '#'
print 80 * '#'


data2 = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
data2 = data2[data2.Stance != 'NONE']

if validate:
    for index, row in dataVal.iterrows():
        if (pred_stances[index] == 'NONE'):
            dataVal.drop(index, inplace=True)
else:
    for index, row in data.iterrows():
        if (pred_stances[index] == 'NONE'):
            data.drop(index, inplace=True)


# Select classifiers to use
#clf2 = SVC(C=0.1, kernel='linear')
#clf2 = LinearSVC(C=37.2)
clf2 = MultinomialNB(alpha=0.1, fit_prior=False)

# ***** TRAIN CLASSIFIERS   *****


# Use optimized parameters from grid_search_improved
pipeline2 = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                               analyzer='word',
                                               ngram_range=(2, 3),
                                               stop_words='english',
                                               max_features=None)),
                      ('tfidf', TfidfTransformer(use_idf=True)),
                      ('clf', clf2)])

if validate:
    print 80 * "="
    print "VALIDATE: FAVOR VS AGAINST"
    print 80 * "="
    print pipeline.named_steps
    print 80 * "="
    pipeline2.fit(data2.Abstract, data2.Stance)

    pred_stances2 = pipeline2.predict(dataVal.Abstract)

    print classification_report(dataVal.Stance, pred_stances2, digits=4)

    #macro_f2 = fbeta_score(dataVal.Stance, pred_stances2, 1.0,
    #                       labels=['FAVOR', 'AGAINST'],
    #                       pos_label='FAVOR',
    #                       average='macro')
    precision, recall, fscore, support = precision_recall_fscore_support(dataVal.Stance, pred_stances2, average=None)
    fscore_against = fscore[0]
    fscore_favor = fscore[1]
    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format((fscore_against+fscore_favor)/2)


else:
    print 80 * "="
    print "TRAIN: FAVOR VS AGAINST"
    print 80 * "="
    print pipeline.named_steps
    print 80 * "="
    pipeline2.fit(data2.Abstract, data2.Stance)

    pred_stances2 = pipeline2.predict(data.Abstract)

    print classification_report(data.Stance, pred_stances2, digits=4)

    #macro_f2 = fbeta_score(data.Stance, pred_stances2, 1.0,
    #                      labels=['FAVOR', 'AGAINST'],
    #                      pos_label='FAVOR',
    #                      average='macro')

    precision, recall, fscore, support = precision_recall_fscore_support(data.Stance, pred_stances2, average=None)

    fscore_against = fscore[0]
    fscore_favor = fscore[1]
    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(sum(fscore)/len(fscore))

print 80 * "="
sum_fscore = fscore_none+fscore_against+fscore_favor
print ("none f score: {}\nfavor f score: {}\nagainst f score: {}".format(fscore_none, fscore_favor, fscore_against))
print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE) is: {:.4f}\n'.format(sum_fscore/3)

print "time = " , time.time()-start_time
