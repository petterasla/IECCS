import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import numpy as np
import pandas as pd
from glob import glob
from System.DataProcessing.GloveVectorizer.glove_transformer import GloveVectorizer

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.ensemble import VotingClassifier

validate = 1
testing = 0

data = pd.read_csv(open('../TextFiles/data/tcp_train.csv'), sep='\t', index_col=0)
val = pd.read_csv(open('../TextFiles/data/tcp_validate.csv'), sep='\t', index_col=0)
test = pd.read_csv(open('../TextFiles/data/tcp_test.csv'), sep='\t', index_col=0)

glove_fnames = glob('../DataProcessing/GloveVectorizer/vectors/*.pkl')
glove_ids = [fname.split('/')[-1].split('_')[0] for fname in glove_fnames]

# *****     FINDING BEST VECTOR SPACE     *****
for fname, glove_id in zip(glove_fnames, glove_ids):
    print 80 * '='
    print 'GLOVE VECTORS:', glove_id
    print 80 * '='

    glove_vecs = pd.read_pickle(fname)

    glove_clf = Pipeline([('vect', GloveVectorizer(glove_vecs)),
                          ('clf', LogisticRegression(C=0.1,
                                                     solver='lbfgs',
                                                     multi_class='multinomial',
                                                     class_weight='balanced',
                                                     ))])

    char_clf = Pipeline([('vect', CountVectorizer(analyzer="word",
                                                  ngram_range=(1,2),
                                                  lowercase=True,
                                                  binary=False,
                                                  stop_words=None,
                                                  max_features=None,
                                                  decode_error='ignore')),
                         ('tfidf', TfidfTransformer(use_idf=False)),
                         ('clf', LinearSVC(C=1.17876863, multi_class='ovr'))])

    word_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                   analyzer='word',
                                                   ngram_range=(2, 3),
                                                   stop_words='english',
                                                   max_features=50000)),
                        ('tfidf', TfidfTransformer(use_idf=True)),
                        ('clf', MultinomialNB(alpha=0.1,
                                              fit_prior=False))])

    vot_clf = VotingClassifier(estimators=[('glove', glove_clf),
                                           ('char', char_clf),
                                           ('word', word_clf)],
                               voting='hard')

    if validate:
        vot_clf.fit(data.Abstract, data.Stance)
        
        pred_stances = vot_clf.predict(val.Abstract)

        print classification_report(val.Stance, pred_stances, digits=4)

        macro_f = fbeta_score(val.Stance, pred_stances, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'],
                              average='macro')


    else:
        cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)

        pred_stances = cross_val_predict(vot_clf, data.Abstract, data.Stance, cv=cv)

        print classification_report(data.Stance, pred_stances, digits=4)

        macro_f = fbeta_score(data.Stance, pred_stances, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'],
                              average='macro')

    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)

    if testing:
        merged = pd.concat([data, val])
        vot_clf.fit(merged.Abstract, merged.Stance)

        pred_stances = vot_clf.predict(test.Abstract)

        print classification_report(val.Stance, pred_stances, digits=4)

        macro_f = fbeta_score(val.Stance, pred_stances, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'],
                              average='macro')

