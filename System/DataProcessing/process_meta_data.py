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
    all = getAllData().Publication_year
    labels = all.unique().tolist()
    label_dict = dict(zip(labels, range(len(labels))))
    dv = DictVectorizer()
    dv.fit_transform(label_dict)
    list_of_dicts = [{year: label_dict[year]} for year in frame.Publication_year]
    return dv.transform(list_of_dicts)


def getLanguageFeature(frame):
    all = getAllData().Language
    sub = frame.Language
    all, sub = checkAndReplaceNan(all, sub, unicode(-1))
    labels = all.unique().tolist()
    label_dict = dict(zip(labels, range(len(labels))))
    dv = DictVectorizer()
    dv.fit_transform(label_dict)
    list_of_dicts = [{lan: label_dict[unicode(lan)]} for lan in sub]
    return dv.transform(list_of_dicts)


def getRefsFeature(frame):
    all = getAllData().References
    sub = frame.References
    all, sub = checkAndReplaceNan(all, sub, unicode(-1))
    labels = all.unique().tolist()
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{ref: label_dict[unicode(int(ref))]} for ref in sub]
    return dv.transform(list_of_dicts)

def getOrganizationInfo(frame):
    all = getAllData().Organization_info
    sub = frame.Organization_info
    all, sub = checkAndReplaceNan(all, sub, unicode(-1))
    info = all.tolist()
    labels = list(set([l[0][0].lower() for l in info if not len(l[0])==1]))
    labels.append(unicode("-1"))
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = []
    for info in sub:
        if len(info.split("'")) < 2:
            list_of_dicts.append({unicode(info): label_dict[unicode(info)]})
        else:
            key = info.split("'")[1].lower()
            value = label_dict[unicode(info.split("'")[1].lower())]
            list_of_dicts.append({key: value})
    return dv.transform(list_of_dicts)

def getKeywords(frame):
    all = getAllData().Keywords
    sub = frame.Keywords
    checkAndReplaceNan(all, sub, unicode("nan"))
    labels = all.tolist()
    labels = list(set([len(sub_list) for sub_list in labels if not sub_list == "nan"]))
    labels.append(unicode("nan"))
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{len(sub_list.split(",")): label_dict[len(sub_list.split(","))]} if not sub_list == unicode("nan") else {unicode("nan"): label_dict[unicode("nan")]} for sub_list in sub]
    return dv.transform(list_of_dicts)

def getMonth(frame):
    all = getAllData().Publication_month
    sub = frame.Publication_month
    all, sub = checkAndReplaceNan(all, sub, unicode("nan"))
    labels = all.unique().tolist()
    labels = list(set([month[:3] for month in labels]))
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{month[:3]: label_dict[month[:3]]} for month in sub]
    return dv.transform(list_of_dicts)

def getVolume(frame):
    all = getAllData().Publication_volume
    sub = frame.Publication_volume
    all, sub = checkAndReplaceNan(all, sub, unicode("-1"))
    labels = all.unique().tolist()
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{vol: label_dict[vol]} for vol in sub]
    return dv.transform(list_of_dicts)

def getType(frame):
    all = getAllData().Publication_type
    sub = frame.Publication_type
    all, sub = checkAndReplaceNan(all, sub, unicode("-1"))
    labels = all.unique()
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{typ: label_dict[typ]} for typ in sub]
    return dv.transform(list_of_dicts)

def getIssue(frame):
    all = getAllData().Publication_issue
    sub = frame.Publication_issue
    all, sub = checkAndReplaceNan(all, sub, unicode("-1"))
    labels = all.unique()
    print labels
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{issue: label_dict[issue]} for issue in sub]
    return dv.transform(list_of_dicts)

def getPublicationLength(frame):
    all = getAllData().Publication_length
    sub = frame.Publication_length
    all, sub = checkAndReplaceNan(all, sub, unicode("-1"))
    labels = all.unique()
    print labels
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{length: label_dict[unicode(int(length))]} for length in sub]
    return dv.transform(list_of_dicts)

def getAuthors(frame):
    all = getAllData().Authors
    sub = frame.Authors
    all, sub = checkAndReplaceNan(all, sub, unicode("-1"))
    labels = all.tolist()
    labels = list(set([author for sublist in labels if not sublist == unicode("-1") for author in sublist]))
    labels.append(unicode("-1"))
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = []
    for author in sub:
        try:
            key = author.split("'")[1]
            value = label_dict[key]
            list_of_dicts.append({key: value})
        except:
            key = unicode("-1")
            list_of_dicts.append({key: label_dict[key]})

    return dv.transform(list_of_dicts)

def getDocType(frame):
    all = getAllData().Document_type
    sub = frame.Document_type
    all, sub = checkAndReplaceNan(all, sub, unicode("-1"))
    labels = all.unique()
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = [{typ: label_dict[unicode(typ)]} for typ in sub]
    return dv.transform(list_of_dicts)

def getSubject(frame):
    all = getAllData().Subjects
    sub = frame.Subjects
    all, sub = checkAndReplaceNan(all, sub, 1)
    labels = all.tolist()
    labels = list(set([len(sub_list) for sub_list in labels if not sub_list == 1]))
    labels.append(unicode("nan"))
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = []
    for subj in sub:
        if type(subj) is int:
            key = unicode("nan")
            value = label_dict[key]
            list_of_dicts.append({key: value})
        else:
            key = len(subj.split("'"))/2
            value = label_dict[key]
            list_of_dicts.append({key: value})
    return dv.transform(list_of_dicts)

def getSubHeader(frame):
    all = getAllData().Sub_headers
    sub = frame.Sub_headers
    all, sub = checkAndReplaceNan(all, sub, 1)
    labels = all.tolist()
    labels = list(set([len(sub_list) for sub_list in labels if not sub_list == 1]))
    labels.append(unicode("nan"))
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = []
    for subj in sub:
        if type(subj) is int:
            key = unicode("nan")
            value = label_dict[key]
            list_of_dicts.append({key: value})
        else:
            key = len(subj.split("'"))/2
            value = label_dict[key]
            list_of_dicts.append({key: value})
    return dv.transform(list_of_dicts)

def getHeader(frame):
    all = getAllData().Headers
    sub = frame.Headers
    all, sub = checkAndReplaceNan(all, sub, 1)
    labels = all.tolist()
    labels = list(set([len(sub_list) for sub_list in labels if not sub_list == 1]))
    labels.append(unicode("nan"))
    print labels
    dv, label_dict = fitDictVect(labels)
    list_of_dicts = []
    for subj in sub:
        if type(subj) is int:
            key = unicode("nan")
            value = label_dict[key]
            list_of_dicts.append({key: value})
        else:
            key = len(subj.split("'"))/2
            value = label_dict[key]
            list_of_dicts.append({key: value})
    return dv.transform(list_of_dicts)


def containNan(dataframe):
    return dataframe.isnull().values.any()

def replaceNan(frame, value):
    frame.fillna(value, inplace=True)
    return frame

def checkAndReplaceNan(frame1, frame2, value):
    if containNan(frame1):
        frame1 = replaceNan(frame1, value)
    if containNan(frame2):
        frame2 = replaceNan(frame2, value)
    return frame1, frame2

def fitDictVect(labels):
    dv = DictVectorizer()
    label_dict = dict(zip(labels, range(len(labels))))
    dv.fit_transform(label_dict)
    return dv, label_dict

def checkSize(dataframe, abstracts):
    a = len(abstracts)
    b = dataframe.loc[abstracts].shape
    print("Length of abstracts:  {}".format(a))
    print("Length after doing loc: {}".format(b))