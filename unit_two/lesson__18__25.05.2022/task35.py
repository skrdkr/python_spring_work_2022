
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


class Auth:
    def __init__(self, login, password, dbname, conn):
        self.login = login
        self.password = password
        self.dbname = dbname
        self.conn = conn
        self.is_auth = False

    def reg(self): #регистрация
        print("Зарегистрируйтесь, пожалуйста!")
        id_group = int(input("Введите номер группы: "))
        surname = input("Введите фамилию: ")
        name = input("Введите имя: ")
        patronity = input("Введите отчетсво: ")
        age = int(input("Введите возраст: "))
        login = input("Введите логин: ")
        phone = int(input("Введите телефон без +7: "))
        e_mail = input("Введите e-mail: ")
        pwd_input = input("Введите пароль: ")
        pwd_hash = str(bcrypt.hashpw(pwd_input.encode('utf-8'), bcrypt.gensalt()))[2:-1]
        new_user = Profile(id_group, surname, name, patronity, age, login, phone, e_mail, pwd_hash)
        new_user.set_profile(self.conn)             #заводим нового пользователя в БД
        print(f"Добро пожаловать {name} {surname}")
        self.is_auth = True

    def log_in(self): #вход в тестовую систему
        user = self.dbname.get_profile(self.conn, self.login)           #проверяем наличие профиля по логину
        if user:
            user_db_pwd = bytes(user[0][9], encoding="utf-8")           #если есть, то проверяем пароль
            valid = bcrypt.checkpw(self.password.encode(), user_db_pwd)
            if valid:
                print(f"Добро пожаловать {user[0][3]} {user[0][2]}!")   #приветствие
                self.is_auth = True
            else:
                print("Неверный пароль")        #тут, конечно, нужно просить повторить ввод пароля
        else:
            print("Нет такого пользователя")
            return Auth.reg(self)               #предлагаем зарегистрироваться

    def log_out(self):  #выход из системы
        self.is_auth = False


class Test:
    def __init__(self, dbname, conn):
        self.dbname = dbname
        self.conn = conn

    def get_list_tests(self): #получаем список тестов по темам
        cur = conn.cursor()
        cur.execute(f"SELECT theme from test;")
        t_list = list(sum(cur.fetchall(), ()))
        conn.commit()
        print("Список тестовых тем:")
        for i in range(len(t_list)):
            print(f"{i+1}. {t_list[i]}")
        id_test = int(input("Поле выбора теста: "))
        return id_test

    def get_questions(self, id_test):       #получаем список вопросов по тесту на выбранную тему
        cur = conn.cursor()
        cur.execute(f"select t.theme,  tq.id, q.question_text " #джойны БД по выбранному тесту
                    f"from test t, test_question tq, question q "
                    f"where t.id_test = tq.id_test and q.id_question = tq.id_question and t.id_test = {id_test}")
        res = list(sum(cur.fetchall(), ()))
        conn.commit()
        q_list = []                         #отбираем только вопросы из джойнов БД
        for i in range(2, len(res)+1, 3):
            q_list.append(res[i])
        print("Список вопросов:")
        for i in range(len(q_list)):        #выводим список вопросов
            print(f"{i+1}. {q_list[i]}")


class TestSystem:
    def __init__(self, dbname, conn, user):
        self.dbname = dbname
        self.conn = conn
        self.user = user

    def run_test(self):                         #запускам приложение
        if user.is_auth == True:                #проверяем аутентификацию пользователя
            test = Test(self.dbname, self.conn)
            id_test = test.get_list_tests()
            test.get_questions(id_test)


connection = Db("db_psy", "user_psycopg", "1234")
conn = connection.get_connect()

login = input("Введите логин: ") #имитация полей ввода приложения
password = input("Введите пароль: ")

user = Auth(login, password, connection, conn) #аутентификация пользователя. Это часть, скорее всего, тоже нужно
user.log_in()                                   #засунуть в TestSystem, но времени не хватило это обдумать

test_system = TestSystem(connection, conn, user)
test_system.run_test()



