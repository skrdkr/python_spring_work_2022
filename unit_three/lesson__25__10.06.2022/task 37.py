#TOKEN = '5402077477:AAEKjFYD9KEobhbkPBXTeRZt5cwruVny8-k'

import telebot
import psycopg
import bcrypt
from abc import ABC, abstractmethod
import datetime

class Db:
    '''Класс Базы данных'''
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        '''Инициализация экземпляра Базы данных'''
        self.conn = psycopg.connect(host="localhost", port=5432, dbname="db_psy", user="user_psycopg",
                                      password="1234")
        self.cur = self.conn.cursor()

    @staticmethod
    def get_instance():
        '''Получение уже созданного экземпляра Базы данных'''
        if not Db.instance:
            Db()
        return Db.instance

    def get_connect(self):
        '''Возвращает уже созданное соединение'''
        return self.conn

    def get_profile(self, login):
        '''Получение профиля пользователя из Базы данных'''
        self.cur.execute(f"SELECT * from student where login = '{login}';")
        user = self.cur.fetchall()
        return user

    def set_profile(self, message):
        '''Добавление профиля в Базу данных'''
        user_info = message.text
        user_info_list = user_info.split(',')
        pwd = str(bcrypt.hashpw(user_info_list[8].encode('utf-8'), bcrypt.gensalt()))[2:-1]
        self.cur.execute(f'''INSERT INTO student("id_group", "surname", "name", "patronity", "age", "login", "phone", 
                "e_mail", "password", "id_telegram_user") VALUES ({int(user_info_list[0])}, '{user_info_list[1]}', '{user_info_list[2]}', 
                '{user_info_list[3]}', {int(user_info_list[4])}, '{user_info_list[5]}', '+7{user_info_list[6]}', 
                '{user_info_list[7]}', '{pwd}', {message.from_user.id})''')
        self.conn.commit()
        bot.send_message(message.chat.id, f"Добро пожаловать, {user_info_list[2]}")
        bot.send_message(message.chat.id, f"Для начала тестирования введите /test")


class Auth:
    '''Класс аутентификации пользователя'''

    def __init__(self, dbname):
        '''Метод инициализации аутентификации к конкретной Базе данных'''
        self.dbname = dbname
        self.is_auth = False

    def reg(self, message):
        '''Метод для регистрации пользователя'''
        bot.send_message(message.chat.id, "Зарегистрируйтесь, пожалуйста!")
        user_info = bot.send_message(message.chat.id, "Введите через запятую (без пробелов) номер группы, фамилию, имя, "
                                                      "отчество, возраст, логин, номер телефона (без +7 или 8), "
                                                      "e-mail, пароль")
        bot.register_next_step_handler(user_info, self.dbname.set_profile)
        self.is_auth = True

    def log_in(self, message):
        '''Метод ввода и проверки логина и пароля'''    #для телеграмма можно было бы проверять по id_user
        lg_pwd = message.text
        login = lg_pwd.split(',')[0]
        pwd = lg_pwd.split(',')[1]
        user = self.dbname.get_profile(login)  # проверяем наличие профиля по логину
        if user:
            user_db_pwd = bytes(user[0][9], encoding="utf-8")  # если есть, то проверяем пароль
            valid = bcrypt.checkpw(pwd.encode(), user_db_pwd)
            if valid:
                bot.send_message(message.chat.id, f"С возвращением, {user[0][3]}!")  # приветствие
                self.is_auth = True
                bot.send_message(message.chat.id, f"Для начала тестирования введите /test")
                #не понимаю, почему код ниже здесь не работает - в конце работает правильно. Должен же триггериться по команде
                #result = bot.send_message(message.chat.id, f"Если хотите посмотреть историю сдачи тестов, "
                                                           #f"то введите /result")
                #bot.register_next_step_handler(result, result_info)
            else:
                bot.send_message(message.chat.id, f"Неверный пароль!")  # тут, конечно, нужно просить повторить ввод пароля
        else:
            bot.send_message(message.chat.id, f"Нет такого пользователя!")
            return Auth.reg(self, message)  # предлагаем зарегистрироваться


