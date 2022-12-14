import requests
from bs4 import BeautifulSoup
import re
import originExtractor

hellos = []

def corsByProtcol(url):

    totalTags = 0
    totalCORS = 0
    corsImgs = 0
    corsScripts =0
    corsFrames = 0
    
    # we want all iframes, img, script
    headers = {'Accept-Encoding': 'identity'}


    hostname = originExtractor.get_hostname(url, '')
    protocol = originExtractor.get_protocol(url)
    print("host: " + hostname)
    print("protocol: " + protocol)
    r = requests.get(url, headers=headers)

    htmlMaterial = r.text

    soup = BeautifulSoup(htmlMaterial, 'html.parser')

    # all tags that have a src attribute where the src is not our og source
    everything= soup.find_all(lambda tag: tag.has_attr("src"))
    everythingCORS=soup.find_all(lambda tag: tag.has_attr("src") and originExtractor.get_protocol(tag["src"]) not in (protocol, None))
    # print("percent")
    # print(len(everythingCORS))

    # doing scripts separately bc sometimes they have js code that access outside urls
    scripts = soup.find_all(lambda tag: tag.name == "script" and not tag.has_attr("src"))

    for tag in everything:
        totalTags += 1

        if originExtractor.get_protocol(tag["src"]) != protocol:
            totalCORS += 1
            tag["src"] = ""

            if tag.has_attr("srcset"):
                print("here")
                #print(tag["srcset"])
                # srcset has alternative images if src isn't working
                # leading to more cross-origin requests
                tag["srcset"] = ""

            if tag.name == "iframe":
                corsFrames += 1
                # this adds a grey box for iframe case
                tag["style"] = tag["style"] + "background: grey" if "style" in tag else "background: grey; height: 300; width: 300"

            if tag.name == "img":
                corsImgs += 1
                # grey box for img case
                tag["src"] = "grey_im.jpg"

            if tag.name == "script":
                corsScripts += 1
                tag["src"] = ""

        elif tag.has_attr("srcset"):
                print("here")
                print(tag["srcset"])

    tagi = 0
    for tag in scripts: 
        tagi += 1
        totalTags += 1
        if not tag.contents:
            continue
        # yeeting all different hostname urls in scripts
        #print(tag.contents)

        ci = 0
        for c in tag.contents:
            ci += 1
            pros = re.findall('(\w+)://', c)
            for pro in pros:
                if pro != protocol:
                    print(ci, tagi)
                    print(pro)
                    hellos.append(c)
                    totalCORS += 1

        tag.contents = [re.sub('(\w+)://', protocol + "://", tag.contents[0])]

    print({"totalTags: ": totalTags,
           "totalCORS:": totalCORS,
           "Images Rendered with CORS ": corsImgs,
           "Frames Rendered with CORS ": corsFrames,
           "Scripts Rendered with CORS ": corsScripts})

    with open("trial_html.html", 'w') as f:
        f.write(str(soup.prettify()))



corsByProtcol('https://www.youtube.com/')

# for h in hellos:
#     print(h)
#     print('\n')
#     print('\n')
#     print('\n')
#     print('\n')

#     print('\n')