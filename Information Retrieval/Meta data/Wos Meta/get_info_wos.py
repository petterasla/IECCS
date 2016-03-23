import time
from wos import WosClient
import wos.utils
from xml.etree import ElementTree
import credentials as c
import pandas as pd

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

# Get all titles
titles = pd.read_csv("../../tcp_abstracts.txt")
# Return a small list of titles for testing
small_list_titles = titles.Title.iloc[:1]

def queryWoS(titles):
    # Create an empty list which should contain info later
    info = []
    # Connect to Web of Science
    with WosClient(c.getUserName(), c.getPassword()) as client:
        # Looping through the titles (search parameter)
        for title in titles:
            # Replace '|' with ','
            title = title.replace("|","")
            # Check if the title contains any operators (like AND, OR, NOT)
            if isOperator(title):
                title = removeOperator(title)
            # Create the query string
            query_string = 'TI=' + title
            print query_string
            # Perform the query on wos engine
            xmlString = wos.utils.query(client, query_string)
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

l = queryWoS(small_list_titles)
#print l[0].keys()

def dfs_recursive(dict, key=None, visited=None):
    if visited is None:
        visited = set()
        print "start: \n"
    key_list = []
    try:
        key_list = dict.keys()
    except:
        print
        print "Key: " + key
        print "Value: " + str(dict)
        print
    if len(key_list) == 0:
        print 30*"=" + " LEAF VALUE " + 30*"="
    for next_key in key_list:
        visited.add(next_key)
        #print("Visiting key: " + str(next_key))
        dfs_recursive(dict[next_key], next_key, visited)


dfs_recursive(l[0], l[0].keys()[0])

