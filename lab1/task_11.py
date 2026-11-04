age = int(input("введите ваш возраст: "))
income = float(input("введите ежемесячный доход: "))
credit = float(input("введите размер запрашиваемого кредита: "))
term = int(input("введите срок кредита (сколько месяцев): "))
history = input("кредитная история (отличная/хорошая/удовлетворительная/плохая): ").lower()
has_guarantors = input("есть ли поручители? (да/нет): ")
has_deposit = input("есть залог? (да/нет): ")

sootn = credit/income

risk = "низкий"
percent_rate = 5
recommendation = "одобрить"

if sootn > 24:  
    risk = "критический"
    percent_rate = 25.0
    recommendation = "отклонить"
elif sootn > 12:  
    risk = "высокий"
    percent_rate = 18.0
elif sootn > 6:  
    risk = "средний"
    percent_rate = 12.0

if history == "плохая":
    risk = "критический"
    percent_rate = 25.0
    recommendation = "отклонить"
elif history == "удовлетворительная":
    if risk == "низкий":
        risk = "средний"
        percent_rate += 3 
    else:
        risk = "высокий"
        percent_rate += 5
if age < 21 or age > 65:
    percent_rate += 2
    if risk == "низкий":
        risk = "средний"
if has_deposit or has_guarantors:
    percent_rate -= 2
    if risk == "высокий":
        risk = "средний"
    elif risk == "средний":
        risk = "низкий"

if risk == "критический":
    recommendation = "отклонить"

print(f"Соотношение кредита к доходу: {sootn:.1f} месячных доходов")
print("Категория риска: ", risk)
print("Предлагаемая процентная ставка: ", percent_rate, "%")
print("Рекомендация: ", recommendation)