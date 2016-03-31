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

def queryWos(tcp_data, start, start_sample, end_sample):
    # Return a small list of titles, year and ids for testing

    small_list_ids = tcp_data.index.values.tolist()[start_sample:end_sample]
    # Create an empty list which should contain info later
    info = []
    not_found = []
    # Connect to Web of Science
    with WosClient(c.getUserName(), c.getPassword()) as client:
        print("Starting the queries")
        # Looping through the titles (search parameter)
        for i, id in enumerate(small_list_ids):
            # Replace '|' with ','
            title = tcp_data.loc[id].Title.replace("|","").replace("(","").replace(")","").replace("?","").replace('"', '').replace("/"," ")
            # Get year published
            year = tcp_data.loc[id].Year
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
            #print query_string
            # Perform the query on wos engine
            root = None
            try:
                root = wos.utils.query_v2(client, query_string, count=1)
            except suds.WebFault:
                print "Suds.WebFault: Waiting 1 minute"
                print suds.WebFault.args
                time.sleep(60)
            except:
                print "Some other error occured, sleep 30 minute"
                time.sleep(30)
            if root is None:
                # Adding tuple with id and title
                not_found.append(id)
                print("Did not find record with title {}".format(tcp_data.loc[id].Title))
                print("Not found length is {}".format(len(not_found)))
            else:
                # Adding dictionary
                info.append((root, id))
                if len(info) % 25 == 0:
                    print("Successfully retrieved is now {}".format(len(info)))
            if (i+1) % 50 == 0:
                print("Number of queries so far is {}. Time used is {:0.1f} minutes".format((i+1),((time.time()-start)/60.0)))
            time.sleep(1)
    return info, not_found

def extractDataFromRoot(roots, tcp_data):
    data = []
    for root in roots:
        data.append(adder.add(root[0], root[1], tcp_data))
    return data


def init():
    # Get all titles
    start_time = time.time()
    tcp_data = pd.read_csv("../../../tcp_abstracts.txt", index_col="Id")

    # Get a list of dicts containing data wos
    sample_start = 2000
    sample_end = 3000
    list_of_roots_from_wos, not_found = queryWos(tcp_data, start_time, sample_start, sample_end)
    data = extractDataFromRoot(list_of_roots_from_wos, tcp_data)

    file_name = 'wos_data{}.json'.format(sample_end)
    with open(file_name,'w') as f:
        json.dump(data,f)
        f.close()

    not_found_file = 'not_found{}.json'.format(sample_end)
    with open(not_found_file, 'w') as f:
        json.dump(not_found,f)
        f.close()

    print("Time used was {:0.2f} seconds or {:0.1f} minutes".format((time.time() - start_time), ((time.time()-start_time)/60.0)))
    print("Number of successfully retrieved records was {}".format(len(list_of_roots_from_wos)))
    print("Number of unsuccessfully retrieved records was {}".format(len(not_found)))


init()

# TODO: Do trial runs to see if the server is overloaded...