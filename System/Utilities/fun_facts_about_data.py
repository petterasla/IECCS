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
    print("SHOWING INFORMATION FOR THE SELECTED STANCE: '{}'\n".format(stance))
    print("Data consist of {} records".format(len(data)))
    print
    print 80*"-"
    print("TITLE INFO")
    getTitleInfo(data.Title)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("YEAR INFO")
    getPublicationYear(data.Publication_year)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("LANGUAGE INFO")
    getLanguage(data.Language)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("REFERENCE INFO")
    getRefs(data.References)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("ORGANIZATION INFO")
    getOrgInfo(data.Organization_info)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("PUBLICATION LENGTH")
    getPubLength(data.Publication_length)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("AUTHOR INFO")
    getAuthor(data.Authors)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("HEADER AND SUB-HEADER INFO ")
    print 80*"-"
    getHeader(data.Headers, data.Sub_headers)
    print 80*"-" + "\n\n"
    print 80*"-"
    print("SUBJECT INFO")
    print 80*"-"
    getSubject(data.Subjects)

def getHeader(header, sub_header):
    header.fillna("nan", inplace=True)
    sub_header.fillna("nan", inplace=True)
    headers = header.tolist()
    sub_header = sub_header.tolist()
    headers = [h for h in header if h != "nan"]
    headers = [h for sublist in header for h in sublist]
    sub_header = [h for h in header if h != "nan"]
    sub_header = [h for sub in sub_header for h in sub]
    uniq_head = list(set(headers))
    uniq_sub = list(set(sub_header))
    print("There are a total of {} headers, with {} unique ones".format(len(headers), len(uniq_head)))
    print("And a total of {} sub headers with {} unique ones".format(len(sub_header), len(uniq_sub)))


def getAuthor(frame):
    frame.fillna("nan", inplace=True)
    authors = frame.tolist()
    authors = [a for a in authors if a != "nan"]
    authors = [a for sublist in authors for a in sublist]
    uniq_authors = list(set(authors))
    print("There are a total {} contributing authors".format(len(authors)))
    print("while the unique number of authors are {}".format(len(uniq_authors)))

def getPubLength(frame):
    frame.fillna("nan", inplace=True)
    lengths = frame.tolist()
    lengths = [int(l) for l in lengths if l != "nan"]
    uniq_len = list(set(lengths))
    print("The shortest length of a publication is {}, while the longest is {}".format(min(uniq_len), max(uniq_len)))
    print("The average publication length is {:.2f}".format(sum(lengths)/float(len(lengths))))

def getOrgInfo(frame):
    frame.fillna("nan", inplace=True)
    info = frame.tolist()
    info = [i for i in info if i != "nan"]
    country = [org[0].lower() for sub in info for org in sub]
    uniq_country = list(set(country))
    uniq_country = [str(country[0].upper() + country[1:]) for country in uniq_country]
    city = [org[1].lower() for sub in info for org in sub]
    uniq_city = list(set(city))
    uniq_city = [str(c[0].upper() + c[1:]) for c in uniq_city]

    print("There are organization info from {} unique countries"
          "\nSome of them are {}".format(len(uniq_country), uniq_country[:5]))
    print("From {} different cities. Some of the cities are:\n{}".format(len(uniq_city), uniq_city[:10]))


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

def getSubject(header):
    header.fillna("nan", inplace=True)
    headers = header.tolist()
    headers = [h for h in headers if h != "nan"]
    headers = [h.lower().strip() for sublist in headers for h in sublist]
    uniq_head = list(set(headers))
    print("There are a total of {} subjects, with {} unique ones".format(len(headers), len(uniq_head)))



def getStanceData(stance):
    d = ptd.getMetaDataAsList()
    data = pd.DataFrame(d)
    return data[data.Stance == stance]

getInfoAboutStance("All")
#getInfoAboutStance("FAVOR")
#getInfoAboutStance("AGAINST")
#getInfoAboutStance("NONE")



