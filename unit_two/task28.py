#todo: Реализовать декоратор в котором нужно подсчитать кол-во вызовов декорированной функции в процессе выполнения кода.
# Выгрузить статистику подсчета в файл debug.log в формате: Название функции, кол-во вызовов, дата-время последнего выполнения
'''
Пример:
render, 10,  12.05.2022 12:00
show,    5,  12.05.2022 12:02
render, 15,  12.05.2022 12:07

Декоратор должен применяться для различных функций с переменным числом аргументов.
Статистику вызовов необходимо записывать в файл при каждом запуске скрипта.
'''

#из задания и примера не совсем ясно, что должно быть в debug.log - одна строчка с информацией
#о вызванной функции, или один декоратор должен, принимая разные функции, записывать разную информацию в один файл
#в отдельные строчки, идущие друг за другом. Первый вариант я реализовал ниже, второй, к сожалению, не получается,
#так как декоратор постоянно перезаписывает информацию в файле, и не совсем понятно, как один декоратор может
#записывать в отдельные строчки одного файла разную информацию о разных функциях


from datetime import datetime

def debug_log(func):
    counter = {f'{func.__name__}': [0, '0']}
    def wrapper(*args, **kwargs):
        launch_time = datetime.now()
        launch_time = launch_time.strftime("%d.%m.%Y %H:%M")
        counter[f'{func.__name__}'][0] += 1
        counter[f'{func.__name__}'][1] = launch_time
        with open("debug.log", "w") as f: #если вместо "w" будет "a", декоратор будет записывать каждый вызов функции
            f.write(f"{func.__name__}, {counter[f'{func.__name__}'][0]}, {counter[f'{func.__name__}'][1]}\n")
        return func(*args, **kwargs)
    return wrapper

@debug_log
def text_upper(text):
    return print(text.upper())

@debug_log
def concat_text(str_1, str_2):
    return print(f"{str_1} is {str_2}")


text_upper("python")
text_upper("ruby")
text_upper("javascript")
text_upper("java")

#concat_text("Python", "fun") #вариант функции с двумя аргументами, но декоратор перезапишет содержимое debug.log
#concat_text("Python", "...")
#concat_text("Python", "not fun")



