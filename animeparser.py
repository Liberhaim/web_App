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


def setnextdate(tag1, tag2):
    next_date = str
    if tag1[0].text.strip() == "Следующий эпизод":
        next_episod = tag2[0].text.strip().split(' ')
        try:
            datestring = next_episod[0] + next_episod[1][:-1] + next_episod[2] + next_episod[4].strip()
            next_date = datetime.strptime(datestring, '%d%b%Y%H:%M')
        except:
            next_date = "дата не корректна"
        finally:
            return next_date
    else:
        return tag2[2].text


def parser(link_url, headers=HEADERS):

    req = requests.get(link_url, headers)
    src = req.content

    soups = BeautifulSoup(src, 'lxml')

    # Получение имени на проект
    title = soups.find("h1").text
    # print(f"\nНазвание аниме: {anime_title}")

    # Получение нормальной ссылк ина картинку
    link_jpeg = soups.find("div", class_="poster-icon").next_element.next_element.next_element
    for link in link_jpeg:
        link_src_img = link.get("src")
    # print(f"\nСсылка на картинку: {link_src_img}\n")

    # Получение рейтинга
    rating = soups.find('span', class_="rating-value").text.replace(',', '.')


    locale.setlocale(locale.LC_ALL, ("ru-RU", 'UTF-8'))
    # Дата следующего эпизода

    tag_dd = soups.find("div", class_="anime-info").find_all("dd")
    tag_dt = soups.find("div", class_="anime-info").find_all("dt")

    # Получить инфу "дату выхода серии" / информ. о том что серия "вышла", иначе "дата не корректна"
    date_next_ongoing = setnextdate(tag_dt, tag_dd)

    # разбор таблицы с тегом "dd" класса "anime-info"
    index = 0
    aa = []
    table_dd = soups.find("div", class_="anime-info").find_all("dd", class_="col-6")
    for item in table_dd:
        items = item.text.strip()
        if items.find(",") > 0 and index < 12:
            aa.append(" ".join(items.split()))
        elif items.find('\n') > 0 and index >= 12:
            tempstr = re.sub(r'\s+', ' ', items)
            aa.append(re.sub(pattern=r'\)', repl="), ", string=tempstr)[:-2])
            # aa.append(tempstr.replace(")", "), ")[:-1])
        else:
            aa.append(items)
        index += 1
    status = aa[2]
    number_episodes = aa[1]
    if status == 'Онгоинг':
        duber_list = aa[11]
    else:
        duber_list = aa[12]
    genre = aa[3]


# скачать картинку
# def downad_pic()
#     p = requests.get(link_src_img)
#     out = open(f"{anime_title}.jpg", "wb")
#     out.write(p.content)
#     out.close()

    content = {
        "title": title,
        "link_src_img": link_src_img,
        "rating": rating,
        "date_next_ongoing": date_next_ongoing,
        'duber_list': duber_list,
        "genre": genre,
        "status": status,
        "number_episodes": number_episodes
    }

    return content


if __name__ == "__main__":
    # открыть текстовый файл с именами аниме, иная создать его
    with open('url_list_anime.txt', 'r', encoding="utf-8") as ListAnime:
        listanime = ListAnime.readlines()

    count_anime = len(listanime)

    for i in range(0, 3, 1):
        content = parser(listanime[i].strip())

