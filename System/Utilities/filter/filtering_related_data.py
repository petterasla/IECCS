import System.DataProcessing.process_data as ptd
import pandas as pd
import json
import numpy as np

def filterSubjects(data, store=False):

    with open("../../TextFiles/data/meta_data.json", "r") as f:
        original_data = json.load(f)

    print("Len of data: {}".format(len(data)))
    s = []
    for d in data:
        if d["Subjects"] is not None:
            for subjects in d["Subjects"]:
                for subject in subjects.split(","):
                    s.append(subject.lower().strip())

    print("len of new subjects  = {}".format(len(s)))
    uniq = list(set(s))
    print uniq
    print("len of unique new subjects = {}\n".format(len(uniq)))


    print("len of TCP data: {}".format(len(original_data)))
    s_o = []
    for d in original_data:
        try:
            if d["Subjects"] is not None:
                for subjects in d["Subjects"]:
                    for subject in subjects.split(","):
                        s_o.append(subject.lower().strip())
        except:
            continue

    print("len of old subjects = {}".format(len(s_o)))
    uniq_o = list(set(s_o))
    print uniq_o
    print("len of unique old subjects = {}\n".format(len(uniq_o)))

    counter = 0
    for subject in uniq:
        if subject in uniq_o:
            counter += 1

    print("Number of subjects in related data found in original = {}\n".format(counter))

    print("Subjects not in original data:")
    unrecognized_subjects = []
    for subject in uniq:
        if subject not in uniq_o:
            unrecognized_subjects.append(subject)
    print("Lenght of unreq data: {}".format(len(unrecognized_subjects)))

    found = list()
    not_found = list()
    f_subs = [
        "government & law",
        "hardware & architecture",
        "business",
        "business & economics",
        "acoustics",
        "law",
        "legal",
        "robotics",
        "textiles",
        "telecommunications",
        "artificial intelligence"
    ]
    for s in f_subs:
        unrecognized_subjects.append(s)

    unrecognized_subjects = list(set(unrecognized_subjects))
    ## EX:
    ## [u'Geosciences, Multidisciplinary', u'Geology', u'GEOSCIENCES, MULTIDISCIPLINARY']
    for i, d in enumerate(data):
        if d["Subjects"] is not None:
            #print("\nID: {}".format(i+1))
            for subjects in d["Subjects"]:
                #print("Subjects: {}".format(subjects))
                for subject in subjects.split(","):
                    if subject.lower().strip() in unrecognized_subjects:
                        not_found.append(d["WOS"])
                    else:
                        found.append(d["WOS"])
                        #print("NOT FOUND: \t{}".format(subject))
    found = list(set(found))
    not_found_temp = list(set(not_found))

    n_found = []
    for ids in found:
        if ids not in not_found_temp:
            n_found.append(ids)
    print("Found: {}\nNot found: {}".format(len(n_found), len(not_found_temp)))
    #WOS:000291279200005
    #for ids in not_found_temp[:5]:
    #    for d in data:
    #        if d["WOS"] == ids:
    #            print("WOS ID {}\nSubjects: {}\nAbstract: {}\n".format(d["WOS"], d["Subjects"], d["Abstract"]))
    counter = len(n_found)
    for idx, ids in enumerate(not_found_temp):
        for d in data:
            if d["WOS"] == ids:
                abstract = d["Abstract"]
                abs_tokens = [a.lower() for a in abstract.split(" ")]
                if "climate" in abs_tokens:
                    n_found.append(ids)


    print("\nNumber of related records = {}\nAdded {} samples which included 'climate'".format(len(n_found), len(n_found)-counter))
    print("Filtered away: {}\n".format(len(not_found_temp)-(len(n_found)-counter)))

    print("Three samples which were filtered away:\n")
    for ids in not_found_temp[:3]:
        for d in data:
            if d["WOS"] == ids:
                abstract = d["Abstract"]
                print("\t{}".format(d["WOS"]))
                print("\tSubjects: {}".format(d["Subjects"]))
                print("\t{}\n".format(abstract))

    print("Subjects not found in TCP data and not found in the hand-picked subjects AKA unrecognizable subjects:\n")
    unrec_sub_store = sorted(unrecognized_subjects)
    for s in unrec_sub_store:
        print("\t{}".format(s))


    print("\nLenght of unrec subjects: {}".format(len(unrecognized_subjects)))

    final_filter = []
    for ids in n_found:
        for d in data:
            if d["WOS"] == ids:
                final_filter.append(d)

    if store:
        storeToJson(uniq_o, "file/old_unique_subjects.json")
        storeToJson(uniq, "file/new_unique_subjects.json")
        storeToJson(unrec_sub_store, "file/new_subjects_not_found_in_TCP_subjects.json")

    print("len of final filter: {}".format(len(final_filter)))
    return final_filter

