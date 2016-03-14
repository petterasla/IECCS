import json
import csv
import os
import pandas as pd
import glob
import codecs
import difflib
import time

def getStanceByEndorse(endorse):
    if endorse <= 3:
        return "FAVOR"
    elif endorse >= 5:
        return "AGAINST"
    else:
        return "NONE"

def get_abstract_info():
    return pd.read_csv("../System/TextFiles/tcp_abstracts.txt")
    #return pd.read_csv("../tcp_abstracts.txt")

def convert_csv_file_to_json(folder_name):
    # List for storing the individual dicts
    l = []
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
        l.append(individual_dict)

    # Return the dict and global counter
    return l


def cconvert_folders_to_json():
    # Get list of current folders in directory
    folders = os.listdir(os.getcwd())
    # Removing mac's hidden file ".DS_Store" and this python file
    new_folders = [folder for folder in folders if not folder in [".DS_Store","convert_to_one_big_json.py", "output.log", "meta_data.json"]]
    # Final dictionary with every file
    final_list = []
    # Looping through every folder in directory
    for folder in new_folders:
        # Return a dictionary for the files in one folder
        temp_list = convert_csv_file_to_json(folder)
        print "Folder: " + str(folder)
        # Adding each file in the dictionary to the final dictionary
        for item in temp_list:
            final_list.append(item)


    # Store as json
    with open("meta_data.json", "w") as output:
        json.dump(final_list, output)
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
    # Create a list which should store all the files as dicts
    tcp_list = []
    # Loop through original TCP files and add as dictionaries
    for i in range(tcp_data.shape[0]):
        dict = {}
        dict["_id"] = tcp_data.Id.iloc[i]
        dict["Abstract"] = tcp_data.Abstract.iloc[i]
        dict["Endorsement"] = tcp_data.Endorse.iloc[i]
        dict["Stance"] = getStanceByEndorse(tcp_data.Endorse.iloc[i])
        dict["Year"] = tcp_data.Year.iloc[i]
        dict["Category"] = tcp_data.Cat.iloc[i]
        dict["Title"] = tcp_data.Title.iloc[i]
        tcp_list.append(dict)
    # A counter for number of matches of meta titles and tcp titles
    match_counter = 0
    print "starting the comparison loop"
    for d in tcp_list:
        # Setting a key "Match" to false unless matching of titles is proved otherwise
        d["Match"] = False
        # Getting title for the tcp data
        tcp_title = d["Title"].replace("|",",").lower()
        # Looping through the meta data files
        for meta_d in meta_dict:
            # Getting title for the meta data
            try:
                meta_title = meta_d["Title"].lower()
            except:
                continue
            # Comparing the titles, if 95% match they are accounted as equal
            if difflib.SequenceMatcher(None, meta_title, tcp_title).ratio() > 0.95:
                match_counter += 1
                # Adding additional data from tcp to meta dictionary
                d["Match"] = True
                
                
                for key in meta_d:
                    d[key] = meta_d[key]
                ps = d["Page start"]
                pe = d["Page end"]
                try:
                    if len(pe) > 0 and len(ps) > 0 and pe >= ps:
                        # Just setting this because some page numbers are set to 123134-123.
                        # No paper are longer than 100 pages..
                        if int(pe) - int(ps) < 100:
                            d["Page count"] = int(pe)-int(ps)
                except:
                    print "Page count error.."
                if match_counter % 50 == 0:
                    print "Counter: " + str(match_counter) + "\t Time: " + str(time.time()-start)
                break

    print "number of matches = " + str(match_counter)
    print "Time used: " + str(time.time()-start)

    # Store as json
    with open("matching_data.json", "w") as output:
        json.dump(tcp_list, output)
        output.close()


compare_titles_between_meta_and_tcp_data()

