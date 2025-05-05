import os
import json

def create_flat_store_mapping():
    flat_mapping = {}
    folder = r"C:\zolpo\tivtaam\tivtaam_prices_stores_auto"  # ← עדכן אם צריך

    for filename in os.listdir(folder):
        if filename.endswith(".json") and not filename.startswith("flat_store_mapping"):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    store_data = json.load(f)

                if isinstance(store_data, list):
                    for store in store_data:
                        if isinstance(store, dict):
                            store_id = store.get("StoreID")
                            store_name = store.get("StoreName")
                            if store_id and store_name:
                                store_id_str = str(store_id).zfill(3)
                                flat_mapping[store_id_str] = store_name
                        else:
                            print(f"⚠️ רשומה לא תקינה בקובץ {filename}: {store}")
                else:
                    print(f"⚠️ הקובץ {filename} לא מכיל רשימת אובייקטים.")

            except Exception as e:
                print(f"❌ שגיאה בקריאת הקובץ {filename}: {e}")

    output_path = os.path.join(folder, "flat_store_mapping_tivtaam.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(flat_mapping, f, ensure_ascii=False, indent=4)

    print(f"\n📦 נוצר מיפוי שטוח של {len(flat_mapping)} סניפים ב־{output_path}")

if __name__ == "__main__":
    create_flat_store_mapping()
