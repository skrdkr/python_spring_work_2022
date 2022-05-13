#todo Задача 2. Транспонирование матрицы, transpose(matrix)
#Написать функцию transpose(matrix), которая выполняет транспонирование матрицы. Решить с использованием списковых включений.

def transpose(matrix):
    return print(f"Матрица {matrix} после транспонирования "
                 f"{[[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]}")

transpose([[1, 2, 3], [4, 5, 6]])

