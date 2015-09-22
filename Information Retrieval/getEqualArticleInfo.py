import json
import sys
sys.path.insert(0, "/Users/petterasla/Desktop/Skole/9. semester/In-Depth project/IECCS/Information Retrieval/retrieval/retrieval/spiders")
import getArticleTitle

def compareData():
    articleInfo = getArticleTitle.getArticleInfo("tcp_articles.txt")
    print "Article: " + articleInfo[0][2] + " -- published: " + str(articleInfo[0][1])

    with open("retrieval/retrieval/spiders/metaInfo.json") as metaJson:
        metaInfo = json.load(metaJson)
        metaJson.close()

    print "MetaInfo: " + str(metaInfo) + "\n\n"

    titleArticle = articleInfo[0][2].lower().strip()
    titleMeta = metaInfo[0]["message"]["items"][0]["title"][0].lower().strip()
    print titleArticle
    print titleMeta
    print titleArticle == titleMeta

    print "\n"

    yearArticle = str(articleInfo[0][1]).strip()
    yearMeta = str(metaInfo[0]["message"]["items"][0]["issued"]["date-parts"][0][0]).strip()
    print yearArticle
    print yearMeta
    print yearArticle == yearMeta
    print "\n"

    info = []
    print "size of meta info before: " + str(len(metaInfo))
    print "size of articles info before: " + str(len(articleInfo))
    for article in articleInfo[0:30]:
        articleDict = {}
        status = {}
        for meta in metaInfo[0:30]:
            if (article[2]!= meta["message"]["query"]["search-terms"]):
                print "title and search term not the same"
                print "\n"
                continue
            else:
                print "Same article title and search terms in meta"
                articleTitle = article[2].lower().strip()
                articleYear = str(article[1].lower().strip())
                try:
                    metaTitle = meta["message"]["items"][0]["title"][0].lower().strip()
                except:
                    print "Title not found"
                try:
                    metaYear = str(meta["message"]["items"][0]["issued"]["date-parts"][0][0]).strip()
                except:
                    print "Year not found"
                try:
                    metaPublisher = meta["message"]["items"][0]["publisher"]
                except:
                    print "Publisher not found"
                try:
                    metaDOI = meta["message"]["items"][0]["DOI"]
                except:
                    print "DOI not found"
                try:
                    metaOriginURL = meta["message"]["items"][0]["URL"]
                except:
                    print "OriginURL not found"
                try:
                    metaISSN = meta["message"]["items"][0]["ISSN"]
                except:
                    print "ISSN not found"
                try:
                    metaSubject = meta["message"]["items"][0]["subject"]
                except:
                    print "Subject doesnt exist"
                try:
                    metaType = meta["message"]["items"][0]["type"]
                except:
                    print "Meta type not found"

                metaAuthor = []
                for author in meta["message"]["items"][0]["author"]:
                    metaAuthorDict = {}
                    try:
                        firstName = author["given"].encode('ascii', 'ignore')
                        metaAuthorDict["First name"] = firstName
                    except:
                        print "First name not found"
                    try:
                        metaAuthorDict["Last name"] = author["family"].encode('ascii', 'ignore')
                        metaAuthor.append(metaAuthorDict)
                    except:
                        print "Last name not found"


                print "comparing this info: "
                print articleTitle
                print metaTitle
                print articleYear
                print metaYear
                print "\n"

                articleDict["Title"] = str(articleTitle)
                articleDict["Year"] = str(articleYear)
                status["isMetaEqualToOriginal"] = "False"


                if (articleTitle == metaTitle):
                    print "title is the same --> put into same shit!"

                    articleDict["Publisher"] = str(metaPublisher)
                    articleDict["DOI"] = str(metaDOI)
                    articleDict["OriginURL"] = str(metaOriginURL)
                    articleDict["Author"] = metaAuthor
                    articleDict["ISSN"] = str(metaISSN)
                    articleDict["Subject"] = str(metaSubject)
                    articleDict["Type"] = str(metaType)
                    status["isMetaEqualToOriginal"] = "True"
                else:
                    print "DIFFERENT TITLES"
                    articleDict["Meta title"] = metaTitle.encode('ascii', 'ignore')

                articleDict["Status"] = status
                info.append(articleDict)
                metaInfo.remove(meta)
                print "\n"
                break
    print "size of meta info after: " + str(len(metaInfo))
    print info


    print "Size of info: " + str(len(info))
    return info

def addAbstract(info):
    with open("retrieval/retrieval/spiders/abstracts.json") as metaJson:
        abstracts = json.load(metaJson)
        metaJson.close()

    print abstracts[0]
    title1 = abstracts[0]["title"]
    title2 = info[0]["Title"]

    print title1
    print title2
    print title1 == title2

    print "\n\n ADding abstracts..."

    for x in info:
        for abstract in abstracts:
            title = abstract["title"].lower()
            print "X in info:"
            print x["Title"]
            print x["Title"] == title

            x["Status"]["isAbstractEqualToOriginal"] = "False"
            if (x["Title"] != title):
                continue
            else:
                print "titles are equal, append abstract and url"
                x["URL"] = abstract["url"].encode('ascii', 'ignore')
                x["Abstract"] = abstract["abstract"][0].encode('ascii', 'ignore')
                x["Status"]["isAbstractEqualToOriginal"] = "True"
                print "SETTING ABSTRACT EQUAL TO TRUE!"
                print "\n"
                break
    for x in info:
        print x
    print "\n Size of info: " + str(len(info))



info = compareData()
addAbstract(info)