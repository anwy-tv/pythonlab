from datetime import datetime, date
today = date.today()
purchase_sum = float(input("сумма покупки: "))
age = int(input("ваш возраст: "))
birthday = input("день вашего рождения: ")
vip_status = input("вы являетесь vip клиентом? да/нет: ")
sale = 0

if purchase_sum > 1000:
    sale = 0.10

if age >= 63:
    sale += 0.05

try:
    bday_date = datetime.strptime(birthday, "%d.%m.%Y").date()
    if bday_date.day == today.day and bday_date.month == today.month:
        sale += 0.05
except ValueError:
    print("вы неверно ввели дату!")

if vip_status.lower() == "да":
    sale = max(sale, 0.15)
sale = min(sale, 0.25)
total = purchase_sum * (1 - sale)
print ("итоговая скидка:", sale * 100, "%")
print("сумма покупки со скидкой: ", total, "$")