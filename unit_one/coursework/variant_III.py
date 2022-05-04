#todo: III вариант (пирамидальная сортировка )
'''
"Реализовать на Python пирамидальную сортировку представленную в псевдокоде
в учебнике “Introduction to Algorithms”  на стр. 178 - 184.

Задача.
Перепишите процедуру  MAX_HEAPIFY и напечатайте получившеестся бинарное дерево
при входном списке A = [50, 14, 60, 7, 20, 70, 55, 5, 15, -10]"
'''

array = [50, 14, 60, 7, 20, 70, 55, 5, 15, -10]

def heap(array, len_tree, index_el): #находим наибольшее среди родителя и потомков в узле
    biggest = index_el
    left = 2 * index_el + 1
    right = 2 * index_el + 2
    if left < len_tree and array[left] > array[index_el]:
        biggest = left
    if right < len_tree and array[right] > array[biggest]:
        biggest = right
    if biggest != index_el:
        array[biggest], array[index_el] = array[index_el], array[biggest]
        heap(array, len_tree, biggest) #так как элементы поменялись, нужно проверить правильность нижних узлов

def max_heapify(array): #строим бинарное дерево массива
    for i in range(len(array)-1, -1, -1): #начинаем с последнего элемента
        heap(array, len(array), i)
    return array

def heap_tree_sort(array): #сортировка кучей
    max_heapify(array)      #строим бинарное дерево массива
    for i in range(len(array)-1, 0, -1): #опять начинаем с конца
        array[i], array[0] = array[0], array[i] #корень дерева меняем на конечный элемент массива
        heap(array, i, 0) #так как поменялся родитель, опять проверяем нижние узлы
    return array

print(f"Заданный массив: {array}")
print(f"Бинарное дерево массива: {max_heapify(array)}")
print(f"Результат пирамидальной сортировки: {heap_tree_sort(array)}")
