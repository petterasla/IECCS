from __future__ import print_function
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../../"))


import System.DataProcessing.process_data as ptd
from pprint import pprint
from time import time
import logging
import pandas as pd
import System.Utilities.write_to_file as write
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC, SVC
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.cross_validation import StratifiedKFold
from sklearn.preprocessing import FunctionTransformer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import SGDClassifier, LogisticRegression

file = write.initFile("ex12-linearSVC-part2")

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


###############################################################################
# Load
strength = 'soft'

#data = pd.read_csv('../../TextFiles/data/tcp_train.csv', sep='\t')
data = ptd.getTrainingData()
data = data[data.Stance != 'NONE']

cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)

print("%d training documents" % len(data.Abstract))
write.writeTextToFile("%d training documents" % len(data.Abstract),file)
print("%d categories" % 3)
write.writeTextToFile("%d categories" % 3,file)
print()

###############################################################################
# Classifiers
# MultinomialNB(), BernoulliNB(), SVM(), LinearSVM(), SGDClassifier(), LogisticRegression()
clf = MultinomialNB()

print("Using train, validation and test approach with clf {}".format(clf))
write.writeTextToFile("Using train, validation and test approach with clf {}".format(clf), file)

###############################################################################
# define a pipeline combining a text feature extractor with a simple classifier
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', clf)
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
parameters = {
    'vect__analyzer': ['word'],
    'vect__ngram_range': [(1, 1), (1, 2), (1, 3), (2, 3)],
    'vect__stop_words': [None, 'english'],
    #'vect__max_features': (None, 50000),
    'tfidf__use_idf': (True, False),
    #'clf__alpha': np.logspace(-1, 0, 5),
    'clf__fit_prior': [True, False],
    #'clf__kernel': ['linear'],
    #'clf__C': np.logspace(-1, 1.3, 6),
    #'clf__penalty': ['l2'],
    #'clf__solver': ['newton-cg', 'lbfgs']
    #'clf__loss': ['modified_huber', 'squared_hinge', 'perceptron'],
    'clf__alpha': np.logspace(-1, 0.5, 4)
}
if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=10, verbose=1, cv=cv,
                               scoring='f1_macro')

    print("Performing grid search...")
    write.writeTextToFile("Performing grid search...",file)
    print("pipeline:", [name for name, _ in pipeline.steps])
    write.writeTextToFile("pipeline:" % [name for name, _ in pipeline.steps],file)
    print("parameters:")
    write.writeTextToFile("parameters:",file)
    pprint(parameters)
    write.writeTextToFile(parameters,file)
    t0 = time()
    grid_search.fit(data.Abstract, data.Stance)
    print("done in %0.3fs" % (time() - t0))
    write.writeTextToFile("Done in %0.3fs " % (time() - t0), file)
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    write.writeTextToFile("Best score: %0.3f" % grid_search.best_score_, file)
    print("Best parameters set:")
    write.writeTextToFile("Best parameters set:", file)
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
        write.writeTextToFile("\t%s: %r" % (param_name, best_parameters[param_name]), file)


file.close()