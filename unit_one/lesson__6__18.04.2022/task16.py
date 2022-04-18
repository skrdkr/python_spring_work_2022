#todo: Для написанной игры "Поле чудес" нужно сделать рефакторинг кода , сгруппировать
'''функционал в логические блоки и оформить эти блоки кода в виде функций. Стараться
чтобы каждая функция выполняла одно универсальное действие.'''

import random

print(f"***** В ЭФИРЕ КАПИТАЛ-ШОУ 'ПОЛЕ ЧУДЕС' *****")

words = ["пенал", "ручка", "линейка"]
discrip = ["Есть у школьника", "Подружка карандаша", "Прибор измерения"]

def g_word(words_list):
    index = random.randint(0, len(words_list) - 1)
    guessed_word = words_list[index]
    return guessed_word

def hash_g_word(g_word):
    hashed_guessed_word = ["#"] * len(g_word)
    return hashed_guessed_word

def discription(words, g_word, discrip):
    index = words.index(g_word)
    return discrip[index]

def opening_letter(letter, g_word):
    global hash_g_word
    hash_g_word[g_word.index(letter)] = letter
    return print(f"Правильно\n{hash_g_word}")

def wrong_letter():
    global attempts
    attempts -= 1
    return print(f"Нет такой буквы. Количество оставшихся попыток: {attempts}")

def winning_condition(hash_g_word):
    if '#' not in hash_g_word:
        return True

def losing_condition():
    global attempts
    if attempts == 0:
        return True

g_word = g_word(words)
hash_g_word = hash_g_word(g_word)
discrip_item = discription(words, g_word, discrip)
attempts = 10

print(f"Внимание! Вопрос!\n{discrip_item}. Что это? Вы можете ошибиться {attempts} раз\n{hash_g_word}")

while attempts > 0:
    proposed_letter = input("Введите букву: ")
    if proposed_letter in g_word:
        opening_letter(proposed_letter, g_word)
        if winning_condition(hash_g_word):
            print(f"Поздравляем! Вы отгадали слово '{g_word}'!")
            break
    elif proposed_letter not in g_word:
        wrong_letter()
        if losing_condition():
            print(f"К сожалению, вы не угадали слово '{g_word}'")