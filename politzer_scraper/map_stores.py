import os
import json

def create_flat_store_mapping():
    flat_mapping = {}
    folder = r"C:\zolpo\politzer\politzer_prices_stores_auto"  # תיקיית קבצי ה-JSON

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                stores = json.load(f)
                for store in stores:
                    store_id = store.get("StoreID")
                    store_name = store.get("StoreName")
                    if store_id and store_name:
                        flat_mapping[store_id.zfill(3)] = store_name  # אפס מוביל אם צריך

    # שמירת המיפוי לקובץ JSON
    output_path = os.path.join(folder, 'flat_store_mapping_politzer.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(flat_mapping, f, ensure_ascii=False, indent=4)

    print(f"📦 מיפוי סניפים שטוח נשמר ב: {output_path}")

# קריאה למיפוי
if __name__ == "__main__":
    create_flat_store_mapping()
