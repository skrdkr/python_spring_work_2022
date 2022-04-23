#todo: Для игры "Отгадай число от 0 до 100" реализованной на занятии 4 homework/task3
'''
написать Save Game по следующему сценарию:
В запущенной игре по нажатию клавиши S появляется вывод:
1. Продолжить
2. Сохранить игру

При выборе пункта 1. игра продолжается.
При выборе пункта 2. пользователю предлагается ввести название для
сохранения, после чего нужно сделать сериализацию состояния игры.
Законсервировать все объекты которые отвечают за состоянии игры в файл
game_dump.pkl   Сериализацию и десериализацию сделать на базе библиотеки pickle.

При старте игры пользователю должен предлагатся выбор
1. Новая игра
2. Восстановить игру
При выборе 1. начинается новая игра.
При выборе 2. пользователю выводится список всех сохраненных игр(происходит десериализация).
Из них он выберает нужную, после чего загружается состояние игры на момент сохранения.
'''


#уверен, код можно сделать проще. Точно знаю, что именно можно обернуть в функции и упростить, но, к сожалению,
#не хватило времени. С файлом решения задачи оставил еще получившиеся файлы при тестах

import random
import ser_deser.deserializer as deser
import ser_deser.serializer as ser

guessed_num = random.randint(0,100)
print(f"Загаданное число: {guessed_num}\n")             #на всякий случай для проверки сохранений и загрузок

game_start = input("\nВыберите один из вариантов:\n\t1. Новая игра\n\t2. Загрузить игру\n\tПоле для ввода: ")

match game_start:

    case "1":
        count = 0
        while count != 10:
            proposed_num = input(f"\nЗагадано число от 0 до 100. Попробуй угадай. Попытка {count + 1}. "
                                f"Если хотите прервать игру, то введите S: ")
            if proposed_num == "S" or proposed_num.upper() == "S":
                in_put = input("\nВыберите один из вариантов:\n\t1. Продолжить\n"
                               "\t2. Сохранить игру и выйти\n\tПоле для ввода: ")
                match in_put:
                    case "1":
                        proposed_num = int(input("\nВведите число: "))          #данная конструкция будет повторяться
                        if proposed_num == guessed_num:                         #ее как раз не хватило времени
                            print("Правильно. Вы угадали")                      #обернуть в функцию
                            break
                        elif proposed_num != guessed_num and count == 9:
                            print(f"\nПопытки закончились. Вы проиграли")
                            break
                        elif proposed_num > guessed_num:
                            print(f"Загаданное число меньше")
                        elif proposed_num < guessed_num:
                            print(f"Загаданное число больше")
                        count += 1
                    case "2":
                        save_game = [count, guessed_num]
                        #filename = f"save_{count+1}.pkl"               #это автоматическое присвоение названия файлу
                        filename = input("Введите название сохранения: ")
                        #file_name_for_save_list = f"save_{count+1}.pkl\n"
                        file_name_for_save_list = f"{filename}.pkl\n"
                        #ser.to_pickle(save_game, filename, "wb")
                        ser.to_pickle(save_game, f"{filename}.pkl", "wb")
                        with open("saves_list.txt", "a") as f:          #файл со списком всех сохранений
                            f.write(f"{filename}.pkl\n")
                        break
            else:
                proposed_num = int(proposed_num)
                if proposed_num == guessed_num:
                    print("Правильно. Вы угадали")
                    break
                elif proposed_num != guessed_num and count == 9:
                    print(f"\nПопытки закончились. Вы проиграли")
                    break
                elif proposed_num > guessed_num:
                    print(f"Загаданное число меньше")
                elif proposed_num < guessed_num:
                    print(f"Загаданное число больше")
                count += 1

    case "2":

        with open("saves_list.txt", "r") as f:
            saves = f.readlines()
        saves = list(set(saves))
        print("\nВведите номер сохранения:")
        checking_saves = []
        for i in range(len(saves)):
            if saves[i] not in checking_saves:
                checking_saves.append(saves[i])
                print(f"\t{i + 1}. {saves[i][:-5].strip()}")
        load_num = input("Поле для ввода: ")
        load_file = f"{saves[int(load_num)-1].strip()}"
        game_load = deser.from_pickle(load_file)
        count = game_load[0]
        guessed_num = game_load[1]
        while count != 10:
            proposed_num = input(f"\nЗагадано число от 0 до 100. Попробуй угадай. Попытка {count + 1}. "
                                 f"Если хотите прервать игру, то введите S: ")
            if proposed_num == "S" or proposed_num.upper() == "S":
                in_put = input(
                    "\nВыберите один из вариантов:\n\t1. Продолжить\n\t2. Сохранить игру и выйти\n\tПоле для ввода: ")
                match in_put:
                    case "1":
                        proposed_num = int(input("\nВведите число: "))
                        if proposed_num == guessed_num:
                            print("Правильно. Вы угадали")
                            break
                        elif proposed_num != guessed_num and count == 9:
                            print(f"\nПопытки закончились. Вы проиграли")
                            break
                        elif proposed_num > guessed_num:
                            print(f"Загаданное число меньше")
                        elif proposed_num < guessed_num:
                            print(f"Загаданное число больше")
                        count += 1
                    case "2":
                        save_game = [count, guessed_num]                    #то же конструкция повторяется - можно
                        # filename = f"save_{count+1}.pkl"                  #обернуть в функцию
                        filename = input("Введите название сохранения: ")
                        # file_name_for_save_list = f"save_{count+1}.pkl\n"
                        file_name_for_save_list = f"{filename}.pkl\n"
                        # ser.to_pickle(save_game, filename, "wb")
                        ser.to_pickle(save_game, f"{filename}.pkl", "wb")
                        with open("saves_list.txt", "a") as f:
                            f.write(f"{filename}.pkl\n")
                        break
            else:
                proposed_num = int(proposed_num)
                if proposed_num == guessed_num:
                    print("Правильно. Вы угадали")
                    break
                elif proposed_num != guessed_num and count == 9:
                    print(f"\nПопытки закончились. Вы проиграли")
                    break
                elif proposed_num > guessed_num:
                    print(f"Загаданное число меньше")
                elif proposed_num < guessed_num:
                    print(f"Загаданное число больше")
                elif proposed_num != guessed_num:
                    print(f"Неправильно. Осталось {10 - (count + 1)}")
                count += 1
