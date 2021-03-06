import urllib2
from lxml import etree
import sys

username = 'student'
password = 'dj78dfGF'
query = 'garden'

# Submit an authenticated request to the AURIN Open API
def openapi_request(url):

    # create an authenticated HTTP handler and submit URL
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_manager)
    urllib2.install_opener(opener)

    req = urllib2.Request(url)
    handler = urllib2.urlopen(req)

    return handler.read()

# Get a list of all available datasets and their licences
url='http://openapi.aurin.org.au/csw?request=GetRecords&service=CSW&version=2.0.2&typeNames=csw:Record&elementSetName=full&resultType=results&constraintLanguage=CQL_TEXT&constraint_language_version=1.1.0&maxRecords=1000'
xml = openapi_request(url)
root = etree.fromstring(xml)
#print etree.tostring(root, pretty_print=True)
for dataset in root.findall(".//csw:Record", root.nsmap):
    #print etree.tostring(dataset, pretty_print=True)
    title = dataset.find(".//dc:title", root.nsmap).text
    print title
    #print dataset.find('dct:references',root.nsmap).text

sys.exit()
# Query the attributes of the first dataset
dataset = root.findall(".//dc:title", root.nsmap)[0].text
url = 'http://openapi.aurin.org.au/wfs?request=DescribeFeatureType&service=WFS&version=1.1.0&typeName='+dataset
print '================ DATASET PROPERTIES ================'
print 'Query URL: '+url
xml = openapi_request(url)
root = etree.fromstring(xml)
print etree.tostring(root, pretty_print=True)


# Get the first feature (row) of the first dataset
url = 'http://openapi.aurin.org.au/wfs?request=GetFeature&service=WFS&version=1.1.0&TypeName='+dataset+'&MaxFeatures=1'
print '================ FIRST FEATURE ================'
print 'Query URL: '+url
xml = openapi_request(url)
root = etree.fromstring(xml)
print etree.tostring(root, pretty_print=True)



