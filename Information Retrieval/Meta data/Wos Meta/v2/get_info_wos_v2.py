import json
import time
from xml.etree import ElementTree
import suds
import credentialsv2 as c
import pandas as pd
import wos.utils
from wos import WosClient

import adder


def isOperator(string):
    operators = ["AND", "OR", "NOT", "NEAR", "SAME"]
    for word in string.split(" "):
        if word.upper() in operators:
            return True
    return False

def removeOperator(string):
    operators = ["AND", "OR", "NOT", "NEAR", "SAME"]
    return ' '.join([word for word in string.split(" ") if word.upper() not in operators])

def queryWos(titles, years):
    # Create an empty list which should contain info later
    info = []
    # Connect to Web of Science
    with WosClient(c.getUserName(), c.getPassword()) as client:
        # Looping through the titles (search parameter)
        for i,title in enumerate(titles):
            # Replace '|' with ','
            title = title.replace("|","")
            # Get year published
            year = years[i]
            # Create year query with +/- 1 year
            query_string_year = 'PY=(' + str(year-1) + ' OR ' + str(year) + ' OR ' + str(year+1) + ')'
            # Check if the title contains any operators (like AND, OR, NOT)
            if isOperator(title):
                title = removeOperator(title)
            # Create title query
            query_string_title = 'TI=' + title
            # Create query AND operator string
            query_AND_operator = ' AND '
            # Create the query string
            query_string = query_string_title + query_AND_operator + query_string_year
            print query_string
            # Perform the query on wos engine
            root = None
            try:
                root = wos.utils.query_v2(client, query_string, count=1)
                time.sleep(1)
            except suds.WebFault:
                print "Suds.WebFault: Waiting 1 minute"
                print suds.WebFault.message
                time.sleep(60)
            except:
                print "Some other error occured"
            info.append(root)
    return info

def extractDataFromRoot(roots):
    data = []
    for i,root in enumerate(roots):
        data.append(adder.add(root, i))
    return data


def init():
    # Get all titles
    tcp_data = pd.read_csv("../../../tcp_abstracts.txt")
    # Return a small list of titles for testing
    small_list_titles = tcp_data.Title.iloc[:2]
    small_list_years = tcp_data.Year.iloc[:2]
    # Get a list of dicts containing data wos
    list_of_roots_from_wos = queryWos(small_list_titles, small_list_years)
    data = extractDataFromRoot(list_of_roots_from_wos)

    """
    with open('wos_data.json','w') as f:
        json.dump(data,f)
        f.close()
    """

init()