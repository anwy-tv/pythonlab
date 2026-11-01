sales = [
    {"name": "latte", "price": 100, "quantity": 5},
    {"name": "cappuccino", "price": 100, "quantity": 12},
    {"name": "raf", "price": 100, "quantity": 8},
    {"name": "americano", "price": 100, "quantity": 13},
    {"name": "cheesecake", "price": 100, "quantity": 19},
]
print("Уникальных наименований:", len(sales))
revenue = {}
for item in sales:
    total = item["price"] * item["quantity"]
    if item["name"] in revenue:
        revenue[item["name"]] += total
    else:
        revenue[item["name"]] = total
 
print("Выручка по каждому товару:")
for name in revenue:
    print(name, "-", revenue[name])
 
# ищем самый прибыльный товар
best_name = ""
best_sum = -1
for name in revenue:
    if revenue[name] > best_sum:
        best_sum = revenue[name]
        best_name = name
 
print("Самый прибыльный товар:", best_name, "(", best_sum, ")")
