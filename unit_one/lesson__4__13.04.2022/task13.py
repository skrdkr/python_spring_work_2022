#todo: Дан целочисленный массив размера N из 10 элементов.
#Преобразовать массив, увеличить каждый его элемент на единицу.

while True:
    num_row = input("Введите десять целых чисел через запятую: ")

    num_row.replace(" ", "")   #если будут добавлены пробелы

    num_list = list(num_row.split(","))

    for i in range(len(num_list)):              #Решил для себя немного усложнить и не идти через заранее данный
        num_list[i] = int(num_list[i]) + 1      #массив целых чисел. Если задан заранее, код будет проще
        num_list[i] = str(num_list[i])          #for i in range(len(num_list)):
                                                #   num_list[i] = num_list[i] + 1
    num_row_string = ", ".join(num_list)

    print(f"Каждое ваше число было увеличено на один: {num_row_string}")

    answer = input("\nХотите продолжить? Введите 'y' английское, если да; или любой иной символ - если нет: ")
    if answer == "y":
        continue
    elif answer != "y":
        break