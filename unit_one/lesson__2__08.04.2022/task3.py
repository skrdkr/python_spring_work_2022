print(f'\n\t***Операции над числами***')

while True:
    first_num = float(input("\nВведите первое число (десятичное число указывается с точкой): "))
    second_num = float(input("Введите второе число (десятичное число указывается с точкой): "))

    print(f"Сумма введенных чисел: {first_num+second_num}")
    print(f"Разность введенных чисел: {first_num-second_num}")
    print(f"Частное введенных чисел: {first_num/second_num}")
    print(f"Произведение введенных чисел: {first_num*second_num}")
    print(f"Результат целочисленного деления введенных чисел: {first_num//second_num}")
    print(f"Результат деления с остатком: {first_num%second_num}")
    print(f"Результат возведения первого числа в степень, равной второму числу: {first_num**second_num}\n")

    answer = input("Хотите продолжить вычисления с другими числами? Введите 'y' английское, если да; "
                   "или любой иной символ - если нет: ")
    if answer == "y":
        continue
    elif answer != "y":
        break