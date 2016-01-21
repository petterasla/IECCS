import pandas as pd
import System.DataProcessing.process_data as ptd
import numpy as np

from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline, make_union
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score


abstracts = ptd.getAbstractData()
endorsement_data = ptd.getEndorsementData()
target_data = []
for endorse in endorsement_data.tolist():
    target_data.append(ptd.getAbstractStance('soft'), endorse)

cv = StratifiedKFold(target_data, n_folds=7, shuffle=True,
                     random_state=1)
classifiers = [LinearSVC(C=''), MultinomialNB()]

for clf in classifiers:
    print 80 * "="
    print clf.tostring()
    print 80 * "="

    pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='',
                                                  ngram_range='',
                                                  stop_words=,
                                                  max_features=None)),
                         ('clf', clf)])

    pred_stances = cross_val_predict(pipeline, abstracts,
                                     target_data, cv=cv)

    print classification_report(target_data, pred_stances, digits=4)

    macro_f = fbeta_score(target_data, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR'], average='macro')

    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)



