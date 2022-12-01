import requests
from bs4 import BeautifulSoup


headers = {'Accept-Encoding': 'identity'}
url = 'https://61040-fa22.github.io/3-recitation-and-studio.html'
r = requests.get(url, headers=headers)

htmlMaterial = r.text

soup = BeautifulSoup(htmlMaterial, 'html.parser')

print(soup)
