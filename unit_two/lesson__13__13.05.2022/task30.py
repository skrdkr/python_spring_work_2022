#todo: Найти сумму элементов матрицы,
#Написать msum(matrix)  которая подсчитывает сумму всех элементов функцию Найти сумму всех элементов матрицы:

matrix = [[1, 2, 3], [4, 5, 6]]

def load_matrix(filename):
    with open(filename, "r") as f:
        stroke_lst = f.readlines()
        result = [[int(i) for i in el] for el in [i.split() for i in stroke_lst]] \
            if len({len(i) for i in [i.split() for i in stroke_lst]}) == 1 else False
    return result


def msum(lst):
    return print(f"Сумма всех элементов матрицы {lst} равна {sum([sum(el) for el in lst])}")

msum(matrix)
msum(load_matrix("matrix.txt"))

