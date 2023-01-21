"""
install packedge:
    pip install requests
    pip install lxml
    pip install beautifulsoup4

"""
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import time


HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
}
content = {}


def parser(link_url, headers=HEADERS):

    req = requests.get(link_url, headers)
    src = req.content

    soups = BeautifulSoup(src, 'lxml')

    # Получение имени на проект
    anime_title = soups.find("h1").text
    # print(f"\nНазвание аниме: {anime_title}")

    # Получение нормальной ссылк ина картинку
    link_jpeg = soups.find("div", class_="poster-icon").next_element.next_element.next_element
    for link in link_jpeg:
        link_src_img = link.get("src")
    # print(f"\nСсылка на картинку: {link_src_img}\n")

    # Получение рейтинга
    anime_rating = soups.find('span', class_="rating-value").text.replace(',', '.')

    # print(f"Рейтинг: {anime_rating}/10")

    # # Дата следующего эпизода
    # next_episod = ""
    # is_serial_exit = False
    # _ = soups.find("div", class_="anime-info").find("dd", class_="col-12")
    # _ = _.text.strip().split('\n')
    # if _[0] != "":
    #     next_episod = _[1].strip() + ", " + _[0].strip()
    # else:
    #     is_serial_exit = True
    #     is_serial_exit = "Вышел"
    #     # print("empty str")

    locale.setlocale(locale.LC_ALL, ("ru-RU", 'UTF-8'))
    # Дата следующего эпизода
    next_date = ""
    is_serial_exit = False
    tag_dd = soups.find("div", class_="anime-info").find_all("dd")
    print(tag_dd[2].text)
    if tag_dd[2].text != "Вышел":
        next_episod = tag_dd[0].text.strip().split(' ')
        print(next_episod)
        try:
            datestring = next_episod[0] + '-' + next_episod[1][:-1] + '-' + next_episod[2]
            next_date = datetime.strptime(datestring, '%d-%b-%Y').date()
            print(next_date)
        except:
            next_date = "data not correct"


    # разбор таблицы с тегом "anime-info"
    aa = []
    date_next_ongoing = soups.find("div", class_="anime-info").find_all("dd", class_="col-6")
    for item in date_next_ongoing:
        items = item.text.strip()
        if items.find(",") > 0:
            aa.append(re.sub(r'\W+', ", ", items))
        else:
            aa.append(items)
    # aa = []
    # for item in date_next_ongoing:
    #     items = item.text.strip()
    #     if items.find(",") >= 1:
    #         s = ''.join(items.split())
    #         aa.append(s)
    #     else:
    #         aa.append(items)

    # date_next_ongoing = _.get("data-title") + ' (' + _.text.strip() + ')'

    # print(f'Следующий эпизод: {data_next_ongoing.get("data-title")} ({data_next_ongoing.text.strip()})')
    anime_duber_list = aa[11]
    genre = aa[3]

    # удаление ненужных символов из строки и создание списка с озвучкой дабберов
    del_symbol = ["'", " "]
    for item in del_symbol:
        if item in anime_duber_list:
            anime_duber_list = anime_duber_list.replace(item, "")

    # print(f"В озвучке: {anime_duber_list}")

# скачать картинку
# def downad_pic()
#     p = requests.get(link_src_img)
#     out = open(f"{anime_title}.jpg", "wb")
#     out.write(p.content)
#     out.close()

    content = {
        "anime_title": anime_title,
        "link_src_img": link_src_img,
        "anime_rating": anime_rating,
        "date_next_ongoing": date_next_ongoing,
        "next_date" : next_date,
        'anime_duber_list': anime_duber_list,
        "genre": genre
    }

    return content


if __name__ == "__main__":
    # открыть текстовый файл с именами аниме, иная создать его
    with open('url_list_anime.txt', 'r') as ListAnime:
        listanime = ListAnime.readlines()

    count_anime = len(listanime)

    for i in range(0, 4, 1):
        content = parser(listanime[i].strip())

