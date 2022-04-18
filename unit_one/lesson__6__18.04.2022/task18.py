'''
#todo:Создайте программу, которая будет выводить все возможные комбинации при броске 2 игральных костей
и сумму их значений. У игральной кости стороны пронумерованы от 1 до 6.

Пример вывода:
Сумма 2   комбинация [(1,1)]
Сумма 3   комбинация [(1,2),(2,1)]
Сумма 4   комбинация [(1,3),(3,1),(2,2)]
........................................
Выводы комбинаций оформить в список кортежей.
'''

f_dice = [x for x in range(1,7)]
s_dice = f_dice.copy()

combo_and_sum = {}

for i in f_dice:
    for k in s_dice:
        tuple_el = (i, k)
        combo_and_sum[tuple_el] = sum(tuple_el)

combo_and_sum_sort = {'2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': [], '11': [],
                      '12': []}

for key, value in combo_and_sum.items():
    match value:
        case 2:
            combo_and_sum_sort['2'].append(key)
        case 3:
            combo_and_sum_sort['3'].append(key)
        case 4:
            combo_and_sum_sort['4'].append(key)
        case 5:
            combo_and_sum_sort['5'].append(key)
        case 6:
            combo_and_sum_sort['6'].append(key)
        case 7:
            combo_and_sum_sort['7'].append(key)
        case 8:
            combo_and_sum_sort['8'].append(key)
        case 9:
            combo_and_sum_sort['9'].append(key)
        case 10:
            combo_and_sum_sort['10'].append(key)
        case 11:
            combo_and_sum_sort['11'].append(key)
        case 12:
            combo_and_sum_sort['12'].append(key)

for key, value in combo_and_sum_sort.items():
    print(f"Сумма {key} получается из комбинаций значений {value}")



