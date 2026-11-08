def cache(func):
    saved = {}

    def wrapper(*args):
        if args in saved:
            print("берем результат из кэша для", *args)
            return saved[args]
        print("считаем заново для", *args)
        result = func(*args)
        saved[args] = result
        return result
    return wrapper


@cache
def square(n):
    return n * n

print("первый вызов square(5):", square(5))
print("второй вызов square(5):", square(5))
print("вызов square(7):", square(7))