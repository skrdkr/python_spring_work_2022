print(f'\n\t***Перемешивание значений переменных***')

while True:
    a_num = float(input("\nВведите значение числа A (десятичное число указывается с точкой): "))
    b_num = float(input("Введите значение числа B (десятичное число указывается с точкой): "))
    c_num = float(input("Введите значение числа С (десятичное число указывается с точкой): "))

    a_num, b_num, c_num = c_num, a_num, b_num

    print(f"Перемешенные значения по схеме А в В, В в С, С в А:\n\tА: {a_num}\n\tВ: {b_num}\n\tС: {c_num}\n")

    answer = input("Хотите продолжить работу с другими числами? Введите 'y' английское, если да; "
                   "или любой иной символ - если нет: ")
    if answer == "y":
        continue
    elif answer != "y":
        break