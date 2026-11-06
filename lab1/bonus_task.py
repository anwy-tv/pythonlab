# поход в магазин
# вводим перечень товаров: товар, кол-во, цена, стоимость фулл считается
# декоратор который будет делать скидку в размере 10 процентов если общая сумма более 100 рублей
# итоговый чек выводится в файл 
def read_items(title):
    
purchases = {}

def sale(func):
    def wrapper(*args):
        if func(total_sum) > 100:
            sale = 0.1
            result = total_sum*(1-sale)
        return result
    return wrapper

def total_sum():
    while True:
        name = input("товар: ").lower()
        if name == "":
           break
        amount = float(input(f"сумма ({name}): "))




with open("total_sum.txt", "w", encoding="utf-8") as f:
    f.write(total_sum)