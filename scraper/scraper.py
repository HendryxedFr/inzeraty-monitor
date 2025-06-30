# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import uuid
from datetime import datetime, timedelta
import os

headers = {"User-Agent": "Mozilla/5.0"}

def parse_date_from_text(text):
    import re
    match = re.search(r'\[(\d{1,2})\.(\d{1,2})\.\s*(\d{4})\]', text)
    if match:
        day, month, year = map(int, match.groups())
        return datetime(year, month, day)
    return None

def load_existing_ids(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        try:
            data = json.load(f)
            return {ad["id"] for ad in data if "id" in ad}
        except:
            return set()

def scrap_bazos():
    print("🔄 Načítám Bazoš...")
    ads = []
    for page in range(1, 20):
        url = f"https://mobil.bazos.cz/{page}/"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.select("div.inzeraty")
        if not items:
            break

        for item in items:
            title_tag = item.select_one("h2.nadpis a")
            title = title_tag.text.strip() if title_tag else "Bez názvu"
            link = "https://mobil.bazos.cz" + title_tag["href"] if title_tag else ""

            price_tag = item.select_one("div.inzeratycena b")
            price = price_tag.text.strip() if price_tag else "Neuvedeno"

            location_tag = item.select_one("div.inzeratylok")
            location = location_tag.get_text(" ", strip=True) if location_tag else "Neznámá lokalita"

            desc_tag = item.select_one("div.popis")
            desc = desc_tag.text.strip() if desc_tag else "Bez popisu"

            img_tag = item.select_one("img")
            image = ""
            if img_tag and "src" in img_tag.attrs:
                src = img_tag["src"]
                image = src if src.startswith("http") else f"https:{src}" if src.startswith("//") else f"https://www.bazos.cz{src}"

            ad_id = link.split("/")[-1].replace(".php", "") if link else str(uuid.uuid4())
            ads.append({
                "id": ad_id,
                "title": title,
                "price": price,
                "location": location,
                "description": desc,
                "images": [image] if image else [],
                "url": link,
                "source": "bazos",
                "date": datetime.today().strftime("%Y-%m-%d")
            })
    return ads

def scrap_sbazar():
    print("🔄 Načítám Sbazar...")
    ads = []
    for page in range(1, 30):
        url = f"https://www.sbazar.cz/lista/mobil-telefony?page={page}"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("li[data-offer-id]")

        for item in items:
            ad_id = item.get("data-offer-id", str(uuid.uuid4()))
            a_tag = item.select_one("a[href]")
            url_full = f"https://www.sbazar.cz{a_tag['href']}" if a_tag else ""

            title_tag = item.select_one("div.mt-1")
            title = title_tag.text.strip() if title_tag else "Bez názvu"

            price_tag = item.select_one("div[class*='cardLg']")
            price = price_tag.text.strip() if price_tag else "Neuvedeno"

            img_tag = item.select_one("img")
            image = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""

            ads.append({
                "id": ad_id,
                "title": title,
                "price": price,
                "location": "",
                "description": "",
                "images": [image] if image else [],
                "url": url_full,
                "source": "sbazar",
                "date": datetime.today().strftime("%Y-%m-%d")
            })
    return ads

if __name__ == "__main__":
    OUTPUT_FILE = "docs/data.json"
    existing_ids = load_existing_ids(OUTPUT_FILE)

    all_ads = scrap_bazos() + scrap_sbazar()
    filtered_ads = [ad for ad in all_ads if ad["id"] not in existing_ids]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered_ads, f, ensure_ascii=False, indent=2)

    print(f"✅ Uloženo {len(filtered_ads)} inzerátů do {OUTPUT_FILE}")