import time


def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"функция {func.__name__} выполнялась {round((end - start) * 1000, 2)} мс")
        return result
    return wrapper


@timing
def sum_numbers(n):
    total = 0
    for number in range(n):
        total += number
    return total


@timing
def pause():
    time.sleep(0.2)


print("сумма чисел:", sum_numbers(44400))
pause()