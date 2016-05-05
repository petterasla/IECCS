import json
import csv
import os
import pandas as pd
import glob
import codecs
import difflib
import time

path = os.getcwd()+"/additional_data"
titles = []
for i, filename in enumerate(os.listdir(path)):
    print("Filename: {}".format(filename))
    with open(path+"/"+filename, 'r') as read_file:
        x = json.load(read_file)
    for d in x:
        titles.append(d)

print("len of titles: {}".format(len(titles)))

with open("../../../../System/TextFiles/data/related_data_final_filtering_with_titles.json") as f:
    related = json.load(f)

print("len of related: {}".format(len(related)))

c = 0
for d1 in related:
    for d2 in titles:
        if d1["WOS"] == d2["WOS"]:
            c += 1
            d1["Title"] = d2["Title"]
            d1["Publisher_info"] = d2["Publisher_info"]

print("Successfully ids checked should be equal: {} == {}".format(len(related), c))

for key in related[0].keys():
    c = 0
    for d in related:
        if d[key] is not None:
            c += 1
    print("Key: {} is = {}".format(key, c))

#with open("related_data_final_filtering_with_titles.json", "w") as f:
#    json.dump(related, f)
#    print("dumped")