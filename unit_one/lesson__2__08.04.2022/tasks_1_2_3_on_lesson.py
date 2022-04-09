int_number = 1
float_number = 2.0
bool_item = True
string_item = "hello"
none_item = None

print(f"{int_number}: {type(int_number)}")
print(f"{float_number}: {type(float_number)}")
print(f"{bool_item}: {type(bool_item)}")
print(f"{string_item}: {type(string_item)}")
print(f"{none_item}: {type(none_item)}\n")

age = "23"
age = int(age)
print(f"{age}: {type(age)}\n")
'''Не преобразовывает строку с буквами в число
foo = "23abc"
foo = int(foo)
print(f"{foo}: {type(foo)}")
'''

'''Переменная определена неправильно
age = 123abc
age = bool(age)
print(f"{age}: {type(age)}\n")
'''

flag = 1
flag = bool(flag)
print(f"Flag: {type(flag)} {flag}\n")

str_one = "Privet"
str_two = ""
str_one = bool(str_one)
str_two = bool(str_two)
print(f"str_one: {type(str_one)} {str_one}")
print(f"str_two: {type(str_two)} {str_two}\n")

one = 1
zero = 0
one = bool(one)
zero = bool(zero)
print(f"One: {type(one)} {one}")
print(f"Zero: {type(zero)} {zero}\n")

false_item = False
false_item = str(false_item)
print(f"false_item: {type(false_item)} {false_item}\n")

age = 36.6
temperature = 25
temp_age = age
temp_temperature = temperature
age = temp_temperature
temperature = temp_age

# age, temperature = temperature, age

print(f"Age: {age}")
print(f"Temperature: {temperature}")
