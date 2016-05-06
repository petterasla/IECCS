import json
import time
from xml.etree import ElementTree
import suds
import credentials as c
import pandas as pd
import wos.utils
from wos import WosClient
#import adder_related

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

def getPublisherInfo(root):
    try:
        full_address = root.findall(".REC/static_data/summary/publishers/publisher/address_spec/full_address")[0].text
        return full_address
    except:
        #print("No publisher info found")
        return None

def getWOS(root):
    try:
        ret = root.findall(".REC/UID")[0].text
        return ret
    except:
        return None

def extractDataFromRoot(root_list):
    data = []
    for root in root_list:
        d = {}
        d["Title"] = getTitle(root)
        d["Publisher_info"] = getPublisherInfo(root)
        d["WOS"] = getWOS(root)
        data.append(d)
    return data



def getWos(data, start, end):
    l = []
    for dic in data[start:end]:
        try:
            if dic["WOS"]:
                l.append(dic["WOS"])
        except:
            continue
    return l

def queryWos(WOS, start_time):
    root_list = []
    with WosClient(c.getUserName(), c.getPassword()) as client:
        print("Starting to look for title and publisher info")
        for i, id in enumerate(WOS):
            try:
                root = wos.utils.query_by_id(client, id)
                root_list.append(root)
            except:
                print("Some error while adding roots. Waiting 30 sec")
                time.sleep(15)
            if (i+1) % 50 == 0:
                print("Queries so far is {}. Time used is {:0.1f}".format((i+1),((time.time()-start_time)/60.0)))
            time.sleep(0.5)
    return root_list

def init():
    start_time = time.time()
    with open("../../../../System/TextFiles/data/related_data_checked_for_duplicates.json") as f:
        related = json.load(f)

    parts = len(related)/8

    start = -parts
    end = 0
    for i in range(8):
        start += parts
        end += parts
        print("Start: {} to end: {}".format(start, end))
        if i == 7:
            end = None

        WOS_IDs = getWos(related, start, end)
        print WOS_IDs
        root_list = queryWos(WOS_IDs, start_time)
        additional_data = extractDataFromRoot(root_list)

        print additional_data[0]
        filename = "additional_data/data{}.json".format(i)
        with open(filename, "w") as f:
            json.dump(additional_data, f)
        print("Time used was {:0.2f} seconds or {:0.1f} minutes".format((time.time() - start_time), ((time.time()-start_time)/60.0)))
        print("Number of successfully retrieved records was {} of {}".format(len(additional_data), end-start))
        time.sleep(200)


init()