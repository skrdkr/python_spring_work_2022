'''
# Bonus:
В качестве бонуса можно реализовать Telegtram - бота который в виде викторины задает
вопросы. Вопросы можно взять из тестовой системы. После вывода бот принимает вариант ответа.
В конце викторины выводит кол-во правильных и неправильных ответов и приз в случае успеха.
В качестве библиотеки можно взять  библиотеку telebot. Описание по разработки и примеры найти
в многочисленных статьях в Internet.
'''

#TOKEN = '5402077477:AAEKjFYD9KEobhbkPBXTeRZt5cwruVny8-k'

import telebot
import psycopg
import random

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


class Test:
    '''Класс теста'''
    def __init__(self, dbname):
        '''Метод инициализации конкретного теста из Базы данных'''
        self.dbname = dbname

    def get_questions(self):
        '''Забираем из БД все вопросы с правильными ответами'''
        self.dbname.cur.execute(f"select id_question, question_text, right_answer from question")
        res = list(sum(self.dbname.cur.fetchall(), ()))
        q_right_ans_dict = {}
        for i in range(0, len(res), 3):
            q_right_ans_dict[res[i]] = [res[i+1], res[i+2]]
        return q_right_ans_dict #возвращаем словарь (ключи - id вопросов, значения - списки (текст вопрос, верный ответ)


    def get_answers(self, question):
        '''Метод возвращает список вариантов ответов'''
        self.dbname.cur.execute(f"SELECT answer_text from answers where id_question = {question};")
        ans_list = list(sum(self.dbname.cur.fetchall(), ()))
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for item in ans_list:
            markup.add(item)
        return markup #возвращаем "кнопки" ответов на конкретный вопрос

db_worker = Db()
test = Test(db_worker)
questions = test.get_questions()
user_qs = [] #записываем все id вопросов, которые были выведены пользователю

bot = telebot.TeleBot('5402077477:AAEKjFYD9KEobhbkPBXTeRZt5cwruVny8-k')

@bot.message_handler(commands=['start'])
def start_quiz(message):
    '''Начало квиза'''
    bot.send_message(message.chat.id, "Добрый день! Начинаем викторину по Python! "
                                      "Для получения вопроса напишите или тапните /quiz")

@bot.message_handler(commands=['quiz', 'continue'])
def question(message):
    '''Вывод вопроса и вариантов ответа к нему'''
    ids_questions = list(questions.keys())
    id_question = random.choice(ids_questions) #рандомно выбираем вопрос из списка вопросов
    user_qs.append(id_question)
    q_text = questions[id_question][0]
    mark_up = test.get_answers(id_question)
    user_ans = bot.send_message(message.chat.id, f"{q_text}", reply_markup=mark_up)
    bot.register_next_step_handler(user_ans, result) #получаем ответ пользователя и переходим к выводу результата

@bot.message_handler(content_types=['text'])
def result(message):
    '''Вывод результата пользователю'''
    user_a = message.text
    right_ans = questions[user_qs[-1]][1]
    result = "Правильный ответ" if user_a.lower() == right_ans.lower() else "Неправильный ответ"
    bot.send_message(message.chat.id, f"{result}")
    msg = bot.send_message(message.chat.id, "Еще вопрос? Напишите /continue")
    bot.register_next_step_handler(msg, question) #возвращаемся к выводу следующего вопроса

bot.polling(none_stop=True, interval=0)

