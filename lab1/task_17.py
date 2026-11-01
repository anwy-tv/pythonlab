def merge_dicts(a, b):
    for key in b:
        if key not in a:
            a[key] = b[key]
        elif type(a[key]) == dict and type(b[key]) == dict:
            merge_dicts(a[key], b[key]) 
        elif type(a[key]) == list and type(b[key]) == list:
            for item in b[key]:
                if item not in a[key]:
                    a[key].append(item)
        elif type(a[key]) == set and type(b[key]) == set:
            for item in b[key]:
                a[key].add(item)
        elif type(a[key]) == tuple and type(b[key]) == tuple:
            for item in b[key]:
                if item not in a[key]:
                    a[key] += (item,)  
        else:
            a[key] = b[key]


dict_a = {"a": 1, "b": {"c": 1, "f": 4}}
dict_b = {"d": 1, "b": {"c": 2, "e": 3}}
print("первый словарь:", dict_a)
print("второй словарь:", dict_b)
merge_dicts(dict_a, dict_b)
print("первый словарь после слияния: ", dict_a)

x = {"list": [1, 2], "set": {1, 2}, "tuple": (1, 2), "inner": {"k": [1]}}
y = {"list": [2, 3], "set": {2, 3}, "tuple": (2, 3), "inner": {"k": [5], "m": 1}}
merge_dicts(x, y)
print("слияние с коллекциями:", x)
