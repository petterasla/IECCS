import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import numpy as np
import pandas as pd
from glob import glob
from System.DataProcessing.GloveVectorizer.glove_transformer import GloveVectorizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.ensemble import VotingClassifier


data = pd.read_csv(open('../TextFiles/data/tcp_train.csv'), sep='\t', index_col=0)

cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)

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

    #vot_clf = VotingClassifier(estimators=[('glove', glove_clf)], voting='hard')

    pred_stances = cross_val_predict(glove_clf, data.Abstract, data.Stance, cv=cv)
    print classification_report(data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR'],
                          average='macro')

    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)