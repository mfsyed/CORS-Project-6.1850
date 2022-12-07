import requests
from bs4 import BeautifulSoup
import re
# helper function for getting a hostname from a url
def get_hostname(new_url):
    new_host = re.findall('://(www.)?([\w\-\.]+)', new_url)
    #sometimes the url doesn't have a hostname (assumedly the host is the og)
    if new_host == []:
        return hostname
    return new_host[0][1]

def get_protocol(new_url):
    return re.findall('(\w+)://', new_url)[0]

# we want all iframes, img, script
headers = {'Accept-Encoding': 'identity'}
# you can try this with netflix, 
#                       1040 website (change html code from assets/main.css -> https://61040-fa22.github.io/assets/main.css)   
#                                     if you want it to have the table)
#                       yahoo news
# things get real weird with youtube, cnn
url = 'https://www.netflix.com/'
hostname = get_hostname(url)
protocol = get_protocol(url)
print("host: " + hostname)
print("protocol: " + protocol)
r = requests.get(url, headers=headers)

htmlMaterial = r.text

soup = BeautifulSoup(htmlMaterial, 'html.parser')
# all tags that have a src attribute where the src is not our og source
everything=soup.find_all(lambda tag: tag.has_attr("src") and get_hostname(tag["src"]) != hostname)
# doing scripts separately bc sometimes they have js code that access outside urls
scripts = soup.find_all(lambda tag: tag.name == "script" and not tag.has_attr("src"))

for tag in everything:
    tag["src"] = ""
    if tag.has_attr("srcset"):
        # srcset has alternative images if src isn't working
        # leading to more cross-origin requests
        tag["srcset"] = ""
    if tag.name == "iframe":
        # this adds a grey box for iframe case
        tag["style"] = tag["style"] + "background: grey" if "style" in tag else "background: grey; height: 300; width: 300"
    if tag.name == "img":
        # grey box for img case
        tag["src"] = "grey_im.jpg"
for tag in scripts:
    if not tag.contents:
        continue
    # yeeting all different hostname urls in scripts
    tag.contents = [re.sub('(\w+)://([\w\-\.]+)', protocol + "://" + hostname, tag.contents[0])]

with open("trial_html.html", 'w') as f:
    f.write(str(soup.prettify()))