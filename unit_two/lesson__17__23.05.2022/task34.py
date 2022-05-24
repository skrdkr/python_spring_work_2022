#todo: Реализовать классы DB и Profile

import psycopg
import bcrypt

class Db:
    '''Данный класс содержит конструктор и метод get_connect. В конструкторе инициализируются переменные
     (атрибуты доступа к БД) . Метод возвращает соединение.'''

    # В констукторе инициализируем атрибуты доступа к БД
    def __init__(self, name, user, password):
        self.name = name
        self.user = user
        self.password = password

    # Метод возвращает соединение к БД
    def get_connect(self):
        connect = psycopg.connect(host="localhost", port=5432, dbname=self.name, user=self.user, password=self.password)
        return connect

    # метод возвращает профиль по логину
    def get_profile(self, conn, login):
        cur = conn.cursor()
        cur.execute(f"SELECT * from student where login = '{login}';")
        obj = cur.fetchall()
        conn.commit()
        return obj


class Profile:
    ''' Данный класс содержит конструктор и метод set_profile и get_profile для добавления и получения
     пользователя соответсвенно'''
    # В констукторе инициализируем атрибуты сущности Profile
    def __init__(self, id_group, surname, name, patronity, age, login, phone, e_mail, password):
        self.id_group = id_group
        self.surname = surname
        self.name = name
        self.patronity = patronity
        self.age = age
        self.login = login
        self.phone = phone
        self.e_mail = e_mail
        self.password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))[2:-1] #хэшированный пароль

    # в аргументе conn передается дискриптор подключения к БД
    def set_profile(self, conn):
        # Добавляет профиль в БД
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO student("id_group", "surname", "name", "patronity", "age", "login", "phone", 
                "e_mail", "password") VALUES ({self.id_group}, '{self.surname}', '{self.name}', '{self.patronity}', {self.age}, 
                '{self.login}', '+7{self.phone}', '{self.e_mail}', '{self.password}')''')
        conn.commit()

    def get_profile(self, conn):
        # Извлекает профиль из БД
        cur = conn.cursor()
        cur.execute(f"SELECT * from student where login = '{self.login}';")
        obj = cur.fetchall()
        conn.commit()
        return obj


connection = Db("db_psy", "user_psycopg", "1234")

conn = connection.get_connect()

print(connection.get_profile(conn, "sidorov"))

new_student = Profile(1, 'Петров', 'Петр', 'Петрович', 25, 'petrov', 9119112222, 'petrov@mail.ru', '1234')

new_student.set_profile(conn)

print(new_student.get_profile(conn))

