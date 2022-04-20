#todo: Требуется создать csv-файл «algoritm.csv» со следующими столбцами:
#– id - номер по порядку (от 1 до 10);
#– текст из списка algorithm

algorithm = [ "C4.5" , "k - means" , "Метод опорных векторов" , "Apriori" ,
"EM" , "PageRank" , "AdaBoost", "kNN" , "Наивный байесовский классификатор" , "CART" ]

#Каждое значение из списка должно находится на отдельной строке.

def csv_strokes(list):
    strokes = []
    for i in range(1, len(list)+1):
        stroke = f"{i}, {list[i-1]}\n"
        strokes.append(stroke)
    return strokes


f = open("algorithm.csv", "w", encoding = "utf-8")
columns = "id, algorithm\n"
f.write(columns)
f.writelines(csv_strokes(algorithm))
f.close()

