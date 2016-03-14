# Fix path for use in terminal ###
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