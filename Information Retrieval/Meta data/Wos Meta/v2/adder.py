def add(root, id, tcp_data):
    dic = {}

    dic["_id"] = id
    dic["Abstract"] = tcp_data.loc[id].Abstract.replace("|",",")
    dic["Endorsement"] = tcp_data.loc[id].Endorse
    dic["Stance"] = getStanceByEndorse(tcp_data.loc[id].Endorse)
    dic["Category"] = tcp_data.loc[id].Cat
    dic["Title"] = tcp_data.loc[id].Title.replace("|",",")
    dic["Publication_year"] = tcp_data.loc[id].Year

    dic["Language"] = getLanguage(root)
    dic["References"] = getRefs(root)
    dic["Organization_info"] = getOrganizationInfo(root)
    dic["Keywords"] = getKeywords(root)
    dic["Headers"] = getHeaders(root)
    dic["Sub_headers"] = getSubHeader(root)
    dic["Subjects"] = getSubjects(root)
    dic["Publisher_info"] = getPublisherInfo(root)
    dic["Publication_month"] = getPublicationInfo(root, "pubmonth")
    dic["Publication_volume"] = getPublicationInfo(root, "vol")
    dic["Publication_type"] = getPublicationInfo(root, "pubtype")
    dic["Publication_issue"] = getPublicationInfo(root, "issue")
    dic["Publication_length"] = getPublicationLength(root)
    dic["Authors"] = getAuthors(root)
    dic["Document_type"] = getDocumentType(root)
    dic["WOS"] = getWOS(root)

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
        #print("No 'language' found")
        return None

def getRefs(root):
    l = root.findall(".REC/static_data/fullrecord_metadata/refs")
    try:
        return l[0].attrib['count']
    except:
        #print("No 'refs' found")
        return None

def getAddressSpec(list, tryNumber):
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
    individual = None
    try:
        individual = [country, city]
        individual = [country, city, org]
        individual = [country, city, street, org]
        return individual
    except:
        if individual is None:
            print("Organization_spec was 'None' with try {} out of 3".format(tryNumber))
        return individual


def getOrganizationInfo(root):
    orgs = []
    lis = root.findall(".REC/static_data/fullrecord_metadata/addresses/address_name/")
    lis2 = root.findall("./REC/static_data/fullrecord_metadata/reprint_addresses/address_name/address_spec/")
    lis3 = root.findall(".REC/static_data/item/reprint_contact/address_spec/")
    if len(lis) > 0:
        for li in lis:
            ret = getAddressSpec(li, 1)
            if ret is not None:
                orgs.append(ret)
    elif len(lis2) > 0:
        ret = getAddressSpec(lis2, 2)
        if ret is not None:
            orgs.append(ret)
    elif len(lis3) > 0:
        ret = getAddressSpec(lis3, 3)
        if ret is not None:
            orgs.append(ret)

    if len(orgs) == 0:
        #print("No 'organizations' found")
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
        #print("No 'keywords' found")
        return None

def getHeaders(root):
    lis = root.findall(".REC/static_data/fullrecord_metadata/category_info/headings/")
    if len(lis) > 0:
        return [l.text for l in lis]
    else:
        #print("No 'headers' found")
        return None

def getSubHeader(root):
    lis = root.findall(".REC/static_data/fullrecord_metadata/category_info/subheadings/")
    if len(lis) > 0:
        return [l.text for l in lis]
    else:
        #print("No 'Sub headers' found")
        return None

def getSubjects(root):
    lis = root.findall(".REC/static_data/fullrecord_metadata/category_info/subjects/")
    if len(lis) > 0:
        return [l.text for l in lis]
    else:
        #print("No subjects found")
        return None

def getPublisherInfo(root):
    address = root.findall(".REC/static_data/summary/publishers/publisher/address_spec/full_address")[0].text
    city = root.findall(".REC/static_data/summary/publishers/publisher/address_spec/city")[0].text
    name = root.findall(".REC/static_data/summary/publishers/publisher/names/name/full_name")[0].text
    try:
        pub_info = [i.strip() for i in address.split(",")]
        if len(city) > 0:
            pub_info[1] = city
        pub_info.append(name)

        if len(pub_info) > 0:
            return pub_info.reverse()
    except:
        #print("No publisher info found")
        return None

def getPublicationInfo(root, key):
    dic = root.findall(".REC/static_data/summary/pub_info")[0].attrib
    try:
        return dic[key]
    except:
        #print("No publication info with key '{}' found".format(key))
        return None

def getPublicationLength(root):
    ret = root.findall(".REC/static_data/summary/pub_info/")[0].attrib['page_count']
    if len(ret) == 0:
        #print("No 'page count' found")
        return None
    else:
        return ret

def getAuthors(root):
    lis = root.findall(".REC/static_data/summary/names/")
    author = []
    for li in lis:
        for l in li:
            if l.tag == "wos_standard":
                author.append(l.text)
    if len(author) > 0:
        return author
    else:
        #print("No 'author' found")
        return None

def getDocumentType(root):
    ret = root.findall(".REC/static_data/summary/doctypes/doctype")[0].text
    if len(ret) == 0:
        #print("No 'document type' found")
        return None
    else:
        return ret

def getWOS(root):
    ret = root.findall(".REC/UID")[0].text
    if len(ret) == 0:
        #print("No 'WOS' found")
        return None
    else:
        return ret

def getAbstract(root):
    ret = root.findall("static_data/fullrecord_metadata/abstracts/abstract/abstract_text/")
    try:
        return ret[0].text
    except:
        return None

