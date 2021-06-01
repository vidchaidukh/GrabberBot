from bs4 import BeautifulSoup as bf
import requests
from random import choice
import sqlite3
headers = [{'User-Agent': 'Firefox 45 on Mac OS X (Mavericks)'},
             {'User-Agent': 'Firefox 88 on Windows 10'}]

def catch(url):
    print('catch olx')

    r = requests.get(url, headers = choice(headers))
    with open('test.html', 'wb') as output_file:
        output_file.write(r.text.encode('utf-8'))
    soup = bf(r.text.encode('utf-8'), 'html.parser')
    offers = soup.findAll('td', {'class': "offer"})
    for offer in offers[:1]:
        url_advert = offer.find('h3').find('a').get('href')
        print(url_advert)
        grab_advert(url_advert)


def grab_advert(url_advert):
    r = requests.get(url_advert, headers=choice(headers))
    with open('test.html', 'wb') as output_file:
        output_file.write(r.text.encode('utf-8'))
    soup = bf(r.text.encode('utf-8'), 'html.parser')
    date = soup.find('span', {'data-cy': "ad-posted-at"}).text
    name = soup.find('h1').text

    print(date, name)
