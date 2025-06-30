import requests
from bs4 import BeautifulSoup
import json
import uuid
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0"}

def scrap_bazos():
    print("Scraping Bazos...")
    url = "https://mobil.bazos.cz/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ads = []
    for item in soup.select(".inzerat"):
        title_tag = item.select_one(".nadpis a")
        title = title_tag.text.strip() if title_tag else "Bez názvu"
        link = "https://bazos.cz" + title_tag["href"] if title_tag else ""
        price_tag = item.select_one(".cena")
        price = price_tag.text.strip() if price_tag else "Neuvedeno"
        location_tag = item.select_one(".inzeraty p span.velikost")
        location = location_tag.text.strip() if location_tag else "Neznámá lokalita"
        desc = item.select("p")[1].text.strip() if len(item.select("p")) > 1 else "Bez popisu"
        img_tag = item.select_one("img")
        image = "https:" + img_tag["src"] if img_tag else ""

        ads.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "price": price,
            "location": location,
            "description": desc,
            "images": [image] if image else [],
            "url": link,
            "source": "bazos"
        })
    return ads

def scrap_sbazar():
    print("Scraping Sbazar...")
    url = "https://www.sbazar.cz/30-elektro-pocitace"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ads = []
    for item in soup.select("article.ListItem"):
        title_tag = item.select_one("h3")
        title = title_tag.text.strip() if title_tag else "Bez názvu"
        link_tag = item.select_one("a[href]")
        link = "https://www.sbazar.cz" + link_tag["href"] if link_tag else ""
        price_tag = item.select_one(".Price")
        price = price_tag.text.strip() if price_tag else "Neuvedeno"
        location_tag = item.select_one(".Locality")
        location = location_tag.text.strip() if location_tag else "Neznámá lokalita"
        desc_tag = item.select_one("p")
        desc = desc_tag.text.strip() if desc_tag else "Bez popisu"
        img_tag = item.select_one("img")
        image = img_tag["src"] if img_tag else ""

        ads.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "price": price,
            "location": location,
            "description": desc,
            "images": [image] if image else [],
            "url": link,
            "source": "sbazar"
        })
    return ads

def scrap_aukro():
    print("Scraping Aukro...")
    url = "https://aukro.cz/mobily-a-gps"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ads = []
    for item in soup.select("article.sc-bdVaJa"):
        title_tag = item.select_one("a.sc-1p2j45a-1")
        title = title_tag["title"].strip() if title_tag and "title" in title_tag.attrs else "Bez názvu"
        link = "https://aukro.cz" + title_tag["href"] if title_tag else ""
        price_tag = item.select_one("div.sc-1n4y4tv-3")
        price = price_tag.text.strip() if price_tag else "Neuvedeno"
        location = "Aukro"
        description = "Aukro inzerát – podrobnosti až na stránce"

        img_tag = item.select_one("img")
        image = img_tag["src"] if img_tag else ""

        ads.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "price": price,
            "location": location,
            "description": description,
            "images": [image] if image else [],
            "url": link,
            "source": "aukro"
        })
    return ads

if __name__ == "__main__":
    data = scrap_bazos() + scrap_sbazar() + scrap_aukro()
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
