"""
install package:
    pip install requests
    pip install lxml
    pip install beautifulsoup4

"""
import re
import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

HEADERS = {
    "Accept"    : "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
}



def set_next_date(tag1, tag2):
    next_date = str
    if tag1 == "Следующий эпизод":
        next_episode = tag2.split(' ')
        try:
            date_string = next_episode[0] + next_episode[1][0:3] + next_episode[2] + next_episode[4].strip()
            next_date = datetime.strptime(date_string, '%d%b%Y%H:%M')
        except:
            next_date = "дата не корректна"
            # raise
        finally:
            return next_date
    else:
        return tag2.text


def parser(link_url, headers=HEADERS):
    locale.setlocale(locale.LC_ALL, ("ru-RU", 'UTF-8'))

    req = requests.get(link_url, headers)
    src = req.content

    soups = BeautifulSoup(src, 'lxml')

    # Получение имени на проект
    title = soups.find("h1").text

    # Получение нормальной ссылки на картинку
    link_jpeg = soups.find("div", class_="poster-icon").next_element.next_element.next_element
    for link in link_jpeg:
        link_src_img = link.get("src")

    # Получение рейтинга
    rating = soups.find('span', class_="rating-value").text.replace(',', '.')


    # разбор таблицы класса "anime-info"
    # разбор таблицы с тегом "dt" класса "anime-info"
    dt = []
    table_dt = soups.find("div", class_="anime-info").find_all("dt", class_="col-6")
    for item in table_dt:
        items = item.text.strip()
        if items.find(",") > 0 and index < 12:
            dt.append(" ".join(items.split()))
        elif items.find('\n') > 0 and index >= 12:
            temp_str = re.sub(r'\s+', ' ', items)
            dt.append(re.sub(pattern=r'\)', repl="), ", string=temp_str)[:-2])
        else:
            dt.append(items)

    # разбор таблицы с тегом "dd" класса "anime-info"
    index = 0
    dd = []
    table_dd = soups.find("div", class_="anime-info").find_all("dd", class_="col-6")
    for item in table_dd:
        items = item.text.strip()
        if items.find(",") > 0 and index < 12:
            dd.append(" ".join(items.split()))
        elif items.find('\n') > 0 and index >= 10:
            temp_str = re.sub(r'\s+', ' ', items)
            dd.append(re.sub(pattern=r'\)', repl="), ", string=temp_str)[:-2])
        else:
            dd.append(items)
        index += 1


    # создание словаря класса "anime-info"
    class_anime_info = dict(zip(dt, dd))

    # Получить информацию "дату выхода серии" / информ. О том что серия "вышла", иначе "дата не корректна"
    # date_next_ongoing_for_tv = []
    try:
        tag_dd = soups.find("div", class_="anime-info").find("dd", class_="col-12").text.strip()
        tag_dt = soups.find("div", class_="anime-info").find("dt", class_="col-12").text.strip()
        date_next_ongoing_for_tv = set_next_date(tag_dt, tag_dd).strftime("%H:%m %d/%m/%Y")
    except:
        date_next_ongoing_for_tv = 'Тайтл вышел'


    anime_content = {
        "url": link_url,
        "title": title,
        "link_src_img": link_src_img,
        "rating": rating,
        "date_next_ongoing_for_tv": date_next_ongoing_for_tv,
        'dubber_list': class_anime_info['Озвучка'],
        "genre": class_anime_info['Жанр'],
        "status": class_anime_info['Статус'],
        "number_episodes": class_anime_info['Эпизоды'],
        "age_limit": class_anime_info['Возрастные ограничения'],
        "type_anime": class_anime_info['Тип'],
        "start_data": class_anime_info['Выпуск']
    }

    return anime_content


if __name__ == "__main__":

    # открыть текстовый файл с url аниме
    with open('url_list_anime.txt', 'r', encoding="utf-8") as ListAnime:
        list_anime = ListAnime.readlines()

    count_anime = len(list_anime)
    anime_json = dict()
    start_time = time.time()

    for i in range(0, count_anime - 1, 1):
        anime_json[i] = parser(list_anime[i].strip(), HEADERS)

    print(f'время потрачено: {time.time() - start_time}')
    print(anime_json)

    with open("anime_json.json", "w", encoding='utf-8') as file:
        # file.write(json.dumps(anime_json))
        json.dump(anime_json, file, indent=2, ensure_ascii=False)

    # path_webdriver = r"C:\project_python\ParserAmimegoOrg\webdriver\chromedriver.exe"
    #
    # s = Service(path_webdriver)
    #
    # chromeOptions = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=s)
    # url = "file:///D:/1.html"
    # driver.get(url)
    # time.sleep(5)
    # driver.close()
    # driver.quit()
