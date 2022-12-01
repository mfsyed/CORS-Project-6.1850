import requests
import bs4


headers = {'Accept-Encoding': 'identity'}
url = 'https://61040-fa22.github.io/3-recitation-and-studio.html'
r = requests.get(url, headers=headers)

print(r.text)
