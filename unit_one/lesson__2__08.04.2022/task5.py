print(f'\n\t***Нахождение длин отрезков и их суммы***')

while True:
    dote_a = float(input("\nВведите координату точки A на числовой оси (десятичное число указывается с точкой): "))
    dote_b = float(input("Введите координату точки B на числовой оси (десятичное число указывается с точкой): "))
    dote_c = float(input("Введите координату точки C на числовой оси (десятичное число указывается с точкой): "))

    ac_length = abs(dote_c - dote_a)
    bc_length = abs(dote_c - dote_b)
    acbc_sum_length = ac_length + bc_length

    print (f"Длина отрезка АС: {ac_length}\n"
           f"Длина отрезка BC: {bc_length}\n"
           f"Сумма отрезков AC и BC: {acbc_sum_length}\n")

    answer = input("Хотите продолжить вычисления с другими точками? Введите 'y' английское, если да; "
                   "или любой иной символ - если нет: ")
    if answer == "y":
        continue
    elif answer != "y":
        break