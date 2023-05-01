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

lists = list(_json.values())
n = 7

template = Template('''
{% set number = 0 %}


<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="jinjastyle.css" type="text/css"/>
  <title>Словарь</title>
</head>
<body>
  <table>
    <tr>
      <th>Заголовок 1 </th>
      <th>Заголовок 2 </th>
      <th>Заголовок 3 </th>
      <th>Заголовок 4 </th>     
    </tr>
    {% for value in range( 0, my_dict | length, 4) %}
    <tr>
        {% for tex in range( 0, 4, 1 ) -%}
        {% set number = tex + value %}
            {%- if my_dict | length > number -%}
                <td> <img class="picmarginauto" src=" {{ my_dict[number]['link_src_img'] }}">
                <div class="textmarginauto"> {{ my_dict[number]['title'] }} </div>
                </td>
            {% endif %}
        {%- endfor -%}
    </tr>
    {%- endfor -%}
  </table>
</body>
</html>
''')

# html = template.render(my_dict=_json)
html = template.render(my_dict=lists, cnt=n)
print(html)

with open("dsa.html", "w", encoding='utf-8') as d:
    d.write(html)
