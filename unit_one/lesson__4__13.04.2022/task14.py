#todo: Дан массив размера N. Найти индексы двух ближайших чисел из этого массива.
'''
Пример:
mass = [1,2,17,16,30,51,2,70,3,2]

Для числа 2 индексы двух ближайших чисел: 6 и 9

Пример:
mass = [1,2,17,54,30,89,2,1,6,2]
Для числа 1 индексы двух ближайших чисел: 0 и 7
Для числа 2 индексы двух ближайших чисел: 6 и 9
'''



mass = [1, 5, 3, 45, 15, 3, 77, 19, 1, 3, 88, 1]      #пока не удалось придумать какого-то универсального алгоритма

print(mass)

checking_nums = []

for i in mass:
    if mass.count(i) > 1 and i not in checking_nums:
        checking_nums.append(i)

        counts = mass.count(i)
        start_index = mass.index(i)
        indexes = [start_index]
        while counts > 1:
            upgoing_index = mass.index(i, start_index + 1, len(mass))
            indexes.append(upgoing_index)
            start_index = upgoing_index
            counts -= 1

        if abs(indexes[0] - indexes[1]) > abs(indexes[1] - indexes[2]):
            print(f"Для числа {i} индексы двух ближайших чисел: {indexes[1]} и {indexes[2]}")
        elif abs(indexes[0] - indexes[1]) < abs(indexes[1] - indexes[2]):
            print(f"Для числа {i} индексы двух ближайших чисел: {indexes[0]} и {indexes[1]}")