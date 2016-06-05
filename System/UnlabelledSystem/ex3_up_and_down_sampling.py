import System.DataProcessing.process_data as ptd
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import pandas as pd
import json

#################
#    Parameters #
#################

store_to_file = 0
downsample_rate_favor = 0.5
downsample_rate_none = 0.3
use_downsample = 1
use_upsample = 1
strength = 'soft'

################
#    Load Data #
################


print("Loading data...")
train_data = pd.concat([ptd.getTrainingData(), ptd.getValidationData(), ptd.getTestData()])
unlabelled_data = ptd.getUnlabelledData()

if use_downsample:
    print("using down sampling")
    sub_none = ptd.getDownsample2_0(train_data, "NONE", strength, downsample_rate_none)
    sub_favor = ptd.getDownsample2_0(train_data, "FAVOR", strength, downsample_rate_favor)
    against = train_data[train_data.Stance == "AGAINST"]

    train_data = pd.concat([sub_favor, sub_none, against])

if not use_downsample and not use_upsample:
    print("using nothing")

if use_upsample:
    print("using up sampling")
    train_data = pd.concat([train_data, train_data[train_data.Stance == "AGAINST"]])

#########################
#   Train classifier    #
#########################


print("Training classifier")
best_classifier = MultinomialNB(alpha=0.1)

pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                              analyzer='word',
                                              ngram_range=(2, 3),
                                              stop_words= 'english',
                                              max_features=50000)),
                     ('clf', best_classifier)])

pipeline.fit(train_data.Abstract, train_data.Stance)


#########################
#   Predict data        #
#########################


print("Predicting labels")
predictions = pipeline.predict(unlabelled_data.Abstract)


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
