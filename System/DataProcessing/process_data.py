import re
import csv
import random
import urllib
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment import vader as vader
from bs4 import BeautifulSoup
from scipy import sparse
# When using vader.SentimentIntensityAnalyzer() sentiment methods, you might have to download and store this in
# /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/nltk/sentiment/vader_lexicon.txt'
# https://github.com/nltk/nltk/blob/develop/nltk/sentiment/vader_lexicon.txt
"""
If you use the VADER sentiment analysis tools, please cite:

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
Sentiment Analysis of Social Media Text. Eighth International Conference on
Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""
from nltk.tokenize import word_tokenize
import json
import string
import pandas as pd


# ****************************  Get basic data *****************************
def getData():
    """
    Reading the text file and stores it as a DataFrame with following columns:
    Id,Year,Cat,Endorse,Title,Abstract

    :return:        A DataFrame
    """
    return pd.read_csv("../TextFiles/tcp_abstracts.txt")


def getIdData():
    """

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    return data.Id


def getYearData():
    """

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    return data.Year


def getCategoryData():
    """

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    return data.Cat


def getEndorsementData():
    """

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    return data.Endorse


def getTitleData():
    """

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    return data.Title


def getRawAbstractData():
    """
    Extracts the raw abstract data

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    return data.Abstract


def getAbstractData():
    """
    Extracts the abstracts, and convert '|' to ',' in the text due to the original file that was stores as CSV.

    :return:        A Series - pandas.core.series.Series
    """
    abstracts = getRawAbstractData()
    abstracts_list = []
    for abstract in abstracts:
        string = abstract.replace("|", ",")
        abstracts_list.append(re.sub('<[^>]*>', '', string))
    return pd.DataFrame(abstracts_list, columns=["Abstract"]).Abstract
#getAbstractData()


def getAgainstAbstracts(strength):
    """
    Returns all abstracts labeled against based on stregth.

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    abstracts = []

    for abstract, endorsement in (zip(data.Abstract, data.Endorse)):
        if strength=="soft":
            if endorsement >= 5:
                string = abstract.replace("|", ",")
                abstracts.append(re.sub('<[^>]*>', '', string))

        elif strength == "medium":
            if endorsement > 5:
                string = abstract.replace("|", ",")
                abstracts.append(re.sub('<[^>]*>', '', string))

        else:
            if endorsement > 6:
                string = abstract.replace("|", ",")
                abstracts.append(re.sub('<[^>]*>', '', string))

    return pd.DataFrame(abstracts, columns=["Abstract"]).Abstract, ["AGAINST" for i in range(len(abstracts))]


def getDownsample(label, strength, sample_rate):
    """
    Returns downsampled amount of abstracts based on label.

    :return:        A Series - pandas.core.series.Series
    """
    data = getData()
    abstracts = []
    test_abstracts = []
    rate_count = 0

    for abstract, endorsement in (zip(data.Abstract, data.Endorse)):
        if getAbstractStance(strength, endorsement) == label and rate_count % sample_rate == 0:
            string = abstract.replace("|", ",")
            abstracts.append(re.sub('<[^>]*>', '', string))
        else:
            string = abstract.replace("|", ",")
            test_abstracts.append(re.sub('<[^>]*>', '', string))
        rate_count += 1

    return pd.DataFrame(abstracts, columns=["Abstract"]).Abstract, [label for i in range(len(abstracts))], \
           pd.DataFrame(test_abstracts, columns=["Abstract"]).Abstract, [label for i in range(len(test_abstracts))]


def getAbstractStanceVsNoStance(strength, endorsement):
    """
    Converts the endorsement level of the abstract as favor, against or none depending the strength limit

    :param strength:        String that should decide the strength of stance of the abstract ['soft, 'medium', 'hard']
    :param endorsement:     Integer level of endrosement
    :return:                A string with the proper stance
    """

    # 7 levels of endorsement. See paper for further explanation.
    if strength=="soft":
        if endorsement <= 3:
            return "STANCE"
        elif endorsement >= 5:
            return "STANCE"
        else:
            return "NONE"
    elif strength == "medium":
        if endorsement < 3:
            return "STANCE"
        elif endorsement > 5:
            return "STANCE"
        else:
            return "NONE"
    else:
        if endorsement < 2:
            return "STANCE"
        elif endorsement > 6:
            return "STANCE"
        else:
            return "NONE"


