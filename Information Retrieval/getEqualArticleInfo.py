import json
import getArticleTitle

def compareData():
    articleInfo = getArticleTitle.getArticleInfo("tcp_articles.txt")
    with open("retrieval/retrieval/spiders/metaInfo.json") as metaJson:
        metaInfo = json.loads(metaJson)[0]

