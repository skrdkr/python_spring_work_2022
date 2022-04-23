# todo: Шифр Цезаря
'''
Описание шифра.
В криптографии шифр Цезаря, также известный шифр сдвига, код Цезаря или сдвиг Цезаря,
является одним из самых простых и широко известных методов шифрования.
Это тип подстановочного шифра, в котором каждая буква в открытом тексте заменяется буквой на некоторое
фиксированное количество позиций вниз по алфавиту. Например, со сдвигом влево 3, D будет заменен на A,
E станет Б, и так далее. Метод назван в честь Юлия Цезаря, который использовал его в своей частной переписке.

Задача.
Считайте файл message.txt и зашифруйте  текст шифром Цезаря, при этом символы первой строки файла должны
циклически сдвигаться влево на 1, второй строки — на 2, третьей строки — на три и т.д.
 В этой задаче удобно считывать файл построчно, шифруя каждую строку в отдельности.
В каждой строчке содержатся различные символы. Шифровать нужно только буквы кириллицы.
'''

f = open("message.txt", "r", encoding="utf-8")
message_list = f.readlines()
f.close()

alphas = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у",
          "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

def get_passw(list, transfer):
    passw = {}
    for a in list:
        new_index = list.index(a) - transfer
        passw[a] = list[new_index]
    return passw

count = len(message_list)
step = 0
encryp_message = []

while count > 0:
    step += 1
    passw = get_passw(alphas, step)
    list_stroke = list(message_list[-count])
    for i in range(len(list_stroke) - 1):
        if list_stroke[i] in alphas:
            list_stroke[i] = passw[list_stroke[i]]
        elif list_stroke[i].lower() in alphas and list_stroke[i] not in alphas:
            list_stroke[i] = passw[list_stroke[i].lower()].upper()
    encrip_stroke = "".join(list_stroke)
    print(encrip_stroke.strip())
    encryp_message.append(encrip_stroke)
    count -= 1

en_f = open("encryp_message.txt", "w", encoding="utf-8")
en_f.writelines(encryp_message)
en_f.close()


