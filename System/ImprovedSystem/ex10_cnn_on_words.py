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

import pandas
import numpy as np
from sklearn import metrics
from sklearn.metrics import fbeta_score
from sklearn.metrics import classification_report

import tensorflow as tf
from tensorflow.contrib import skflow
import System.Utilities.write_to_file as fileWriter

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
EMBEDDING_SIZE = 20
N_FILTERS = 10
WINDOW_SIZE = 20
FILTER_SHAPE1 = [WINDOW_SIZE, EMBEDDING_SIZE]
FILTER_SHAPE2 = [WINDOW_SIZE, N_FILTERS]
POOLING_WINDOW = 4
POOLING_STRIDE = 2

def cnn_model(X, y):
    """2 layer Convolutional network to predict from sequence of words
    to a class."""
    # Convert indexes of words into embeddings.
    # This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
    # maps word indexes of the sequence into [batch_size, sequence_length,
    # EMBEDDING_SIZE].
    word_vectors = skflow.ops.categorical_variable(X, n_classes=n_words,
                                                   embedding_size=EMBEDDING_SIZE, name='words')
    word_vectors = tf.expand_dims(word_vectors, 3)
    with tf.variable_scope('CNN_Layer1'):
        # Apply Convolution filtering on input sequence.
        conv1 = skflow.ops.conv2d(word_vectors, N_FILTERS, FILTER_SHAPE1, padding='VALID')
        # Add a RELU for non linearity.
        conv1 = tf.nn.relu(conv1)
        # Max pooling across output of Convlution+Relu.
        pool1 = tf.nn.max_pool(conv1, ksize=[1, POOLING_WINDOW, 1, 1],
                               strides=[1, POOLING_STRIDE, 1, 1], padding='SAME')
        # Transpose matrix so that n_filters from convolution becomes width.
        pool1 = tf.transpose(pool1, [0, 1, 3, 2])
    with tf.variable_scope('CNN_Layer2'):
        # Second level of convolution filtering.
        conv2 = skflow.ops.conv2d(pool1, N_FILTERS, FILTER_SHAPE2,
                                  padding='VALID')
        # Max across each filter to get useful features for classification.
        pool2 = tf.squeeze(tf.reduce_max(conv2, 1), squeeze_dims=[1])
    # Apply regular WX + B and classification.
    return skflow.models.logistic_regression(pool2, y)


val_monitor = skflow.monitors.ValidationMonitor(X_val, y_val,
                                                early_stopping_rounds=200,
                                                n_classes=3,
                                                batch_size=10,
                                                print_steps=20)
classifier = skflow.TensorFlowEstimator(model_fn=cnn_model, n_classes=3,
                                        steps=100, optimizer='Adam', learning_rate=0.01,
                                        continue_training=True)

# Write results to file
f = fileWriter.initFile("../TextFiles/FindingsAndResults/ex10/ex10")
# Continuously train for 1000 steps & predict on test set.
i = 0
print("Initiating training...")
fileWriter.writeTextToFile("Initiating training...", f)
while i < 11:
    print(80 * '=')
    fileWriter.writeTextToFile(80 * '=' , f)
    classifier.fit(X_train, y_train, val_monitor, logdir='../TextFiles/logs/cnn_on_words/')

    pred_stances = classifier.predict(X_val)

    score = metrics.accuracy_score(y_val, pred_stances)
    print('Accuracy: {0:.2f}'.format(score))
    fileWriter.writeTextToFile('Accuracy: {0:.2f}'.format(score), f)
    print (classification_report(y_val, pred_stances, digits=4))
    fileWriter.writeTextToFile(classification_report(y_val, pred_stances, digits=4), f)

    macro_f = fbeta_score(y_val, pred_stances, 1.0,
                          labels=[0, 1, 2],
                          average='macro')

    print('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f))
    fileWriter.writeTextToFile('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f), f)
    i += 1

print(80 * '#')
fileWriter.writeTextToFile(80 * '#\n' + 80 * '#', f)
pred_stances = classifier.predict(X_test)

score = metrics.accuracy_score(y_test, pred_stances)
print('Accuracy: {0:f}'.format(score))
fileWriter.writeTextToFile("Accuracy: %f" % score, f)
print (classification_report(y_test, pred_stances, digits=4))
fileWriter.writeTextToFile(classification_report(y_test, pred_stances, digits=4), f)

macro_f = fbeta_score(y_test, pred_stances, 1.0,
                      labels=[0, 1, 2],
                      average='macro')

print('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f))
fileWriter.writeTextToFile('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f), f)

"""
RESULTS ACHIEVED
                    precision    recall  f1-score   support

          AGAINST   0.0714    0.1176    0.0889        17
          NONE      0.7777    0.7942    0.7859      1793
          FAVOR     0.5664    0.5348    0.5501       877

    avg / total     0.7043    0.7052    0.7045      2687

macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): 0.4750
"""