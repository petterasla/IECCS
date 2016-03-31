import json
import time
from xml.etree import ElementTree
import suds
import credentialsv2 as c
import pandas as pd
import wos.utils
from wos import WosClient
import adder_related


def queryRelatedWos(WOS, start_time):
    root_list = []
    with WosClient(c.getUserName(), c.getPassword()) as client:
        print("Starting to look for related records")
        for i,id in enumerate(WOS):
            try:
                records = wos.utils.get_related_records(client, id, count=2)
                roots = records.findall("REC")
                for root in roots:
                    root_list.append(root)
            except:
                print("Some error while adding roots. Waiting 30 sec")
                time.sleep(30)
            if (i+1) % 50 == 0:
                print("Queries so far is {}. Time used is {:0.1f}".format((i+1),((time.time()-start_time)/60.0)))
            time.sleep(1)
    return root_list

def extractDataFromRoot(roots, tcp_data):
    data = []
    for root in roots:
        data.append(adder_related.add(root))
    return data

def init():
    start_time = time.time()
    with open('wos_data.json','r') as f:
        data = json.load(f)
        f.close()

    #WOS = [d['WOS'] for d in data]
    WOS = ["WOS:A1991GM73000001"]
    roots = queryRelatedWos(WOS, start_time)
    related_data = extractDataFromRoot(roots, None)

    number = 1
    filename = "related_data{}.json".format(number)
    with open(filename, 'w') as f:
        json.dump(related_data, f)
        f.close()

    print("Time used was {:0.2f} seconds or {:0.1f} minutes".format((time.time() - start_time), ((time.time()-start_time)/60.0)))
    print("Number of successfully retrieved records was {}".format(len(related_data)))


init()