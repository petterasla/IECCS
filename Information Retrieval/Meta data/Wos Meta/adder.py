def add(dic, new_dic):
    """
    Add important data here with try/except clauses..
    """

    # Add country
    try:
        if dic['Organization_country0']:
            new_dic['Organization_country'] = dic['Organization_country0']
    except:
        print("No 'Organization_country0' found..")
    try:
        if dic['country']:
            new_dic["Country"] = dic['country']
    except:
        print("No 'Organization_country found..")
    # Add city
    try:
        if dic["Organization_city0"]:
            new_dic["Organization_city"] = dic["Organization_city"]
    except:
        print("No 'Organization_city' found...")
    try:
        if dic["city"]:
            new_dic["City"] = dic["city"]
    except:
        print("No 'city' found..")

    # Add state
    try:
        new_dic["State"] = dic["state"]
    except:
        print("No 'state' found...")

    # Add authors
    try:
        if dic["Num_of_authors"] > 1:
            l = []
            for i in range(dic["Num_of_authors"]):
                author_key = "Author_name" + str(i)
                l.append(dic[author_key])
            new_dic["Authors"] = l
        elif dic["Num_of_authors"] == 1:
            new_dic["Authors"] = dic["Author_name0"]
    except:
        print("No 'Authors' found")

    # Add heading..
    try:
        new_dic["Heading"] = dic['heading']
    except:
        print("Heading went wrong")
    # Add publication type
    try:
        new_dic["Publication_type"] = dic['pubtype']
    except:
        print("Publication type went wrong")

    # Add document type
    try:
        new_dic["Document_type"] = dic["doctype"]
    except:
        print("No 'doctype' found..")

    # Add keyword
    try:
        new_dic["Keywords"] = dic["keyword"]
    except:
        print("No 'keyword' found..")

    # Add pagecount
    try:
        new_dic["Page_count"] = dic['page_count']
    except:
        print("No 'page_count' found")

    # Add subject
    try:
        new_dic["Subject"] = dic["subject"]
    except:
        print("No 'subject' found...")

    # Add UID
    try:
        new_dic["UID"] = dic["UID"]
    except:
        print("No 'UID' found..")

    # Add volume
    try:
        new_dic["Vol"] = dic['vol']
    except:
        print("No 'vol' found..")

    # Add organization
    try:
        new_dic["Organization"] = dic["organization"]
    except:
        print("No 'organization' found..")

    # Add issue (whatever that is..)
    try:
        new_dic["Issue"] = dic["issue"]
    except:
        print("No 'issue' found..")

    return new_dic