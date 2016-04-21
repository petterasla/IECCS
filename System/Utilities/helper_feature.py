from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, Imputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn_pandas import DataFrameMapper
import System.DataProcessing.process_meta_data as meta

def getFeatures(list_of_feature_keys):
    feature_list = []
    for key in list_of_feature_keys:
        feature_list.append(feature_dict[key])
    return feature_list

def getFeatureKeys():
    keys = []
    if len(keys) == 0:
        return feature_dict.keys()
    else:
        return keys


feature_dict = {
    "count-vect": ('vect', DataFrameMapper([
        ('Abstract', CountVectorizer(decode_error='ignore',
                                     analyzer='word',
                                     ngram_range=(2,3),
                                     stop_words='english',
                                     max_features=50000))
        ])),

    "tfidf": ('vect', DataFrameMapper([
        ('Abstract', TfidfVectorizer(decode_error='ignore',
                                     analyzer='word',
                                     ngram_range=(2,3),
                                     stop_words='english',
                                     max_features=50000)),
        ])),

    "year-feat": ('year',
        FunctionTransformer(meta.getYearFeature, validate=False)

        #DataFrameMapper([
        #    (['Publication_year'], OneHotEncoder())
        #])
    ),
    "language-feat": ('lan', Pipeline([
        ('language-feat', FunctionTransformer(meta.getLanguageFeature, validate=False))
    ])),
    "reference-feat": ('ref', Pipeline([
        ('reference-feat', FunctionTransformer(meta.getRefsFeature, validate=False))
    ])),
    "orgs-feat": ('org', Pipeline([
        ('orgs-feat', FunctionTransformer(meta.getOrganizationInfo, validate=False))
    ])),
    "keyword-feat": ('key', Pipeline([
        ('keyword-feat', FunctionTransformer(meta.getKeywords, validate=False))
    ])),
    "month-feat": ('pub', Pipeline([
        ('publisher-feat', FunctionTransformer(meta.getMonth, validate=False))
    ])),
    "volume-feat": ('pub', Pipeline([
        ('volume-feat', FunctionTransformer(meta.getVolume, validate=False))
    ])),
    "type-feat": ('pub', Pipeline([
        ('type-feat', FunctionTransformer(meta.getType, validate=False))
    ])),
    "issue-feat": ('pub', Pipeline([
        ('issue-feat', FunctionTransformer(meta.getIssue, validate=False))
    ])),
    "pub-length-feat": ('pub', Pipeline([
        ('pub-length-feat', FunctionTransformer(meta.getPublicationLength, validate=False))
    ])),
    "author-feat": ('pub', Pipeline([
        ('author-feat', FunctionTransformer(meta.getAuthors, validate=False))
    ])),
    "doc-type-feat": ('pub', Pipeline([
        ('doc-type-feat', FunctionTransformer(meta.getDocType, validate=False))
    ])),
    "subject-feat": ('pub', Pipeline([
        ('subject-feat', FunctionTransformer(meta.getSubject, validate=False))
    ])),
    "sub-header-feat": ('pub', Pipeline([
        ('sub-header-feat', FunctionTransformer(meta.getSubHeader, validate=False))
    ])),
    "header-feat": ('pub', Pipeline([
        ('header-feat', FunctionTransformer(meta.getHeader, validate=False))
    ]))

}