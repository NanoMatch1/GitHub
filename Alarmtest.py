from playsound import playsound
import os

for file in os.listdir():
    if file.endswith('.mp3'):
        print(file)


file = 'Breathe.mp3'

# playsound('iPhone.mp3')
# API = '9d7fbec2-b467-4217-82d6-413c483dcbb1'
# from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
# cmc = CoinMarketCapAPI(API)
# r = cmc.cryptocurrency_quotes_latest(symbol = 'DOGE')
# print(r.data)


import requests
from bs4 import BeautifulSoup as bsoup

URL = 'https://coinmarketcap.com/'
page = requests.get(URL)

# print(page.content)
soup = bsoup(page.content, 'html.parser')

print(soup.prettify())
