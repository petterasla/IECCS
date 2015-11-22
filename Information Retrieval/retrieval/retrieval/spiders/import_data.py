import re
import json

#Reading in tcp_articles.txt file and returning a list
def getArticleInfo(doc_name):
    articleInfo = []
    f = open(doc_name,"r")
    line = f.readline()     #Firste line states id, year, title of the article
    line = f.readline()     #Starts reading from the second line
    counter = 0             #Using a counter to get previous articles in the list
    while line:
        split_index = list_duplicates_of(line,",")      # Returning a list with indexes based on comma (",")
        # Checking the first char in the line based on the ascii value: 0-9 is from 48-57
        if ord(line[0]) < 48 or ord(line[0]) > 57 or len(split_index) != 2:
            articleInfo[counter-1][2] = (articleInfo[counter-1][2].strip()) + " " + line[:-1] #Removing \n from the string
        else:
            id = line[:split_index[0]]
            year = line[split_index[0]+1:split_index[1]]
            title = line[split_index[1]+1:-1]               #Removing \n from the string
            article = [id, year, title]
            articleInfo.append(article)
            counter += 1
        line = f.readline()
    f.close()
    return articleInfo

#Reading in tcp_abstracts.txt file and returning a list
def importArticleAbstracts(doc_name):
    articleInfo = []
    f = open(doc_name,"r")
    line = f.readline()     #Firste line states id, year, title of the article
    line = f.readline()     #Starts reading from the second line
    counter = 0             #Using a counter to get previous articles in the list
    while line:
        counter += 1
        data = line.split(",")
        data[4] = data[4].replace("|", ",")
        data[5] = re.sub('<[^<]+?>', '', data[5])
        articleInfo.append(data)
        line = f.readline()
    f.close()

    with open('abstracts_in_list.txt', 'w') as outfile:
        json.dump(articleInfo, outfile)
        outfile.close()

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def generateSearchURL(title):
    return "http://www.scopus.com/results/results.url?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1=" + \
           title + "&field1=TITLE&dateType=Publication_Date_Type&yearFrom=Before+1960&yearTo=Present&loadDate=7&documenttype=All&subjects=LFSC&subjects=HLSC&subjects=PHSC&subjects=SOSC&src=s&st1=" + \
           title + "&st2=&sot=b&sdt=b&sl=&s=TITLE%28" + \
           title + "%29&sid=&searchId=&txGid=&sort=plf-f&originationType=b&rr=&null="

def generateSearchURLs():
    articles = getArticleInfo("../../../tcp_articles.txt")
    URLs = []
    for title in articles:
        URLs.append(generateSearchURL(title[2]))
    return URLs

def generateMetaURL(title):
    return "http://api.crossref.org/works?query=" + \
           title + "&rows=1&sort=score"

def generateMetaURLs():
    articles = getArticleInfo("../../../tcp_articles.txt")
    URLs = []
    for title in articles:
        URLs.append(generateMetaURL(title[2]))
    return URLs


#articleInfo = getArticleInfo("../../../tcp_articles.txt")
#print len(articleInfo)