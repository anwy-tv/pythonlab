#Программа должна запрашивать тип измерения, исходную единицу, целевую единицу и значение.
# | "масса" | "время" | "скорость" | "температура" | "площадь" | "объем" | "давление" | "угол" | "сила":
coeff_length = {
    "метры": 1,
    "километры": 1000,
    "сантиметры": 0.01,
    "миллиметры": 0.001,
    "мили": 1609.34,
}
coeff_speed = {
    "м/с": 1,
    "км/ч": 1 / 3.6,
    "мили/ч": 0.44704,
    "узлы": 0.514444,
}
coeff_time = {
    "секунды": 1,
    "минуты": 60,
    "часы": 3600,
    "сутки": 86400,
}
coeff_weight = {
    "килограммы": 1,
    "граммы": 0.001,
    "тонны": 1000,
    "фунты": 0.453592,
    "унции": 0.0283495,
}

def inp():
    source_mes = input("введите исходную единицу: ").lower()
    not_source_mes = input("введите целевую единицу: ").lower()
    value = float(input("введите значение: "))
    return source_mes, not_source_mes, value


def konvert(source_mes, not_source_mes, value, coeff):
    # переводим в базовую единицу, потом в целевую
    answer = value * coeff[source_mes] / coeff[not_source_mes]
    return answer

def calc(coeff):
    print("Доступно:", ", ".join(coeff))
    source_mes, not_source_mes, value = inp()
    answer = konvert(source_mes, not_source_mes, value, coeff)
    print("результат:", answer, not_source_mes)


print("Выберите единицу измерения:")
print("1 - масса")
print("2 - время")
print("3 - скорость")
print("4 - длина")
measure = input("введите номер: ")
match measure:
    case "1":
        calc(coeff_weight)
    case "2":
        calc(coeff_time)
    case "3":
        calc(coeff_speed)
    case "4":
        calc(coeff_length)