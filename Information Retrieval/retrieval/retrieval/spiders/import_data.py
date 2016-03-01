import re
import json
import pandas as pd

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

def generateSearchURL(title, year):
    return "http://www.scopus.com/results/results.url?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1=" + \
           title + "&field1=TITLE&dateType=Publication_Date_Type&yearFrom=" + \
           str(year-1) + "&yearTo=" + \
           str(year+1) + "&loadDate=7&documenttype=All&subjects=LFSC&subjects=HLSC&subjects=PHSC&subjects=SOSC&src=s&st1=" + \
           title + "&st2=&sot=b&sdt=b&sl=&s=TITLE%28" + \
           title + "%29&sid=&searchId=&txGid=&sort=plf-f&originationType=b&rr=&null="


def generateSearchURLs():
    info = pd.read_csv("../../../tcp_abstracts.txt")
    titles = info.Title
    years = info.Year
    URLs = []
    for i,title in enumerate(titles):
        url = generateSearchURL(title.replace("|",","), years.iloc[i])
        URLs.append(url)
    return URLs


def generateMetaURL(eid):
    return "http://www.scopus.com/onclick/export.uri?" + \
    "oneClickExport=%7b%22Format%22%3a%22CSV%22%2c%22View%22%3a%22FullDocument%22%7d&origin=recordpage&eid=" + \
    eid + "&zone=recordPageHeader&outputType=export&txGid=0"


def generateMetaURLs():
    info = pd.read_csv("../../../tcp_abstracts.txt")
    titles = info.Title
    URLs = []
    for title in titles:
        URLs.append(generateMetaURL(title.replace("|", ",")))
    return URLs

def jsonToTextList(input):
    with open(input) as read_file:
        json_file = json.load(read_file)
    read_file.close()

    l = []
    s1 = "recordpage&"
    s1_len = len(s1)
    for data in json_file:
        url = data['url']
        index = url.index(s1) + s1_len
        new_url = url[:index] + "eid=" + url[index:]
        l.append(new_url)
    return l


#print jsonToTextList("meta100.json")[:2]