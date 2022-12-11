import requests
from bs4 import BeautifulSoup
import re

def get_hostname(new_url, hostname):
    new_host = re.findall('://(www.)?([\w\-\.]+)', new_url)
    #sometimes the url doesn't have a hostname (assumedly the host is the og)
    if new_host == []:
        return hostname
    return new_host[0][1]

def get_protocol(new_url):
    pros = re.findall('(\w+)://', new_url)
    #print("pros")
    #print(pros)
    return re.findall('(\w+)://', new_url)[0]