def getAbstractStance(strength, endorsement):
    """
    Converts the endorsement level of the abstract as favor, against or none depending the strength limit

    :param strength:        String that should decide the strength of stance of the abstract ['soft, 'medium', 'hard']
    :param endorsement:     Integer level of endrosement
    :return:                A string with the proper stance
    """

    # 7 levels of endorsement. See paper for further explanation.
    if strength=="soft":
        if endorsement <= 3:
            return "FAVOR"
        elif endorsement >= 5:
            return "AGAINST"
        else:
            return "NONE"
    elif strength == "medium":
        if endorsement < 3:
            return "FAVOR"
        elif endorsement > 5:
            return "AGAINST"
        else:
            return "NONE"
    else:
        if endorsement < 2:
            return "FAVOR"
        elif endorsement > 6:
            return "AGAINST"
        else:
            return "NONE"
#endorse = getEndorsementData().tolist()
#print endorse[:25]
#print getAbstractStance('soft', endorse[6])


def getLabelPropTopicData(topic):
    """
    Extracts the data from a given topic

    :param topic:   A string with topic name [All, Atheism, Climate Change is a Real Concern,
                    Feminist Movement, Hillary Clinton, Legalization of Abortion]
    :return:        A list with information about that topic
    """
    data = processData("label_propagated_data.txt")
    if (topic == "All"):
        return data
    topicData = []
    for i in range(len(data)):
        if data[i][1] == topic:
            topicData.append(data[i])
    return topicData



def convertNumberStanceToText(allNumberedStances):
    """
    Converts numeric stance (1, 0, -1) to textual stance (FAVOR, NONE, AGAINST)

    :param doc_name:    List of numeric stances
    :return:            List of textual stanecs
    """
    textStances = []
    for i in range(len(allNumberedStances)):
        if allNumberedStances[i] > 0:
            textStances.append("FAVOR")
        elif allNumberedStances[i] == 0:
            textStances.append("NONE")
        else:
            textStances.append("AGAINST")

    return textStances
"""
d = getAnnotatedData()
f = [int(row[1]) for row in d]
e = convertNumberStanceToText(f)
"""
#data = [[row[0], row[1]] for row in d]
#s = sorted(data, key=lambda x: x[0])
#print e[:5]


def getAllStances(data_file="All"):
    """
    Extracts all the stances from the processed data

    :param data_file:   Either a list with data (from getTopicData(topic)) or the whole dataset 'All'
    :return stance:     A list with all the stances
    """
    if data_file == "All":
        data = processData("semeval2016-task6-trainingdata.txt")
    else:
        data = data_file
    stance = []
    for i in range(len(data)):
        stance.append(str(data[i][3]).rstrip())
    return stance


def train_test_split(data, percentage, test_topic):
    """
    This method takes a data list and splits into a training set and test set. It uses the percentage parameter
    to set the size of the test set. If the test_topic parameter is 'All', it will take the whole data set and
    take random samples from every topic. If not, it will only have

    :param data:            A list with data that want to be split in training and test set
    :param percentage:      How big you want the test set to be in percentage.
    :param test_topic:      Name of the topic you want to have in the test set
    :return:                Returns a list [train, test] which include a split of training and test data
    """
    if (test_topic == "All"):
        k = int(percentage*len(data))
        random.shuffle(data)
        test = data[:k]
        train = data[k:]
        return [train, test]
    else:
        topic_data = getTopicData(test_topic)
        k = int(percentage*len(topic_data))
        test = topic_data[:k]
        test_ids = [test[x][0] for x in range(len(test))]
        train = [data[x] for x in range(len(data)) if data[x][0] not in test_ids]
        return [train, test]


