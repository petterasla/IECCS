import json
import sys
sys.path.insert(0, "/Users/petterasla/Desktop/Skole/9. semester/In-Depth project/IECCS/Information Retrieval/retrieval/retrieval/spiders")
import getArticleTitle
import re
import difflib

def compareData():
    #articleInfo = getArticleTitle.getArticleInfo("tcp_articles.txt")
    #print "Article: " + articleInfo[0][2] + " -- published: " + str(articleInfo[0][1])
    with open("retrieval/retrieval/spiders/abstracts_full.json", "r") as articleJson:
        articleInfo = json.load(articleJson)
        articleJson.close()

    print articleInfo[0]

    with open("retrieval/retrieval/spiders/meta.json") as metaJson:
        metaInfo = json.load(metaJson)
        metaJson.close()

    #print "MetaInfo: " + str(metaInfo) + "\n\n"

    titleArticle = articleInfo[0][4].lower().strip()
    titleMeta = metaInfo[0]["message"]["items"][0]["title"][0].lower().strip()
    #print titleArticle
    #print titleMeta
    #print titleArticle == titleMeta
    #print "\n"


    info = []
    print "adding meta to data"
    #print "size of meta info before: " + str(len(metaInfo))
    #print "size of articles info before: " + str(len(articleInfo))
    counter = 0
    for article in articleInfo:
        counter += 1
        if ((counter % 1000) == 0):
            print "Per tusen ferdig: " + str(counter)
        articleDict = {}
        status = {}
        for meta in metaInfo:
            a = article[4]
            a = a.encode("ascii", "ignore")
            b = meta["message"]["query"]["search-terms"]
            if (a.lower() != b.lower()):
                #print "title and search term not the same"
                #print "\n"
                continue
            else:
                #print "Same article title and search terms in meta"
                articleTitle = a
                articleYear = str(article[1])
                try:
                    metaTitle = meta["message"]["items"][0]["title"][0]
                except:
                    pass
                try:
                    metaYear = str(meta["message"]["items"][0]["issued"]["date-parts"][0][0]).strip()
                except:
                    pass
                try:
                    metaPublisher = meta["message"]["items"][0]["publisher"]
                except:
                    pass
                try:
                    metaDOI = meta["message"]["items"][0]["DOI"]
                except:
                    pass
                try:
                    metaOriginURL = meta["message"]["items"][0]["URL"]
                except:
                    pass
                try:
                    metaISSN = meta["message"]["items"][0]["ISSN"]
                except:
                    pass
                try:
                    metaSubject = meta["message"]["items"][0]["subject"]
                except:
                    pass
                try:
                    metaType = meta["message"]["items"][0]["type"]
                except:
                    pass

                metaAuthor = []
                try:
                    for author in meta["message"]["items"][0]["author"]:
                        metaAuthorDict = {}
                        try:
                            firstName = author["given"].encode('ascii', 'ignore')
                            metaAuthorDict["First name"] = firstName
                        except:
                            pass
                        try:
                            metaAuthorDict["Last name"] = author["family"].encode('ascii', 'ignore')
                            metaAuthor.append(metaAuthorDict)
                        except:
                            pass
                except:
                    pass

                """print "comparing this info: "
                print articleTitle
                print metaTitle
                print articleYear
                print metaYear
                print "\n"
                """

                articleDict["Title"] = articleTitle
                articleDict["Year"] = articleYear
                status["isMetaTitleEqualToOriginal"] = "False"
                status["isMetaYearEqualToOriginal"] = "True"

                at = re.sub(r'\W+', '', articleTitle).lower()
                mt = re.sub(r'\W+', '', metaTitle).lower()
                if (difflib.SequenceMatcher(None, at, mt).ratio() > 0.9):
                    #print "title is the same --> put into same shit!"

                    articleDict["Publisher"] = str(metaPublisher)
                    articleDict["DOI"] = str(metaDOI)
                    articleDict["OriginURL"] = str(metaOriginURL)
                    articleDict["Author"] = metaAuthor
                    articleDict["ISSN"] = metaISSN
                    articleDict["Subject"] = metaSubject
                    articleDict["Type"] = str(metaType)
                    ab = article[5]
                    ab = ab.encode("ascii", "ignore")
                    articleDict["Abstract"] = ab
                    articleDict["ID"] = str(article[0])
                    articleDict["Category"] = str(article[2])
                    articleDict["Endorsement"] = str(article[3])
                    status["isMetaTitleEqualToOriginal"] = "True"
                    if (articleYear != metaYear):
                        status["isMetaYearEqualToOriginal"] = "False"
                else:
                    #print "DIFFERENT TITLES"
                    articleDict["Meta title"] = metaTitle
                    print "title not equal:"
                    print  at
                    print  mt

                articleDict["Status"] = status
                info.append(articleDict)
                #print "\n"
                break
    #print "size of meta info after: " + str(len(metaInfo))


    #print "Size of info: " + str(len(info))
    print "finished with meta data comparison"
    print "Example: "
    print info[0]
    print info[1]
    print info[2]

    return info


def printShizzle(info):
    print "size of info: " + str(len(info))
    counter = 0
    for x in info:
        if (x["Status"]["isMetaTitleEqualToOriginal"] == "False"):
            counter += 1
    print "number of meta titles NOT EQUAL to original is " + str(counter)

info = compareData()
printShizzle(info)