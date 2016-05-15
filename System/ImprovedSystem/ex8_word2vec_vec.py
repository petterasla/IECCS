import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import numpy as np
import pandas as pd
import System.DataProcessing.process_data as ptd
from glob import glob
from System.DataProcessing.Word2Vec.word2vec_transformer import Word2VecVectorizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.ensemble import VotingClassifier


train_data = ptd.getTrainingDataWithMeta()
validate_data = ptd.getValidationDataWithMeta()
test = ptd.getTestDataWithMeta()

cv = StratifiedKFold(train_data.Stance, n_folds=10, shuffle=True, random_state=1)

word2vec_fnames = glob('../DataProcessing/Word2Vec/vectors/word2vec_GoogleNews-vectors-negative300_tcp_abstracts.pkl')
print word2vec_fnames
word2vec_ids = [fname.split('/')[-1].split('_')[0] for fname in word2vec_fnames]
print word2vec_ids

# *****     FINDING BEST VECTOR SPACE     *****
print 80 * '='
print 'WORD2VEC VECTORS:', word2vec_ids[0]
print 80 * '='

word2vec_vecs = pd.read_pickle(word2vec_fnames[0])

word2vec_clf = Pipeline([('vect', Word2VecVectorizer(word2vec_vecs)),
                      ('clf', LogisticRegression(C=0.1,
                                                 solver='lbfgs',
                                                 multi_class='multinomial',
                                                 class_weight='balanced',
                                                 ))])

#vot_clf = VotingClassifier(estimators=[('word2vec', word2vec_clf)], voting='hard')

pred_stances = cross_val_predict(word2vec_clf, train_data.Abstract, train_data.Stance, cv=cv)
print classification_report(train_data.Stance, pred_stances, digits=4)

macro_f = fbeta_score(train_data.Stance, pred_stances, 1.0,
                      labels=['AGAINST', 'FAVOR', 'NONE'],
                      average='macro')

print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)