def train_test_split_on_stance(data, test_data, favor_p, against_p, none_p):
    """
    This method takes a data list and splits into a training set and test set. It uses the percentage parameter
    to set the size of each set based on their stance. i.e: FAVOR = 30, AGAINST = 15 and NONE = 45 and percentage
    is set to 0.33, then the test set will consist of 10 FAVOR, 5 AGAINST and 15 NONE.

    :param data:            A list with data that want to be split in training and test set
    :param test_data:       A list with the test data want to split up.
    :param favor_p:         How big you want the FAVOR test set to be in percentage.
    :param against_p:       How big you want the AGAINST test set to be in percentage.
    :param none_p:          How big you want the NONE test set to be in percentage.
    :return:                Returns a list [train, test] which include a split of training and test data
    """
    favor_list, against_list, none_list = [], [], []
    for t in test_data:
        if (t[3] == 'FAVOR'):
            favor_list.append(t)
        elif (t[3] == 'AGAINST'):
            against_list.append(t)
        else:
            none_list.append(t)
    k_favor, k_against, k_none = int(favor_p*len(favor_list)), int(against_p*len(against_list)), int(none_p*len(none_list))
    favor_test, against_test, none_test = favor_list[:k_favor], against_list[:k_against], none_list[:k_none]
    test = against_test + favor_test + none_test
    test_ids = [test[x][0] for x in range(len(test))]
    train = [data[x] for x in range(len(data)) if data[x][0] not in test_ids]
    print "len of data: "+ str(len(data)) + "\t len of favor: " + str(len(favor_list)) + "\t len of against: " \
          + str(len(against_list))+ "\t len of none: " + str(len(none_list)) + \
          "\t Total: " + str(len(favor_list) + len(against_list) + len(none_list))
    print "len of train: "+ str(len(train)) + "\t len of test: " + str(len(test)) + "\t total: " \
          + str(len(train) + len(test))
    return [train, test]
#train_test_split_on_stance(getTopicData(TOPIC2), TOPIC2, 0.2, 0.5, 0.3)


def stemming(data):
    pt = PorterStemmer()
    new_data = []
    for tweet in data.Tweet:
        words = word_tokenize(tweet)
        stemmed_words = []
        for word in words:
            stemmed_words.append(pt.stem(word))
        new_tweet = ""
        for word in stemmed_words:
            new_tweet = new_tweet + " " + word
        new_data.append(new_tweet)

    for i in range(614, 1009):
        data.Tweet.set_value(i, new_data[i-614])
    return data
#data = getAllTweets(getTopicData(TOPIC2)[0:3])
#print data
#k = stemming(data)
#print k


def lemmatizing(data):
    lem = WordNetLemmatizer()
    new_data = []
    for tweet in data.Tweet:
        #tweet = tweet.lower()
        words = word_tokenize(tweet)
        lemmatized = []
        for word in words:
            lemmatized.append(lem.lemmatize(word))
        new_tweet = ""
        for word in lemmatized:
            new_tweet = new_tweet + " " + word
        new_data.append(new_tweet)

    for i in range(614, 1009):
        data.Tweet.set_value(i, new_data[i-614])
    return data
#data = getAllTweets(getTopicData(TOPIC2))
#print data[:3]
#k = lemmatizing(data)
#print k[:3]


def processAbstracts():
    category_approval = 8       # Including the number: 2, 3, 4, 5, 6, 7. See TCP paper for more info.
    favor_endorsement = 2       # Including the number: 1, 2 or 3
    against_endorsement = 5     # Including the number: 5, 6 or 7
    #path = os.path.abspath('')
    with open("../BaselineSystem/abstracts_with_meta.txt", "r") as articleJson:
        articleInfo = json.load(articleJson)
        articleJson.close()
    favor_abstracts = []
    against_abstracts = []
    for article in articleInfo:
        #print article["Status"]["isMetaTitleEqualToOriginal"]
        if (article["Status"]["isMetaTitleEqualToOriginal"] == "False"):
            continue
        else:
            if (int(article["Category"]) >= category_approval):
                continue
            else:
                if (int(article["Endorsement"]) <= favor_endorsement):
                    favor_abstracts.append(article["Abstract"])
                elif (int(article["Endorsement"]) >= against_endorsement):
                    against_abstracts.append(article["Abstract"])

    print "favor abstracts: " + str(len(favor_abstracts)) + "\t against abastracts: " + str(len(against_abstracts))
    return [favor_abstracts, against_abstracts]
#processAbstracts()


def createClimateLexicon(topXwords = 100):
    """
    This method uses (for now) abstracts pulled from The Consensus Project as data to create a lexicon
    based on the most frequent words

    :param topXwords:   Number of words that should be included in the lexicon
    :return:            Returns a lexicon (list) containing with x most frequent words
    """
    with open("../BaselineSystem/abstracts_with_meta.txt", "r") as abstractInfo:
        abstracts = json.load(abstractInfo)
        abstractInfo.close()
    return -1


