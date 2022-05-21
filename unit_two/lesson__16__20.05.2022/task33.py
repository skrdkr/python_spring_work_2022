#todo: Написать авторизацию пользователя в систему.
#Приложение в начале должно предлагать меню
'''
1. Вход
2. Регистрация

1. При выборе пункта "Вход" пользователю необходимо ввести
логин и пароль, поэтапно.
login: _________
password: ________
При вводе данных авторизации, система проверяет есть ли данный
пользователь в БД (логин) если нет то предлагает зарегистрироваться.
Если есть и пароли совпадают, то происходит вход в систему. Пользователю показывается
приглашение вида "Добро пожаловать Вася Пупкин!" и выпадает меню
выбора билетов для тестирования(пока заглушка).

2. При выборе "Регистрация" пользователю необходимо ввести новый
логин, пароль, фио, почту, телефон, группу. После система заводит
запись в БД если пользователя под данным логином нет. Если такой пользователь
уже существует то программа выдает об этом сообщение. Пароль необходимо хранить в БД
в виде хеша + соль.

По хешированию прочитать статью
https://pythonist.ru/heshirovanie-parolej-v-python-tutorial-po-bcrypt-s-primerami/
для хеширования пароля воспользоваться библиотекой bcrypt
'''

import psycopg
import bcrypt

def app_start(): #запуск приложения
    greeting_text = "1. Вход\n" \
                    "2. Регистрация\n" \
                    "Поле для ввода опции: "
    greeting = input(f"{greeting_text}")
    return greeting

def on_or_reg(info_app_start): #действия после ввода значения при запуске приложения
    match info_app_start:
        case "1":
            _in() #вход в систему
        case "2":
            insert_user(reg()) #регистрация и внесение данных в БД

def input_login(user_list): #ввод логина и его проверка на наличие в БД
    login = input("Введите логин: ")
    if login in user_list:
        print("Такой пользователь уже существует, придумайте другой логин")
        return input_login(user_list) #на второй круг
    else:
        return login

def reg(): #ввод данных нового студента (порядок ввода не совсем правильный, но так в БД забил, к сожалению)
    print("Зарегиструйтесь, пожалуйста")
    id_group = int(input("Введите номер группы: "))
    surname = input("Введите фамилию: ")
    name = input("Введите имя: ")
    patronity = input("Введите отчетсво: ")
    age = int(input("Введите возраст: "))
    login = input_login(user_list())
    phone = int(input("Введите телефон c 8: "))
    e_mail = input("Введите e-mail: ")
    pwd_input = input("Введите пароль: ")
    pwd_hash = str(bcrypt.hashpw(pwd_input.encode('utf-8'), bcrypt.gensalt()))[2:-1] #БД не хочет забирать тип byte
    user_info = [id_group, surname, name, patronity, age, login, phone, e_mail, pwd_hash]
    return user_info

def user_list(): #получаем список имеющихся логинов из БД
    with psycopg.connect("dbname=db_psy user=user_psycopg password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT login FROM student;""")
            return list(sum(cur.fetchall(), ())) #вместо списка кортежей от cur.fetchall() получаем список логинов

def pass_get(login): #получаем пароль из БД по логину
    with psycopg.connect("dbname=db_psy user=user_psycopg password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute(f"""SELECT password FROM student WHERE login = '{login}';""")
            return list(sum(cur.fetchall(), ()))[0]

def name_surname(login): #получаем имя и фамилию из БД для приветствия при входе
    with psycopg.connect("dbname=db_psy user=user_psycopg password=1234") as conn:
        with conn.cursor() as cur:
            cur.execute(f"""SELECT name, surname FROM student WHERE login = '{login}';""")
            return list(sum(cur.fetchall(), ()))

def _in(): #вход в систему
    login = input("Введите логин: ")
    user_lst = user_list()
    if login in user_lst:
        res = input("Введите пароль: ")
        valid = bcrypt.checkpw(res.encode(), bytes(pass_get(login), encoding="utf-8")) #проверка введенного пароля
        if valid:
            n_s = name_surname(login)
            return print(f"Добро пожаловать {n_s[0]} {n_s[1]}!"), test_menu()
        else:
            return print("Неправильный пароль\n"), _in()
    else:
        insert_user(reg())


def test_menu(): #получение списка тестов, возвращает сделанный выбор
    chosen_test = input("Выберите тест:\n"
                        "1 - Примитивные типы\n"
                        "2 - Коллекции\n"
                        "3 - Функции\n"
                        "Поле для ввода: ")
    pass

def insert_user(_list): #вносим данные студента в БД и приветствуем
    with psycopg.connect("dbname=db_psy user=user_psycopg password=1234") as conn:
        with conn.cursor() as cur:
            #можно сделать через for, забрав из БД списки столбцов и расфасовав по ним _list
            cur.execute(f"""
                        INSERT INTO student (id_group, surname, name, patronity, age, login, phone, e_mail, password)
                        values ('{_list[0]}', '{_list[1]}', '{_list[2]}', '{_list[3]}', '{_list[4]}', '{_list[5]}', 
                        '{_list[6]}', '{_list[7]}', '{_list[8]}');
                        """)
            print(f"Добро пожаловать {_list[2]} {_list[1]}!")
            return test_menu()

on_or_reg(app_start()) #запуск
