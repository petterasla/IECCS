def add(dic, new_dic):
    """
    Add important data here with try/except clauses..
    """
    # TODO: Include the most important fields with try/except clauses

    # Add organization info: country, city, street and organization
    try:
        l_organization_info = []
        if dic['Num_of_organizations'] >= 1:
            for i in range(dic['Num_of_organizations']):
                key_string_country = "Organization_country"+str(i)
                key_string_city = "Organization_city" + str(i)
                key_string_street = "Organization_street" + str(i)
                key_string_organization = "Organization_org" + str(i)

                # l_individual = [country, city, street, organization]
                if len(dic[key_string_organization]) > 1:
                    l_individual_org = [dic[key_string_country], dic[key_string_city], dic[key_string_street], dic[key_string_organization][1]]
                elif len(dic[key_string_organization]) == 1:
                    l_individual_org = [dic[key_string_country], dic[key_string_city], dic[key_string_street], dic[key_string_organization][0]]
                else:
                    l_individual_org = [dic[key_string_country], dic[key_string_city], dic[key_string_street], dic[key_string_organization]]
                l_organization_info.append(l_individual_org)

            new_dic['Organization_info'] = l_organization_info
    except:
        print("No 'Organization_info' found..")

    # Add publication info
    try:
        if dic['full_address']:
            l = dic['full_address'].split(",")
            for i, item in enumerate(l):
                l[i] = item.strip()

            # Add as list = [street, city, country, full_name]
            try:
                if dic['city']:
                    l[1] = dic['city']
            except:
                print("No 'city' found in publication info..")
            try:
                if dic['full_name']:
                    l.append(dic['full_name'])
            except:
                print("No 'full_name' found in publication info")
    except:
        print("No (publication) 'info' found..")

    # Try publication city
    try:
        if dic["city"]:
            new_dic["Publication_city"] = dic["city"]
    except:
        print("No (publication) 'city' found..")

    # Add state
    try:
        new_dic["State"] = dic["state"]
    except:
        print("No 'state' found...")

    # Add street
    try:
        new_dic["Street"] = dic["street"]
    except:
        print("No (publication) 'street' found..")

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
        print("No 'heading' found..")

    # Add publication type
    try:
        new_dic["Publication_type"] = dic['pubtype']
    except:
        print("No 'pubtype' found..")

    # Add publication month
    try:
        new_dic['Publication_month'] = dic['pubmonth']
    except:
        print("No 'pubmonth' found..")

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