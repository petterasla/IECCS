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

"""
This is an example of using convolutional networks over characters
for DBpedia dataset to predict class from description of an entity.
This model is similar to one described in this paper:
   "Character-level Convolutional Networks for Text Classification"
   http://arxiv.org/abs/1509.01626
and is somewhat alternative to the Lua code from here:
   https://github.com/zhangxiangxiao/Crepe
"""

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

def findMaxLength(abstracts):
    max = 0
    for abstract in abstracts:
        if len(abstract) > max:
            max = len(abstract)
    return max


### Loading data
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
MAX_DOCUMENT_LENGTH = 100 #findMaxLength(data_train.Abstract)
print("Max document length: " + str(MAX_DOCUMENT_LENGTH))

char_processor = skflow.preprocessing.ByteProcessor(MAX_DOCUMENT_LENGTH)
X_train = np.array(list(char_processor.fit_transform(X_train)))
X_val = np.array(list(char_processor.transform(X_val)))
X_test = np.array(list(char_processor.transform(X_test)))
print("Finished processing data...")


### Models
print("Creating models...")
N_FILTERS = 10
FILTER_SHAPE1 = [20, 256]
FILTER_SHAPE2 = [20, N_FILTERS]
POOLING_WINDOW = 4
POOLING_STRIDE = 2

def char_cnn_model(X, y):
    """Character level convolutional neural network model to predict classes."""
    byte_list = tf.reshape(skflow.ops.one_hot_matrix(X, 256),
                           [-1, MAX_DOCUMENT_LENGTH, 256, 1])
    with tf.variable_scope('CNN_Layer1'):
        # Apply Convolution filtering on input sequence.
        conv1 = skflow.ops.conv2d(byte_list, N_FILTERS, FILTER_SHAPE1, padding='VALID')
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
                                                early_stopping_rounds=3,
                                                n_classes=3,
                                                print_steps=5)
classifier = skflow.TensorFlowEstimator(model_fn=char_cnn_model, n_classes=3,
                                        steps=100, optimizer='Adam', learning_rate=0.01,
                                        continue_training=True)

# Continuously train for 1000 steps & predict on test set.
i = 0
print("Initiating training...")
while i<15:
    print(80 * '=')
    classifier.fit(X_train, y_train, val_monitor, logdir='../TextFiles/logs/cnn_on_characters')

    pred_stances = classifier.predict(X_val)

    score = metrics.accuracy_score(y_val, pred_stances)
    print("Accuracy: %f" % score)

    print (classification_report(y_val, pred_stances, digits=4))

    macro_f = fbeta_score(y_val, pred_stances, 1.0,
                          labels=[0, 1, 2],
                          average='macro')

    print('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f))
    i += 1

print(80 * '#')

pred_stances = classifier.predict(X_test)

score = metrics.accuracy_score(y_test, pred_stances)
print("Accuracy: %f" % score)

print (classification_report(y_test, pred_stances, digits=4))

macro_f = fbeta_score(y_test, pred_stances, 1.0,
                      labels=[0, 1, 2],
                      average='macro')

print('macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f))

