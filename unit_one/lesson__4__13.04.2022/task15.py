# Написать игру "Поле чудес"
"""
Отгадываемые слова и описание лежат в разных  массивах по одинаковому индексу.
words = ["оператор", "конструкция", "объект"]
desc_  = [ "Это слово обозначает наименьшую автономную часть языка программирования", "..", ".." ]
Пользователю выводится определение слова и количество букв в виде шаблона. Стиль шаблона может быть любым.
Слово из массива берется случайным порядком. Принимая из ввода букву мы ее открываем
в случае успеха а в случае неуспеха насчитывам штрафные балы. Игра продолжается до 10 штрафных баллов
либо победы.

Пример вывода:

"Это слово обозначает наименьшую автономную часть языка программирования"

▒  ▒  ▒  ▒  ▒  ▒  ▒  ▒

Введите букву: O

O  ▒  ▒  ▒  ▒  ▒  O  ▒


Введите букву: Я

Нет такой буквы.
У вас осталось 9 попыток !
Введите букву:
"""

import random

print(f"***** В ЭФИРЕ КАПИТАЛ-ШОУ 'ПОЛЕ ЧУДЕС' *****")

words = ["пенал", "ручка", "линейка"]
discrip = ["Есть у школьника", "Подружка карандаша", "Прибор измерения"]

while True:
    index = random.randint(0, len(words)-1)
    guessed_word = words[index]
    hashed_guessed_word = ["#"] * len(guessed_word)
    attempts = 10
    print(f"Внимание вопрос.\n{discrip[index]}. Что это? Вы можете ошибиться {attempts} раз(раза)\n{hashed_guessed_word}")

    while attempts > 0:
        proposed_letter = input("Введите букву: ")
        if proposed_letter in guessed_word:
            hashed_guessed_word[guessed_word.index(proposed_letter)] = proposed_letter
            print(hashed_guessed_word)
            if "#" not in hashed_guessed_word:
                print(f"Поздравляем! Вы отгадали слово '{guessed_word}'!")
                break
        elif proposed_letter not in guessed_word and attempts == 1:
            print(f"К сожалению, вы не угадали слово '{guessed_word}'")
            break
        elif proposed_letter not in guessed_word:
            print(f"Нет такой буквы. Количество оставшихся попыток: {attempts - 1}")
            attempts -= 1

    answer = input("\nХотите продолжить? Введите 'y' английское, если да; или любой иной символ - если нет: ")
    if answer == "y":
        continue
    elif answer != "y":
        break
