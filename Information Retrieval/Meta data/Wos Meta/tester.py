from wos import WosClient
import wos.utils
import credentials


with WosClient(credentials.getUserName(), credentials.getPassword()) as client:
    # WOS:A1991GM73000001
    id = "WOS:A1991GM73000001"
    s = wos.utils.get_related_records(client, id, count=2)
    print s

"""
from suds.client import Client
url_service = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearch?wsdl'

client = Client(url_service)

# List of methods from the Web Service Client Language (WSDL)
list_of_methods = [method for method in client.wsdl.services[0].ports[0].methods]

# List of parameters within the method
method = client.wsdl.services[0].ports[0].methods["InsertMethodNameHere"]
params = method.binding.input.param_defs(method)


print list_of_methods
[search, retrieve, relatedRecords, retrieveById, citedReferencesRetrieve, citingArticles, citedReferences]
"""