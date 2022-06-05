# todo: Сделать рефакторинг кода задачи 35.
#  1. Реализовать из класса DB синглтон. Экземляр класса должен быть единственным.
#  2. Сделать класс View абстрактным, а также метод render() абстрактным
#  3. Реализовать  фабрику FabConsoleView в которой пораждаются экзепляры
#     классов TestView, QuestionView и AuthView
#  4. Задокументировать все классы и методы для дендера __doc__
#  5. Переписать Singlton на дандер __new__
#  6. Ограничить атрибуты для класса Person через __slots__


import psycopg
import bcrypt
from abc import ABC, abstractmethod  # для абстрактного View и виртуального render()
import datetime


# import time
# from threading import Thread

class Db:
    '''Класс Базы данных'''
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        '''Инициализация экземпляра Базы данных'''
        self.__conn = psycopg.connect(host="localhost", port=5432, dbname="db_psy", user="user_psycopg",
                                      password="1234")

    @staticmethod
    def get_instance():
        '''Получение уже созданного экземпляра Базы данных'''
        if not Db.instance:
            Db()
        return Db.instance

    def get_connect(self):
        '''Возвращает уже созданное соединение'''
        return self.__conn

    def get_profile(self, conn, login):
        '''Получение профиля пользователя из Базы данных'''
        cur = conn.cursor()
        cur.execute(f"SELECT * from student where login = '{login}';")
        obj = cur.fetchall()
        conn.commit()
        return obj

    @classmethod
    def set_stud_ans(self, q_ans_list, login, id_test):
        '''Занесение в БД ответов на вопросы'''
        cur = conn.cursor()
        cur.execute(f"select id_student from student where login = '{login}'")
        id_student = cur.fetchall()[0][0]
        valid_list = []
        for k, v in q_ans_list.items():
            cur.execute(f"select id_question from question where question_text = '{k}'")
            id_question = cur.fetchall()[0][0]
            cur.execute(f"select right_answer from question where id_question = {id_question}")
            right_ans = cur.fetchall()[0][0]
            valid = True if v.lower() == right_ans.lower() else False
            valid_list.append(valid)
            cur.execute(f"insert into result (id_student, id_question, id_test, student_answer, status) "
                        f"values ({id_student}, {id_question}, {id_test}, '{v}', {valid});")
            conn.commit()
        return valid_list

    @classmethod
    def set_stud_test(self, valid_list, id_test, login, dt_test, tm_test_duration):
        '''Занесение в БД информации о сдаче теста'''
        cur = conn.cursor()
        cur.execute(f"select id_student from student where login = '{login}'")
        id_student = cur.fetchall()[0][0]
        cur.execute(f"select test_pass_bar from test where id_test = '{id_test}'")
        test_pass_bar = cur.fetchall()[0][0]
        test_status = True if (valid_list.count(True) / len(valid_list)) * 100 >= test_pass_bar else False
        cur.execute(f"insert into student_test (id_student, id_test, dt_test, status, tm_test_duration) "
                    f"values ({id_student}, {id_test}, '{dt_test.strftime('%Y-%m-%d %H:%M:%S')}', {test_status}, "
                    f"'{tm_test_duration}');")
        conn.commit()
        match test_status:
            case True:
                print('Тест пройден')
            case False:
                print('Тест не пройден')


class Profile:
    '''Класс создания профиля пользователя'''
    __slots__ = ["id_group", "surname", "name", "patronity", "age", "login", "phone", "e_mail", "password"]

    def __init__(self, id_group, surname, name, patronity, age, login, phone, e_mail, password):
        self.id_group = id_group
        self.surname = surname
        self.name = name
        self.patronity = patronity
        self.age = age
        self.login = login
        self.phone = phone
        self.e_mail = e_mail
        self.password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))[2:-1]  # хэшированный пароль

    def set_profile(self, conn):
        '''Добавление профиля в Базу данных'''
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO student("id_group", "surname", "name", "patronity", "age", "login", "phone", 
                "e_mail", "password") VALUES ({self.id_group}, '{self.surname}', '{self.name}', '{self.patronity}', {self.age}, 
                '{self.login}', '+7{self.phone}', '{self.e_mail}', '{self.password}')''')
        conn.commit()

    def get_profile(self, conn):
        '''Извлечение профиля из Базы данных'''
        cur = conn.cursor()
        cur.execute(f"SELECT * from student where login = '{self.login}';")
        obj = cur.fetchall()
        conn.commit()
        return obj


'''
class Timer:                #попробовал сделать таймер, но последний вопрос "зависает"
    def __init__(self):     #в интернете пишут, что консольный input ничем прервать нельзя
        self.flag = True    # + не нашел способа остановить thread раньше, если на вопросы отвечают быстро

    def exp_timer(self):
        time.sleep(10)      #10 секунд стоит для тестирования кода. Сюда, возможно, будут грузиться данные БД
        self.flag = False   #из столбца теста
