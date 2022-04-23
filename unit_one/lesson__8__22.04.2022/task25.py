#todo: Убрать повторяющиеся буквы и лишние символы
'''
Построить по ключевой фразе часть алфавита. Взять все буквы по одному разу. Не буквы убрать.
Буквы должны идти в том порядке, в котором встретились во фразе в первый раз.

Input             	            Output
apple	                        aple
25.04.2022 Good morning !!	    godmrni
'''

in_put = input("Введите любой текст с любыми символами: ")

def pure_alpha(in_put):
    in_put = list(in_put)
    alphabet = []
    for i in in_put:
        if i.isalpha() and i.lower() not in alphabet:
            alphabet.append(i.lower())
    print(''.join(alphabet))

pure_alpha(in_put)