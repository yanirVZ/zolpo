import json
import os
import schedule
import time
import sys
from datetime import datetime

def load_store_mapping():
    mapping_file = r"C:\Zolpo\yohananof\yohananof_prices_stores_auto\flat_store_mapping_yohananof.json"
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            store_mapping = json.load(f)
        print(f"📦 נטען מיפוי של {len(store_mapping)} סניפים מקובץ flat_store_mapping_yohananof.json")
        return store_mapping
    except Exception as e:
        print(f"⚠️ שגיאה בטעינת מיפוי: {e}")
        return {}

def update_price_files():
    print(f"\n🛠️ התחלת עדכון קבצי Price בשעה {datetime.now().strftime('%H:%M:%S')}...")

    store_mapping = load_store_mapping()
    if not store_mapping:
        print("❌ מיפוי הסניפים ריק — מפסיקים תהליך.")
        sys.exit()

    input_folder = r"C:\Zolpo\yohananof\yohananofprices_auto_json"
    output_folder = r"C:\Zolpo\yohananof\yohananofprices_auto_json_updated"
    report_folder = r"C:\Zolpo\yohananof\reports"

    # יצירת תיקיות אם לא קיימות
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(report_folder, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    not_found_file = os.path.join(report_folder, f"store_ids_not_found_{today}.txt")
    found_file = os.path.join(report_folder, f"store_ids_found_{today}.txt")

    updated_files = 0
    total_files = 0
    not_found_ids = set()
    found_ids = set()

    for filename in os.listdir(input_folder):
        if filename.endswith(".json") and ("Price" in filename or "PriceFull" in filename):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            total_files += 1

            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    price_data = json.load(f)

                root = price_data.get("Root", {})
                store_id = root.get("StoreId", None)

                if store_id:
                    store_id_fixed = store_id.zfill(3)
                    store_name = store_mapping.get(store_id_fixed, "לא נמצא")
                    if store_name == "לא נמצא":
                        not_found_ids.add(store_id_fixed)
                        print(f"⚠️ סניף עם StoreId {store_id_fixed} לא נמצא במיפוי.")
                    else:
                        found_ids.add(store_id_fixed)
                    root["StoreName"] = store_name
                else:
                    root["StoreName"] = "לא נמצא"

                price_data["Root"] = {key: root[key] for key in ["StoreId", "StoreName", "ChainId", "SubChainId", "BikoretNo", "DllVerNo"] if key in root}
                price_data["Root"]["Items"] = root.get("Items", {})

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(price_data, f, ensure_ascii=False, indent=4)

                updated_files += 1
                print(f"✅ עודכן ונשמר: {output_path}")

            except json.JSONDecodeError:
                print(f"⚠️ שגיאת JSON בקובץ {filename}, מדלגים.")
            except Exception as e:
                print(f"⚠️ שגיאה בקובץ {filename}: {e}")

    # כתיבת קובץ סניפים שלא נמצאו
    if not_found_ids:
        with open(not_found_file, 'w', encoding='utf-8') as f:
            for store_id in sorted(not_found_ids):
                f.write(store_id + "\n")
        print(f"📝 נוצר קובץ סניפים שלא נמצאו: {not_found_file}")
    else:
        print("✅ כל הסניפים נמצאו — אין חוסרים.")

    # כתיבת קובץ סניפים שנמצאו
    if found_ids:
        with open(found_file, 'w', encoding='utf-8') as f:
            for store_id in sorted(found_ids):
                f.write(store_id + "\n")
        print(f"📝 נוצר קובץ סניפים שנמצאו: {found_file}")

    print(f"\n📄 סיום: עודכנו {updated_files} מתוך {total_files} קבצים.")
    print("🛑 התהליך הושלם.\n")
    sys.exit()

# תזמון יומי
schedule.every().day.at("13:35").do(update_price_files)

if __name__ == "__main__":
    print("⏳ ממתין ל-11:01 לעדכון קבצי Price עם שמות סניפים...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הופסק ידנית.")
            break
