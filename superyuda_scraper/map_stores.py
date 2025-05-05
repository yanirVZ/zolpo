import os
import json

def create_flat_store_mapping():
    flat_mapping = {}
    folder = r"C:\zolpo\superyuda\superyuda_prices_stores_auto"

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    stores = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ שגיאה בקריאת JSON מתוך הקובץ: {filename}")
                continue

            if not isinstance(stores, list):
                print(f"⚠️ Warning: הקובץ {filename} לא מכיל רשימת אובייקטים")
                continue

            for store in stores:
                if isinstance(store, dict):  # ← זה מונע את השגיאה
                    store_id = store.get("StoreID")
                    store_name = store.get("StoreName")
                    if store_id and store_name:
                        flat_mapping[store_id.zfill(3)] = store_name
                else:
                    print(f"⚠️ Warning: קובץ {filename} מכיל רשומה שהיא לא dict: {store}")

    output_path = os.path.join(folder, 'flat_store_mapping_superyuda.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(flat_mapping, f, ensure_ascii=False, indent=4)

    print(f"📦 מיפוי סניפים נשמר ב: {output_path}")

if __name__ == "__main__":
    create_flat_store_mapping()
