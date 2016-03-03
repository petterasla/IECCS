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
    # Removing Byte Order Mark (BOM) characters, like \x86
    BOM = codecs.BOM_UTF8.decode("utf-8")
    # Detecting all files in a directory and convert csv to json
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

        # Creating a larger dict containing every file in folder
        dict[str(global_counter+i)] = individual_dict

    # Return the dict and global counter
    return dict, global_counter+i

#convert_csv_file_to_json("0 to 1000", 100000)

def convert_folders_to_json():
    # Get list of current folders in directory
    folders = os.listdir(os.getcwd())
    # Removing mac's hidden file ".DS_Store" and this python file
    new_folders = [folder for folder in folders if not folder in [".DS_Store","convert_to_one_big_json.py"]]
    # Global counter used as key for each entry
    counter = 100000
    # Final dictionary with every file
    final_dict = {}
    # Looping through every folder in directory
    for folder in new_folders:
        # Return a dictionary for the files in one folder, and global counter
        dict, counter = convert_csv_file_to_json(folder, counter)
        print "received counter: " + str(counter)
        # Adding each file in the dictionary to the final dictionary
        for key in dict:
            final_dict[key] = dict[key]

    # Store as json
    with open("meta_data.json", "w") as output:
        json.dump(final_dict, output)
        output.close()

#convert_folders_to_json()

# Because of simple differences like ':', '/' and stuff, we had to do a comparing
def compare_titles_between_meta_and_tcp_data():
    start = time.time()
    # Open json file with all the meta data
    with open("meta_data.json", "r") as meta_read:
        meta_dict = json.load(meta_read)
        meta_read.close()

    # Get the TCP data
    tcp_data = get_abstract_info()
    # A counter for number of matches of meta titles and tcp titles
    match_counter = 0
    for key in meta_dict:
        # Setting a key "Match" equal to false unless proved otherwise
        meta_dict[key]["Match"] = False
        # Looping through the tcp files
        for i in range(tcp_data.shape[0]):
            # Getting titles for the meta data and tcp data
            meta_title = meta_dict[key]["Title"].lower()
            tcp_title = tcp_data.Title.iloc[i].replace("|",",").lower()
            # Comparing the titles, if 95% match they are accounted as equal
            if difflib.SequenceMatcher(None, meta_title, tcp_title).ratio() > 0.95:
                match_counter += 1
                # Just dropping matching rows to make it a bit faster (?)
                tcp_data.drop(tcp_data.index[i], inplace=True)
                # Adding additional data from tcp to meta dictionary
                meta_dict[key]["Match"] = True
                meta_dict[key]["Abstract"] = tcp_data.Abstract.iloc[i]
                meta_dict[key]["Endorsement"] = tcp_data.Endorse.iloc[i]
                meta_dict[key]["Category"] = tcp_data.Cat.iloc[i]
                if match_counter % 50 == 0:
                    print "Time: " + str(time.time()-start) + "\t Counter: " + str(match_counter)
                break

    print "number of matches = " + str(match_counter)
    print "Time used: " + str(time.time()-start)

    # Remove un-matched data
    matching_dict = {}
    for key in meta_dict:
        if meta_dict[key]["Match"]:
            matching_dict[key] = meta_dict[key]

    print "Length of matching dict: " + str(len(matching_dict))
    # Store as json
    with open("matching_data.json", "w") as output:
        json.dump(matching_dict, output)
        output.close()


compare_titles_between_meta_and_tcp_data()