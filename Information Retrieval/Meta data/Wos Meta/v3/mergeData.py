import json
import csv
import os
import pandas as pd
import glob
import codecs
import difflib
import time
import System.DataProcessing.process_data as ptd



with open("wos_identities_1991_2011.json", "r") as f:
    wos = json.load( f)

print wos[:3]
print("len of wos before identicals: {}".format(len(wos)))
wos = list(set(wos))
print("len of wos after identicals: {}".format(len(wos)))

with open("../../../../System/TextFiles/data/meta_data.json") as f:
    tcp_data = pd.DataFrame(json.load(f))
    tcp_data = tcp_data[tcp_data.Publication_year == 2011]
    tcp_wos_2011 = tcp_data.WOS.tolist()

print("\nlen of tcp wos 2011: {}".format(len(tcp_wos_2011)))
print tcp_wos_2011[:3]

found = []
for w in wos:
    if w in tcp_wos_2011:
        found.append(w)

print("\nNumber found: {} out of {}".format(len(found), len(tcp_wos_2011)))


    #with open("related_data_final_filtering_with_titles.json", "w") as f:
    #    json.dump(related, f)
    #    print("dumped")