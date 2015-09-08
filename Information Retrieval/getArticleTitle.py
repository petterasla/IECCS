##### Takes the document name and return a list with the articles on the format:
##### [ ['1', '2009', 'This is a title'],
#####   ['2', '2009', 'This is another title'],
#####   ['3', '2010', 'Third title']
##### ]

#from articledownloader.articledownloader import ArticleDownloader
#downloader = ArticleDownloader('7dca2bf4cf2dddf69241416cece3d02a')


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

def generateSearchURL(self, title):
    return "http://www.scopus.com/results/results.url?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1=" + \
           title + "&field1=TITLE&dateType=Publication_Date_Type&yearFrom=Before+1960&yearTo=Present&loadDate=7&documenttype=All&subjects=LFSC&subjects=HLSC&subjects=PHSC&subjects=SOSC&src=s&st1=" + \
           title + "&st2=&sot=b&sdt=b&sl=&s=TITLE%28" + \
           title + "%29&sid=&searchId=&txGid=&sort=plf-f&originationType=b&rr=&null="

def generateSearchURLs(self):
    list = getArticleInfo("tcp_articles.txt")
    URLs = []
    for title in list:
        URLs.append(generateSearchURL(title))
    return URLs


if __name__ == '__main__':
    print "Running main.."
    #list = getArticleInfo("tcp_articles.txt")
    #URLs = []
    #for title in list:
        #URLs.append(generateSearchURL(title))

    #print list[1]
    #DOIs = []
    #antallArtikler = 10
    #for i in range(antallArtikler):
        #print list[i]
        #DOI = downloader.get_dois_from_search(list[i][2], 1)
        #print DOI.pop()
        #DOIs.append([list[i][0], list[i][1], list[i][2], DOI.pop()])

    #for i in range(len(DOIs)):
        #print DOIs[i]

    #print antallArtikler
    #print len(DOIs)

    #print DOI.pop()
    #abstract = downloader.get_abstract_from_doi(DOI.pop(), 'elsevier')
    #print abstract
    #print downloader.get_pdf_from_doi(DOI.pop(), 'test.pdf', 'elsevier')
