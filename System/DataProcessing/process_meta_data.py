"""
This file opens the file with TCP with meta data gathered from Web of Science.
The file is stored as JSON and contains a big list with dictionaries for each
record from TCP data (11 942).

Notice that only the first seven keys are certain in each dictionary, the rest
could potentially be nothing - stored as None (at least should be)

Below is the dictionary info about keys and values

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

Create new methods when needed :-)
"""
import json

def getMetaDataFile():
    with open("../TextFiles/data/meta_data.json", "r") as f:
        data = json.load(f)
    return data

