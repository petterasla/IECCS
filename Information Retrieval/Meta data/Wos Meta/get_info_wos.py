import time
from wos import WosClient
import wos.utils
from xml.etree import ElementTree
import credentials as c
import pandas as pd
import json
import helper

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)

class XmlDictConfig(dict):
    '''
    Example usage:

    tree = ElementTree.parse('your_file.xml')
    root = tree.getroot()
    xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    root = ElementTree.XML(xml_string)
    xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

def isOperator(string):
    operators = ["AND", "OR", "NOT", "NEAR", "SAME"]
    for word in string.split(" "):
        if word.upper() in operators:
            return True
    return False

def removeOperator(string):
    operators = ["AND", "OR", "NOT", "NEAR", "SAME"]
    return ' '.join([word for word in string.split(" ") if word.upper() not in operators])


def queryWoS(titles, years):
    # Create an empty list which should contain info later
    info = []
    # Connect to Web of Science
    with WosClient(c.getUserName(), c.getPassword()) as client:
        # Looping through the titles (search parameter)
        for i,title in enumerate(titles):
            # Replace '|' with ','
            title = title.replace("|","")
            # Get year published
            year = years[i]
            # Create year query with +/- 1 year
            query_string_year = 'PY=(' + str(year-1) + ' OR ' + str(year) + ' OR ' + str(year+1) + ')'
            # Check if the title contains any operators (like AND, OR, NOT)
            if isOperator(title):
                title = removeOperator(title)
            # Create title query
            query_string_title = 'TI=' + title
            # Create query AND operator string
            query_AND_operator = ' AND '
            # Create the query string
            query_string = query_string_title + query_AND_operator + query_string_year
            print query_string
            # Perform the query on wos engine
            xmlString = wos.utils.query(client, query_string, count=1)
            print xmlString
            # Convert to XML object
            root = ElementTree.XML(xmlString)
            # Convert XML object to a dictionary
            xmlDict = XmlDictConfig(root)
            # Add the dictionary to the info list
            info.append(xmlDict)
            # Just for being 'nice' to WoS and not bomb attack the server
            time.sleep(1)
    return info




def dfs_recursive(dict, new_dict, key=None, visited=None, counter=None):
    """
    Recursive method to find leaf nodes (values) in a dictionary

    :param dict:        dict:
    :param new_dict:    dict: Dunno why I called it new_dict..
    :param key:         string:
    :param visited:     set: of visited vertices
    :param counter:     integer: only when trying to store a value with same key
    :return:            Returns a dictionary with values only, no nesting
    """
    # First iteration, set some initial values - not really necessary though
    if visited is None:
        visited = set()
        counter = 0
        print "start: \n"
    # Create a key list
    key_list = []
    # Try to see if the dictionary has any keys.
    try:
        key_list = dict.keys()
    # If not, then there is a leaf node (value) which should be added to dictionary
    except:
        # Add value to the dictionary when leaf node found
        new_dict, counter = helper.addToDict(key, dict, new_dict, counter)
    for next_key in key_list:
        # Recursive dig deeper into the dictionary
        visited.add(next_key)   # Not used.. Just for debugging purpose
        new_dict = dfs_recursive(dict[next_key], new_dict, key=next_key, visited=visited, counter=counter)
    # Return the dictionary with no nesting
    return new_dict


def storeDataAsJson(list_of_dicts):
    """
    This method loops through the converted XML dictionaries and store the important data as a new dictionary
    When all dictionaries done, it should store the list as json

    :param list_of_dicts:   list: containing dictionaries converted from XML
    """
    # TODO: Discover why some fields are stored as the same in many dictionaries, like city:"CHRISTCHURCH"
    # Creates empty dict and empty list
    empty_dic = {}
    new_list_of_dicts = []
    # Loop through the returned dictionaries of WoS
    for i in range(len(list_of_dicts)):
        # Store a new dictionary with values only, no nesting.
        dic = dfs_recursive(list_of_dicts[i], empty_dic, list_of_dicts[i].keys()[0])
        # Store a new final dictionary by adding the most important data
        new_dic = helper.getImportantInfo(dic, i)
        # Add final dictionary to a list
        new_list_of_dicts.append(new_dic)
        # Just for printing purposes
        print
        print 120*"="
        print 120*"="
        print

    # Printing the dictionaries in the final list
    for d in new_list_of_dicts:
        print d
        print "Lenght of dictionary: " + str(len(d.keys()))
        print
    print "Length of new list of dicts: " + str(len(new_list_of_dicts))


    # TODO: When everything is ready, uncomment below and store the shit out the data

    """
    with open('wos_meta_data.json', 'w') as out:
        json.dump(new_list_of_dicts, out)
        out.close()
    """


# Get all titles
tcp_data = pd.read_csv("../../tcp_abstracts.txt")
# Return a small list of titles for testing
small_list_titles = tcp_data.Title.iloc[:5]
small_list_years = tcp_data.Year.iloc[:5]
# Get a list of dicts containing data wos
list_of_dicts_from_wos = queryWoS(small_list_titles, small_list_years)
# Find the important data and store them as json
storeDataAsJson(list_of_dicts_from_wos)



#For testing recursive algorithm
#li = {}
#test = dfs_recursive(l[0], li, key=l[0].keys()[0])
#test = dfs_recursive(l[1], li, key=l[1].keys()[0])


#A 20-YEAR RECORD OF ALPINE GRASSHOPPER ABUNDANCE, WITH INTERPRETATIONS FOR CLIMATE CHANGE
# A GEOLOGICAL PERSPECTIVE ON CLIMATIC-CHANGE - COMPUTER-SIMULATION OF ANCIENT CLIMATES

