import System.DataProcessing.process_data as ptd
import System.DataProcessing.process_meta_data as ptmd
import pandas as pd
import numpy as np
"""
dic["_id"] = id
dic["Abstract"] = Abstract
dic["Endorsement"] = Endorsement value
dic["Stance"] = Endorsement converted to stance
dic["Category"] = Category
dic["Title"] = Title
dic["Publication_year"] = Year

dic["Language"] = Language
dic["References"] = Number of references
dic["Organization_info"] = Organization info (stored as a list with lists [[Country, City, (if street), (if organization name)], [], []])
dic["Keywords"] = Keywords
dic["Headers"] = Document Headers
dic["Sub_headers"] = Document Subheaders
dic["Subjects"] = Docuemnt Subjects
dic["Publisher_info"] = Publisher info (stored as list [Country, City, Publisher name])
dic["Publication_month"] = Publication month
dic["Publication_volume"] = Publication volume
dic["Publication_type"] = Publication type
dic["Publication_issue"] = Publication issue
dic["Publication_length"] = Publication length (number of pages)
dic["Authors"] = Authors (stored as list ["Last name, first name initals"], i.e ["Coleman, SD", "Lawyer, P"]
dic["Document_type"] = Document type
dic["WOS"] = Web of Science ID
"""

def getInfoAboutStance(stance="All"):
    if stance == "All":
        d = ptd.getMetaDataAsList()
        data = pd.DataFrame(d)
    else:
        data = getStanceData(stance)
    print("Data consist of {} records".format(len(data)))

    print("TITLE INFO\n")
    getTitleInfo(data.Title)
    print("YEAR INFO\n")
    getPublicationYear(data.Publication_year)
    print("LANGUAGE INFO\n")
    getLanguage(data.Language)
    print("REFERENCE INFO\n")
    getRefs(data.References)
    print("ORGANIZATION INFO\n")
    #getOrgInfo


def getRefs(frame):
    frame.fillna("nan", inplace=True)
    refs = frame.tolist()
    refs = [int(r) for r in refs if r != "nan"]
    uniq = list(set(refs))
    print("There are {} unique reference counts".format(len(uniq)))
    print("The highest reference count is {0}, while the lowest is {1}".format(max(refs), min(refs)))
    print("The average reference count is: {:.2f}".format(sum(refs)/float(len(refs))))


def getLanguage(frame):
    frame.fillna("nan", inplace=True)
    lang = frame.tolist()
    lang = [l for l in lang if l != "nan"]
    uniq = list(set(lang))
    print("There are {} different languages".format(len(uniq)))
    print("These languages are:\n{}".format(uniq))
    d = dict(zip(uniq, np.zeros(len(uniq))))
    for l in lang:
        d[l] += 1
    print("The distribution is: (the rest was not found)\n{}".format(d))

def getPublicationYear(frame):
    years = frame.tolist()
    unique = set(years)
    print("There are publication from {} different years".format(len(unique)))
    print("These years are:\n{}".format(unique))

def getTitleInfo(frame):
    titles = frame.tolist()
    avg = sum([len(title.split(" ")) for title in titles])/len(titles)
    print("The average word length of titles are: {}".format(avg))
    unique = set([word for title in titles for word in title.split(" ")])
    print("There are {} unique words in the titles".format(len(unique)))

def getStanceData(stance):
    d = ptd.getMetaDataAsList()
    data = pd.DataFrame(d)
    return data[data.Stance == stance]

#getInfoAboutStance("All")
#getInfoAboutStance("FAVOR")
getInfoAboutStance("AGAINST")
#getInfoAboutStance("NONE")

