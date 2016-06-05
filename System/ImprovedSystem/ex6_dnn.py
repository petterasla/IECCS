import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import skflow
from sklearn.metrics import fbeta_score
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
import pandas as pd

data = pd.read_csv(open('../TextFiles/data/tcp_train.csv'), sep='\t', index_col=0)

classifier = skflow.TensorFlowDNNClassifier(hidden_units=[10, 20, 10], n_classes=3)

cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)
pred_stances = cross_val_predict(classifier, data.Abstract, data.Stance, cv=cv)

print classification_report(data.Stance, pred_stances, digits=4)

macro_f = fbeta_score(data.Stance, pred_stances, 1.0,
                      labels=['AGAINST', 'FAVOR', 'NONE'],
                      average='macro')

print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f)