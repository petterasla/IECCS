import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import numpy as np
import pandas as pd
from glob import glob
from System.DataProcessing.GloveVectorizer.glove_transformer import GloveVectorizer
from System.DataProcessing.Word2Vec.word2vec_transformer import Word2VecVectorizer

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.ensemble import VotingClassifier



data = pd.read_csv(open('../TextFiles/data/tcp_train.csv'), sep='\t', index_col=0)
val = pd.read_csv(open('../TextFiles/data/tcp_validate.csv'), sep='\t', index_col=0)
test = pd.read_csv(open('../TextFiles/data/tcp_test.csv'), sep='\t', index_col=0)

glove_fnames = glob('../DataProcessing/GloveVectorizer/vectors/glove.840B.300d_tcp_abstracts.pkl')
glove_ids = [fname.split('/')[-1].split('_')[0] for fname in glove_fnames]

word2vec_fnames = glob('../DataProcessing/Word2Vec/vectors/word2vec_GoogleNews-vectors-negative300_tcp_abstracts.pkl')
word2vec_ids = [fname.split('/')[-1].split('_')[0] for fname in word2vec_fnames]

# *****     FINDING BEST VECTOR SPACE     *****
for fname, glove_id in zip(glove_fnames, glove_ids):
    print 80 * '='
    print 'GLOVE VECTORS:', glove_id, " AND WORD2VEC"
    print 80 * '='

    glove_vecs = pd.read_pickle(fname)
    word2vec_vecs = pd.read_pickle(word2vec_fnames[0])

    glove_clf = Pipeline([('vect', GloveVectorizer(glove_vecs)),
                          ('clf', LogisticRegression(C=0.83,
                                                     solver='lbfgs',
                                                     multi_class='multinomial',
                                                     class_weight='balanced',
                                                     ))])

    word2vec_pipeline = Pipeline([('vect', Word2VecVectorizer(word2vec_vecs)),
                                  ('clf', LogisticRegression(solver='lbfgs',
                                                                    multi_class='multinomial',
                                                                    class_weight='balanced',
                                                                    ))])

    word_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                  analyzer='word',
                                                  ngram_range=(1, 1),
                                                  stop_words='english',
                                                  max_features=None)),
                         ('tfidf', TfidfTransformer(use_idf=False)),
                         ('clf', SVC(C=5.2, kernel='linear', probability=True))])

    vote_pipeline = VotingClassifier(estimators=[('glove', glove_clf),
                                                 ('word2vec', word2vec_pipeline),
                                                 #('mnb', word_clf)
                                                 ],
                                     voting='soft')


    print '\nTRAIN:'
    print 80 * '='
    cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)

    pred_stances = cross_val_predict(vote_pipeline, data.Abstract, data.Stance, cv=cv)

    print classification_report(data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'],
                          average='macro')

    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)

    print 'VALIDATE:'
    print 80 * '='
    vote_pipeline.fit(data.Abstract, data.Stance)

    pred_stances_val = vote_pipeline.predict(val.Abstract)

    print classification_report(val.Stance, pred_stances_val, digits=4)

    macro_f = fbeta_score(val.Stance, pred_stances_val, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'],
                          average='macro')

    print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)

    testing = 0
    if testing:

        print 'TEST:'
        print 80 * '='
        merged = pd.concat([data, val])
        vote_pipeline.fit(merged.Abstract, merged.Stance)

        pred_stances_test = vote_pipeline.predict(test.Abstract)

        print classification_report(test.Stance, pred_stances_test, digits=4)

        macro_f = fbeta_score(test.Stance, pred_stances_test, 1.0,
                              labels=['AGAINST', 'FAVOR', 'NONE'],
                              average='macro')

        print 'macro-average of F-score(FAVOR) and F-score(AGAINST): {:.4f}\n'.format(macro_f)