def convertStancesToNumbers(allStances):
    """
    Converts textual stance (FAVOR, NONE, AGAINST) to numbers (2, 1, 0)

    :param doc_name:    List of textual stances
    :return:            List of numeric stanecs
    """
    numberedStances = []
    for i in range(len(allStances)):
        if allStances[i] == 'FAVOR':
            numberedStances.append(2)
        elif allStances[i] == 'NONE':
            numberedStances.append(1)
        else:
            numberedStances.append(0)

    return numberedStances


def convertStancesToText(allNumberedStances):
    """
    Converts numeric stance (2, 1, 0) to textual stance (FAVOR, NONE, AGAINST)

    :param doc_name:    List of numeric stances
    :return:            List of textual stanecs
    """
    textStances = []
    for i in range(len(allNumberedStances)):
        if allNumberedStances[i] == 2:
            textStances.append("FAVOR")
        elif allNumberedStances[i] == 1:
            textStances.append("NONE")
        else:
            textStances.append("AGAINST")

    return textStances


def determineNegationFeature(texts):
    """
    Creates feature (0 or 1) for whether the tweet contains negated segments or not

    :param doc_name:    Tweet as string
    :return:            Binary value (0 or 1)
    """
    negated = []
    for text in texts:
        feature = vader.negated(text, include_nt=True)
        if feature:
            negated.append(float(1))
        else:
            negated.append(float(0))
    return sparse.csr_matrix(negated, dtype='float').T
#print determineNegationFeature(["hei hei hva skjer", "jada daj ladl"])
def lengthOfTweetFeature(texts):
    """
    Creates a normalized feature between 0 and 1 for the length of the tweet

    :param doc_name:    Tweet as string
    :return:            Float between 0 and 1
    """
    length = [float(len(text)/140.0) for text in texts]     #Maximunm length of a tweet
    return sparse.csr_matrix(length, dtype='float').T
#print lengthOfTweetFeature(["hei hei hva skjer", "jada daj ladl"])


def numberOfTokensFeature(texts):
    """
    Finds the number of tokens in a tweet

    :param doc_name:    Tweet as string
    :return:            Integer
    """
    length = [float(len(word_tokenize(text))) for text in texts]
    return sparse.csr_matrix(length, dtype='float').T


def numberOfCapitalWords(texts):
    """
    Finds the number of capital words in a tweet

    :param text:        Tweet as string
    :return:            Integer number of capital words
    """
    capitalWords = []
    for text in texts:
        capitalized = []
        if vader.allcap_differential(word_tokenize(text)):
            for word in word_tokenize(text):
                if word.isupper():
                    capitalized.append(word)
            capitalWords.append(float(len(capitalized)))
        else:
            capitalWords.append(float(0))
    return sparse.csr_matrix(capitalWords, dtype='float').T
#print numberOfCapitalWords("HEI hvordan Gaar DET!")


def numberOfNonSinglePunctMarks(texts):
    """
    Finds the number of non-single punctuation marks in a tweet

    :param text:        Tweet as a string
    :return:            A list where first element is an integer number of punctuation marks and last element
                        is whether the last punctuation mark is ! or ? (either 0 or 1)
    """
    countz = []
    exlcMark= []
    for text in texts:
        counter = 0
        isQuestionMarkOrExclamationMarkLast = 0
        # for word in word_tokenize(text):
        #     for i in range(len(word)):
        #         # string.punctuation contains: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        #         if (word[i] in string.punctuation) and not (i == len(word)-1) and (word[i+1] in string.punctuation):
        #             counter += 1
        #             if word[len(word)-1] in "!?":
        #                 isQuestionMarkOrExclamationMarkLast = 1
        #             break           # Break here otherwise a word like: "hello!!!!" will count as 3
        word = word_tokenize(text)
        for i in range(1, len(word)):
            if (len(word[i]) == 1) and (word[i-1] in string.punctuation) and (word[i] in string.punctuation): #not (i == len(word)-1) and (word[i+1] in string.punctuation):
                if word[i] in "!":
                    isQuestionMarkOrExclamationMarkLast = 1
                else:
                    isQuestionMarkOrExclamationMarkLast = 0
            elif (len(word[i]) == 1) and (word[i] in string.punctuation):
                counter += 1

        countz.append(float(counter))

    return sparse.csr_matrix(countz, dtype='float').T
#numberOfNonSinglePunctMarks(["hei hei!!#%", "Dette er en test !#!"])
#numberOfNonSinglePunctMarks(["hei !!!",  "ho!?! $$ njsf$$%&!! nofnpr$$$$!?"])


