def add(dic, new_dic):
    """
    Add important data here with try/except clauses..
    """
    # TODO: Include the most important fields with try/except clauses

    # Add country and city
    try:
        l_country = []
        l_city = []
        if dic['Num_of_organizations'] >= 1:
            for i in range(dic['Num_of_organizations']):
                key_string_country = "Organization_country"+str(i)
                key_string_city = "Organization_city" + str(i)
                l_country.append(dic[key_string_country])
                l_city.append(dic[key_string_city])
            new_dic['Organization_country'] = l_country
            new_dic['Organization_city'] = l_city
    except:
        print("No 'Organization_country' found..")
    # Anothter try for country
    try:
        if dic['country']:
            new_dic["Country"] = dic['country']
    except:
        print("No 'country' found..")
    # Anothter try for city
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
        l = []
        if dic["Num_of_authors"] >= 1:
            for i in range(dic["Num_of_authors"]):
                author_key = "Author_name" + str(i)
                l.append(dic[author_key])
            new_dic["Authors"] = l
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