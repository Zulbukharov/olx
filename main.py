import requests
from bs4 import BeautifulSoup
import csv
import phone_parse
import os
from PIL import Image
from io import BytesIO

def write_csv(data):
    with open('olx.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['price'], data['phone'], data['city'], data['url']))

def get_html(url):
    r = requests.get(url)
    # print(r.cookies)
    return r.text

def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pager').find_all('a', class_='block')[-1].get('href')
    return int(pages[pages.find('page=') + len('page=') : ])

def get_page_info(url):
    data = {
        'title': '',
        'price': '',
        'city': '',
        'phone': '',
        'url': '',
    }
    soup = BeautifulSoup(get_html(url), 'lxml')
    offers = soup.find_all('td', class_='offer')
    for i in offers:
        # try:
        #     print(i.find('a').find('img'))
        #     response = requests.get(i.find('a').find('img').get('src'))
        #     img = Image.open(BytesIO(response.content))
        #     del img
        # except:
        #     print('none')
        try:
            data['title'] = i.find('h3').find('strong').text.strip()
        except:
            data['title'] = 'None'
        try:
            data['price'] = i.find('p', class_='price').text.strip()
        except:
            data['price'] = 'None'
        try:
            data['city'] = i.find('td', valign='bottom').find('span').text.strip()
        except:
            data['city'] = 'None'
        try:
            data['phone'] = phone_parse.start((i.find('h3').find('a').get('href')))
        except:
            data['phone'] = 'None'
        try:
            data['url'] = i.find('h3').find('a').get('href')
        except:
            data['url'] = 'None'
        write_csv(data)
        os.system("pkill chrome")
        # os.system("some_command < input_file | another_command > output_file")

def main(query):
    url = 'https://www.olx.kz/list/q-' + query
    page = '?page='
    # for i in range(1, get_pages(get_html(url))):
    for i in range(2, 4):
        print(url + page + str(i))
        get_page_info(url + page + str(i))

if __name__ == '__main__':
    main('xiaomi')
