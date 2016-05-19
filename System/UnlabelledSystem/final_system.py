#! /usr/bin/python
# -*- coding: utf-8 -*-
import System.DataProcessing.process_data as ptd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from glob import glob
from System.DataProcessing.GloveVectorizer.glove_transformer import GloveVectorizer
import pandas as pd
import json
import time

#################
#    Parameters #
#################

start_time = time.time()
store_to_file = 1


################
#    Load Data #
################


print("Loading data...")
train = pd.read_csv(open('../TextFiles/data/tcp_train.csv'), sep='\t', index_col=0)
val = pd.read_csv(open('../TextFiles/data/tcp_validate.csv'), sep='\t', index_col=0)
test = pd.read_csv(open('../TextFiles/data/tcp_test.csv'), sep='\t', index_col=0)

train_data = pd.concat([train, val, test])

unlabelled_data = ptd.getUnlabelledData()

print len(unlabelled_data.Abstract.unique())


#########################
#   Train classifier    #
#########################


print("Training classifier")

glove_fnames = glob('/Users/petterasla/Desktop/Skole/9. semester/In-Depth project/IECCS/System/DataProcessing/GloveVectorizer/finalVec/glove.840B.300d_tcp_abstracts.pkl')
best_classifier = SVC(C=5.2, kernel='linear', probability=True)

glove_vecs = pd.read_pickle(glove_fnames[0])

glove_clf = Pipeline([('vect', GloveVectorizer(glove_vecs)),
                      ('clf', LogisticRegression(solver='lbfgs',
                                                 multi_class='multinomial',
                                                 class_weight='balanced',
                                                 ))])

svm_clf = Pipeline([('vect', CountVectorizer(analyzer="word",
                                              ngram_range=(1, 2),
                                              stop_words=None,
                                              max_features=None,
                                              decode_error='ignore')),
                     ('clf', best_classifier)
                     ])

vot_clf = VotingClassifier(estimators=[('glove', glove_clf),
                                       ('linear', svm_clf)],
                           voting='soft')

vot_clf.fit(train_data.Abstract, train_data.Stance)

#########################
#   Predict data        #
#########################


print("Predicting labels")
predictions = vot_clf.predict(unlabelled_data.Abstract)
print predictions

#########################
#   Print distribution  #
#########################

against_c = 0
favor_c = 0
none_c = 0
for pred in predictions:
    if pred == "AGAINST":
        against_c += 1
    elif pred == "FAVOR":
        favor_c += 1
    else:
        none_c += 1

print("\nThe distribution of predictions are: ")
print("\tFAVOR:  \t{}".format(favor_c))
print("\tAGAINST:\t{}".format(against_c))
print("\tNONE:   \t{}".format(none_c))

unique_years = list(set(unlabelled_data.Publication_year.tolist()))
unlabelled_data = ptd.getUnlabelledDataAsList()

for i, dic in enumerate(unlabelled_data):
    dic["Stance"] = predictions[i]

for year in unique_years:
    favor_c = 0
    against_c = 0
    none_c = 0
    for dic in unlabelled_data:
        if dic["Publication_year"] == year:
            if dic["Stance"] == "AGAINST":
                against_c += 1
            elif dic["Stance"] == "FAVOR":
                favor_c += 1
            else:
                none_c += 1

    print("\nYear distribution: {}".format(year))
    print("\tFAVOR:  \t{}".format(favor_c))
    print("\tAGAINST:\t{}".format(against_c))
    print("\tNONE:   \t{}".format(none_c))

##########################
#   Store as file        #
##########################

if store_to_file:
    with open("../TextFiles/data/related_data_with_predictions.json", "w") as f:
        json.dump(unlabelled_data, f)
        print("dumped")

print("Time used: {:.2f} minutes".format((time.time()-start_time)/60.0))