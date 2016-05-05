#import System.DataProcessing.process_data as ptd
#import System.DataProcessing.process_meta_data as ptmd
import pandas as pd
import numpy as np
import json
import random
import cPickle as pickle

def getStanceData(stance):
    d = ptd.getMetaDataAsList()
    data = pd.DataFrame(d)
    return data[data.Stance == stance]

def storeOrgsToJson(stance="All"):
    if stance == "All":
        d = ptd.getMetaDataAsList()
        frame = pd.DataFrame(d)
    else:
        frame = getStanceData(stance)
    frame = frame.Organization_info
    frame.fillna("nan", inplace=True)
    info = frame.tolist()
    info = [i for i in info if i != "nan"]
    country = [org[0].lower() for sub in info for org in sub]
    uniq_country = list(set(country))
    count_dict = dict(zip(uniq_country, np.zeros(len(uniq_country))))
    country_map = dict(zip(uniq_country, np.zeros(len(uniq_country))))
    for c in country:
        count_dict[c] += 1
    for c in uniq_country:
        country_map[c] = c[0].upper() + c[1:]
        print country_map[c]

    with open("../TextFiles/meta_data/country_mapper.json", "w") as f:
        json.dump(country_map, f)
    #for key in count_dict.keys():
    #    print("{} \t: {}".format(key, count_dict[key]))

    #with open("../TextFiles/meta_data/orgs_NONE.json", "w") as f:
    #    json.dump(count_dict, f)

def storeLanguageToJson(stance="All"):
    if stance == "All":
        d = ptd.getMetaDataAsList()
        frame = pd.DataFrame(d).Language
    else:
        frame = getStanceData(stance).Language
    frame.fillna("nan", inplace=True)
    lang = frame.tolist()
    lang = [l for l in lang if l != "nan"]
    uniq = list(set(lang))
    print("There are {} different languages".format(len(uniq)))
    print("These languages are:\n{}".format(uniq))
    d = dict(zip(uniq, np.zeros(len(uniq))))
    for l in lang:
        d[l] += 1
    for key in d.keys():
        print("{} \t: {}".format(key, d[key]))

    with open("../TextFiles/meta_data/lang_NONE.json", "w") as f:
        json.dump(d, f)


def storeSubjectsToJson(stance="All"):
    if stance == "All":
        d = ptd.getMetaDataAsList()
        frame = pd.DataFrame(d).Subjects
    else:
        frame = getStanceData(stance).Subjects
    frame.fillna("nan", inplace=True)
    headers = frame.tolist()
    headers = [h for h in headers if h != "nan"]
    headers = [h for sublist in headers for h in sublist]
    uniq_head = list(set(headers))
    d = dict(zip(uniq_head, np.zeros(len(uniq_head))))
    for s in headers:
        d[s] += 1

    for key in d.keys():
        print("{} \t: {}".format(key, d[key]))
    print("There are a total of {} subjects, with {} unique ones".format(len(headers), len(uniq_head)))

    with open("../TextFiles/meta_data/subjects_NONE.json", "w") as f:
        json.dump(d, f)


#storeSubjectsToJson("NONE")
#storeOrgsToJson("All")
#storeLanguageToJson("NONE")


def readTestSamples():
    with open("../TextFiles/data/related_dat.json", "r") as f:
        data = json.load(f)

    with open("samples_test.pkl", "r") as f:
        samples = pickle.load(f)

    for idx in samples:
        print("Index: {}, sample title: {}\nSubjects: {}\nSub-Headers:{}\nAbstract: {}\nYear: {}\n".format(idx, data[idx]["Title"], data[idx]["Subjects"], data[idx]["Sub_headers"], data[idx]["Abstract"], data[idx]["Publication_year"]))
        #print("WOS: {}".format(data[idx]["WOS"]))

