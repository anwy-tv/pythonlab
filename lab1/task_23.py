def read_items(title):
    # категории: жилье, питание, транспорт, развлечения, +сбережения
    items = {}
    print(title)
    while True:
        name = input("категория: ").lower()
        if name == "":
            break
        amount = float(input(f"сумма ({name}): "))
        if name in items:
            items[name] += amount
        else:
            items[name] = amount
    return items


def total(items):
    result = 0
    for name in items:
        result += items[name]
    return result


norms = {"жилье": 75, "питание": 10, "транспорт": 6, "развлечения": 3}
saving_norm = 6

print("личный финансовый помощник")
incomes = read_items("введите доходы за месяц")
expenses = read_items("введите расходы за месяц")

income_sum = total(incomes)
expense_sum = total(expenses)
balance = income_sum - expense_sum

if income_sum == 0:
    print("доходов нет, анализ невозможен")
else:
    print("\nанализ")
    print(f"общий доход: {income_sum:.2f}")
    print(f"общие расходы: {expense_sum:.2f}")
    print(f"остаток: {balance:.2f}")

    print("\nрасходы по категориям:")
    biggest = ""
    biggest_sum = -1
    for name in expenses:
        share = expenses[name] / income_sum * 100
        print(f"{name}: {expenses[name]:.2f} ({share:.1f}% от дохода)")
        if expenses[name] > biggest_sum:
            biggest_sum = expenses[name]
            biggest = name
    if biggest != "":
        print(f"больше всего тратится на: {biggest} ({biggest_sum:.2f})")

    savings_percent = balance / income_sum * 100
    print(f"доля дохода, которая остается: {savings_percent:.1f}%")

    print("\nрекомендации по расходам")
    can_save = 0 
    problems = False

    if balance < 0:
        print(f"расходы превышают доходы на {-balance:.2f}, нужно тратить меньше)")
        problems = True

    for name in expenses:
        share = expenses[name] / income_sum * 100
        if name in norms:
            if share > norms[name]:
                limit = income_sum * norms[name] / 100
                diff = expenses[name] - limit
                can_save += diff
                print(f"{name}: {share:.1f}% при норме {norms[name]}%, можно сократить на {diff:.2f}")
                problems = True
        elif share > 15:
            print(f"{name}: занимает {share:.1f}% дохода, проверьте, все ли траты нужны")
            problems = True

    if problems == False:
        print("норма расходов не превышена, все в порядке")
    elif can_save > 0:
        print(f"если уложиться в нормы, можно экономить еще {can_save:.2f} в месяц")

    print("\nсбережения")
    saving_goal = income_sum * saving_norm / 100
    if balance >= saving_goal:
        print(f"вы откладываете {balance:.2f}, это не меньше {saving_norm}% дохода ({saving_goal:.2f})")
    else:
        print(f"рекомендуется откладывать {saving_norm}% дохода - {saving_goal:.2f} в месяц")
        if balance > 0:
            print(f"сейчас остается {balance:.2f}, не хватает {saving_goal - balance:.2f}")
        else:
            print("сейчас отложить ничего не получается")

    current_savings = float(input("\nсколько у вас сейчас накоплено? - "))
    if expense_sum > 0:
        reserve = expense_sum * 3  
        months_covered = current_savings / expense_sum
        print(f"накоплений хватит на {months_covered:.1f} мес. расходов")
        if current_savings >= reserve:
            print("финансовая подушка (3 месяца расходов) есть")
        else:
            print(f"рекомендуемая финансовая подушка - {reserve:.2f}, не хватает {reserve - current_savings:.2f}")
            if balance > 0:
                months = int((reserve - current_savings) // balance)
                if months * balance < reserve - current_savings:
                    months += 1
                print(f"при текущем остатке подушку можно собрать за {months} мес.")

    print("\nпланирование крупных расходов")
    print("введите крупные покупки: ")
    while True:
        goal = input("что вы хотите купить? -  ")
        if goal == "":
            break
        cost = float(input("стоимость: "))
        term = int(input("за сколько месяцев хотите накопить: "))
        need = cost / term
        print(f"чтобы купить {goal} за {term} мес., нужно откладывать {need:.2f} в месяц")
        if balance >= need:
            print("текущего остатка хватает, цель реальна")
        elif balance + can_save >= need:
            print(f"сейчас остатка не хватает, нужно еще поднакопить")
        elif balance > 0:
            months = int(cost // balance)
            if months * balance < cost:
                months += 1
            print(f"за это время не получится накопить, при текущем остатке вы накопите за {months} мес.")
        else:
            print("ваши расходы превышают доходы, так накопить не получится")