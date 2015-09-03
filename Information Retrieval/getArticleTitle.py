##### Takes the document name and return a list with the articles on the form:
##### [ ['1', '2009', 'This is a title'],
#####   ['2', '2009', 'This is another title'],
#####   ['3', '2010', 'Third title']
##### ]

def getArticleInfo(doc_name):
    articleInfo = []
    f = open(doc_name,"r")
    line = f.readline() #Firste line states id, year, title of the article
    line = f.readline()
    counter = 0
    while line:
        split_index = list_duplicates_of(line,",")
        if ord(line[0]) < 48 or ord(line[0]) > 57 or len(split_index) != 2: # Based on the ascii value: 0-9 is from 48-57
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


if __name__ == '__main__':
    print "Running main.."
    list = getArticleInfo("tcp_articles.txt")
    print list[1]

