# -*- coding: utf8 -*-

# подключили библиотеку для работы с json
import json
# подключили Pprint для красоты выдачи текста
from pprint import pprint
from jinja2 import Template

_json = dict()
with open(r"C:\project_python\ParserAmimegoOrg\anime_json.json", "r", encoding='utf-8') as file:
    _json = json.load(file)

for key, value in _json.items():
    print(key, value['title'])
template = Template('''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Словарь</title>
</head>
<body>
  <h1>Словарь</h1>
  <ul>
    {% for key, value in my_dict.items() -%}
      <li><a href="{{ value.link_src_img }}"> <img src="{{value.link_src_img}}" width="189" height="255" alt="lorem"> {{ value.title }}:   </a> </li>
    {% endfor %}
  </ul>
</body>
</html>
''')


html = template.render(my_dict=_json)
print(html)

with open("dsa.html", "w", encoding='utf-8') as d:
    d.write(html)





