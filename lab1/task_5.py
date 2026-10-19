a = int(input("enter number a: "))
b = int(input("enter number b: "))
print("сумма: ", a+b)
print("разность:", a-b)
print("произведение: ", a*b, "возведение в степень: ", a**b, sep = "\n")
if b==0:
    print("на ноль делить нельзя")
else:
    print("частное от деления: ", a/b, "остаток от деления: ", a%b, sep = "\n")
