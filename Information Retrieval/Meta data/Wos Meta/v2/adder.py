import pandas as pd
tcp_data = pd.read_csv("../../../tcp_abstracts.txt")


def add(root, index):
    dic = {}

    dic["_id"] = tcp_data.Id.iloc[index]
    dic["Abstract"] = tcp_data.Abstract.iloc[index].replace("|",",")
    dic["Endorsement"] = tcp_data.Endorse.iloc[index]
    dic["Stance"] = getStanceByEndorse(tcp_data.Endorse.iloc[index])
    dic["Category"] = tcp_data.Cat.iloc[index]
    dic["Title"] = tcp_data.Title.iloc[index].replace("|",",")

    dic["Language"] = getLanguage(root)
    dic["References"] = getRefs(root)
    dic["Organization_info"] = getOrganizationInfo(root)
    dic["Keywords"] = getKeywords(root)
    dic["Headers"] = getHeaders(root)
    dic["Sub_headers"] = getSubHeader(root)
    dic["Subjects"] = getSubjects(root)
    dic["Publisher_info"] = getPublisherInfo(root)
    dic["Publication_year"] = tcp_data.Year.iloc[index]
    dic["Publication_month"] = getPublicationInfo(root, "pubmonth")
    dic["Publication_volume"] = getPublicationInfo(root, "vol")
    dic["Publication_type"] = getPublicationInfo(root, "pubtype")
    dic["Publication_issue"] = getPublicationInfo(root, "issue")
    dic["Publication_length"] = getPublicationLength(root)
    dic["Authors"] = getAuthors(root)
    dic["Document_type"] = getDocumentType(root)
    dic["WOS"] = getWOS(root)

    print len(dic)
    print dic
    return dic

def getStanceByEndorse(endorse):
    if endorse <= 3:
        return "FAVOR"
    elif endorse >= 5:
        return "AGAINST"
    else:
        return "NONE"

def getLanguage(root):
    l = root.findall(".REC/static_data/fullrecord_metadata/languages/")
    try:
        return l[0].text
    except:
        return None

def getRefs(root):
    l = root.findall(".REC/static_data/fullrecord_metadata/refs")
    try:
        return l[0].attrib['count']
    except:
        return None

def getAddressSpec(list):
    individual = None
    for l in list:
        if l.tag == "country":
            country = l.text
        elif l.tag == "city":
            city = l.text
        elif l.tag == "street":
            street = l.text
        elif l.tag == "organizations":
            if len(l) > 1:
                org = l[1].text
            else:
                org = l[0].text
    try:
        individual = [country, city, street, org]
    except:
        print("Could not add organization_spec")
    return individual

def getOrganizationInfo(root):
    orgs = []
    lis = root.findall(".REC/static_data/fullrecord_metadata/addresses/address_name/")
    lis2 = root.findall(".REC/static_data/item/reprint_contact/address_spec/")
    if len(lis) > 0:
        for li in lis:
            orgs.append(getAddressSpec(li))
    elif len(lis2) > 0:
        orgs.append(getAddressSpec(lis2))

    if len(orgs) == 0:
        return None
    else:
        return orgs

def getKeywords(root):
    lis = root.findall(".REC/static_data/fullrecord_metadata/keywords/")
    lis2 = root.findall(".REC/static_data/item/keywords_plus/")
    if len(lis) > 0:
        return [i.text for i in lis]
    elif len(lis2) > 0:
        return [i.text for i in lis2]
    else:
        return None

def getHeaders(root):
    lis = root.findall(".REC/static_data/fullrecord_metadata/category_info/headings/")
    if len(lis) > 0:
        return [l.text for l in lis]
    else:
        return None

def getSubHeader(root):
    lis = root.findall(".REC/static_data/fullrecord_metadata/category_info/subheadings/")
    if len(lis) > 0:
        return [l.text for l in lis]
    else:
        return None

def getSubjects(root):
    lis = root.findall(".REC/static_data/fullrecord_metadata/category_info/subjects/")
    if len(lis) > 0:
        return [l.text for l in lis]
    else:
        return None

def getPublisherInfo(root):
    address = root.findall(".REC/static_data/summary/publishers/publisher/address_spec/full_address")[0].text
    city = root.findall(".REC/static_data/summary/publishers/publisher/address_spec/city")[0].text
    name = root.findall(".REC/static_data/summary/publishers/publisher/names/name/full_name")[0].text
    pub_info = [i.strip() for i in address.split(",")]
    if len(city) > 0:
        pub_info[1] = city
    pub_info.append(name)

    if len(pub_info) > 0:
        return pub_info
    else:
        return None

def getPublicationInfo(root, key):
    dic = root.findall(".REC/static_data/summary/pub_info")[0].attrib
    try:
        return dic[key]
    except:
        return None

def getPublicationLength(root):
    return root.findall(".REC/static_data/summary/pub_info/")[0].attrib['page_count']

def getAuthors(root):
    lis = root.findall(".REC/static_data/summary/names/")
    author = None
    for l in lis:
        if l.tag == "wos_standard":
            author.append(l.text)
    return author

def getDocumentType(root):
    return root.findall(".REC/static_data/summary/doctypes/doctype")[0].text

def getWOS(root):
    return root.findall(".REC/UID")[0].text