import random
number = random.randint(1, 100)
guessing_number = int(input("введите случайное число от 1 до 100: "))
while guessing_number != number:
        if guessing_number > number:
                print("загаданное число меньше введенного. попробуйте еще раз: ", end="")
                guessing_number = int(input())
        elif guessing_number < number:
                print("загаданное число больше введенного. попробуйте еще раз: ", end="")
                guessing_number = int(input())
                continue
print(f"правильно, вы угадали. загаданное число - {number}")


