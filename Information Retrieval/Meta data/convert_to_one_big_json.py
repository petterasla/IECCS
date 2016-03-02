import json
import csv
import os
import pandas as pd
import glob
import codecs
import difflib
import time

def get_abstract_info():
    return pd.read_csv("../tcp_abstracts.txt")

def convert_csv_file_to_json(folder_name, global_counter):
    dict = {}
    # Getting path for a certain folder
    path = os.getcwd()+"/"+folder_name
    print path
    # Individual counter
    #counter = global_counter
    # Removing BOM characters, like \x86
    BOM = codecs.BOM_UTF8.decode("utf-8")
    # Detecting all files in a directory and do shizzle
    for i, filename in enumerate(os.listdir(os.getcwd()+"/"+folder_name)):
        # Create individual dictionary for each file
        individual_dict = {}
        if ".DS_Store" in filename:
            print "Skipping .DS_Store file.."
            continue
        # Have to locate file again, because of no extension at the end of file
        fname = glob.glob(os.path.join(path, filename+"*"))[0]
        with open(fname, 'r') as read_file:
            # Internal CSV reader. Reads first line as fieldnames (column names)
            csv_file = csv.DictReader(read_file)
            for row in csv_file:
                for key in row.keys():
                    # Convert to new keys because of utf-8 BOM problems
                    new_key = key.decode("utf-8").strip(BOM)
                    new_value = row[key].decode("utf-8").strip(BOM)
                    individual_dict[new_key] = new_value

        dict[str(global_counter+i)] = individual_dict

    return dict, global_counter+i
#convert_csv_file_to_json("0 to 1000", 100000)

def convert_folders_to_json():
    folders = os.listdir(os.getcwd())
    new_folders = [folder for folder in folders if not folder in [".DS_Store","convert_to_one_big_json.py"]]
    counter = 100000
    final_dict = {}
    for folder in new_folders:
        dict, counter = convert_csv_file_to_json(folder, counter)
        print "received counter: " + str(counter)
        for key in dict:
            final_dict[key] = dict[key]

    with open("meta_data.json", "w") as output:
        json.dump(final_dict, output)
        output.close()

#convert_folders_to_json()

def compare_titles_between_meta_and_tcp_data():
    start = time.time()
    with open("meta_data.json", "r") as meta_read:
        meta_dict = json.load(meta_read)
        meta_read.close()
    tcp_data = get_abstract_info()

    tcp_titles = tcp_data.Title

    match_counter = 0
    for key in meta_dict:
        for i in range(len(tcp_titles)):
            meta_title = meta_dict[key]["Title"].lower()
            tcp_title = tcp_titles.iloc[i].replace("|",",").lower()
            if difflib.SequenceMatcher(None, meta_title, tcp_title).ratio() > 0.95:
                match_counter += 1

    print "number of matches = " + str(match_counter)
    print "Time used: " + str(time.time()-start)
compare_titles_between_meta_and_tcp_data()