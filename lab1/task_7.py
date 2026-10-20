minutes = int(input("количество минут разговора: "))
messages = int(input("кол-во отправленных смс: "))
internet = int(input("количество израсходованного интернета(мб): "))
payment = 24.99
tax = 1.002

print("базовая сумма тарификации: ", payment)

if internet > 1000:
    add_internet = internet - 1000
    payment += add_internet * 0.79
    print(f"вы потратили лишние {add_internet} мегабайт(-а): + {round(add_internet, 2) * 0.79} рублей")
if minutes > 60:
    add_minutes = minutes - 60
    payment += add_minutes * 0.89
    print(f"вы потратили лишние {add_minutes} минут(-ы): + {round(add_minutes, 2) * 0.89} рублей")
if messages > 30:
    add_sms = messages - 30
    payment += add_sms * 0.59
    print(f"Вы отправили лишние {add_sms} сообщений: + {round(add_sms * 0.59, 2)} рублей")

print("налог: 2%")
payment = round(payment * tax, 2)
print(f"итоговая сумма: {payment}")