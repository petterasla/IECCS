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
strength = 'soft'
validate = 1
test = 1
if test:
    print("Applying on test data")
else:
    print("Not using test")

# ***** LOAD DATA STANCE VS NO STANCE   *****
if test:
    d1 = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
    d2 = pd.read_csv('../TextFiles/data/tcp_validate.csv', sep='\t')
    data = pd.concat([d1, d2])
else:
    data = d1 = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')

binaryStances = []
for endorse in data.Endorse.tolist():
    binaryStances.append(ptd.getAbstractStanceVsNoStance(strength, endorse))

if validate:
    if test:
        dataVal = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
    else:
        dataVal = pd.read_csv('../TextFiles/data/tcp_validate.csv', sep='\t')
    binaryStancesVal = []
    for endorseVal in dataVal.Endorse.tolist():
        binaryStancesVal.append(ptd.getAbstractStanceVsNoStance(strength, endorseVal))


cv = StratifiedKFold(binaryStances, n_folds=10, shuffle=True, random_state=1)

# ***** CLASSIFIER  *****
clf = LinearSVC(C=1.9306977288832496)
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    #MultinomialNB(alpha=0.5)

# ***** TRAIN CLASSIFIERS   *****
print 80 * "="
print clf
print 80 * "="

# Use optimized parameters from grid_search_improved
pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                              analyzer='word',
                                              ngram_range=(1,3),
                                              stop_words=None,
                                              max_features=None)),
                     ('tfidf', TfidfTransformer(use_idf=True)),
                     ('clf', clf)])

if validate:
    pipeline.fit(data.Abstract, binaryStances)
    pred_stances = pipeline.predict(dataVal.Abstract)

    print classification_report(binaryStancesVal, pred_stances, digits=4)

    macro_f = fbeta_score(binaryStancesVal, pred_stances, 1.0,
                          labels=['STANCE', 'NONE'],
                          pos_label='STANCE',
                          average='macro')

else:
    pred_stances = cross_val_predict(pipeline, data.Abstract, binaryStances, cv=cv, n_jobs=10)

    print classification_report(binaryStances, pred_stances, digits=4)

    macro_f = fbeta_score(binaryStances, pred_stances, 1.0,
                          labels=['STANCE', 'NONE'],
                          pos_label='STANCE',
                          average='macro')


print 'macro-average of F-score(STANCE) and F-score(NONE): {:.4f}\n'.format(macro_f)

print 80 * '#'
print 80 * '#'

if test:
    d3 = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')
    d4 = pd.read_csv('../TextFiles/data/tcp_validate.csv', sep='\t')
    data2 = pd.concat([d3, d4])
    data2 = data2[data2.Stance != 'NONE']
else:
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
clf2 = LinearSVC(C=37.275937203149383)
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    #MultinomialNB(alpha=0.5)

# ***** TRAIN CLASSIFIERS   *****
print 80 * "="
print clf2
print 80 * "="

# Use optimized parameters from grid_search_improved
pipeline2 = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                              analyzer='word',
                                              ngram_range=(1,1),
                                              stop_words='english',
                                              max_features=None)),
                     ('tfidf', TfidfTransformer(use_idf=False)),
                     ('clf', clf2)])

if validate:
    pipeline2.fit(data2.Abstract, data2.Stance)

    pred_stances2 = pipeline2.predict(dataVal.Abstract)

    print classification_report(dataVal.Stance, pred_stances2, digits=4)

    macro_f2 = fbeta_score(dataVal.Stance, pred_stances2, 1.0,
                           labels=['FAVOR', 'AGAINST'],
                           pos_label='FAVOR',
                           average='macro')


else:
    pipeline2.fit(data2.Abstract, data2.Stance)

    pred_stances2 = pipeline2.predict(data.Abstract)

    print classification_report(data.Stance, pred_stances2, digits=4)

    macro_f2 = fbeta_score(data.Stance, pred_stances2, 1.0,
                          labels=['FAVOR', 'AGAINST'],
                          pos_label='FAVOR',
                          average='macro')

print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f2)


print "time = " , time.time()-start_time
