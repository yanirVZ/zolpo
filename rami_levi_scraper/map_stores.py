import os
import json

def map_stores():
    stores_mapping = {}
    folder = r"C:\zolpo\rami_levi_prices_stores"  # תיקיית ה-JSON
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                store_data = json.load(f)
                stores_mapping[filename] = store_data

    # שמירת המיפוי לקובץ JSON
    with open('stores_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(stores_mapping, f, ensure_ascii=False, indent=4)

    print(f"📦 מיפוי סניפים נשמר ב-stores_mapping.json")

# קריאה למיפוי הסניפים
map_stores()
