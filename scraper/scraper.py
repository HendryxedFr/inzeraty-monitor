import requests
from bs4 import BeautifulSoup
import json
import uuid
from pathlib import Path
import re
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0"}

def scrap_bazos():
    print("Scraping Bazos...")
    url = "https://mobil.bazos.cz/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ads = []
    base_url = "https://mobil.bazos.cz"

    for item in soup.select("div.inzeraty.inzeratyflex"):
        title_tag = item.select_one("h2.nadpis a")
        title = title_tag.text.strip() if title_tag else "Bez názvu"
        link = base_url + title_tag["href"] if title_tag else ""

        image_tag = item.select_one("div.inzeratynadpis img.obrazek")
        image = ""
        if image_tag:
            src = image_tag.get("src", "")
            if src.startswith("//"):
                image = "https:" + src
            else:
                image = src

        popis_tag = item.select_one("div.inzeratynadpis div.popis")
        description = popis_tag.text.strip() if popis_tag else "Bez popisu"

        price_tag = item.select_one("div.inzeratycena b")
        price = price_tag.text.strip().replace("Kč", "").strip() if price_tag else "Neuvedeno"

        location_tag = item.select_one("div.inzeratylok")
        location = location_tag.get_text(separator=" ", strip=True) if location_tag else "Neznámá lokalita"

        # Extrahuj datum přidání
        date_added = None
        date_span = item.select_one("span.velikost10")
        if date_span:
            date_text = date_span.text
            date_match = re.search(r"\[(\d{1,2}\.\d{1,2}\.\s*\d{4})\]", date_text)
            if date_match:
                date_str = date_match.group(1).strip()
                try:
                    date_obj = datetime.strptime(date_str, "%d.%m. %Y").date()
                    date_added = date_obj.isoformat()
                except ValueError:
                    date_added = None

        ads.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "price": price,
            "location": location,
            "description": description,
            "images": [image] if image else [],
            "url": link,
            "source": "bazos",
            "date_added": date_added
        })

    print(f"✅ Uloženo {len(ads)} inzerátů z Bazoš")
    return ads

if __name__ == "__main__":
    Path("docs").mkdir(parents=True, exist_ok=True)
    ads = scrap_bazos()
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(ads, f, ensure_ascii=False, indent=2)