class View(ABC):
    '''Абстрактный класс для отрисовки'''

    @abstractmethod
    def render(self):
        '''Абстрактный метод для отрисовки'''
        raise NotImplementedError("Необходимо перегрузить метод")


class FabConsoleView:
    '''Класс фабрики классов отрисовки'''

    @classmethod  # метод будем брать без создания экземпляра класса
    def get_view(cls, view_type):
        '''Метод, возвращающий конкретный класс отрисовки'''
        match view_type:
            case "test_view":
                return TestView()


class TestView(View):
    '''Класс отрисовки списка тестов'''

    def render(self, list_test, message):
        '''Метод для отрисовки списка тестов'''
        msg = 'Темы тестов\n'
        for i in range(len(list_test)):
            msg += f"{i + 1} - {list_test[i]}\n"
        bot.send_message(message.chat.id, msg)


class Test:
    '''Класс теста'''
    def __init__(self, dbname):
        '''Метод инициализации конкретного теста из Базы данных'''
        self.dbname = dbname

    def get_list_tests(self, message):
        '''Метод возвращает список тестов'''
        self.dbname.cur.execute(f"SELECT theme from test;")
        t_list = list(sum(self.dbname.cur.fetchall(), ()))
        t_render = FabConsoleView.get_view("test_view").render(t_list, message)  # отрисовка через фабрику
        return t_render

    def get_questions(self, id_test):
        '''Метод возвращает список вопросов и отрисовывает их'''
        self.dbname.cur.execute(f"select t.theme,  tq.id, q.question_text "  # джойны БД по выбранному тесту
                    f"from test t, test_question tq, question q "
                    f"where t.id_test = tq.id_test and q.id_question = tq.id_question and t.id_test = {id_test}")
        res = list(sum(self.dbname.cur.fetchall(), ()))
        q_list = []  # отбираем только вопросы из джойнов БД (излишне, но писалось под другую бизнес-логику)
        for i in range(2, len(res) + 1, 3):
            q_list.append(res[i])
        return q_list

    def get_answers(self, q_list):
        '''Метод возвращает список ответов'''
        q_ans_msg = ""
        for i in range(len(q_list)):
            q_ans_msg += f"\n{q_list[i]}:\n"
            self.dbname.cur.execute(f"SELECT id_question from question where question_text = '{q_list[i]}';")
            id_question = list(sum(self.dbname.cur.fetchall(), ()))[0]
            self.dbname.cur.execute(f"SELECT answer_text from answers where id_question = {id_question};")
            ans_list = list(sum(self.dbname.cur.fetchall(), ()))
            for i in range(len(ans_list)):
                q_ans_msg += f"{i+1}: {ans_list[i]}\n"
        return q_ans_msg  # возвращаем список ответов

db_worker = Db()
test = Test(db_worker)
id_test = 0 #ввел глобальные переменные, так как лучше способа не нашел
id_student = 0
dt_test = datetime.datetime.now()

bot = telebot.TeleBot('5402077477:AAEKjFYD9KEobhbkPBXTeRZt5cwruVny8-k')

@bot.message_handler(commands=['start'], content_types=['text'])
def auth_user(message):
    global db_worker
    user = Auth(db_worker)
    msg = bot.send_message(message.chat.id, "Добрый день! Для прохождения теста введи логин и пароль в формате 'логин,пароль'")
    bot.register_next_step_handler(msg, user.log_in) #аутентификация пользователя

@bot.message_handler(commands=['test'], content_types=['text'])
def test_list(message):
    global db_worker
    global test
    global dt_test
    dt_test = datetime.datetime.now()
    test.get_list_tests(message)
    id_test = bot.send_message(message.chat.id, "Введите номер теста")
    bot.register_next_step_handler(id_test, question) #с номером теста переходим в следующую функцию