def finalFiltering():
    with open("../TextFiles/data/related_data_checked_for_duplicates.json", "r") as f:
        data = json.load(f)

    with open("../TextFiles/data/meta_data.json", "r") as f:
        original_data = json.load(f)

    print len(data)
    s = []
    for d in data:
        if d["Subjects"] is not None:
            for subjects in d["Subjects"]:
                for subject in subjects.split(","):
                    s.append(subject.lower().strip())

    print("len of new subjects  = {}".format(len(s)))
    uniq = list(set(s))
    print("len of new subjects = {}\n".format(len(uniq)))

    print len(original_data)
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
    print("len of old subjects = {}\n".format(len(uniq_o)))


    counter = 0
    for subject in uniq:
        if subject in uniq_o:
            counter += 1

    print("Number of subjects in related data found in original = {}\n".format(counter))

    print("Printing subjects not in original data:")
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
    print("Filtered away: {}".format(len(not_found_temp)-(len(n_found)-counter)))

    for ids in not_found_temp[:5]:
        for d in data:
            if d["WOS"] == ids:
                abstract = d["Abstract"]
                print("{}".format(d["WOS"]))
                print("Subjects: {}".format(d["Subjects"]))
                print("{}\n".format(abstract))

    for s in sorted(unrecognized_subjects):
        print s
    print("\nLenght of unrec subjects: {}".format(len(unrecognized_subjects)))
    final_filter = []
    for ids in n_found:
        for d in data:
            if d["WOS"] == ids:
                final_filter.append(d)

    #if len(final_filter) == len(n_found):
    #    with open("related_data_final_filtering.json", "w") as f:
    #        json.dump(final_filter, f)
    #        print(len(final_filter))
    #        print("dumped")


def removeDuplicates():
    with open("../TextFiles/data/related_data.json", "r") as f:
        data = json.load(f)

    print("len of related data: {}".format(len(data)))
    uniq = list()
    wos_ids = list()
    for d in data:
        if d["WOS"] not in wos_ids:
            uniq.append(d)
            wos_ids.append(d["WOS"])
    print("len of related data: {}".format(len(uniq)))
    test = []
    for d in data:
        test.append(d["WOS"])
    test = set(test)
    print("len of related data: {}".format(len(test)))

    #if len(test) == len(uniq):
        #with open("related_data_checked_for_duplicates.json", "w") as f:
        #    json.dump(uniq, f)
        #    print("dumped")

