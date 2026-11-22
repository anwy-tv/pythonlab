# На странице раздела находим ссылки на все фильмы.
# На странице каждого фильма берём сеансы из блока JSON-LD (с названием, кинотеатром, временем, названием).
# Считаем статистику и сохраняем результат в файлы.

import csv
import json
import re
import time
from collections import Counter
from statistics import mean

import requests
from bs4 import BeautifulSoup

BASE = "https://ticketpro.by"
LIST_URL = BASE + "/ru/bilety-v-kino"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_soup(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def get_film_links():
    """Ссылки на фильмы со страницы раздела."""
    soup = get_soup(LIST_URL)
    hrefs = {a["href"] for a in soup.select('a[href^="/ru/event/kinoplan-release-"]')}
    return [BASE + h for h in sorted(hrefs)]


def parse_film(url):
    """Все сеансы фильма: название, дата и время, место, цена, возраст."""
    soup = get_soup(url)

    # возраст ищем в тексте страницы, например "16+"
    match = re.search(r"\b(0|6|12|14|16|18)\s*\+(?!\d)", soup.get_text(" "))
    age = match.group(1) + "+" if match else "не указано"

    sessions = []
    for script in soup.find_all("script", type="application/ld+json"):
        if not script.string:
            continue
        for item in json.loads(script.string).get("@graph", []):
            if item.get("@type") != "Event":
                continue
            sessions.append({
                "title": item["name"],
                "date_time": item["startDate"].replace("T", " ")[:16],
                "venue": item["location"]["name"],
                "price": float(str(item["offers"]["price"]).replace(",", ".")),
                "age": age,
                "url": item["url"],
            })
    return sessions


def analyze(events):
    prices = [e["price"] for e in events]
    venues = Counter(e["venue"] for e in events)
    top_venue, top_count = venues.most_common(1)[0]
    cheapest = min(events, key=lambda e: e["price"])
    priciest = max(events, key=lambda e: e["price"])
    return "\n".join([
        f"Всего сеансов: {len(events)}",
        f"Минимальная стоимость билета: {min(prices):.2f} BYN",
        f"Максимальная стоимость билета: {max(prices):.2f} BYN",
        f"Средняя стоимость билета: {mean(prices):.2f} BYN",
        f"Самая загруженная площадка: {top_venue} ({top_count} сеансов)",
        f"Самый дорогой билет: {priciest['title']}, {priciest['venue']}, "
        f"{priciest['date_time']} - {priciest['price']:.2f} BYN",
        f"Самый дешёвый билет: {cheapest['title']}, {cheapest['venue']}, "
        f"{cheapest['date_time']} - {cheapest['price']:.2f} BYN",
    ])


def main():
    events = []
    links = get_film_links()
    print(f"Найдено фильмов: {len(links)}")
    for i, url in enumerate(links, 1):
        found = parse_film(url)
        events.extend(found)
        print(f"[{i}/{len(links)}] сеансов: {len(found)}  {url}")
        time.sleep(1)  # пауза, чтобы не нагружать сайт

    if not events:
        print("Сеансы не найдены")
        return

    report = analyze(events)
    print("\n" + report)

    with open("events.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=events[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(events)
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report + "\n")


if __name__ == "__main__":
    main()