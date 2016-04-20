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
                                     ngram_range=(1,2),
                                     stop_words='english',
                                     max_features=None))
        ])),

    "tfidf": ('vect', DataFrameMapper([
        ('Abstract', TfidfVectorizer(decode_error='ignore',
                                     analyzer='word',
                                     ngram_range=(1,2),
                                     stop_words='english',
                                     max_features=None)),
        ])),

    "year-feat": ('year',
        #('year-feat',
        FunctionTransformer(meta.getYearFeature, validate=False)

        #DataFrameMapper([
        #    (['Publication_year'], OneHotEncoder())
        #])
    ),
    "category-feat": ('cat', Pipeline([
        ('category-feat', FunctionTransformer(meta.getCategoryFeature, validate=False))
    ])),
    "language-feat": ('lan', Pipeline([
        ('language-feat', FunctionTransformer(meta.getLanguageFeature, validate=False))
    ])),
    "reference-feat": ('ref', Pipeline([
        ('reference-feat', FunctionTransformer(meta.getRefsFeature, validate=False))
    ]))
}