#removeDuplicates()
#readTestSamples()
finalFiltering()
'''
mapData = [
    {"code":"AF" , "name":"Afghanistan", "value":32358260, "color":"#eea638"},
    {"code":"AL" , "name":"Albania", "value":3215988, "color":"#d8854f"},
    {"code":"DZ" , "name":"Algeria", "value":35980193, "color":"#de4c4f"},
    {"code":"AO" , "name":"Angola", "value":19618432, "color":"#de4c4f"},
    {"code":"AR" , "name":"Argentina", "value":40764561, "color":"#86a965"},
    {"code":"AM" , "name":"Armenia", "value":3100236, "color":"#d8854f"},
    {"code":"AU" , "name":"Australia", "value":22605732, "color":"#8aabb0"},
    {"code":"AT" , "name":"Austria", "value":8413429, "color":"#d8854f"},
    {"code":"AZ" , "name":"Azerbaijan", "value":9306023, "color":"#d8854f"},
    {"code":"BH" , "name":"Bahrain", "value":1323535, "color":"#eea638"},
    {"code":"BD" , "name":"Bangladesh", "value":150493658, "color":"#eea638"},
    {"code":"BC" , "name":"Barbados", "value":100000000, "color":"#a7a739"},
    {"code":"BY" , "name":"Belarus", "value":9559441, "color":"#d8854f"},
    {"code":"BE" , "name":"Belgium", "value":10754056, "color":"#d8854f"},
    {"code":"BL", "name":"Belize", "value":10000000, "color": "#a7a737"},
    {"code":"BJ" , "name":"Benin", "value":9099922, "color":"#de4c4f"},
    {"code":"BK" , "name":"Bermuda", "value":19099922, "color":"#a7a737"},
    {"code":"BT" , "name":"Bhutan", "value":738267, "color":"#eea638"},
    {"code":"BO" , "name":"Bolivia", "value":10088108, "color":"#86a965"},
    {"code":"BA" , "name":"Bosnia and Herzegovina", "value":3752228, "color":"#d8854f"},
    {"code":"BW" , "name":"Botswana", "value":2030738, "color":"#de4c4f"},
    {"code":"BR" , "name":"Brazil", "value":196655014, "color":"#86a965"},
    {"code":"BN" , "name":"Brunei", "value":405938, "color":"#eea638"},
    {"code":"BG" , "name":"Bulgaria", "value":7446135, "color":"#d8854f"},
    {"code":"BF" , "name":"Burkina Faso", "value":16967845, "color":"#de4c4f"},
    {"code":"BI" , "name":"Burundi", "value":8575172, "color":"#de4c4f"},
    {"code":"KH" , "name":"Cambodia", "value":14305183, "color":"#eea638"},
    {"code":"CM" , "name":"Cameroon", "value":20030362, "color":"#de4c4f"},
    {"code":"CA" , "name":"Canada", "value":34349561, "color":"#a7a737"},
    {"code":"CV" , "name":"Cape Verde", "value":500585, "color":"#de4c4f"},
    {"code":"CF" , "name":"Central African Rep.", "value":4486837, "color":"#de4c4f"},
    {"code":"TD" , "name":"Chad", "value":11525496, "color":"#de4c4f"},
    {"code":"CL" , "name":"Chile", "value":17269525, "color":"#86a965"},
    {"code":"CN" , "name":"China", "value":1347565324, "color":"#eea638"},
    {"code":"CO" , "name":"Colombia", "value":46927125, "color":"#86a965"},
    {"code":"KM" , "name":"Comoros", "value":753943, "color":"#de4c4f"},
    {"code":"CD" , "name":"Congo, Dem. Rep.", "value":67757577, "color":"#de4c4f"},
    {"code":"CG" , "name":"Congo, Rep.", "value":4139748, "color":"#de4c4f"},
    {"code":"CR" , "name":"Costa Rica", "value":4726575, "color":"#a7a737"},
    {"code":"CI" , "name":"Cote d'Ivoire", "value":20152894, "color":"#de4c4f"},
    {"code":"HR" , "name":"Croatia", "value":4395560, "color":"#d8854f"},
    {"code":"CU" , "name":"Cuba", "value":11253665, "color":"#a7a737"},
    {"code":"CY" , "name":"Cyprus", "value":1116564, "color":"#d8854f"},
    {"code":"CZ" , "name":"Czech Rep.", "value":10534293, "color":"#d8854f"},
    {"code":"DK" , "name":"Denmark", "value":5572594, "color":"#d8854f"},
    {"code":"DJ" , "name":"Djibouti", "value":905564, "color":"#de4c4f"},
    {"code":"DO" , "name":"Dominican Rep.", "value":10056181, "color":"#a7a737"},
    {"code":"EC" , "name":"Ecuador", "value":14666055, "color":"#86a965"},
    {"code":"EG" , "name":"Egypt", "value":82536770, "color":"#de4c4f"},
    {"code":"SV" , "name":"El Salvador", "value":6227491, "color":"#a7a737"},
    {"code":"GQ" , "name":"Equatorial Guinea", "value":720213, "color":"#de4c4f"},
    {"code":"ER" , "name":"Eritrea", "value":5415280, "color":"#de4c4f"},
    {"code":"EE" , "name":"Estonia", "value":1340537, "color":"#d8854f"},
    {"code":"ET" , "name":"Ethiopia", "value":84734262, "color":"#de4c4f"},
    {"code":"FJ" , "name":"Fiji", "value":868406, "color":"#8aabb0"},
    {"code":"FI" , "name":"Finland", "value":5384770, "color":"#d8854f"},
    {"code":"FR" , "name":"France", "value":63125894, "color":"#d8854f"},
    {"code":"FP" , "name":"French Polynesia", "value":100000000, "color":"#8aabb0"},
    {"code":"GA" , "name":"Gabon", "value":1534262, "color":"#de4c4f"},
    {"code":"GM" , "name":"Gambia", "value":1776103, "color":"#de4c4f"},
    {"code":"GE" , "name":"Georgia", "value":4329026, "color":"#d8854f"},
    {"code":"DE" , "name":"Germany", "value":82162512, "color":"#d8854f"},
    {"code":"GH" , "name":"Ghana", "value":24965816, "color":"#de4c4f"},
    {"code":"GR" , "name":"Greece", "value":11390031, "color":"#d8854f"},
    {"code":"GC", "name":"Greenland", "value":100000000, "color":"#d8854f"},
    {"code":"GJ", "name":"Guadeloupe", "value":100000000, "color":"#a7a739"},
    {"code":"GT" , "name":"Guatemala", "value":14757316, "color":"#a7a737"},
    {"code":"GN" , "name":"Guinea", "value":10221808, "color":"#de4c4f"},
    {"code":"GW" , "name":"Guinea-Bissau", "value":1547061, "color":"#de4c4f"},
    {"code":"GY" , "name":"Guyana", "value":756040, "color":"#86a965"},
    {"code":"HT" , "name":"Haiti", "value":10123787, "color":"#a7a737"},
    {"code":"HN" , "name":"Honduras", "value":7754687, "color":"#a7a737"},
    {"code":"HK" , "name":"Hong Kong, China", "value":7122187, "color":"#eea638"},
    {"code":"HU" , "name":"Hungary", "value":9966116, "color":"#d8854f"},
    {"code":"IS" , "name":"Iceland", "value":324366, "color":"#d8854f"},
    {"code":"IN" , "name":"India", "value":1241491960, "color":"#eea638"},
    {"code":"ID" , "name":"Indonesia", "value":242325638, "color":"#eea638"},
    {"code":"IR" , "name":"Iran", "value":74798599, "color":"#eea638"},
    {"code":"IQ" , "name":"Iraq", "value":32664942, "color":"#eea638"},
    {"code":"IE" , "name":"Ireland", "value":4525802, "color":"#d8854f"},
    {"code":"IL" , "name":"Israel", "value":7562194, "color":"#eea638"},
    {"code":"IT" , "name":"Italy", "value":60788694, "color":"#d8854f"},
    {"code":"JM" , "name":"Jamaica", "value":2751273, "color":"#a7a737"},
    {"code":"JP" , "name":"Japan", "value":126497241, "color":"#eea638"},
    {"code":"JO" , "name":"Jordan", "value":6330169, "color":"#eea638"},
    {"code":"KZ" , "name":"Kazakhstan", "value":16206750, "color":"#eea638"},
    {"code":"KE" , "name":"Kenya", "value":41609728, "color":"#de4c4f"},
    {"code":"KP" , "name":"Korea, Dem. Rep.", "value":24451285, "color":"#eea638"},
    {"code":"KR" , "name":"Korea, Rep.", "value":48391343, "color":"#eea638"},
    {"code":"KW" , "name":"Kuwait", "value":2818042, "color":"#eea638"},
    {"code":"KG" , "name":"Kyrgyzstan", "value":5392580, "color":"#eea638"},
    {"code":"LA" , "name":"Laos", "value":6288037, "color":"#eea638"},
    {"code":"LV" , "name":"Latvia", "value":2243142, "color":"#d8854f"},
    {"code":"LB" , "name":"Lebanon", "value":4259405, "color":"#eea638"},
    {"code":"LS" , "name":"Lesotho", "value":2193843, "color":"#de4c4f"},
    {"code":"LR" , "name":"Liberia", "value":4128572, "color":"#de4c4f"},
    {"code":"LY" , "name":"Libya", "value":6422772, "color":"#de4c4f"},
    {"code":"LT" , "name":"Lithuania", "value":3307481, "color":"#d8854f"},
    {"code":"LU" , "name":"Luxembourg", "value":515941, "color":"#d8854f"},
    {"code":"MK" , "name":"Macedonia, FYR", "value":2063893, "color":"#d8854f"},
    {"code":"MG" , "name":"Madagascar", "value":21315135, "color":"#de4c4f"},
    {"code":"MW" , "name":"Malawi", "value":15380888, "color":"#de4c4f"},
    {"code":"MY" , "name":"Malaysia", "value":28859154, "color":"#eea638"},
    {"code":"ML" , "name":"Mali", "value":15839538, "color":"#de4c4f"},
    {"code":"MF" , "name":"Malta", "value":150839538, "color":"#d8854f"},
    {"code":"MB" , "name":"Martinique", "value":10000000, "color":"#a7a739"},
    {"code":"MR" , "name":"Mauritania", "value":3541540, "color":"#de4c4f"},
    {"code":"MU" , "name":"Mauritius", "value":1306593, "color":"#de4c4f"},
    {"code":"MX" , "name":"Mexico", "value":114793341, "color":"#a7a737"},
    {"code":"MD" , "name":"Moldova", "value":3544864, "color":"#d8854f"},
    {"code":"MI" , "name":"Monaco", "value":12800114, "color":"#eea638"},
    {"code":"MN" , "name":"Mongolia", "value":2800114, "color":"#eea638"},
    {"code":"ME" , "name":"Montenegro", "value":632261, "color":"#d8854f"},
    {"code":"MA" , "name":"Morocco", "value":32272974, "color":"#de4c4f"},
    {"code":"MZ" , "name":"Mozambique", "value":23929708, "color":"#de4c4f"},
    {"code":"MM" , "name":"Myanmar", "value":48336763, "color":"#eea638"},
    {"code":"NA" , "name":"Namibia", "value":2324004, "color":"#de4c4f"},
    {"code":"NP" , "name":"Nepal", "value":30485798, "color":"#eea638"},
    {"code":"NL" , "name":"Netherlands", "value":16664746, "color":"#d8854f"},
    {"code":"NZ" , "name":"New Zealand", "value":4414509, "color":"#8aabb0"},
    {"code":"NB" , "name":"New Caledonia", "value":10000000, "color":"#8aabb0"},
    {"code":"NI" , "name":"Nicaragua", "value":5869859, "color":"#a7a737"},
    {"code":"NE" , "name":"Niger", "value":16068994, "color":"#de4c4f"},
    {"code":"NG" , "name":"Nigeria", "value":162470737, "color":"#de4c4f"},
    {"code":"NO" , "name":"Norway", "value":4924848, "color":"#d8854f"},
    {"code":"IF" , "name":"North Ireland", "value":100000000, "color":"#d8854f"},
    {"code":"OM" , "name":"Oman", "value":2846145, "color":"#eea638"},
    {"code":"PK" , "name":"Pakistan", "value":176745364, "color":"#eea638"},
    {"code":"PU" , "name":"Palau", "value":100000000, "color":"#8aabb0"},
    {"code":"PA" , "name":"Panama", "value":3571185, "color":"#a7a737"},
    {"code":"PG" , "name":"Papua New Guinea", "value":7013829, "color":"#8aabb0"},
    {"code":"PY" , "name":"Paraguay", "value":6568290, "color":"#86a965"},
    {"code":"PE" , "name":"Peru", "value":29399817, "color":"#86a965"},
    {"code":"PH" , "name":"Philippines", "value":94852030, "color":"#eea638"},
    {"code":"PL" , "name":"Poland", "value":38298949, "color":"#d8854f"},
    {"code":"PT" , "name":"Portugal", "value":10689663, "color":"#d8854f"},
    {"code":"PR" , "name":"Puerto Rico", "value":3745526, "color":"#a7a737"},
    {"code":"QA" , "name":"Qatar", "value":1870041, "color":"#eea638"},
    {"code":"RA" , "name":"Reunion", "value":10000000, "color":"#de4c4f"},
    {"code":"RO" , "name":"Romania", "value":21436495, "color":"#d8854f"},
    {"code":"RU" , "name":"Russia", "value":142835555, "color":"#d8854f"},
    {"code":"RW" , "name":"Rwanda", "value":10942950, "color":"#de4c4f"},
    {"code":"SA" , "name":"Saudi Arabia", "value":28082541, "color":"#eea638"},
    {"code":"SN" , "name":"Senegal", "value":12767556, "color":"#de4c4f"},
    {"code":"RS" , "name":"Serbia", "value":9853969, "color":"#d8854f"},
    {"code":"SL" , "name":"Sierra Leone", "value":5997486, "color":"#de4c4f"},
    {"code":"SG" , "name":"Singapore", "value":5187933, "color":"#eea638"},
    {"code":"SK" , "name":"Slovak Republic", "value":5471502, "color":"#d8854f"},
    {"code":"SI" , "name":"Slovenia", "value":2035012, "color":"#d8854f"},
    {"code":"SB" , "name":"Solomon Islands", "value":552267, "color":"#8aabb0"},
    {"code":"SO" , "name":"Somalia", "value":9556873, "color":"#de4c4f"},
    {"code":"ZA" , "name":"South Africa", "value":50459978, "color":"#de4c4f"},
    {"code":"ES" , "name":"Spain", "value":46454895, "color":"#d8854f"},
    {"code":"LK" , "name":"Sri Lanka", "value":21045394, "color":"#eea638"},
    {"code":"SD" , "name":"Sudan", "value":34735288, "color":"#de4c4f"},
    {"code":"SR" , "name":"Suriname", "value":529419, "color":"#86a965"},
    {"code":"SZ" , "name":"Swaziland", "value":1203330, "color":"#de4c4f"},
    {"code":"SE" , "name":"Sweden", "value":9440747, "color":"#d8854f"},
    {"code":"CH" , "name":"Switzerland", "value":7701690, "color":"#d8854f"},
    {"code":"SY" , "name":"Syria", "value":20766037, "color":"#eea638"},
    {"code":"TW" , "name":"Taiwan", "value":23072000, "color":"#eea638"},
    {"code":"TJ" , "name":"Tajikistan", "value":6976958, "color":"#eea638"},
    {"code":"TZ" , "name":"Tanzania", "value":46218486, "color":"#de4c4f"},
    {"code":"TH" , "name":"Thailand", "value":69518555, "color":"#eea638"},
    {"code":"TG" , "name":"Togo", "value":6154813, "color":"#de4c4f"},
    {"code":"TT" , "name":"Trinidad and Tobago", "value":1346350, "color":"#a7a737"},
    {"code":"TN" , "name":"Tunisia", "value":10594057, "color":"#de4c4f"},
    {"code":"TR" , "name":"Turkey", "value":73639596, "color":"#d8854f"},
    {"code":"TM" , "name":"Turkmenistan", "value":5105301, "color":"#eea638"},
    {"code":"UG" , "name":"Uganda", "value":34509205, "color":"#de4c4f"},
    {"code":"UA" , "name":"Ukraine", "value":45190180, "color":"#d8854f"},
    {"code":"AE" , "name":"United Arab Emirates", "value":7890924, "color":"#eea638"},
    {"code":"GB" , "name":"United Kingdom", "value":62417431, "color":"#d8854f"},
    {"code":"US" , "name":"United States", "value":313085380, "color":"#a7a737"},
    {"code":"UY" , "name":"Uruguay", "value":3380008, "color":"#86a965"},
    {"code":"UZ" , "name":"Uzbekistan", "value":27760267, "color":"#eea638"},
    {"code":"VE" , "name":"Venezuela", "value":29436891, "color":"#86a965"},
    {"code":"PS" , "name":"West Bank and Gaza", "value":4152369, "color":"#eea638"},
    {"code":"VN" , "name":"Vietnam", "value":88791996, "color":"#eea638"},
    {"code":"YE" , "name":"Yemen, Rep.", "value":24799880, "color":"#eea638"},
    {"code":"ZM" , "name":"Zambia", "value":13474959, "color":"#de4c4f"},
    {"code":"ZW" , "name":"Zimbabwe", "value":12754378, "color":"#de4c4f"}
]
stance = "NONE"
with open("../TextFiles/meta_data/orgs_"+stance+".json", "r") as f:
    countries = json.load(f)
    print("leng of countries = {}".format(len(countries)))

with open("../TextFiles/meta_data/country_mapper.json", "r") as f:
    mapper = json.load(f)
    print("leng of mapper = {}".format(len(mapper)))

mapData_all = []
for country in countries.keys():
    for dic in mapData:
        if mapper[country] == dic["name"]:
            name = dic["name"]
            code = dic["code"]
            value = int(countries[country])
            color = dic["color"]
            mapData_all.append({"code":code, "name":name, "value":value, "color":color})

print("length of mapData = {}".format(len(mapData_all)))
with open("../TextFiles/meta_data/organization_"+stance+".json", "w") as f:
    json.dump(mapData_all, f)

'''
