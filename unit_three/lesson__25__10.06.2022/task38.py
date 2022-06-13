# todo: Реализовать две сопрограммы. Первая с заданной периодичность(раз в 2,3 сек) пишет в файл и выводит результат.
# другая делает запрос к БД на выборку  билета и отображает поочередно  название билета (раз в 2,3 сек)


'''
# Bonus:
В качестве бонуса можно реализовать Telegtram - бота который в виде викторины задает
вопросы. Вопросы можно взять из тестовой системы. После вывода бот принимает вариант ответа.
В конце викторины выводит кол-во правильных и неправильных ответов и приз в случае успеха.
В качестве библиотеки можно взять  библиотеку telebot. Описание по разработки и примеры найти
в многочисленных статьях в Internet.
'''


import random                   #для случайного выбора темы теста
import asyncio                  #асинхронное выполнение
from aiofile import async_open  #асинхронная работа с файлами
import asyncpg                  #асинхронная работа с postgrisql
import datetime                 #для трекинга выполнения корутин без слипов на 2,3 секунды


class Test:
    '''Класс теста'''

    @classmethod
    async def get_list_tests(cls):
        '''Метод возвращает список тестов'''
        count = 0 #чтобы избежать бесконечного цикла
        while count <= 5:
            print(f"Вход в БД {datetime.datetime.now()}") #фиксируем время начала подключения к БД
            con = await asyncpg.connect(host="localhost", port=5432, user="user_psycopg", database="db_psy",
                                          password="1234")
            print(f"Запрос данных из БД {datetime.datetime.now()}")     #фиксируем время начала подключения к БД
            async with con.transaction():
                cur = await con.fetch('SELECT theme from test;')        #возвращает экземпляры объекта asyncpg.Record
                theme_lists = [dict(cur[i]) for i in range(len(cur))]   #преобразуем экземпляры asyncpg.Record в словари
                val_list = [[v for v in theme_lists[i].values()] for i in range(len(theme_lists))] #извлекаем темы тестов
                print(random.choice(val_list)[0]) #рандомно выбираем тему
            count += 1
            await asyncio.sleep(2)


async def logger():
    count = 0
    while count <= 5:
        text_1 = "Привет\n"
        print(f"Открытие файла на запись {datetime.datetime.now()}")    #фиксируем время начала открытия файла
        async with async_open("logger.log", "a+", encoding="utf-8") as f:
            print(f"Запись 'Привет' {datetime.datetime.now()}")         #фиксируем время начала записи в файл
            await f.write(text_1)
        await asyncio.sleep(3)
        count += 1


async def main():
    await asyncio.gather(logger(), Test.get_list_tests()) #объединяем корутины. Без слипов сначала будет открытие файла на запись,
                                                        #потом (пока открывается файл) будет подключение к БД, потом
asyncio.run(main())                                     #(пока подключается БД) запись в файл, в конце запрос данных из БД



