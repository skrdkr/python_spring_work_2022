#todo: Задан словарь, его значения необходимо внести по соответвющим тегам и атрибутам вместо вопросов (?)
# заполненный шаблон записать в файл index.html

page = {"title": "Тег BODY",
        "charset": "utf-8",
        "alert": "Документ загружен",
        "p": "Ut wisis enim ad minim veniam,  suscipit lobortis nisl ut aliquip ex ea commodo consequat."}


template = """ 
<!DOCTYPE HTML>
<html>
 <head>
  <title>?</title>
  <meta charset=?>
 </head>
 <body onload="alert(?)">
 
  <p>?</p>

 </body>
</html>
"""

list_temp = template.split(' ')

for key in page.keys():
    for i in range(len(list_temp)-1):
        if key in list_temp[i]:
            list_temp[i] = list_temp[i].replace("?", page[key])

template = ' '.join(list_temp)

f = open("index.html", "w", encoding="utf-8")
f.writelines(template)
f.close()
