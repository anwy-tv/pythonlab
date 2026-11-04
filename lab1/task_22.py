def type_check(*types):
    def decorator(func):
        def wrapper(*args):
            for i in range(len(types)):
                if type(args[i]) != types[i]:
                    raise TypeError(f"аргумент {i + 1} должен быть {types[i].__name__}, а передан {type(args[i]).__name__}")
            return func(*args)
        return wrapper
    return decorator


@type_check(int, int)
def add(a, b):
    return a + b


print("add(50, 2) =", add(50, 2))

try:
    print("50 + 2 =", add(50, 2))
except TypeError as e:
    print("ошибка:", e)