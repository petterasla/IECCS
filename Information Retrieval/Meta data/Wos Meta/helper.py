import pandas as pd
import adder

def getStanceByEndorse(endorse):
    if endorse <= 3:
        return "FAVOR"
    elif endorse >= 5:
        return "AGAINST"
    else:
        return "NONE"

def addOrganizationInfo(key,dic):
    if dic[key] is list:
        for i,d in enumerate(dic[key]):
            key_string_city = "Organization_city" + str(i)
            key_string_country = "Organization_country" + str(i)
            try:
                dic[key_string_city] = d['address_spec']['organizations']['city']
                dic[key_string_country] = d['address_spec']['organizations']['country']
            except KeyError:
                print "Key Error (wrong path) while storing organization address spec"
            except:
                print "Something went wrong storing organization address spec"

        dic["Num_of_organizations"] = len(dic[key])
    else:
        key_string_city = "Organization_city0"
        key_string_country = "Organization_country0"
        try:
            dic[key_string_city] = dic['address_spec']['organizations']['city']
            dic[key_string_country] = dic['address_spec']['organizations']['country']
            dic["Num_of_organizations"] = 1
        except KeyError:
            print "Key Error (wrong path) while storing organization address spec"
        except:
            print "Something went wrong storing organization address spec"
    return dic

def addAuthorInfo(key,dic):
    try:
        if dic is list:
            "AUTHOR DIC IS LIST"
            for i,d in enumerate(dic):
                key_string_author = "Author_name" + str(i)
                try:
                    dic[key_string_author] = d['wos_standard']
                except KeyError:
                    print "Key Error (wrong path) while storing organization address spec"
                except:
                    print "Something went wrong storing organization address spec"

            dic["Num_of_authors"] = len(dic)
            print
        return dic
    except:
        print("Author not list")
    try:
        key_string_author = "Author_name0"
        print "ADDING SIMPLE AUTHOR"
        dic[key_string_author] = dic['wos_standard']
        dic["Num_of_authors"] = 1
        return dic
    except KeyError:
        print "Key Error (wrong path) while storing organization address spec"
    except:
        print "Something went wrong storing organization address spec"
    return dic

tcp_data = pd.read_csv("../../tcp_abstracts.txt")
def getImportantInfo(dic):
    new_dic = {}
    new_dic["_id"] = tcp_data.Id.iloc[1]
    new_dic["Abstract"] = tcp_data.Abstract.iloc[1].replace("|",",")
    new_dic["Endorsement"] = tcp_data.Endorse.iloc[1]
    new_dic["Stance"] = getStanceByEndorse(tcp_data.Endorse.iloc[1])
    new_dic["Year"] = tcp_data.Year.iloc[1]
    new_dic["Category"] = tcp_data.Cat.iloc[1]
    new_dic["Title"] = tcp_data.Title.iloc[1].replace("|",",")


    new_dic = adder.add(dic, new_dic)

    return new_dic

def addToDict(key, val, dic, counter):
    if key=='count':
        return dic, counter
    if key == 'address_name':
        dic = addOrganizationInfo(key,dic)
    elif key == 'name':
        dic = addAuthorInfo(key, dic)
    try:
        if dic[key]:
            counter += 1
            new_key = key + str(counter)
            "Key already used.. Counter now = " + str(counter)
            dic[new_key] = val
    except KeyError:
        dic[key] = val
    except:
        print("Some other than KeyError appeared when adding key-value")
    return dic, counter

