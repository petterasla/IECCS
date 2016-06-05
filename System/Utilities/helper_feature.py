import time
import string
import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from System.DataProcessing import process_data as ptd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, Imputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn_pandas import DataFrameMapper
from System.DataProcessing import process_meta_data as meta
import cPickle as pickle
from nltk.stem.wordnet import WordNetLemmatizer

def getFeatures(list_of_feature_keys):
    feature_list = []
    for key in list_of_feature_keys:
        feature_list.append(feature_dict[key])
    return feature_list

def removeFeatureKeys(discard=["tfidf"]):
    """
    Return all features except the 'discard' parameter. The parameter
    removes object from list.

    :param discard:     String. Either 'count-vect' or 'tfidft
    :return:
    """
    keys = []
    if len(keys) == 0:
        return [key for key in feature_dict.keys() if not key in discard]
    else:
        return keys


feature_dict = {
    "count-vect": ('vect', DataFrameMapper([
        ('Abstract', CountVectorizer(decode_error='ignore',
                                     analyzer='word',
                                     ngram_range=(1, 2),
                                     stop_words='english',
                                     max_features=None))
        ])),

    "tfidf": ('vect', DataFrameMapper([
        ('Abstract', TfidfVectorizer(decode_error='ignore',
                                     analyzer='word',
                                     ngram_range=(1, 1),
                                     stop_words='english',
                                     max_features=None,
                                     use_idf=False)),
        ])),

    "year-feat": ('year', FunctionTransformer(meta.getYearFeature, validate=False)),
    "language-feat": ('language-feat', FunctionTransformer(meta.getLanguageFeature, validate=False)),
    "reference-feat": ('reference-feat', FunctionTransformer(meta.getRefsFeature, validate=False)),
    "orgs-feat": ('orgs-feat', FunctionTransformer(meta.getOrganizationInfo, validate=False)),
    "keyword-feat": ('keyword-feat', FunctionTransformer(meta.getKeywords, validate=False)),
    "month-feat": ('publisher-feat', FunctionTransformer(meta.getMonth, validate=False)),
    "volume-feat": ('volume-feat', FunctionTransformer(meta.getVolume, validate=False)),
    "type-feat": ('type-feat', FunctionTransformer(meta.getType, validate=False)),
    "issue-feat": ('issue-feat', FunctionTransformer(meta.getIssue, validate=False)),
    "pub-length-feat": ('pub-length-feat', FunctionTransformer(meta.getPublicationLength, validate=False)),
    "author-feat": ('author-feat', FunctionTransformer(meta.getAuthors, validate=False)),
    "doc-type-feat": ('doc-type-feat', FunctionTransformer(meta.getDocType, validate=False)),
    "subject-feat": ('subject-feat', FunctionTransformer(meta.getSubject, validate=False)),
    "sub-header-feat": ('sub-header-feat', FunctionTransformer(meta.getSubHeader, validate=False)),
    "header-feat": ('header-feat', FunctionTransformer(meta.getHeader, validate=False)),
    "title-feat": ('vect', DataFrameMapper([
        ("Title", [CountVectorizer(analyzer="word",
                                   ngram_range=(1, 1))])
    ])),
    "LDA-abstract-feat": ('vect', DataFrameMapper([
        ("LDA", [CountVectorizer(analyzer="word",
                                     ngram_range=(1, 1)),
                    TfidfTransformer(use_idf=False)]
         )
    ])),
    "tokens-abstract-feat": ('token-feat', DataFrameMapper([
        ("Abstract", FunctionTransformer(ptd.numberOfTokensFeature, validate=False))
    ])),
    "tokens-title-feat": ('token-feat', DataFrameMapper([
        ("Title", FunctionTransformer(ptd.numberOfTokensFeature, validate=False))
    ])),
}





