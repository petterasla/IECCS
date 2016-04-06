from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
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
    "id-idf": ('vect', Pipeline([('vect', CountVectorizer(decode_error='ignore',
                                                 analyzer='word',
                                                 ngram_range=(1,3),
                                                 stop_words=None,
                                                 max_features=50000)),
        ('tfidf', TfidfTransformer(use_idf=True))
    ])),
    "count-vect": ('vect', Pipeline([
        ('vect', CountVectorizer(decode_error='ignore',
                                 analyzer='word',
                                 ngram_range=(1,3),
                                 stop_words=None,
                                 max_features=50000))
    ])),
    "year-feat": ('year', Pipeline([
        ('year-feat', FunctionTransformer(meta.getYearFeature, validate=False))
    ])),
    "category-feat": ('cat', Pipeline([
        ('category-feat', FunctionTransformer(meta.getCategoryFeature, validate=False))
    ]))
}