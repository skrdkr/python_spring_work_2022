'''
#todo: Создайте функцию compute_bill, считающаю итоговую сумму товаров в чеке.
Функция должна принимать 1 параметр - словарь, в котором указано количество едениц товара.
Цены хранятся в словаре:
'''

prices = {"banana": 4, "apple": 2, "orange": 1.5, "pear": 3,}

def quantity_dict():
   banana = float(input("Введите вес покупаемых бананов, кг: "))
   apple = float(input("Введите вес покупаемых яблок, кг: "))
   orange = float(input("Введите вес покупаемых апельсинов, кг: "))
   pear = float(input("Введите вес покупаемых груш, кг: "))
   quantity_dict = {"banana": banana, "apple": apple, "orange": orange, "pear": pear,}
   return quantity_dict

def compute_bill(quantity_dict):
   global prices
   item_total_prices = []
   for key in prices.keys():
     item_total_price = prices[key] * quantity_dict[key]
     item_total_prices.append(item_total_price)
   total_sum = sum(item_total_prices)
   return print(f"\nОбщая цена ваших покупок: {total_sum} долларов")

quantity_dict = quantity_dict()
compute_bill(quantity_dict)