def unique_elements(lst, result=None):
    if result is None:
        result = []
    for item in lst:
        if type(item) == list:
            unique_elements(item, result)  # заходим во вложенный список
        elif item not in result:
            result.append(item)
    return result


list_a = [11, 6, 7, [1, 0, 1], 7, [19, [19, [1], 3, [4, 14, 7]]]]
print("исходный список:", list_a)
print("уникальные элементы:", unique_elements(list_a))