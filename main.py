import requests
from bs4 import BeautifulSoup
import csv
import time

# Поисковый запрос
query = input('введите название компании: ').lower().strip()
url = f"https://www.rusprofile.ru/search?query={query}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/92.0.4515.131 Safari/537.36"
}

def scrap_companies(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    companies = []
    # Находим все блоки с компаниями
    cards = soup.find_all("div", class_="list-element")

    for card in cards:
        try:
            name_tag = card.find("a", class_="list-element__title")
            name = name_tag.get_text(strip=True) if name_tag else "Нет названия"

            inn = "Не найден"
            inn_spans = card.find_all("span")
            for span in inn_spans:
                if "ИНН" in span.get_text():
                    inn = span.get_text().replace("ИНН:", "").strip()
                    break

            companies.append({"Название": name, "ИНН": inn})
        except Exception as e:
            print(f"Ошибка в карточке: {e}")

    return companies

# Сохраняем в CSV
def save_to_csv(data, filename="companies.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Название", "ИНН"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    data = scrap_companies(url)
    save_to_csv(data)