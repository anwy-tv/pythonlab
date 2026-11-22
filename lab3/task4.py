# Датасет: Student Depression Dataset (Kaggle) — студенты вузов Бангладеш.
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Student_Depression_Dataset.csv"
OUT_DIR = BASE_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)


def section(title: str) -> None:
    print("\n" + "=" * 80 + f"\n{title}\n" + "=" * 80)


# pandas
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

section("1. Первые строки и размер данных")
print(df.head())
print("Размер:", df.shape)

section("2. Типы данных")
print(df.dtypes)
df.info()

section("3. Описательная статистика")
print("Числовые признаки:")
print(df.describe().T)
print("\nКатегориальные признаки:")
print(df.describe(include=["object", "string"]).T)

section("4. Пропущенные значения")
missing_before = df.isna().sum()
print(missing_before)
print("Всего пропусков:", int(missing_before.sum()))

# заполнение: числовые - медиана, категориальные - мода.
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = [c for c in df.columns if c not in num_cols]

for col in num_cols:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].median())
for col in cat_cols:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].mode()[0])
print("Пропусков после заполнения:", int(df.isna().sum().sum()))

section("5. Полные дубликаты")
n_dup = int(df.duplicated().sum())
print("Найдено полных дубликатов:", n_dup)
df = df.drop_duplicates().reset_index(drop=True)
print("Размер после удаления:", df.shape)

section("6. Новые числовые столбцы")
# бинарная кодировка целевого признака (среднее = доля депрессии)
df["Depression_flag"] = (df["Depression"] == "Yes").astype(int)
# сколько лет студент уже учится
df["Study_years"] = df["Current_semester"] / 2
# расходы в тысячах
df["Cost_thousands"] = df["Cost_without_study"] / 1000
print(df[["Current_semester", "Study_years", "Cost_without_study",
          "Cost_thousands", "Depression", "Depression_flag"]].head())

section("7. Матрица корреляции (Пирсон)")
num_cols = df.select_dtypes(include="number").columns.tolist()
corr_cols = ["Age", "Current_semester", "CGPA", "Cost_without_study", "Depression_flag"]
corr = df[corr_cols].corr().round(3)
print(corr)
corr.to_csv(OUT_DIR / "correlation_matrix.csv")

section("8. Группировка по главному категориальному признаку (Health_condition)")
# ключевой числовой показатель — CGPA
group_stats = (
    df.groupby("Health_condition")
    .agg(
        count=("CGPA", "size"),
        mean_CGPA=("CGPA", "mean"),
        median_CGPA=("CGPA", "median"),
        depression_rate=("Depression_flag", "mean"),
    )
    .round(3)
    .sort_values("depression_rate", ascending=False)
)
print(group_stats)
group_stats.to_csv(OUT_DIR / "group_stats_health.csv")

section("9. Сводная таблица: доля депрессии, % (состояние здоровья × достаток семьи)")
pivot = (
    df.pivot_table(
        index="Health_condition",
        columns="Family_background",
        values="Depression_flag",
        aggfunc="mean",
    )
    * 100
).round(1)
pivot = pivot.loc[["Good", "Normal", "Abnormal", "Critical"],
                  ["Lower Middle class", "Middle class", "Rich class"]]
print(pivot)
pivot.to_csv(OUT_DIR / "pivot_depression_rate.csv")

section("10. Топ-5 после фильтрации")
# фильтр: студенты с хорошей успеваемостью (CGPA >= 3.5)
filtered = df[df["CGPA"] >= 3.5]
print(f"После фильтра CGPA >= 3.5 осталось {len(filtered)} из {len(df)} записей")
top5_regions = (
    filtered.groupby("Home_division")
    .agg(count=("Depression_flag", "size"),
         depression_rate=("Depression_flag", "mean"),
         mean_CGPA=("CGPA", "mean"))
    .query("count >= 30")          # отсекаем малые группы
    .sort_values("depression_rate", ascending=False)
    .head(5)
    .round(3)
)
print("Топ-5 регионов с наибольшей долей депрессии среди студентов с CGPA >= 3.5:")
print(top5_regions)
top5_regions.to_csv(OUT_DIR / "top5_regions.csv")

df.to_csv(OUT_DIR / "dataset_clean.csv", index=False)

# plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# шаблон для всех графиков
pio.templates["lab"] = go.layout.Template(
    layout=dict(
        template="plotly_white",
        font=dict(family="Arial", size=14),
        title=dict(x=0.5, font=dict(size=20)),
        colorway=["#2E6F9E", "#E07B39", "#4C9F70", "#B5485D", "#8A6FBF"],
        margin=dict(l=70, r=40, t=80, b=60),
    )
)
pio.templates.default = "lab"

ORDER = ["Good", "Normal", "Abnormal", "Critical"]

# столбчатая диаграмма на основе сводной таблицы (группированная)
bar_df = pivot.reset_index().melt(
    id_vars="Health_condition", var_name="Family_background", value_name="Depression_rate"
)
fig1 = px.bar(
    bar_df, x="Health_condition", y="Depression_rate", color="Family_background",
    barmode="group", text="Depression_rate",
    category_orders={"Health_condition": ORDER},
    title="Доля депрессии по состоянию здоровья и достатку семьи",
    labels={"Health_condition": "Состояние здоровья",
            "Depression_rate": "Доля депрессии, %",
            "Family_background": "Достаток семьи"},
)
fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig1.update_yaxes(range=[0, 115])
fig1.write_html(OUT_DIR / "1_bar_depression_rate.html")

fig2 = px.box(
    df, x="Health_condition", y="CGPA", color="Health_condition",
    points="outliers",
    category_orders={"Health_condition": ORDER},
    title="Распределение CGPA по состоянию здоровья",
    labels={"Health_condition": "Состояние здоровья", "CGPA": "CGPA (средний балл)"},
)
fig2.update_layout(showlegend=False)
fig2.write_html(OUT_DIR / "2_box_cgpa_by_health.html")

# Точечная диаграмма + линия тренда (scatter потому что дат нет в датасете)
x = df["Cost_without_study"].to_numpy()
y = df["CGPA"].to_numpy()
slope, intercept = np.polyfit(x, y, 1)
r = np.corrcoef(x, y)[0, 1]
x_line = np.linspace(x.min(), x.max(), 100)

fig3 = px.scatter(
    df, x="Cost_without_study", y="CGPA", opacity=0.45,
    title=f"Расходы вне учёбы и CGPA (r = {r:.2f})",
    labels={"Cost_without_study": "Расходы вне учёбы (в месяц)",
            "CGPA": "CGPA (средний балл)"},
)
fig3.add_trace(go.Scatter(
    x=x_line, y=slope * x_line + intercept, mode="lines",
    name="Линия тренда", line=dict(color="#B5485D", width=3),
))
fig3.update_layout(legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"))
fig3.write_html(OUT_DIR / "3_scatter_cost_cgpa.html")

# Тепловая карта сводной таблицы
fig4 = px.imshow(
    pivot, text_auto=".1f", aspect="auto",
    color_continuous_scale="RdYlBu_r",
    title="Доля депрессии (%): состояние здоровья × достаток семьи",
    labels=dict(x="Достаток семьи", y="Состояние здоровья",
                color="Доля депрессии, %"),
)
fig4.write_html(OUT_DIR / "4_heatmap_pivot.html")

print("\nГотово. Графики и таблицы сохранены в:", OUT_DIR)
for f in (fig1, fig2, fig3, fig4):
    f.show()   
