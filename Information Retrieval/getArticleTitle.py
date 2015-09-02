def getArticleInfo():
    articleInfo = []
    f = open("tcp_articles.txt","r")
    line = f.readline() #Firste line states id, year, title of the article
    print "first line: " + str(line)
    line = f.readline()
    counter = 0
    while line:
        if ord(line[0]) < 48 or ord(line[0]) > 57: # Based on the ascii value: 0-9 is from 48-57
            #print "APPENDING"
            articleInfo[counter-1][2] = (articleInfo[counter-1][2].strip()) + " " + line
            print articleInfo[counter-1][2]
        else:
            split_index = list_duplicates_of(line,",")
            print split_index
            id = line[:split_index[0]]
            print id
            year = line[split_index[0]+1:split_index[1]]
            print year
            title = line[split_index[1]+1:-1] #Removing \n from the string
            print title
            article = [id, year, title]
            articleInfo.append(article)
            counter += 1
            #print "NEW: " + str(article)

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
    list = getArticleInfo()
    print str(list[1:5])

