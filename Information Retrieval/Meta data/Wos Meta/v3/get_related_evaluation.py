import json
import time
from xml.etree import ElementTree
import suds
import credentialsv3 as c
import pandas as pd
import wos.utils
from wos import WosClient
import System.DataProcessing.process_data as ptd


def queryRelatedWos(WOS, start_time):
    root_list = []
    with WosClient(c.getUserName(), c.getPassword()) as client:
        print("Starting to look for related records")
        for i, id in enumerate(WOS):
            try:
                records = wos.utils.get_related_records_v2(client, id, count=2)
                roots = records.findall("REC")
                for root in roots:
                    root_list.append(root)
            except:
                print("Some error while adding roots. Waiting 30 sec")
                time.sleep(5)
            if (i+1) % 50 == 0:
                print("Queries so far is {}. Time used is {:0.1f}".format((i+1),((time.time()-start_time)/60.0)))
            time.sleep(0.5)
    return root_list

def extractDataFromRoot(roots):
    l = []
    for root in roots:
        dic = {}
        dic["WOS"] = getWOS_id(root)
        l.append(dic)
    return l

def getWOS_id(root):
    ret = root.findall("UID")[0].text
    if len(ret) == 0:
        #print("No 'WOS' found")
        return None
    else:
        return ret

def getWos(data, start, end):
    l = []
    for dic in data[start:end]:
        try:
            if dic["WOS"]:
                l.append(dic["WOS"])
        except:
            continue
    return l


def init():
    start_time = time.time()
    with open('../meta_data_wos_all_correct.json','r') as f:
        d = json.load(f)

    data = []

    for dic in d:
        if dic["Publication_year"] != 2011:
            data.append(dic)

    print("len of old       {}".format(len(d)))
    print("len of filtered: {}".format(len(data)))
    print("difference: {}".format(len(d)-len(data)))

    parts = len(data)/15
    start = -parts
    end = 0
    for i in range(parts):
        print("part: {}".format(i))
        start += parts
        end += parts
        if i == parts-1:
            end = None

        WOS = getWos(data, start, end)
        #WOS = ["WOS:A1991GM73000001"]
        roots = queryRelatedWos(WOS, start_time)
        related_data = extractDataFromRoot(roots)


        filename = "data/related_data_only_2011_{}.json".format(i)
        with open(filename, 'w') as f:
            json.dump(related_data, f)

        print("Time used was {:0.2f} seconds or {:0.1f} minutes".format((time.time() - start_time), ((time.time()-start_time)/60.0)))
        print("Number of successfully retrieved records was {}".format(len(related_data)))
        time.sleep(200)

init()