@bot.message_handler(content_types=['text'])
def question(message):
    global db_worker
    global test
    global id_test
    global id_student
    id_test = message.text
    db_worker.cur.execute(f"select id_student from student where id_telegram_user = {message.from_user.id}")
    id_student = list(sum(db_worker.cur.fetchall(), ()))[0]
    q_list = test.get_questions(id_test)
    q_ans_msg = test.get_answers(q_list)
    bot.send_message(message.chat.id, q_ans_msg)
    student_answers = bot.send_message(message.chat.id, "Введите ответы на вопросы через запятую")
    bot.register_next_step_handler(student_answers, set_result) #с ответами пользователя переходим в следующую функцию


@bot.message_handler(content_types=['text'])
def set_result(message): #ужасный код ниже - надо разбивать, но не нашел способа, как сделать лучше
    global db_worker
    global id_test
    global id_student
    global dt_test
    finish_time = datetime.datetime.now()
    tm_test_duration = finish_time - dt_test
    stud_ans = message.text
    stud_ans_list = stud_ans.split(",")
    db_worker.cur.execute(f"select theme from test where id_test = {id_test}")
    theme = list(sum(db_worker.cur.fetchall(), ()))[0]
    db_worker.cur.execute(f"select id_question from question where theme = '{theme}'")
    id_questions = list(sum(db_worker.cur.fetchall(), ()))
    stud_ans_statuses = []
    for i in range(len(id_questions)):
        db_worker.cur.execute(f"select answer_text from answers where id_question = {id_questions[i]}")
        ans_list = list(sum(db_worker.cur.fetchall(), ()))
        stud_ans = ans_list[int(stud_ans_list[i])-1]
        db_worker.cur.execute(f"select right_answer from question where id_question = '{id_questions[i]}';")
        right_ans = list(sum(db_worker.cur.fetchall(), ()))[0]
        status = True if stud_ans.lower() == right_ans.lower() else False
        stud_ans_statuses.append(status)
        db_worker.cur.execute(f"insert into result (id_student, id_question, id_test, student_answer, status) "
                              f"values ({id_student}, {id_questions[i]}, {id_test}, '{stud_ans}', '{status}');")
        db_worker.conn.commit()
    db_worker.cur.execute(f"select test_pass_bar from test where id_test = {id_test};")
    test_pass_bar = list(sum(db_worker.cur.fetchall(), ()))[0]
    test_status = True if (stud_ans_statuses.count(True) / len(stud_ans_statuses)) > (test_pass_bar / 100) else False
    db_worker.cur.execute(f"insert into student_test(id_student, id_test, dt_test, status, tm_test_duration) "
                          f"values({id_student}, {id_test}, '{dt_test.strftime('%Y-%m-%d %H:%M:%S')}', '{test_status}', "
                          f"'{tm_test_duration}');")
    db_worker.conn.commit()
    match test_status:
        case True:
            bot.send_message(message.chat.id, "Тест сдан. Поздравляем!")
        case False:
            bot.send_message(message.chat.id, "Тест не сдан. К сожалению!")
    bot.send_message(message.chat.id, "Если хотите пройти еще один тест, то введите /test")
    result = bot.send_message(message.chat.id, "Если хотите посмотреть историю сдачи тестов, то введите /result")
    bot.register_next_step_handler(result, result_info) #здесь работает, а в начале нет

@bot.message_handler(commands=['result'], content_types=['text'])
def result_info(message): #вывод истории сдачи тестов
    global db_worker
    global id_student
    db_worker.cur.execute(f"select id_test, dt_test, status, tm_test_duration from student_test where id_student = {id_student};")
    info_stud_testing = list(sum(db_worker.cur.fetchall(), ()))
    msg = ''
    for i in range(0, len(info_stud_testing), 4):
        db_worker.cur.execute(f"select theme from test where id_test = {info_stud_testing[i]};")
        theme = list(sum(db_worker.cur.fetchall(), ()))[0]
        msg += f"Тест на тему '{theme}' {'сдан' if info_stud_testing[i+2] == True else 'не сдан'} " \
               f"{info_stud_testing[i+1]}\n\n"
    bot.send_message(message.chat.id, msg)
    bot.send_message(message.chat.id, "Если хотите пройти еще один тест, то введите /test")

bot.polling(none_stop=True, interval=0)