def filterCommonTCP(data):
    new_2011 = []
    new_2011_processed = []
    new_data_total = []
    print("len of incomming data: {}".format(len(data)))

    old = pd.read_json("../../TextFiles/data/meta_data.json")
    old_2011 = old[old.Publication_year == 2011]
    old_2011_wos = old_2011.WOS.unique().tolist()

    data_temp = convertToInt(data)
    for d in data_temp:
        if d["Publication_year"] == 2011:
            new_2011.append(d)

    print("old length 2011: {}".format(len(old_2011_wos)))
    print("new length 2011: {}".format(len(new_2011)))

    identical_dict = dict(zip(old_2011_wos, np.zeros(len(old_2011_wos))))
    identical = 0

    for d in new_2011:
        try:
            hit = identical_dict[d["WOS"]]
            identical += 1
        except:
            new_2011_processed.append(d)

    print("Number of identical papers = {}\n".format(identical))
    print ("len of new data 2011 after processed: {}".format(len(new_2011_processed)))

    for d in data:
        if d["Publication_year"] != 2011:
            new_data_total.append(d)

    new_data_total = new_data_total + new_2011_processed
    print ("len of new data total: {}".format(len(new_data_total)))
    return new_data_total


def filterDuplicates(data):

    new_data = []
    print("len of related data: {}\n".format(len(data)))

    uniq_ids = pd.DataFrame(data).WOS.unique().tolist()
    wos_dic = dict(zip(uniq_ids, np.zeros(len(uniq_ids))))

    for d in data:
        wos_dic[d["WOS"]] += 1


    for d in data:
        if wos_dic[d["WOS"]] == 1:
            new_data.append(d)

    for key in wos_dic.keys()[:10]:
        print("\tkey: {} \t Value: {}".format(key, wos_dic[key]))
    print("\nlen of related data: {}".format(len(new_data)))
    return new_data

def filter2011(data):
    new_data = []
    print("len of incomming data: {}".format(len(data)))
    for d in data:
        if d["Publication_year"] != "2011":
            new_data.append(d)

    print("len of after removing 2011 data: {}".format(len(new_data)))
    return new_data

def filterAbstracts(data):
    new_data = []
    print("len of data: {}".format(len(data)))
    for dic in data:
        if dic["Abstract"] is not None:
            new_data.append(dic)
    print("len of data after: {}".format(len(new_data)))
    return new_data



def convertToInt(data):
    for d in data:
        d["Publication_year"] = int(d["Publication_year"])
    return data

def storeToJson(file, path):
    with open(path, "w") as f:
        json.dump(file, f)
        print("dumped file with path: {}".format(path))

def filter_process(store=False):
    # Small batch
    #with open("../../TextFiles/data/related_data.json", "r") as f:
    #    data = json.load(f)

    # Large batch
    with open("one_file.json", "r") as f:
        data = json.load(f)

    print 80*'='
    print "Abstract filter:"
    print 80*'='
    print
    data_with_abs = filterAbstracts(data)
    print
    print 80*'='
    print "2011 filter:"
    print 80*'='
    print
    data_no_2011 = filter2011(data_with_abs)
    print
    print 80*'='
    print "Duplicate filter:"
    print 80*'='
    print
    data_no_dup = filterDuplicates(data_no_2011)
    print
    print 80*'='
    print "Common TCP 2011 filter:"
    print 80*'='
    print
    data_no_common_with_tcp = filterCommonTCP(data_no_dup)
    print
    print 80*'='
    print "Subject filter:"
    print 80*'='
    print
    data_relevant_subjects = filterSubjects(data_no_common_with_tcp, store=True)
    print
    print 80*'='
    print "Storing:"
    print 80*'='
    print
    if store:
        storeToJson(data_relevant_subjects, "related_data_correct_v3_post2011_many.json")

filter_process(store=False)