'''


class View(ABC):
    '''Абстрактный класс для отрисовки'''

    @abstractmethod
    def render(self):
        '''Абстрактный метод для отрисовки'''
        raise NotImplementedError("Необходимо перегрузить метод")


'''
class View:

    def render(self):
        pass
'''


class TestView(View):
    '''Класс отрисовки списка тестов'''

    def render(self, list_test):
        '''Метод для отрисовки списка тестов'''
        print("Выберите тему теста:")
        for i in range(len(list_test)):
            t_template = f"{i + 1} - {list_test[i]}"
            print(t_template)
        id_test = input("Поле для ввода номера теста: ")
        return id_test


class Question(View):
    '''Класс отрисовки вопроса'''

    def render(self, q_list):
        '''Метод для отрисовки вопроса, записи в БД ответов на вопросы и вывода статуса сдачи теста'''
        # timer = Timer()
        # th = Thread(target=timer.exp_timer, args=())
        # th.start() #при быстрых ответах приходится ждать окончание потока - как остановить раньше, пока не додумал
        q_ans_dict = {}
        for i in range(len(q_list)):
            q_template = f"{i + 1} - {q_list[i]}:"
            print(q_template)
            ans_list = FabConsoleView.get_view("answers_view").render(q_list[i])  # отрисовка через фабрику
            user_ans = input("Поле для ответа: ")
            q_ans_dict[q_list[i]] = ans_list[int(user_ans)-1]
            # if timer.flag == False: #проверяет значение таймера, но проблема с последним вопросом
            # print("Время вышло! Увы!")
            # break
        return q_ans_dict #возвращает словарь вопрос-ответ студента для обработки в функции Db.set_stud_ans


class Answers(View):
    '''Класс отрисовки ответов'''

    def render(self, question):
        '''Метод для отрисовки ответов'''
        ans_list = Test.get_answers(self, question)  # получаем список ответов
        for i in range(len(ans_list)):
            ans_template = f"{i + 1}: {ans_list[i]}"
            print(ans_template)
        return ans_list


class Log_in(View):
    '''Класс отрисовки логина и пароля'''

    def render(self):
        '''Метод для отрисовки логина и пароля'''
        login = "Введите логин: "
        pwd = "Введите пароль: "
        return [login, pwd]


class FabConsoleView:
    '''Класс фабрики классов отрисовки'''

    @classmethod  # метод будем брать без создания экземпляра класса
    def get_view(cls, view_type):
        '''Метод, возвращающий конкретный класс отрисовки'''
        match view_type:
            case "log_in_view":
                return Log_in()
            case "test_view":
                return TestView()
            case "question_view":
                return Question()
            case "answers_view":
                return Answers()


class Auth:
    '''Класс аутентификации пользователя'''

    def __init__(self, dbname, conn):
        '''Метод инициализации аутентификации к конкретной Базе данных'''
        self.dbname = dbname
        self.conn = conn
        self.is_auth = False

    def reg(self):
        '''Метод для регистрации пользователя'''
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
        new_user.set_profile(self.conn)  # заводим нового пользователя в БД
        print(f"Добро пожаловать {name} {surname}")
        self.is_auth = True
        return login

    def log_in(self):
        '''Метод ввода и проверки логина и пароля'''
        login = input(FabConsoleView.get_view("log_in_view").render()[0])  # отрисовка через фабрику
        pwd = input(FabConsoleView.get_view("log_in_view").render()[1])  # отрисовка через фабрику
        user = self.dbname.get_profile(self.conn, login)  # проверяем наличие профиля по логину
        if user:
            user_db_pwd = bytes(user[0][9], encoding="utf-8")  # если есть, то проверяем пароль
            valid = bcrypt.checkpw(pwd.encode(), user_db_pwd)
            if valid:
                print(f"Добро пожаловать {user[0][3]} {user[0][2]}!")  # приветствие
                self.is_auth = True
                return login
            else:
                print("Неверный пароль")  # тут, конечно, нужно просить повторить ввод пароля
        else:
            print("Нет такого пользователя")
            return Auth.reg(self)  # предлагаем зарегистрироваться

    def log_out(self):
        '''Метод для выхода из системы'''
        self.is_auth = False


class Test:
    '''Класс теста'''

    def __init__(self, dbname, conn):
        '''Метод инициализации конкретного теста из Базы данных'''
        self.dbname = dbname
        self.conn = conn

    def get_list_tests(self):
        '''Метод возвращает список тестов'''
        cur = conn.cursor()
        cur.execute(f"SELECT theme from test;")
        t_list = list(sum(cur.fetchall(), ()))
        conn.commit()
        t_render = FabConsoleView.get_view("test_view").render(t_list)  # отрисовка через фабрику
        return t_render

    def get_questions(self, id_test):
        '''Метод возвращает список вопросов и отрисовывает их'''
        cur = conn.cursor()
        cur.execute(f"select t.theme,  tq.id, q.question_text "  # джойны БД по выбранному тесту
                    f"from test t, test_question tq, question q "
                    f"where t.id_test = tq.id_test and q.id_question = tq.id_question and t.id_test = {id_test}")
        res = list(sum(cur.fetchall(), ()))
        conn.commit()
        q_list = []  # отбираем только вопросы из джойнов БД (излишне, но писалось под другую бизнес-логику)
        for i in range(2, len(res) + 1, 3):
            q_list.append(res[i])
        q_ans_dict = FabConsoleView.get_view("question_view").render(q_list)  # отрисовка через фабрику
        return q_ans_dict

    def get_answers(self, question):
        '''Метод возвращает список ответов'''
        cur = conn.cursor()
        cur.execute(f"SELECT id_question from question where question_text = '{question}';")
        id_question = list(sum(cur.fetchall(), ()))[0]
        cur.execute(f"SELECT answer_text from answers where id_question = {id_question};")
        ans_list = list(sum(cur.fetchall(), ()))
        return ans_list  # возвращаем список ответов


class TestSystem:
    '''Класс ядра системы с бизнес-логикой'''

    def __init__(self, dbname, conn):
        '''Метод инициализации системы'''
        self.dbname = dbname
        self.conn = conn

    def run(self):
        '''Метод запуска системы'''
        user = Auth(connection, conn)
        login = user.log_in()
        user.__dict__["login"] = login  #добавляем в атрибуты текущего экземпляра класса логин
        if user.is_auth:  # проверяем аутентификацию пользователя
            test = Test(self.dbname, self.conn)
            id_test = test.get_list_tests()
            start_time = datetime.datetime.now()        #начало выполнения теста
            q_ans_dict = test.get_questions(id_test)    #сам тест
            finish_time = datetime.datetime.now()       #окончание выполнения теста
            test_duration = finish_time - start_time    #продолжительность выполнения теста
            valid_list = Db.set_stud_ans(q_ans_dict, user.login, id_test) #заносим ответы студента в БД
            Db.set_stud_test(valid_list, id_test, user.login, finish_time, test_duration) #заносим в БД статус выполнения теста


connection = Db()  # создание единственного экземпляра класса
conn = connection.get_connect()  # создание единственного соединения

test_system = TestSystem(connection, conn)
test_system.run()

# your_db = Db() #выдаст ошибку "Нельзя создать второй экземпляр"
# my_db = Db.get_instance()  # использует уже созданный экземпляр БД
# my_db_con = my_db.get_connect()  # соответственно, то же соединение, что было установлено у уже созданного экземпляра БД
# test_system = TestSystem(my_db, my_db_con) #проверка работы singleton'а
# test_system.run() #проверка работы singleton'а

# проверка __slots__
# user = Profile(1, "pushkov", "ivan", "ivanovich", 23, "pushkov", "+79119112222", "pushkov@mail.ru", "1234")
# user.country = "Russia" #еще один атрибут не добавляется


'''
#проверка получения инфо из БД по пройденным тестам конкретным студентом
login = "kashaev"
cur = conn.cursor()
#джойны из трех таблиц test (получение темы теста), student (получение ФИО студента) 
#и student_test (получение статуса сдачи теста)
cur.execute(f"select t.theme,  s.surname, s.name, s.patronity,  st.status "
            f"from test t, student s, student_test st "
            f"where t.id_test = st.id_test and st.id_student = s.id_student and s.login = '{login}'")
info = cur.fetchall()
for i in range(len(info)):
    print(f"Тест на тему '{info[i][0]}' студент {info[i][1]} {info[i][2]} {info[i][3]} "
          f"{'сдал' if info[i][4] == True else 'не сдал'}")
'''