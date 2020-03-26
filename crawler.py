import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)  # Response
    return r.text  # HTML


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    tds = soup.find('table', class_="tab").find_all('tr')
    links = []
    for td in tds:
        a = td.find('a').get('href')
        # rf40/pochtovye-indeksy-kaluzhskaya-oblast.html
        link = 'http://ruspostindex.ru/' + a
        # http://ruspostindex.ru/rf01/pochtovye-indeksy-adygeya-respublika.html
        links.append(link)
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        h1 = soup.find('h1', class_='').text.strip()
        h1_second = soup.find('h1', class_='pi').text.strip()
    except:
        h1 = ''
        h1_second = ''
    try:
        content_page = soup.find('table', class_='tab').text.strip()
    except:
        content_page = ''
    data = {'h1': h1,
            'h1_second': h1_second,
            'content_page': content_page}
    return data


def write_csv(data):
    with open('ruspostindex.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow({data['h1'],
                         data['h1_second'],
                         data['content_page']
                         })
        print(data['h1'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)

def main():
    start = datetime.now()

    url = 'http://ruspostindex.ru/'
    all_links = get_all_links(get_html(url))
    with Pool(40) as p:
        p.map(make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()
