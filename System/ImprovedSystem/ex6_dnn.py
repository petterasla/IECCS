import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD

from glob import glob
from System.DataProcessing.GloveVectorizer.glove_transformer import GloveVectorizer
import pandas as pd

# data
data = pd.read_csv(open('../TextFiles/data/tcp_train.csv'), sep='\t', index_col=0)



# Sequential model
model = Sequential()

# Stacking layers
model.add(Dense(output_dim=64, input_dim=100))
model.add(Activation("relu"))
model.add(Dense(output_dim=10))
model.add(Activation("softmax"))

# configure its learning process
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# configure your optimizer
#model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))

# iterate on your training data in batches
model.fit(glove_vecs_data, y, nb_epoch=5, batch_size=32)

# Evaluate your performance
loss_and_metrics = model.evaluate(X_test, Y_test, batch_size=32)

# predictions on new data
classes = model.predict_classes(X_test, batch_size=32)
proba = model.predict_proba(X_test, batch_size=32)