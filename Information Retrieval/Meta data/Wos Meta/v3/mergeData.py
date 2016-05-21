import json
import os
import pandas as pd
import numpy as np

def mergeAllFilesFromFolder(path):
    path = os.getcwd()+path
    files = []
    for i, filename in enumerate(os.listdir(path)):
        print("Filename: {}".format(filename))
        with open(path+"/"+filename, 'r') as read_file:
            x = json.load(read_file)
        for d in x:
            files.append(d)

    print("len of ids: {}".format(len(files)))
    return files

def convertToInt(data):
    for d in data:
        d["Publication_year"] = int(d["Publication_year"])
    return data

def getTCPData(yearList=[]):
    with open("../../../../System/TextFiles/data/meta_data.json") as f:
        d1 = json.load(f)
        d2 = convertToInt(d1)
        data = pd.DataFrame(d2)

    wos_year_ids = []
    for year in yearList:
        temp_list = []
        temp_list = data[data.Publication_year == year].WOS.tolist()
        wos_year_ids = wos_year_ids + temp_list

    print("len of tcp id = {} after including yearlist: {}".format(len(wos_year_ids), yearList))
    return wos_year_ids

def getData(store=False, path="random"):
    data_ids = mergeAllFilesFromFolder("/data/2011")

    temp = []
    for dic in data_ids:
        temp.append(dic["WOS"])

    data_wos_ids = list(set(temp))

    yearList = [1991, 1992, 1993]
    tcp_wos_ids = getTCPData(yearList)

    print("len of new ids that should fit in years {} === {}".format(yearList, len(data_wos_ids)))

    c = 0
    for id in data_wos_ids:
        if id in tcp_wos_ids:
            c += 1

    print("number of records found in the year list: {} was === {}".format(yearList, c))

    if store:
        with open(path, "w") as f:
            json.dump(data_wos_ids, f)
            print("dumped with path: {}".format(path))

getData(store=False, path="llol")