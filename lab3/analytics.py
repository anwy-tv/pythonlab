"""
Лабораторная работа №3, задание 2.
Аналитика успеваемости студентов (NumPy).

- таблица оценок: 22 студента x 5 предметов (шкала 2-5);
- средний балл каждого студента, лучшие и худшие;
- средний балл по каждому предмету, самая простая и самая сложная дисциплина;
- распределение стипендиального фонда.
"""

import numpy as np


SEED = 42
MIN_MARK, MAX_MARK = 1, 10    
PASS_MARK = 4                 

SCHOLARSHIP_FUND = 8_500.00   
TOP_N = 3                     
HIGH_AVG = 8.0                
HIGH_BONUS = 1.4             

SUBJECTS = np.array(["оптика  ", "основы радиоэлектроники  ", "дифференциальные уравнения  ", "современная политэкономия  ", "ТВиМС"])

# условная "сложность" предметов: средняя отметка по группе до учёта способностей студентов
SUBJECT_MEAN = np.array([7.0, 6.2, 8.6, 7.6, 7.8])

STUDENTS = np.array([
    "Азарчик", "Мирчук", "Марко", "Ясюк", "Кивель", "Гурский",
    "Тихонова", "Аптыкаева", "Глебко", "Банчук", "Бардышев", "Макуркин",
    "Станчик", "Мурков", "Комалов", "Мацкевич", "Маляревич", "Лопухов",
    "Радьков", "Есеневич", "Малаховский", "Пахомов",
])


def generate_grades() -> np.ndarray:
    rng = np.random.default_rng(SEED)
    n_st, n_sub = len(STUDENTS), len(SUBJECTS)
    ability = rng.normal(0, 1.3, size=(n_st, 1))      # у каждого студента свой уровень
    noise = rng.normal(0, 1.0, size=(n_st, n_sub))    # случайный разброс по предметам
    raw = SUBJECT_MEAN + ability + noise
    return np.clip(np.rint(raw), MIN_MARK, MAX_MARK).astype(int)



def distribute_scholarship(grades: np.ndarray, avg: np.ndarray) -> np.ndarray:
    eligible = grades.min(axis=1) >= PASS_MARK
    weights = np.where(avg >= HIGH_AVG, HIGH_BONUS, 1.0) * eligible
    if weights.sum() == 0:
        return np.zeros(len(avg))

    total_kop = int(round(SCHOLARSHIP_FUND * 100))
    exact = total_kop * weights / weights.sum()
    kop = np.floor(exact).astype(int)
    rest = total_kop - kop.sum()
    kop[np.argsort(-(exact - kop), kind="stable")[:rest]] += 1
    return kop / 100


def fmt_money(x: float) -> str:
    return f"{x:,.2f}".replace(",", " ")


def build_report(grades: np.ndarray) -> str:
    avg_student = grades.mean(axis=1)          # средний балл студентов
    avg_subject = grades.mean(axis=0)          # средний балл по предметам
    payout = distribute_scholarship(grades, avg_student)

    lines = []
    add = lines.append

    # 1. Таблица оценок
    col = 18
    header = (f"{'Студент':<14}" + "".join(f"{s:>{col}}" for s in SUBJECTS)
              + f"{'Средний':>10}{'Стипендия':>12}")
    add(header)
    add("-" * len(header))
    for i, name in enumerate(STUDENTS):
        row = "".join(f"{g:>{col}}" for g in grades[i])
        add(f"{name:<14}{row}{avg_student[i]:>10.2f}{payout[i]:>12.2f}")
    add("-" * len(header))
    add(f"{'Ср. по предм.':<14}" + "".join(f"{a:>{col}.2f}" for a in avg_subject)
        + f"{avg_student.mean():>10.2f}{payout.sum():>12.2f}")

    # 2. Лучшие и худшие студенты
    best = np.argsort(-avg_student, kind="stable")[:TOP_N]
    worst = np.argsort(avg_student, kind="stable")[:TOP_N]
    add(f"\nЛучшие студенты (топ-{TOP_N}):")
    for i in best:
        add(f"  {STUDENTS[i]:<14} {avg_student[i]:.2f}")
    add(f"Худшие студенты (топ-{TOP_N}):")
    for i in worst:
        add(f"  {STUDENTS[i]:<14} {avg_student[i]:.2f}")

    # 3. Самая простая и самая сложная дисциплина 
    easy = np.flatnonzero(np.isclose(avg_subject, avg_subject.max()))
    hard = np.flatnonzero(np.isclose(avg_subject, avg_subject.min()))
    add(f"\nСамая простая дисциплина: {', '.join(SUBJECTS[easy])} "
        f"(средний балл {avg_subject[easy[0]]:.2f})")
    add(f"Самая сложная дисциплина: {', '.join(SUBJECTS[hard])} "
        f"(средний балл {avg_subject[hard[0]]:.2f})")

    # дополнительно: число неудовлетворительных отметок (1-3) по предметам
    fails = (grades < PASS_MARK).sum(axis=0)
    add("Неудовлетворительных отметок (ниже 4) по предметам: "
        + ", ".join(f"{s} - {n}" for s, n in zip(SUBJECTS, fails)))

    # 4. Стипендия
    n_paid = int((payout > 0).sum())
    add(f"\nСтипендиальный фонд: {fmt_money(SCHOLARSHIP_FUND)} BYN")
    add(f"Получают стипендию: {n_paid} из {len(STUDENTS)} студентов")
    if n_paid:
        add(f"Размер выплаты: от {fmt_money(payout[payout > 0].min())} "
            f"до {fmt_money(payout.max())} BYN")
    for i in np.argsort(-payout, kind="stable")[:n_paid]:
        add(f"  {STUDENTS[i]:<14} {payout[i]:>10.2f} BYN (средний {avg_student[i]:.2f})")

    return "\n".join(lines)


def save_table(grades: np.ndarray, path: str = "grades.csv") -> None:
    header = "Студент;" + ";".join(SUBJECTS)
    rows = np.column_stack([STUDENTS, grades.astype(str)])
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        f.write(header + "\n")
        for r in rows:
            f.write(";".join(r) + "\n")


def main() -> None:
    grades = generate_grades()
    report = build_report(grades)
    print(report)
    save_table(grades)
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report + "\n")
    print("\nСохранено: grades.csv, report.txt")


if __name__ == "__main__":
    main()
