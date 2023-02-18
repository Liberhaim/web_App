"""
install package:
    pip install requests
    pip install lxml
    pip install beautifulsoup4

"""
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

HEADERS = {
    "Accept"    : "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
}


def set_next_date(tag1, tag2):
    next_date = str
    if tag1 == "Следующий эпизод":
        next_episode = tag2[0].text.strip().split(' ')
        try:
            date_string = next_episode[0] + next_episode[1][:-1] + next_episode[2] + next_episode[4].strip()
            next_date = datetime.strptime(date_string, '%d%b%Y%H:%M')
        except:
            next_date = "дата не корректна"
            # raise
        finally:
            return next_date
    else:
        return tag2[2].text


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

    tag_dd = soups.find("div", class_="anime-info").find_all("dd")
    tag_dt = soups.find("div", class_="anime-info").find("dt").text.strip()

    date_next_ongoing_for_tv = []

    # try:
    #     key_dict_next_episode = soups.find("div", class_="anime-info").find("dt", class_="col-12").text.strip()
    #     value_dict_next_episode = soups.find("div", class_="anime-info").find("dd", class_="col-12").text.strip()
    #     next_episode = value_dict_next_episode.split(' ')
    #     date_string = next_episode[0] + next_episode[1][:-1] + next_episode[2] + next_episode[4].strip()
    #     next_date = datetime.strptime(date_string, '%d%b%Y%H:%M')
    #
    #     print(f"сериал показывают: {title}")
    #     print(f"дата {key_dict_next_episode}: {next_date}")
    # except:
    #     print(f"сериал уже вышел: {title}")

    # day = "4"
    # mouth = "февр"
    # year = "2023"
    # time = "17:30"
    # date = day + mouth + year + time
    # next_date = datetime.strptime(date, '%d%b%Y%H:%M')
    # print(next_date)
    # date_next_ongoing_for_tv = dict(zip(key_dict_next_episode, value_dict_next_episode))



    # table_dt = soups.find("div", class_="anime-info").find_all("dt", class_="col-6")

    # Получить информацию "дату выхода серии" / информ. О том что серия "вышла", иначе "дата не корректна"
    date_next_ongoing_for_tv = set_next_date(tag_dt, tag_dd)

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
    status = dd[2]
    number_episodes = dd[1]


    # создание словаря класса "anime-info"
    class_anime_info = dict(zip(dt, dd))

    type_anime = dd[0]
    if class_anime_info['Тип'] == 'ТВ Сериал':
        print('ok')

    if type_anime == 'OVA':
        if status == 'Онгоинг':
            dubber_list = dd[11]
            age_limit = dd[9]
            start_data = dd[6]
        elif status == 'Вышел':
            dubber_list = dd[10]
            age_limit = dd[8]
            start_data = dd[5]

    elif type_anime == 'ТВ Сериал':
        if status == 'Онгоинг':
            dubber_list = dd[11]
            age_limit = dd[9]
            start_data = dd[6]
        elif status == 'Вышел':
            dubber_list = dd[12]
            age_limit = dd[8]
            start_data = dd[5]

    genre = dd[3]

# скачать картинку
# def download_pic()
#     p = requests.get(link_src_img)
#     out = open(f"{anime_title}.jpg", "wb")
#     out.write(p.content)
#     out.close()

    anime_content = {
        "title": title,
        "link_src_img": link_src_img,
        "rating": rating,
        "date_next_ongoing_for_tv": date_next_ongoing_for_tv,
        'dubber_list': dubber_list,
        "genre": genre,
        "status": status,
        "number_episodes": number_episodes,
        "age_limit": age_limit,
        "type_anime": type_anime,
        "start_data": start_data
    }

    return anime_content


if __name__ == "__main__":

    # открыть текстовый файл с url аниме
    with open('url_list_anime.txt', 'r', encoding="utf-8") as ListAnime:
        list_anime = ListAnime.readlines()

    count_anime = len(list_anime)

    for i in range(0, count_anime-1, 1):
        content = parser(list_anime[i].strip(), HEADERS)


# сделать ключ значение ключ тег td занчение тег dd
