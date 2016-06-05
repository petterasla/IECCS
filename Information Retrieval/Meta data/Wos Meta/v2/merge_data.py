import json
import csv
import os
import pandas as pd
import time

path = os.getcwd()+"/related"
titles = []
for i, filename in enumerate(os.listdir(path)):
    print("Filename: {}".format(filename))
    with open(path+"/"+filename, 'r') as read_file:
        x = json.load(read_file)
    for d in x:
        titles.append(d)

print("len of titles: {}".format(len(titles)))


with open("one_file.json", "w") as f:
    json.dump(titles, f)
    print("dumped")