#todo: Числа в буквы
'''
Замените числа, написанные через пробел, на буквы. Не числа не изменять.

Пример.
Input	                            Output
8 5 12 12 15	                    hello
8 5 12 12 15 , 0 23 15 18 12 4 !	hello, world!
'''

alphas = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
          "v", "w", "x", "y", "z"]

key_code = {'0': " ", "!": "!", "?": "?", ",": ","}
for a in alphas:
    key_code[f"{alphas.index(a)+1}"] = a

nums = input("Введите числа от 1 до 26 через пробел, а мы преобразуем их в буквы: ") #нужно будет ввести числа из
                                                                                        # примера


def num_to_alpha(in_put, key_code):
    in_put = in_put.split(" ")
    for i in range(len(in_put)):
        in_put[i] = key_code[in_put[i]]
    in_put = "".join(in_put)
    print(f"Результат преобразования: {in_put.capitalize()}")

num_to_alpha(nums, key_code)


