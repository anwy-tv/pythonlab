numbers = input("enter your numbers: ")
num = list(map(float, numbers.split()))
print("все числа: ", num)

unique = list(set(num))
print("уникальные числа:", unique)

even = []
not_even = []
negative = []
floated = []
five = 0
for number in num:
    if number % 2 == 0:
        even.append(number)
    else:
        not_even.append(number)
    if number < 0:
        negative.append(number)
    if number.is_integer() == False:
        floated.append(number)
    if number % 5 == 0:
        five += number

print("четные: ", even)
print("нечетные: ", not_even)
print("отрицательные: ", negative)
print("числа с плавающей точкой: ", floated)
print("сумма всех чисел, кратных пяти: ", five)
print("самое маленькое число: ", min(num))
print("самое большое число: ", max(num))
