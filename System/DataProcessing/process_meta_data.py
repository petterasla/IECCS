#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""
This file opens the file with TCP with meta data gathered from Web of Science.
The file is stored as JSON and contains a big list with dictionaries for each
record from TCP data (11 942).

Notice that only the first seven keys are certain in each dictionary, the rest
could potentially be nothing - stored as None (at least should be)

Below is the dictionary info about keys and values

dic["_id"] = id
dic["Abstract"] = Abstract
dic["Endorsement"] = Endorsement value
dic["Stance"] = Endorsement converted to stance
dic["Category"] = Category
dic["Title"] = Title
dic["Publication_year"] = Year

dic["Language"] = Language
dic["References"] = Number of references
dic["Organization_info"] = Organization info (stored as a list with lists [[Country, City, (if street), (if organization name)], [], []])
dic["Keywords"] = Keywords
dic["Headers"] = Document Headers
dic["Sub_headers"] = Document Subheaders
dic["Subjects"] = Docuemnt Subjects
dic["Publisher_info"] = Publisher info (stored as list [Country, City, Publisher name])
dic["Publication_month"] = Publication month
dic["Publication_volume"] = Publication volume
dic["Publication_type"] = Publication type
dic["Publication_issue"] = Publication issue
dic["Publication_length"] = Publication length (number of pages)
dic["Authors"] = Authors (stored as list ["Last name, first name initals"], i.e ["Coleman, SD", "Lawyer, P"]
dic["Document_type"] = Document type
dic["WOS"] = Web of Science ID

Create new methods when needed :-)
"""
import json
from scipy import sparse
import pandas as pd
import time
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, Imputer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.base import TransformerMixin
import math
import numpy as np
import difflib
import System.DataProcessing.process_data as ptd


def getAllData():
    data = ptd.getMetaDataAsList()
    return pd.DataFrame(data)

# Working
def getYearFeature(frame):
    all = getAllData()
    labels = all.Publication_year.unique().tolist()
    label_dict = {}
    for index, year in enumerate(labels):
        label_dict[year] = index
    print("unique years: {}".format(len(labels)))
    print("len of frame: {}".format(len(frame)))
    dv = DictVectorizer()
    dv.fit_transform(label_dict).toarray()
    list_of_dicts = []
    for year in frame.Publication_year:
        list_of_dicts.append({year: label_dict[year]})
    return dv.transform(list_of_dicts)

# Not working
def getRefsFeature(abstracts):
    print abstracts
    exit()
    data = getDataFrameFromAbstracts()

    sub_frame = data.loc[abstracts]
    checkSize(sub_frame, abstracts)
    mapper = DataFrameMapper([
        (["References"], [Imputer(), OneHotEncoder()])
    ], sparse=True)

    return mapper.fit_transform(sub_frame)

def getLanguageFeature(abstracts):
    data = getDataFrameFromAbstracts()
    labels = data.Language.unique().tolist()
    sub_frame = data.loc[abstracts]
    mapper = LabelEncoder()
    mapper.fit(labels)
    transformed = np.asarray(mapper.transform(sub_frame.Language.tolist())).reshape(-1, 1)
    return transformed

def getCategoryFeature(abstracts):
    data = getDataFrameFromAbstracts()
    sub_frame = data.loc[abstracts]
    feature = [float(cat) for cat in cats]
    return sparse.csr_matrix(feature, dtype='float').T


def containNan(dataframe):
    return dataframe.isnull().values.any()

def checkSize(dataframe, abstracts):
    a = len(abstracts)
    b = dataframe.loc[abstracts].shape
    print("Length of abstracts:  {}".format(a))
    print("Length after doing loc: {}".format(b))