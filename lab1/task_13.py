numbers = input("enter your numbers")
num = list(map(float, numbers.split()))
print(num)

unique = list(set(num))
print(unique)

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
print(even)
print(not_even)
print(negative)
print(floated)
print(five)
print(min(num))
print(max(num))
