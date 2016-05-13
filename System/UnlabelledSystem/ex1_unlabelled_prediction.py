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

################
#    Load Data #
################


print("Loading data...")
train_data = pd.concat([ptd.getTrainingData(), ptd.getValidationData(), ptd.getTestData()])
unlabelled_data = ptd.getUnlabelledData()


#########################
#   Train classifier    #
#########################


print("Training classifier")
best_classifier = LinearSVC()

pipeline = Pipeline([('vect', CountVectorizer()),
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
