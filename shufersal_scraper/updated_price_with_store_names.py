import json
import os
from datetime import datetime
from collections import OrderedDict

def load_store_mapping():
    mapping_file = r"C:\zolpo\shufersal\flat_store_mapping_shufersal.json"
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            store_mapping = json.load(f)
        print(f"📦 נטען מיפוי של {len(store_mapping)} סניפים מקובץ flat_store_mapping_shufersal.json")
        return store_mapping
    except Exception as e:
        print(f"⚠️ שגיאה בטעינת מיפוי: {e}")
        return {}

def update_price_files():
    print(f"\n🛠️ התחלת עדכון קבצי Price בשעה {datetime.now().strftime('%H:%M:%S')}...")

    store_mapping = load_store_mapping()
    if not store_mapping:
        print("❌ מיפוי הסניפים ריק — מפסיקים תהליך.")
        return

    input_folder = r"C:\zolpo\shufersal\json_files_names"
    output_folder = r"C:\zolpo\shufersal\json_files_updated_names"
    os.makedirs(output_folder, exist_ok=True)

    updated_files = 0
    total_files = 0

    for filename in os.listdir(input_folder):
        if filename.endswith(".json") and ("Price" in filename or "price" in filename):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            total_files += 1

            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    price_data = json.load(f)

                root = price_data.get("root", {})
                store_id = root.get("StoreId")
                store_id_fixed = store_id.zfill(3) if store_id else None
                store_name = store_mapping.get(store_id_fixed, "לא נמצא")

                # סדר חדש עם StoreName לפני StoreId
                new_root = OrderedDict()
                new_root["StoreName"] = store_name
                for key, value in root.items():
                    new_root[key] = value

                price_data["root"] = new_root

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(price_data, f, ensure_ascii=False, indent=4)

                updated_files += 1
                print(f"✅ עודכן: {filename}")

            except json.JSONDecodeError:
                print(f"⚠️ שגיאת JSON בקובץ {filename}, מדלגים.")
            except Exception as e:
                print(f"⚠️ שגיאה בקובץ {filename}: {e}")

    print(f"\n📄 סיום: עודכנו {updated_files} מתוך {total_files} קבצים.")
    print("🛑 התהליך הושלם.\n")

if __name__ == "__main__":
    update_price_files()
