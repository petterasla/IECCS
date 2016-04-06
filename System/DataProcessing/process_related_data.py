"""
This file opens the file with TCP  related records gathered from Web of Science.
The file is stored as JSON and contains a big list with dictionaries for each
record (20 791 records).

Notice that only abstract has been filtered and is safe to request. The rest could potentially be nothing
- stored as None (at least should be)

Below is the dictionary info about keys and values of related data

dic["Abstract"] = Abstract
dic["Title"] = Title
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

def getRelatedDataFile():
    with open("../TextFiles/data/related_data.json", "r") as f:
        data = json.load(f)
    return data
