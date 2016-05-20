import System.DataProcessing.process_data as ptd
import pandas as pd
import json
import numpy as np

def filterSubjects(data):

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
    for s in sorted(unrecognized_subjects):
        print("\t{}".format(s))

    print("\nLenght of unrec subjects: {}".format(len(unrecognized_subjects)))

    final_filter = []
    for ids in n_found:
        for d in data:
            if d["WOS"] == ids:
                final_filter.append(d)

    print("len of final filter: {}".format(len(final_filter)))
    return final_filter

def filterCommonTCP(data):
    new_data = []

    old = pd.read_json("../../TextFiles/data/meta_data.json")
    old_2011 = old[old.Publication_year == 2011]
    old_2011_wos = old_2011.WOS.unique().tolist()

    data_temp = convertToInt(data)
    data = []
    for d in data_temp:
        if d["Publication_year"] == 2011:
            data.append(d)

    print("old length 2011: {}".format(len(old_2011_wos)))
    print("new length 2011: {}".format(len(data)))

    identical_dict = dict(zip(old_2011_wos, np.zeros(len(old_2011_wos))))
    identical = 0

    for d in data:
        try:
            hit = identical_dict[d["WOS"]]
            identical += 1
        except:
            new_data.append(d)

    print("Number of identical papers = {}\n".format(identical))

    print ("len of old after: {}".format(len(new_data)))
    return new_data


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



def filter_process(store=False):
    with open("../../TextFiles/data/related_data.json", "r") as f:
        data = json.load(f)

    print 80*'='
    print "Abstract filter:"
    print 80*'='
    print
    data_with_abs = filterAbstracts(data)
    print
    print 80*'='
    print "Duplicate filter:"
    print 80*'='
    print
    data_no_dup = filterDuplicates(data_with_abs[:1000])
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
    data_relevant_subjects = filterSubjects(data_no_common_with_tcp)
    print
    print 80*'='
    print "Storing:"
    print 80*'='
    print

    if store:
        with open("related_data_correct_v2.json", "w") as f:
            json.dump(data_relevant_subjects, f)
            print("dumped")

filter_process()