def print_top_words(model, feature_names, n_top_words, filename, store=False):
    topic_word_collection = []
    for topic_idx, topic in enumerate(model.components_):
        s = "Topic {}: {}".format(topic_idx + 1, [(idx, str(feature_names[i])) for idx, i in enumerate(topic.argsort()[:-n_top_words - 1:-1])])
        #print s
        topic_word_collection.append(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    if store:
        with open(filename, "w") as f:
            pickle.dump(topic_word_collection, f)
    return topic_word_collection


def LDA_scikit(stance="All", use_in_experiment=False, frame=None):
    n_top_words = 10
    n_topics = 1
    start = time.time()
    table = string.maketrans("", "")
    if not use_in_experiment:
        if stance == "All":
            data = ptd.getData().Abstract
        else:
            data = ptd.getDataWithMeta()
            data = data[data.Stance == stance].Abstract
    else:
        data = frame.Abstract

    data_as_list = data.tolist()
    raw_docs = []
    for d in data_as_list:
        raw_docs.append(str(d).translate(table, string.punctuation).lower())

    collection = []
    print("Extracting tf features for LDA...")
    for doc in raw_docs:
        tf_vectorizer = CountVectorizer(stop_words='english')
        tf_tfidf = TfidfVectorizer(stop_words='english')
        tf = tf_vectorizer.fit_transform([doc])
        tf2 = tf_tfidf.fit_transform([doc])
        model = LatentDirichletAllocation(n_topics=n_topics, random_state=1)
        model.fit(tf)

        tf_feature_names = tf_vectorizer.get_feature_names()
        topic_word_collection = print_top_words(model, tf_feature_names, n_top_words, "abstract_"+stance+"_count.pkl")
        #print
        #model.fit(tf2)
        #tf_feature_names2 = tf_vectorizer.get_feature_names()
        #topic_word_collection2 = print_top_words(model, tf_feature_names2, n_top_words, "abstract_"+stance+"_tfidf.pkl")
        collection.append(topic_word_collection)

    #print("\nTime used: {:.4f}".format((time.time()-start)/60.0))
    return [model[0] for model in collection]



#LDA_scikit("AGAINST")
#LDA_scikit("NONE")
#LDA_scikit("FAVOR")
#LDA_scikit()

def getCount(stance="AGAINST"):
    base = "../DataProcessing/TopicModelling/abstract/"
    #base = "../DataProcessing/TopicModelling/title/"

    type_ = "abstract_"     # "abstract_" or "title_"
    with open(base + type_ + stance+ "_count.pkl") as f:
        file1 = pickle.load(f)
    with open(base + type_ + stance +"_tfidf.pkl") as f:
        file2 = pickle.load(f)
    data = file1 + file2

    uniq_words = list(set([word[1] for word in data]))
    print("# of uniq words in {} topic is: {}".format(stance, len(uniq_words)))

    l = ptd.getMetaDataAsList()
    df = pd.DataFrame(l)
    favor = df[df.Stance == "FAVOR"]
    none = df[df.Stance == "NONE"]
    against = df[df.Stance == "AGAINST"]

    t_favor = list(set([word for sublist in favor.Title.tolist() for word in sublist.split(" ")]))
    t_none = list(set([word for sublist in none.Title.tolist() for word in sublist.split(" ")]))
    t_against = list(set([word for sublist in against.Title.tolist() for word in sublist.split(" ")]))
    print("Length of unique words in {} is {}.\nLength of unique words in {} is {}.\nLength of unique words in {} is {}".format("AGAINST", len(t_against), "FAVOR", len(t_favor), "NONE", len(t_none)))
    print
    counter = 0
    if stance == "AGAINST":
        for title in t_favor:
            for word in title.split(" "):
                if word in uniq_words:
                    counter += 1
        print("Number of title words from FAVOR found in {} is {}\n".format(stance, counter))
        counter = 0
        for title in t_none:
            for word in title.split(" "):
                if word in uniq_words:
                    counter += 1
        print("Number of title words from NONE found in {} is {}".format(stance, counter))
    elif stance == "FAVOR":
        for title in t_against:
            for word in title.split(" "):
                if word in uniq_words:
                    counter += 1
        print("Number of title words from AGAINST found in {} is {}\n".format(stance, counter))
        counter = 0
        for title in t_none:
            for word in title.split(" "):
                if word in uniq_words:
                    counter += 1
        print("Number of title words from NONE found in {} is {}".format(stance, counter))
    else:
        for title in t_against:
            for word in title.split(" "):
                if word in uniq_words:
                    counter += 1
        print("Number of title words from AGAINST found in {} is {}\n".format(stance, counter))
        for title in t_favor:
            for word in title.split(" "):
                if word in uniq_words:
                    counter += 1
        print("Number of title words from FAVOR found in {} is {}".format(stance, counter))

#getCount()
#getCount("FAVOR")
#getCount("NONE")

def lemmatizer(frame):
    data = frame.Abstract
    l = WordNetLemmatizer()
    lemma_list = []
    print("Start lemmatizing")
    for doc in data:
        tokenized = word_tokenize(doc)
        lemmatized = [l.lemmatize(word) for word in tokenized]
        lemma_list.append(" ".join(lemmatized))

    print data.iloc[0]
    print lemma_list[0]
    data = pd.Series(lemma_list)
    print data.iloc[0]

    print("Length are equal? {} == {}".format(len(data), len(lemma_list)))
    if len(data) == len(lemma_list):
        with open("test_LEMMA_abstract.pkl", "w") as f:
            pickle.dump(lemma_list, f)

#lemmatizer(ptd.getTrainingDataWithMeta())
#lemmatizer(ptd.getValidationDataWithMeta())
#lemmatizer(ptd.getTestDataWithMeta())

def addLDA(train, val, test):
    with open("../TextFiles/ex4/train_LDA_abstract.pkl", "r") as f:
        train["LDA"] = pickle.load(f)
    with open("../TextFiles/ex4/val_LDA_abstract.pkl", "r") as f:
        val["LDA"] = pickle.load(f)
    with open("../TextFiles/ex4/test_LDA_abstract.pkl", "r") as f:
        test["LDA"] = pickle.load(f)

    return train, val, test

def lemmatizeAbstracts(train_data, validate_data, test_data):
    with open("../TextFiles/ex4/train_LEMMA_abstract.pkl", "r") as f:
        train = pickle.load(f)
    with open("../TextFiles/ex4/val_LEMMA_abstract.pkl", "r") as f:
        val = pickle.load(f)
    with open("../TextFiles/ex4/test_LEMMA_abstract.pkl", "r") as f:
        test = pickle.load(f)

    train_data.Abstract = pd.Series(train)
    validate_data.Abstract = pd.Series(val)
    test_data.Abstract = pd.Series(test)
    return train_data, validate_data, test_data
