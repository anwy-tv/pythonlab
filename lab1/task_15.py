sales = [
    {"name": "латте", "price": 8, "quantity": 50},
    {"name": "капучино", "price": 8, "quantity": 60},
    {"name": "раф", "price": 10, "quantity": 25},
    {"name": "американо", "price": 5, "quantity": 20},
    {"name": "чизкейк", "price": 9, "quantity": 20},
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
