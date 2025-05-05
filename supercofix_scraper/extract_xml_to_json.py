import os
import json

def create_flat_store_mapping():
    flat_mapping = {}
    folder = r"C:\zolpo\supercofix\supercofix_prices_stores_auto"

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    stores = json.load(f)
            except Exception as e:
                print(f"❌ שגיאה בקריאת הקובץ {filename}: {e}")
                continue

            for store in stores:
                if isinstance(store, dict):
                    store_id = store.get("StoreID")
                    store_name = store.get("StoreName")
                    if store_id and store_name:
                        flat_mapping[store_id.zfill(3)] = store_name
                else:
                    print(f"⚠️ Warning: קובץ {filename} מכיל רשומה לא תקינה: {store}")

    output_path = os.path.join(folder, 'flat_store_mapping_supercofix.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(flat_mapping, f, ensure_ascii=False, indent=4)

    print(f"📦 מיפוי סניפים שטוח נשמר ב: {output_path}")

if __name__ == "__main__":
    create_flat_store_mapping()
