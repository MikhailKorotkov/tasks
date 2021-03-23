import requests
from bs4 import BeautifulSoup
import re

animals = []
animals_counter = {'А': 0, 'Б': 0, 'В': 0, 'Г': 0, 'Д': 0, 'Е': 0, 'Ё': 0, 'Ж': 0, 'З': 0, 'И': 0, 'Й': 0, 'К': 0,
                   'Л': 0, 'М': 0, 'Н': 0, 'О': 0, 'П': 0, 'Р': 0, 'С': 0, 'Т': 0, 'У': 0, 'Ф': 0, 'Х': 0, 'Ц': 0,
                   'Ч': 0, 'Ш': 0, 'Щ': 0, 'Ъ': 0, 'Ы': 0, 'Ь': 0, 'Э': 0, 'Ю': 0, 'Я': 0}

URL = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
URL_PREFIX = 'https://ru.wikipedia.org/'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_next_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    next_page = soup.find(id="mw-pages").find_next('a')
    if next_page.contents[0] == "Следующая страница":
        next_page = URL_PREFIX + next_page['href']
    else:
        next_page = next_page.find_next('a')
        next_page = URL_PREFIX + next_page['href']
    return next_page


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_="mw-category-group")

    for item in items.find_all('a', href=True):
        animals.append(item['title'])
    stopper = item['title'][0]
    return stopper


def parse(url=URL):
    html = get_html(url)
    if html.status_code == 200:
        stopper = get_content(html.text)
        return html.text, stopper
    else:
        print('Error')


def main():
    pt = parse()
    np = get_next_page(pt[0])
    stopper = pt[1]
    while np.startswith('https://ru.wikipedia.org//w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F') \
            and re.match(r'[А-Я]', stopper):
        pt = parse(np)
        np = get_next_page(pt[0])
        stopper = pt[1]


if __name__ == '__main__':
    main()
    animals = animals[0:len(animals)-200]
    for animal in animals:
        key = animal[0]
        animals_counter[key] += 1
    print(animals_counter)

v = {'А': 1090, 'Б': 1395, 'В': 483, 'Г': 820, 'Д': 530, 'Е': 27, 'Ё': 2, 'Ж': 211, 'З': 395, 'И': 322, 'Й': 0, 'К': 2003,
     'Л': 469, 'М': 1054, 'Н': 287, 'О': 618, 'П': 1462, 'Р': 390, 'С': 1653, 'Т': 766, 'У': 197, 'Ф': 169, 'Х': 222,
     'Ц': 28, 'Ч': 456, 'Ш': 115, 'Щ': 56, 'Ъ': 0, 'Ы': 0, 'Ь': 0, 'Э': 51, 'Ю': 0, 'Я': 171}
