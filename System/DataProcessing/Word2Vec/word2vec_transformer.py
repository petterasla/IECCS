import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))

# For use in Pipeline, patch function 'clone' file sklearn/base.py
# by replacing
#
# equality_test = (new_obj_val == params_set_val or
#                 new_obj_val is params_set_val)
#
# with
#
# equality_test = True
#
# See https://github.com/scikit-learn/scikit-learn/issues/5522

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, word2vec_vectors):
        self.word2vec_vectors = word2vec_vectors

    def fit(self, raw_documents, y=None):
        return self

    def fit_transform(self, raw_documents, y=None):
        return self.transform(raw_documents)

    def transform(self, raw_documents):
        return self.word2vec_vectors.loc[raw_documents].as_matrix()