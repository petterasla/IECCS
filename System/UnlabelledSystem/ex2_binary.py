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
strength = 'soft'

################
#    Load Data #
################


print("Loading data...")
train_data = pd.concat([ptd.getTrainingData(), ptd.getValidationData(), ptd.getTestData()])
unlabelled_data = ptd.getUnlabelledData()


#########################
#   Train classifier    #
#########################

#### Stance vs No Stance #####

print("\nTrain Stance vs No stance classifier")

binaryStances = []
for endorse in train_data.Endorse.tolist():
    binaryStances.append(ptd.getAbstractStanceVsNoStance(strength, endorse))

best_classifier = MultinomialNB()

pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                              analyzer='word',
                                              ngram_range=(1, 1),
                                              stop_words= None,
                                              max_features=None)),
                     ('clf', best_classifier)])

pipeline.fit(train_data.Abstract, binaryStances)


#########################
#   Predict data        #
#########################

print("Predicting labels for stance vs no stance")

predictions1 = pipeline.predict(unlabelled_data.Abstract)


###############################
#   Filtering away no stance  #
###############################

print("Removing 'NONE' from unlabeled list and trainig list")
unlabelled_data_list = ptd.getUnlabelledDataAsList()

for i, dic in enumerate(unlabelled_data_list):
    dic["Stance"] = predictions1[i]

new_unlabeled = []
for dic in unlabelled_data_list:
    if dic["Stance"] == "STANCE":
        new_unlabeled.append(dic)

new_unlabeled = pd.DataFrame(new_unlabeled)

train_data = train_data[train_data.Stance != "NONE"]

#########################
#   Train classifier    #
#########################

#### Favor vs against #####
print("\nTraining Favor vs against classifier")

best_classifier = MultinomialNB()

print("Checking for only two classes: {}".format(len(train_data.Stance.unique())))

pipeline = Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                              analyzer='word',
                                              ngram_range=(1, 1),
                                              stop_words= None,
                                              max_features=None)),
                     ('clf', best_classifier)])

pipeline.fit(train_data.Abstract, train_data.Stance)


#########################
#   Predict data        #
#########################

print("Predicting labels for stance vs no stance")

predictions2 = pipeline.predict(new_unlabeled.Abstract)


#############################
#   Add predictions to list #
#############################

print("Checking lengths")
c = 0
for dic in unlabelled_data_list:
    if dic["Stance"] != "NONE":
        c += 1

if c == len(predictions2):
    print("Prediction lengths are equal, should be fine..")
else:
    print("Prediction length NOT equal - problems..")

print("\nAdding predictions to list")

counter_index = 0
for dic in unlabelled_data_list:
    if dic["Stance"] == "NONE":
        continue
    else:
        if dic["Stance"] == "STANCE":
            dic["Stance"] = predictions2[counter_index]
            counter_index += 1

#########################
#   Print distribution  #
#########################

against_c = 0
favor_c = 0
none_c = 0
for dic in unlabelled_data_list:
    if dic["Stance"] == "AGAINST":
        against_c += 1
    elif dic["Stance"] == "FAVOR":
        favor_c += 1
    else:
        none_c += 1

print("\nThe distribution of predictions are: ")
print("\tFAVOR:  \t{}".format(favor_c))
print("\tAGAINST:\t{}".format(against_c))
print("\tNONE:   \t{}".format(none_c))

unique_years = unlabelled_data.Publication_year.unique()


for year in unique_years:
    favor_c = 0
    against_c = 0
    none_c = 0
    for dic in unlabelled_data_list:
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
