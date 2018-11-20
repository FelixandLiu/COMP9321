import urllib.request
import xml.etree.ElementTree as ET
import requests
def method1():
    indicator_list=[]
    url = urllib.request.urlopen( "http://api.worldbank.org/v2/indicators?page=6" )
    tree = ET.parse( url )
    root = tree.getroot()
    for elem in root:
        indicator_list.append(elem.get( 'id' ))
    print(indicator_list)


url = requests.get( "http://api.worldbank.org/v2/indicators?page=6" )
print(url)