def isExclamationMark(texts):
    """
    Finds the number of non-single punctuation marks in a tweet

    :param text:        Tweet as a string
    :return:            A list where first element is an integer number of punctuation marks and last element
                        is whether the last punctuation mark is ! or ? (either 0 or 1)
    """
    exlcMark= []
    for text in texts:
        counter = 0
        isQuestionMarkOrExclamationMarkLast = 0
        # for word in word_tokenize(text):
        #     for i in range(len(word)):
        #         # string.punctuation contains: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        #         if (word[i] in string.punctuation) and not (i == len(word)-1) and (word[i+1] in string.punctuation):
        #             counter += 1
        #             if word[len(word)-1] in "!?":
        #                 isQuestionMarkOrExclamationMarkLast = 1
        #             break           # Break here otherwise a word like: "hello!!!!" will count as 3
        word = word_tokenize(text)
        for i in range(1, len(word)):
            if (len(word[i]) == 1) and (word[i-1] in string.punctuation) and (word[i] in string.punctuation): #not (i == len(word)-1) and (word[i+1] in string.punctuation):
                if word[i] in "!":
                    isQuestionMarkOrExclamationMarkLast = 1
                else:
                    isQuestionMarkOrExclamationMarkLast = 0


        exlcMark.append(isQuestionMarkOrExclamationMarkLast)

    return sparse.csr_matrix(exlcMark, dtype='int').T


def numberOfLengtheningWords(texts):
    """
    Counts the number of words that are longer than usual like: cooool.
    It will count every word that has (at least) three of the same consecutive letters

    :param text:        Tweet as a string
    :return:            Integer number of lengthening words.
    """
    lengthening = []
    for text in texts:
        counter = 0
        for word in word_tokenize(text):
            for i in range(len(word)):
                letter = word[i]
                if (len(word) > 2) and (i < len(word)-2) and (word[i+1] == letter) and (word[i+2] == letter):
                    counter +=1
                    break
        lengthening.append(float(counter))

    return sparse.csr_matrix(lengthening, dtype='float').T
#print numberOfLengtheningWords("cooolll balll hey how arre you")


def determineSentiment(texts):
    """
    Determines the sentiment of a tweet based on the vader module

    :param text:        Tweet as a string
    :return:            Returns a dict of {neg:x, neu:y, pos:z, compound:w}
    """
    sentiment = []
    for text in texts:
        # Adding 1.0 because Naive Bayes doesnt do well with negative values.
        sentiment.append(vader.SentimentIntensityAnalyzer().polarity_scores(text)['compound'] + 1.0)
    return sparse.csr_matrix(sentiment, dtype='float').T


def getPOStags(tweet):
    """
    Using the input with help of the NLTK library to return the tweet with part-of-speech tags.

    :param tweet:   Tweet as a string
    :return:        Return the tweet with part-of-speech tags
    """
    # nltk.help.upenn_tagset() to see what each tag means..
    return nltk.pos_tag(tweet)


def getNumberOfPronouns(posTaggedTweet):
    """
    Count number of pronouns used in a tweet

    :param posTaggedTweet:  A list containing tuples of (token, pos-tag)
    :return:                Return number of pronouns as integer
    """
    return float(len([i for (i,x) in posTaggedTweet if x == 'PRP' or x == 'PRP$']))


def getPosAndNegWords(tweet):
    """
    Finds positive and negative boosted words in the tweet

    :param tweet:   Tweet as a string
    :return:        Returns a list with two floats between 0 and 1. First element represent pos and second repr neg
    """
    pos = 0
    neg = 0
    a = vader.SentimentIntensityAnalyzer()
    for word in word_tokenize(tweet):
        if a.polarity_scores(word)['pos'] > 0.9:
            pos += 1
        if a.polarity_scores(word)['neg'] > 0.9:
            neg += 1

    l = float(len(word_tokenize(tweet)))
    return [pos/l, neg/l]


def getSkepticalTweets():
    url = "https://www.skepticalscience.com/print.php"
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace("\n", " ")

    tweets = []
    for i in range (1,156):
        s = str(i) + ' "'
        startIndex = text.find(s) + 3
        endIndex = text.find('"', startIndex+5)
        tweets.append(text[startIndex:endIndex])
    return tweets
#print getSkepticalTweets()