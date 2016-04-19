# Fix path for use in terminal ###
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

from sklearn.cross_validation import train_test_split
import process_data as ptd

def split_test_val_train(strength):
    data = ptd.getData()

    stances = ptd.convertEndorsementToStance(data, strength)

    #data.drop('Endorse', axis=1, inplace=True)
    data['Stance'] = stances

    X, X_test, y, y_test = train_test_split(data, data.Stance, test_size=0.25, random_state=1, stratify=data.Stance)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

    X_train.to_csv('tcp_train.csv', sep='\t')
    X_val.to_csv('tcp_validate.csv', sep='\t')
    X_test.to_csv('tcp_test.csv', sep='\t')


# Perform the split (only needed once)
split_test_val_train('soft')

#### CONVERT META JSON TO TRAIN/VAL/TEST WITH META:

with open("../TextFiles/data/meta_data.json", "r") as f:
    data = json.load(f)

print("len of meta data: {}".format(len(data)))

train = pd.read_csv("tcp_train.csv", sep='\t')
val = pd.read_csv("tcp_validate.csv", sep='\t')
test = pd.read_csv("tcp_test.csv", sep='\t')


train_ids = train.Id.tolist()
val_ids = val.Id.tolist()
test_ids = test.Id.tolist()



train_meta_dict = []
val_meta_dict = []
test_meta_dict = []
for d in data:
    if d["_id"] in train_ids:
        train_meta_dict.append(d)
    elif d["_id"] in val_ids:
        val_meta_dict.append(d)
    else:
        test_meta_dict.append(d)

print("len of train.csv: {}".format(len(train_ids)))
print("len of train.csv: {}".format(len(train)))
print("len of train.csv: {}".format(len(train_meta_dict)))

print("len of validate.csv: {}".format(len(val)))
print("len of validate.csv: {}".format(len(val_meta_dict)))
print("len of validate.csv: {}".format(len(val_ids)))

print("len of test.csv: {}".format(len(test_ids)))
print("len of test.csv: {}".format(len(test)))
print("len of test.csv: {}".format(len(test_meta_dict)))

print("len of data shuold be equal to the sum: {} == {} ".format(len(data), (len(test_meta_dict) + len(train_meta_dict) + len(val_meta_dict))))

pd.DataFrame(train_meta_dict).to_csv("../TextFiles/data/tcp_train_meta.csv", sep="\t")
pd.DataFrame(val_meta_dict).to_csv("../TextFiles/data/tcp_validate_meta.csv", sep="\t")
pd.DataFrame(test_meta_dict).to_csv("../TextFiles/data/tcp_test_meta.csv", sep="\t")