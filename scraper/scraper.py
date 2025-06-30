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
    print("Scraping Bazos...")
    ads = []
    today = datetime.today()
    seven_days_ago = today - timedelta(days=7)

    for page in range(1, 20):
        url = f"https://mobil.bazos.cz/{page}/"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.select("div.inzeraty")
        if not items:
            break

        base_url = "mobil.bazos.cz"

        for item in items:
            title_tag = item.select_one("h2.nadpis a")
            title = title_tag.text.strip() if title_tag else "Bez názvu"

            path = title_tag["href"] if title_tag and "href" in title_tag.attrs else ""
            link = f"https://{base_url}{path}" if path else ""

            date_text = item.text
            date = parse_date_from_text(date_text)
            if date and date < seven_days_ago:
                continue

            price_tag = item.select_one("div.inzeratycena b")
            price = price_tag.text.strip() if price_tag else "Neuvedeno"

            location_tag = item.select_one("div.inzeratylok")
            location = location_tag.get_text(" ", strip=True) if location_tag else "Neznámá lokalita"

            desc_tag = item.select_one("div.popis")
            desc = desc_tag.text.strip() if desc_tag else "Bez popisu"

            img_tag = item.select_one("img")
            image_path = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""
            if image_path.startswith("//"):
                image = f"https:{image_path}"
            elif image_path:
                image = f"https://{base_url}/{image_path.lstrip('/')}"
            else:
                image = ""

            ad_id = path.split("/")[-1].replace(".php", "") if path else str(uuid.uuid4())

            ads.append({
                "id": ad_id,
                "title": title,
                "price": price,
                "location": location,
                "description": desc,
                "images": [image] if image else [],
                "url": link,
                "source": "bazos",
                "date": date.strftime("%Y-%m-%d") if date else ""
            })

    return ads

if __name__ == "__main__":
    OUTPUT_FILE = "docs/data.json"
    existing_ids = load_existing_ids(OUTPUT_FILE)

    new_ads = scrap_bazos()
    filtered_ads = [ad for ad in new_ads if ad["id"] not in existing_ids]

    all_ads = list(filtered_ads)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_ads, f, ensure_ascii=False, indent=2)

    print(f"✅ Uloženo {len(all_ads)} inzerátů do {OUTPUT_FILE}")
