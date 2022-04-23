#todo: Изучаем пакет pandas
#
# После установки библиотеки pandas выполните следующие действия:
#
# Изучите справку по модулю (для чего нужен модуль , какие возможности предоставляет)
# Найдите расположение директории модуля pandas и изучите его содержимое
# Получите список доступных атрибутов модуля pandas
# Импортируйте модуль pandas в исполняемый скрипт
# С помощью модуля pandas ознакомьтесь со структурой  DataFrame, фильтрации данных,
# загрузки данных из формата сsv (рассмотрите примеры статьи)
# Установите библиотеку matplotlib, создайте график на своем наборе данных.

#Опорная статья:  https://egorovegor.ru/pandas-obrabotka-i-analiz-dannyh-v-python/

import pandas as pd
import matplotlib.pyplot as plt

area = pd.Series({"California": 423967, "Texas": 695662, "New York": 141297, "Florida": 170312, "Illinois": 149995})
pop = pd.Series({"California": 38332521, "Texas": 26448193, "New York": 19651127,
                 "Florida": 19552860, "Illinois": 12882135})

data = pd.DataFrame({"area": area, "pop": pop})

print(data)
print(f"\n{data['area']}") #фильтрация по столбцу "area"
print(f"\n{data[1:3]}") #фильтрация по строкам - 2 и 3 строки

data.to_csv("states_data.csv")
data_2 = pd.read_csv("states_data.csv")

data_2.index = pd.Series([1, 2, 3, 4, 5])
data_2 = data_2.rename(columns={"Unnamed: 0" : "state"})
print(f"\n{data_2}")

#data_2.plot(kind="barh", y="area", x="state", color="blue") вывод диаграммы по площадям
data_2.pivot(columns="state").plot(kind="bar") #вывод диаграммы и по площади, и по населению
plt.show()
