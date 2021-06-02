from datetime import datetime, timedelta

from bs4 import BeautifulSoup as bf
import requests
from random import choice
import sqlite3
headers = [{'User-Agent': 'Firefox 75 on Mac OS X (Mavericks)'},
            {'User-Agent': 'Firefox 88 on Windows 10'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/82.0'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/80.0'}]

def catch(url, req_id, last_update):
    '''Функція грабінгу та парсингу сторінки з оголошеннями, отримання посилання на кожне оголошення, дату публікації
    та місцезнаходження'''

    try:
        r = requests.get(url, headers = choice(headers))
        with open('test.html', 'wb') as output_file:
            output_file.write(r.text.encode('utf-8'))
        soup = bf(r.text.encode('utf-8'), 'html.parser')
    except:
        return -1
    try:
        offers = soup.findAll('td', {'class': "offer"})
        next_page = soup.find('span', {'class': "fbold next abs large"}).find('a').get('href')
    except:
        print('secs')

        return 0
    for offer in offers[6:]:
        date = date_format(offer.findAll('small', {'class': "breadcrumb x-normal"})[-1].find('span').text)

        adv_date_list = [int(item) for item in date.split(',')]
        last_update_list = [int(item) for item in last_update.split(',')]

        if datetime(*adv_date_list) < datetime(*last_update_list):
            print('first')
            return 1
        url_advert = offer.find('h3').find('a').get('href')
        location = offer.findAll('small', {'class': "breadcrumb x-normal"})[1].find('span').text
        grab_advert(url_advert, date, location, req_id)
    catch(next_page, req_id, last_update)


def grab_advert(url_advert, date, location, req_id):
    '''Функція грабінгу та парсингу сторінки оголошення, отримання 6 різних параметрів оголошення'''

    r = requests.get(url_advert, headers=choice(headers))
    with open('test.html', 'wb') as output_file:
        output_file.write(r.text.encode('utf-8'))
    soup = bf(r.text.encode('utf-8'), 'html.parser')
    name = soup.find('h1').text
    id_adv = soup.find('span', {'class': 'css-7oa68k-Text eu5v0x0'}).text.split()[1]
    try:
        price = soup.find('h3').text
    except:
        price = "Не указано"

    try:
        img_href = soup.find('img', {'class':"css-1bmvjcs"}).get('src')
        response = requests.get(img_href)
        with open('img/' + id_adv +'.png', 'wb') as f:
            f.write(response.content)
    except:
        pass
    try:
        description = soup.find('div', {'class': 'css-g5mtbi-Text'}).text.replace('<br>', '\n')
    except:
        description = "Не указано"
    print(date, name, id_adv, price, description)
    write_to_adverts(req_id, id_adv, name, price, date, location, url_advert, description)

def date_format(text):
    '''Функція приведення часу платформи до стандартизованого формату бд'''

    months = {'май':'5'}
    time_now = datetime.now()
    date_list = text.split(' ')
    if date_list[0] == "Сегодня":
        date = time_now.strftime("%Y/%m/%d").split('/') + date_list[-1].split(':')
    elif date_list[0] == "Вчера":
        yesterday = time_now - timedelta(days=1)
        date = yesterday.strftime("%Y/%m/%d").split('/') + date_list[-1].split(':')
    else:
        date = [str(time_now.year), months.get(date_list[-1]), date_list[0]] + ['00', '00']
    date_str = ','.join(date)
    return date_str

def write_to_adverts(req_id, id_adv, name, price, date, location, url_advert, description):
    '''Функція додавання запису в таблицю adverts'''

    try:
        conn = sqlite3.connect('db/database.db', check_same_thread=False)
        cursor = conn.cursor()
        print('writed')
        cursor.execute('INSERT INTO adverts (id_request, id_advert, platform, header, price, time, location, url_advert, desc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (req_id, id_adv, 'olx', name, price, date, location, url_advert, description))
        cursor.close()
        conn.commit()
    except:
        pass
