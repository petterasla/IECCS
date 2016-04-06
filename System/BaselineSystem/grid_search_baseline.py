
"""
SVC
Implementation of Support Vector Machine classifier using libsvm: the kernel can be non-linear but its SMO algorithm
does not scale to large number of samples as LinearSVC does. Furthermore SVC multi-class mode is implemented using
one vs one scheme while LinearSVC uses one vs the rest. It is possible to implement one vs the rest with SVC by using
the sklearn.multiclass.OneVsRestClassifier wrapper. Finally SVC can fit dense data without memory copy if the input is
C-contiguous. Sparse data will still incur memory copy though.

sklearn.linear_model.SGDClassifier
SGDClassifier can optimize the same cost function as LinearSVC by adjusting the penalty and loss parameters.
In addition it requires less memory, allows incremental (online) learning, and implements various loss functions and
regularization regimes.
"""

from __future__ import print_function

# Fix path for use in terminal ###
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

import System.DataProcessing.process_data as ptd
from pprint import pprint
from time import time
import logging

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold
import pandas as pd

#print(__doc__)

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


###############################################################################
# Load data
data = pd.read_csv('../TextFiles/data/tcp_train.csv', sep='\t')

cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)


print("%d documents" % len(data))
print()

###############################################################################
# define a pipeline combining a text feature extractor with a simple
# classifier
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    #('clf', MultinomialNB()),
    #('clf', LinearSVC()),
    ('clf', SVC()),
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
parameters = {
    'vect__analyzer': ['word'],
    'vect__ngram_range': [(1, 1), (1,2), (1,3)],
    'vect__stop_words': [None, 'english'],
    'vect__max_features': (None, 50000),
    'tfidf__use_idf': (True, False),
    'clf__kernel': ['rbf', 'linear', 'poly', 'sigmoid'],
    'clf__shrinking': (True, False),
    #'clf__decision_function_shape': ['ovo', 'ovr', None]
}
if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=10, verbose=1, cv=cv)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(abstracts, labels)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))