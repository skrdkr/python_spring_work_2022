
import psycopg
import bcrypt
import time
from threading import Thread

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


class View:
    def render(self):
        pass

class Timer:                #попробовал сделать таймер, но последний вопрос "зависает"
    def __init__(self):     #в интернете пишут, что консольный input ничем прервать нельзя
        self.flag = True    # + не нашел способа остановить thread раньше, если на вопросы отвечают быстро

    def exp_timer(self):
        time.sleep(10)      #10 секунд стоит для тестирования кода. Сюда, возможно, будут грузиться данные БД
        self.flag = False   #из столбца теста


class TestView(View):
    def render(self, list_test):
        print("Выберите тему теста:")
        for i in range(len(list_test)):
            t_template = f"{i+1} - {list_test[i]}"
            print(t_template)
        id_test = input("Поле для ввода номера теста: ")
        return id_test


class Question(View):
    def render(self, q_list):
        timer = Timer()
        th = Thread(target=timer.exp_timer, args=())
        th.start() #при быстрых ответах приходится ждать окончание потока - как остановить раньше, пока не додумал
        for i in range(len(q_list)):
            q_template = f"{i+1} - {q_list[i]}:"
            print(q_template)
            Answers.render(self, q_list[i])
            user_ans = input("Поле для ответа: ") #будет использовано для внесения в БД
            if timer.flag == False: #проверяет значение таймера, но проблема с последним вопросом
                print("Время вышло! Увы!")
                break


class Answers(View):
    def render(self, question):
        ans_list = Test.get_answers(self, question) #получаем список ответов
        for i in range(len(ans_list)):
            ans_template = f"{i+1}: {ans_list[i]}"
            print(ans_template)

class Log_in(View):
    def render(self):
        login = "Введите логин: "
        pwd = "Введите пароль: "
        return [login, pwd]


class Auth:
    def __init__(self, dbname, conn):
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
        new_user = Profile(id_group, surname, name, patronity, age, login, phone, e_mail, pwd_input)
        new_user.set_profile(self.conn)             #заводим нового пользователя в БД
        print(f"Добро пожаловать {name} {surname}")
        self.is_auth = True

    def log_in(self): #вход в тестовую систему
        login = input(Log_in.render(self)[0])
        pwd = input(Log_in.render(self)[1])
        user = self.dbname.get_profile(self.conn, login)           #проверяем наличие профиля по логину
        if user:
            user_db_pwd = bytes(user[0][9], encoding="utf-8")           #если есть, то проверяем пароль
            valid = bcrypt.checkpw(pwd.encode(), user_db_pwd)
            #valid = True if pwd == user[0][9] else False
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
        t_render = TestView.render(self, t_list)
        return t_render

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
        Question.render(self, q_list)

    def get_answers(self, question): #получаем список ответов
        cur = conn.cursor()
        cur.execute(f"SELECT id_question from question where question_text = '{question}';")
        id_question = list(sum(cur.fetchall(), ()))[0]
        cur.execute(f"SELECT answer_text from answers where id_question = {id_question};")
        ans_list = list(sum(cur.fetchall(), ()))
        return ans_list #возвращаем список ответов


class TestSystem:
    def __init__(self, dbname, conn):
        self.dbname = dbname
        self.conn = conn

    def run(self):                         #запускам приложение
        user = Auth(connection, conn)
        user.log_in()
        if user.is_auth:                #проверяем аутентификацию пользователя
            test = Test(self.dbname, self.conn)
            id_test = test.get_list_tests()
            test.get_questions(id_test)


connection = Db("db_psy", "user_psycopg", "1234")
conn = connection.get_connect()

test_system = TestSystem(connection, conn)
test_system.run()




