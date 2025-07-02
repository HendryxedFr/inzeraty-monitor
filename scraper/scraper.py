import hashlib
import json
import os
from datetime import datetime

# Simulované získání inzerátů (nahraď reálným scrapingem)
def fetch_ads_for_filter(filter_data):
    # Napodobené výsledky – každý běh bude jiný pro test
    return [
        {"title": f"{filter_data['name']} iPhone 13", "price": 6500, "location": "Praha", "url": "https://bazos.cz/inzerat1"},
        {"title": f"{filter_data['name']} iPhone 14", "price": 8000, "location": "Brno", "url": "https://bazos.cz/inzerat2"}
    ]

def get_ad_hash(ad):
    return hashlib.md5((ad['title'] + str(ad['price']) + ad['location']).encode()).hexdigest()

def load_seen_hashes(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_hashes(filename, hashes):
    with open(filename, "w") as f:
        json.dump(list(hashes), f)

def main():
    with open("filters.json", "r") as f:
        filters = json.load(f)

    for filt in filters:
        filter_id = filt["id"]
        ads = fetch_ads_for_filter(filt)

        hash_file = f"seen_hashes/{filter_id}_hashes.json"
        output_file = f"output/{filter_id}.json"
        os.makedirs("seen_hashes", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        seen_hashes = load_seen_hashes(hash_file)
        new_ads = []
        for ad in ads:
            ad_hash = get_ad_hash(ad)
            if ad_hash not in seen_hashes:
                ad["timestamp"] = datetime.utcnow().isoformat()
                new_ads.append(ad)
                seen_hashes.add(ad_hash)

        if new_ads:
            with open(output_file, "w") as f:
                json.dump(new_ads, f, indent=2, ensure_ascii=False)
            save_seen_hashes(hash_file, seen_hashes)

if __name__ == "__main__":
    main()