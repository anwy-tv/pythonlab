from datetime import datetime


def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            with open(filename, "a", encoding="utf-8") as file:
                file.write(f"{now} | {func.__name__} | args: {args} | kwargs: {kwargs}\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@log_calls("calls.txt")
def add(a, b):
    return a + b


@log_calls("calls.txt")
def hello(name, greeting="привет"):
    return f"{greeting}, {name}"


print("add(2, 3) =", add(2, 3))
print("hello:", hello("аня", greeting="доброе утро"))

print("содержимое файла calls.txt:")
with open("calls.txt", encoding="utf-8") as file:
    print(file.read())