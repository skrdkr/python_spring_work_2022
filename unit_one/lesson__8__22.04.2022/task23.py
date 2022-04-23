#todo: Взлом шифра
#Вы знаете, что фраза зашифрована кодом цезаря с неизвестным сдвигом.
#Попробуйте все возможные сдвиги и расшифруйте фразу.

encryp_message = "grznuamn zngz cge sge tuz hk uhbouay gz loxyz atrkyy eua'xk jazin"

alphas = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
          "v", "w", "x", "y", "z"]
transfer_list = [x for x in range(-26, 27)]


def get_passw(list, transfer):
    passw = {}
    for a in list:
        if (list.index(a) - transfer) > (len(list) - 1):
            new_index = (list.index(a) - transfer) - len(list)
            passw[a] = list[new_index]
        elif (list.index(a) - transfer) <= (len(list) - 1):
            new_index = list.index(a) - transfer
            passw[a] = list[new_index]
    return passw

print(f"Зашифрованное сообщение:\n{encryp_message}")

#step = int(input("Введите предполагаемый сдвиг шифра Цезаря: ")) <---- сначала вводил, потом надоело, сделал через
                                                                        #список

list_stroke = list(encryp_message)

count = 0
while count < len(transfer_list):
    passw = get_passw(alphas, transfer_list[count])
    orig_message = ""
    for i in list_stroke:
        if i in alphas:
            orig_message += passw[i]
        else:
            orig_message += i
    #print(transfer_list[count], orig_message)         <---- здесь выводятся все возможные варианты
    if "dutch" in orig_message:
        if transfer_list[count] > 0:
            print(f"\nСдвиг вверх по алфавиту: {abs(transfer_list[count])} позиций\n"
                  f"Зашифрованное сообщение: {orig_message}")
        elif transfer_list[count] < 0:
            print(f"\nСдвиг вниз по алфавиту: {abs(transfer_list[count])} позиций\n"
                  f"Зашифрованное сообщение: {orig_message}")
    count += 1

