print("введите дату рождения")
day = int(input("день: "))
month = int(input("месяц: "))
year = int(input("год: "))

print(day, month, year) 

print("знак зодиака", end=" ") #selection of zodiac sign 
if month == 1:
    if day < 20:
        print("Козерог")
    else:
        print("Водолей")
elif month == 2:
    if day < 19:
        print("Водолей")
    else:
        print("Рыбы")
elif month == 3:
    if day < 21:
        print("Рыбы")
    else:
        print("Овен")
elif month == 4:
    if day < 20:
        print("Овен")
    else:
        print("телец")
elif month == 5:
    if day < 21:
        print("Телец")
    else:
        print("Близнецы")
elif month == 6:
    if day < 22:
        print("Близнецы")
    else:
        print("Рак")
elif month == 7:
    if day < 23:
        print("Рак")
    else:
        print("Лев")
elif month == 8:
    if day < 23:
        print("Лев")
    else:
        print("Дева")
elif month == 9:
    if day < 23:
        print("Дева")
    else:
        print("Весы")
elif month == 10:
    if day < 24:
        print("Весы")
    else:
        print("Скорпион")
elif month == 11:
    if day < 22:
        print("Скорпион")
    else:
        print("Стрелец")
elif month == 12:
    if day < 22:
        print("Стрелец")
    else:
        print("Козерог")