#todo: II вариант (алгоритм сортировки слиянием)
'''
Реализовать на Python алгоритм сортировки слиянием представленный в псевдокоде
в учебнике “Introduction to Algorithms”  на стр. 71 - 77.

Задача.
Перепишите процедуру  MERGE_SORT и отсортируйте последовательность
A = [31, 41, 9, 26, 41, 58, -1 , 6 , 101 , 13] по возрастанию
'''

array = [31, 41, 9, 26, 41, 58, -1, 6, 101, 13]

def merge(left_part, right_part):
    sorted_list = []
    l_p_index = 0   #первый элемент левой части списка
    r_p_index = 0   #первый элемент правой части списка

    while l_p_index < len(left_part) and r_p_index < len(right_part):   #обход частей по-элементно
        if left_part[l_p_index] <= right_part[r_p_index]:   #добавляем элемент из левой части в отсортированный список
            sorted_list.append(left_part[l_p_index])
            l_p_index += 1 #переходим к следующему элементу из левой части
        else:
            sorted_list.append(right_part[r_p_index])   #добавляем элемент из правой части в отсортированный список
            r_p_index += 1  #переходим к следующему элементу из правой части
    sorted_list.extend(left_part[l_p_index:]) #добавление отсортированного остатка левой части
    sorted_list.extend(right_part[r_p_index:]) #добавление отсортированного остатка правой части
    return sorted_list


def merge_sort(array):
    if len(array) <= 1:
        return array
    mid = len(array) // 2                   #индекс середины списка
    left_part = merge_sort(array[:mid])     #продолжаем дробить список
    right_part = merge_sort(array[mid:])
    return merge(left_part, right_part)

print(f"Несортированный список: {array}")
print(f"Список после сортировки слиянием по возрастанию: {merge_sort(array)}")
