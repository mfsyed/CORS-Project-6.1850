import requests
from bs4 import BeautifulSoup


headers = {'Accept-Encoding': 'identity'}
url = 'https://www.youtube.com/'
r = requests.get(url, headers=headers)

htmlMaterial = r.text

soup = BeautifulSoup(htmlMaterial, 'html.parser')

iframes=soup.find_all('iframe')

for iframe in iframes:
    print (iframe['src'])


imgs =soup.find_all('img')

scripts = soup.find_all('script')

print(scripts)