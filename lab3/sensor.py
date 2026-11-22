"""
Лабораторная работа №3, задание 3.
Аналитика работы датчика температуры в теплице (SciPy).

1. scipy.interpolate  - восстановление температуры на каждый час;
2. scipy.optimize     - поиск максимума и минимума (minimize_scalar);
3. scipy.integrate    - средняя температура за сутки (quad);
4. scipy.optimize.root_scalar - моменты пересечения нормы 22 °C;
5. график с исходными данными, кривой, экстремумами и линией нормы.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar, root_scalar
from scipy.integrate import quad

# ----------------------------- ВХОДНЫЕ ДАННЫЕ -------------------------
# Датчик температуры воздуха в теплице с томатами. Система климат-контроля
# давала сбои, поэтому в записи есть пропуски:
#   03:30 - 06:00 (ночь) и 11:00 - 15:00 (самое жаркое время).
# Время - часы от начала суток (дробная часть = минуты), температура - °C.
TIMES = np.array([0.0, 1.0, 2.0, 3.5, 6.0, 7.0, 8.5, 10.0, 11.0,
                  15.0, 16.0, 17.5, 19.0, 20.0, 22.0, 23.5])
TEMPS = np.array([17.4, 16.9, 16.4, 15.8, 15.6, 16.9, 19.2, 22.8, 24.6,
                  27.1, 26.3, 24.2, 21.5, 20.1, 18.6, 17.8])

NORM = 22.0          # оптимальная температура не выше, °C
DAY_START, DAY_END = 0.0, 24.0

OUT_PLOT = "temperature.png"
OUT_CSV = "hourly_temperature.csv"
OUT_REPORT = "report.txt"


def fmt_time(hours: float) -> str:
    """7.5 -> '07:30'."""
    total_min = int(round(hours * 60))
    return f"{total_min // 60 % 24:02d}:{total_min % 60:02d}"


# ------------------------- 1. ИНТЕРПОЛЯЦИЯ ---------------------------
# Кубический сплайн даёт гладкую кривую, проходящую через все измерения.
spline = CubicSpline(TIMES, TEMPS)


def temp(t):
    return spline(t)


hours = np.arange(DAY_START, DAY_END + 1)          # 0, 1, ..., 24
hourly = temp(hours)

# --------------------- 2. МАКСИМУМ И МИНИМУМ -------------------------
# Грубая сетка находит окрестность экстремума, затем minimize_scalar
# уточняет его в пределах +-1 часа (метод bounded).
grid = np.linspace(DAY_START, DAY_END, 2401)
vals = temp(grid)


def refine(guess: float, sign: float):
    """sign=+1 - ищем минимум, sign=-1 - максимум."""
    lo, hi = max(DAY_START, guess - 1), min(DAY_END, guess + 1)
    res = minimize_scalar(lambda t: sign * float(temp(t)),
                          bounds=(lo, hi), method="bounded",
                          options={"xatol": 1e-6})
    return res.x, float(temp(res.x))


t_min, T_min = refine(grid[vals.argmin()], +1)
t_max, T_max = refine(grid[vals.argmax()], -1)

# ------------------ 3. СРЕДНЯЯ ТЕМПЕРАТУРА ЗА ДЕНЬ -------------------
# Среднее значение функции = интеграл / длина интервала.
integral, _err = quad(lambda t: float(temp(t)), DAY_START, DAY_END)
mean_temp = integral / (DAY_END - DAY_START)

# ---------------- 4. ПЕРЕСЕЧЕНИЯ ОТМЕТКИ 22 °C ------------------------
# Ищем смену знака f(t) - NORM на сетке и уточняем корень методом brentq.
def f(t):
    return float(temp(t)) - NORM


crossings = []
g = vals - NORM
for i in np.where(np.sign(g[:-1]) * np.sign(g[1:]) < 0)[0]:
    sol = root_scalar(f, bracket=(grid[i], grid[i + 1]), method="brentq", xtol=1e-9)
    direction = "превышение нормы" if g[i] < 0 else "возврат к норме"
    crossings.append((sol.root, direction))

# Суммарное время, когда температура была выше нормы
above = 0.0
edges = [DAY_START] + [c[0] for c in crossings] + [DAY_END]
for a, b in zip(edges[:-1], edges[1:]):
    if f((a + b) / 2) > 0:
        above += b - a

# ------------------------------ ОТЧЁТ -------------------------------


def build_report() -> str:
    lines = [
        "Температура воздуха в теплице за сутки",
        "",
        "Восстановленная температура по часам:",
    ]
    for h, v in zip(hours, hourly):
        measured = "  (измерено)" if h in TIMES else ""
        lines.append(f"  {fmt_time(h)}  {v:6.2f} °C{measured}")
    lines += [
        "",
        f"Максимум: {T_max:.2f} °C в {fmt_time(t_max)}",
        f"Минимум:  {T_min:.2f} °C в {fmt_time(t_min)}",
        f"Средняя температура за сутки: {mean_temp:.2f} °C",
        f"Норма: не выше {NORM:.0f} °C",
    ]
    if crossings:
        lines.append("Моменты пересечения отметки нормы:")
        for t, kind in crossings:
            lines.append(f"  {fmt_time(t)} ({t:.4f} ч) - {kind}")
        lines.append(f"Время выше нормы: {above:.2f} ч ({above * 60:.0f} мин)")
    else:
        lines.append("Отметка нормы не пересекалась.")
    return "\n".join(lines)


# ------------------------------ ГРАФИК -------------------------------


def plot() -> None:
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(grid, vals, color="tab:blue", lw=2, label="Восстановленная кривая (сплайн)")
    ax.scatter(TIMES, TEMPS, color="black", zorder=5, label="Исходные измерения")
    ax.scatter(hours, hourly, color="tab:blue", s=18, alpha=0.5, zorder=4,
               label="Значения на каждый час")
    ax.axhline(NORM, color="tab:red", ls="--", lw=1.5, label=f"Норма ({NORM:.0f} °C)")
    ax.fill_between(grid, NORM, vals, where=vals > NORM, color="tab:red", alpha=0.12,
                    label="Выше нормы")

    ax.scatter([t_max], [T_max], color="red", s=110, marker="^", zorder=6,
               label=f"Максимум: {T_max:.1f} °C ({fmt_time(t_max)})")
    ax.scatter([t_min], [T_min], color="green", s=110, marker="v", zorder=6,
               label=f"Минимум: {T_min:.1f} °C ({fmt_time(t_min)})")
    for t, kind in crossings:
        ax.scatter([t], [NORM], color="orange", edgecolor="black", s=60, zorder=6)
        dx = 6 if kind == "превышение нормы" else -40   # подпись не должна наезжать на точки
        ax.annotate(fmt_time(t), (t, NORM), textcoords="offset points",
                    xytext=(dx, -16), fontsize=9)

    # пропуски в данных
    gaps = [(a, b) for a, b in zip(TIMES[:-1], TIMES[1:]) if b - a > 2]
    for k, (a, b) in enumerate(gaps):
        ax.axvspan(a, b, color="gray", alpha=0.12, label="Пропуски в данных" if k == 0 else None)

    ax.set_title("Температура воздуха в теплице за сутки")
    ax.set_xlabel("Время суток, ч")
    ax.set_ylabel("Температура, °C")
    ax.set_xticks(range(0, 25, 2))
    ax.set_xlim(DAY_START, DAY_END)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_PLOT, dpi=150)
    plt.show()


def main() -> None:
    report = build_report()
    print(report)
    with open(OUT_REPORT, "w", encoding="utf-8") as fh:
        fh.write(report + "\n")
    np.savetxt(OUT_CSV, np.column_stack([hours, hourly]), delimiter=";",
               header="hour;temperature_C", comments="", fmt=["%d", "%.2f"])
    plot()
    print(f"\nСохранено: {OUT_REPORT}, {OUT_CSV}, {OUT_PLOT}")


if __name__ == "__main__":
    main()
