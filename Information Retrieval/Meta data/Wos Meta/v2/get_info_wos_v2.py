import json
import time
from xml.etree import ElementTree
import suds
import credentialsv2 as c
import pandas as pd
import wos.utils
from wos import WosClient
import re
import adder
import difflib


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

    #with open("data/wos_not_meta_data.json", "r") as f:
    #    small_list_ids = json.load(f)
    # Create an empty list which should contain info later
    info = []
    not_found = []
    # Connect to Web of Science
    with WosClient(c.getUserName(), c.getPassword()) as client:
        print("Starting the queries")
        # Looping through the titles (search parameter)
        for i, id in enumerate(tcp_data.index.values.tolist()[start_sample:end_sample]):
            # Replace '|' with ','
            title = tcp_data.loc[id].Title.replace("|",",").replace("?","").replace('"', '').replace("/"," ").replace("-", " ").replace(":", " ")
            title = re.sub(r'\([^)]*\)', '', title)
            title = title.replace("(","").replace(")","")
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
            wait = 2
            try:
                root = wos.utils.query_v2(client, query_string, count=1)
            except suds.WebFault:
                print "Suds.WebFault: Waiting {} sec".format(wait)
                print suds.WebFault.args
                time.sleep(wait)
            except:
                print "Some other error occured, sleep {} sec".format(wait)
                time.sleep(wait)
            if root is None:
                # Adding tuple with id and title
                not_found.append(id)
                print("Did not find record with title {}".format(title))
                print("Not found length is {}".format(len(not_found)))
            else:
                # Adding dictionary
                tcp_data_title = tcp_data.loc[id].Title.replace("|", ",")
                tcp_data_title = re.sub(r'\([^)]*\)', '', tcp_data_title)
                wos_title = getTitle(root)
                wos_title = re.sub(r'\([^)]*\)', '', wos_title)
                print("tcp title: {}".format(tcp_data_title))
                print("wos title: {}".format(wos_title))
                print
                if difflib.SequenceMatcher(None, tcp_data_title, wos_title).ratio() > 0.95:
                    if getAbstract(root) is not None:
                        info.append((root, id))
                        print("Successfully retrieved is now {}".format(len(info)))
                    else:
                        print
                        print("Abstract was none")
                        print
                else:
                    print("titles not alike...")
                    not_found.append(id)
            print("Number of queries so far is {}. Time used is {:0.1f} minutes".format((i+1),((time.time()-start)/60.0)))
            time.sleep(0.5)
    return info, not_found

def extractDataFromRoot(roots, tcp_data):
    data = []
    for root in roots:
        data.append(adder.add(root[0], root[1], tcp_data))
    return data

def getAbstract(root):
    ret = root.findall(".REC/static_data/fullrecord_metadata/abstracts/abstract/abstract_text/")
    try:
        return ret[0].text
    except:
        return None

def getTitle(root):

    try:
        ret = root.findall(".REC/static_data/summary/titles/")
        titles = [i.text for i in ret]
        lengths = [len(s) for s in titles]
        index = lengths.index(max(lengths))
        title = titles[index]
        return title
    except:
        return None

def init():
    # Get all titles
    tcp_data = pd.read_csv("../../../../System/TextFiles/data/tcp_abstracts.txt", index_col="Id")
    parts = 15
    slice = len(tcp_data)/parts
    start = -slice
    end = slice
    for i in range(parts):
        start += slice
        end += slice
        if i == parts-1:
            end = None

        start_time = time.time()
        # Get a list of dicts containing data wos
        list_of_roots_from_wos, not_found = queryWos(tcp_data, start_time, start, end)
        data = extractDataFromRoot(list_of_roots_from_wos, tcp_data)
        print ("len of abstracts = {}".format(len(list_of_roots_from_wos)))

        if end is None:
            end = "_of_not_found"

        file_name = 'data/abstract_check/wos_data_{}.json'.format(end)
        with open(file_name,'w') as f:
            json.dump(data,f)

        not_found_file = 'data/abstract_check/not_found{}.json'.format(end)
        with open(not_found_file, 'w') as f:
            json.dump(not_found, f)

        s1 = "Time used was {:0.2f} seconds or {:0.1f} minutes \n".format((time.time() - start_time), ((time.time()-start_time)/60.0))
        s2 = "Number of successfully retrieved records was {} \n".format(len(list_of_roots_from_wos))
        s3 = "Number of unsuccessfully retrieved records was {} \n".format(len(not_found))

        with open("data/abstract_check/wos_info.txt", "a") as f:
            f.write(s1)
            f.write(s2)
            f.write(s3)




init()

