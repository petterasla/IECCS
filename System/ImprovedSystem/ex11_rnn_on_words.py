#  Copyright 2015-present The Scikit Flow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from sklearn import metrics
from sklearn.metrics import fbeta_score
from sklearn.metrics import classification_report

import pandas

import tensorflow as tf
from tensorflow.contrib import skflow


def convertToInt(pandas):
    numberedStances = []
    for stance in pandas:
        if stance == 'FAVOR':
            numberedStances.append(2)
        elif stance == 'NONE':
            numberedStances.append(1)
        else:
            numberedStances.append(0)

    return numberedStances


### Load data
print("Loading data...")
data_train = pandas.read_csv(open('../TextFiles/data/tcp_train.csv'), sep='\t', index_col=0)
data_val = pandas.read_csv(open('../TextFiles/data/tcp_validate.csv'), sep='\t', index_col=0)
data_test = pandas.read_csv(open('../TextFiles/data/tcp_test.csv'), sep='\t', index_col=0)
X_train, y_train = data_train.Abstract, pandas.Series(convertToInt(data_train.Stance))
X_val, y_val = data_val.Abstract, pandas.Series(convertToInt(data_val.Stance))
X_test, y_test = data_test.Abstract, pandas.Series(convertToInt(data_test.Stance))
print("Finished loading data...")


### Process vocabulary
print("Processing data...")
MAX_DOCUMENT_LENGTH = 100
print("Max document length: " + str(MAX_DOCUMENT_LENGTH))
vocab_processor = skflow.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
X_train = np.array(list(vocab_processor.fit_transform(X_train)))
X_val = np.array(list(vocab_processor.transform(X_val)))
X_test = np.array(list(vocab_processor.transform(X_test)))

n_words = len(vocab_processor.vocabulary_)
print('Total words: %d' % n_words)
print("Finished processing data...")


### Models
print("Creating models...")
EMBEDDING_SIZE = 50

def average_model(X, y):
    word_vectors = skflow.ops.categorical_variable(X, n_classes=n_words,
                                                   embedding_size=EMBEDDING_SIZE, name='words')
    features = tf.reduce_max(word_vectors, reduction_indices=1)
    return skflow.models.logistic_regression(features, y)

def rnn_model(X, y):
    """Recurrent neural network model to predict from sequence of words
    to a class."""
    # Convert indexes of words into embeddings.
    # This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
    # maps word indexes of the sequence into [batch_size, sequence_length,
    # EMBEDDING_SIZE].
    word_vectors = skflow.ops.categorical_variable(X, n_classes=n_words,
                                                   embedding_size=EMBEDDING_SIZE, name='words')
    # Split into list of embedding per word, while removing doc length dim.
    # word_list results to be a list of tensors [batch_size, EMBEDDING_SIZE].
    word_list = skflow.ops.split_squeeze(1, MAX_DOCUMENT_LENGTH, word_vectors)
    # Create a Gated Recurrent Unit cell with hidden size of EMBEDDING_SIZE.
    cell = tf.nn.rnn_cell.GRUCell(EMBEDDING_SIZE)
    # Create an unrolled Recurrent Neural Networks to length of
    # MAX_DOCUMENT_LENGTH and passes word_list as inputs for each unit.
    _, encoding = tf.nn.rnn(cell, word_list, dtype=tf.float32)
    # Given encoding of RNN, take encoding of last step (e.g hidden size of the
    # neural network of last step) and pass it as features for logistic
    # regression over output classes.
    return skflow.models.logistic_regression(encoding, y)

val_monitor = skflow.monitors.ValidationMonitor(X_val, y_val,
                                                early_stopping_rounds=3,
                                                n_classes=3,
                                                print_steps=5)

classifier = skflow.TensorFlowEstimator(model_fn=rnn_model, n_classes=3,
                                        steps=1000, optimizer='Adam', learning_rate=0.01,
                                        continue_training=True)

# Continuously train for 1000 steps & predict on test set.
i = 0
print("Initiating training...")
while i < 15:
    print(80 * '=')
    classifier.fit(X_train, y_train, val_monitor, logdir='../TextFiles/logs/rnn_on_words/')

    pred_stances = classifier.predict(X_val)

    score = metrics.accuracy_score(y_val, pred_stances)
    print('Accuracy: {0:f}'.format(score))

    print (classification_report(y_val, pred_stances, digits=4))

    macro_f = fbeta_score(y_val, pred_stances, 1.0,
                          labels=[0, 1, 2],
                          average='macro')

    print('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f))
    i += 1

pred_stances = classifier.predict(X_test)

score = metrics.accuracy_score(y_test, classifier.predict(X_test))
print('Accuracy: {0:f}'.format(score))

print (classification_report(y_test, pred_stances, digits=4))

macro_f = fbeta_score(y_test, pred_stances, 1.0,
                      labels=[0, 1, 2],
                      average='macro')

print('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f))