import json
import os
import schedule
import time
import sys
from datetime import datetime

# טוען את המיפוי מקבצי ה-JSON של הסניפים
def load_store_mapping():
    store_mapping = {}
    folder = r"C:\zolpo\ramilevi\rami_levi_prices_stores_auto"
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    store_data = json.load(f)
                    for store in store_data:
                        if isinstance(store, dict) and "StoreID" in store:
                            store_mapping[store["StoreID"]] = store["StoreName"]
                        else:
                            print(f"⚠️ פורמט לא תקין בקובץ {filename}")
            except json.JSONDecodeError:
                print(f"⚠️ שגיאת JSON בקובץ {filename}, מדלגים עליו.")
            except Exception as e:
                print(f"⚠️ שגיאה בקובץ {filename}: {e}")
    return store_mapping

# עדכון קבצי ה-Price/PriceFull עם שם הסניף לפי המיפוי
def update_price_files():
    print(f"\n🛠️ התחלת עדכון קבצי Price בשעה {datetime.now().strftime('%H:%M:%S')}...")
    store_mapping = load_store_mapping()
    print(f"📌 מיפוי שהתקבל: {len(store_mapping)} סניפים")

    price_folder = r"C:\zolpo\ramilevi\rami_levi_auto_json"
    for filename in os.listdir(price_folder):
        if filename.endswith(".json") and ("Price" in filename or "PriceFull" in filename):
            file_path = os.path.join(price_folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    price_data = json.load(f)

                root = price_data.get("Root", {})
                store_id = root.get("StoreId", None)

                if store_id and store_id in store_mapping:
                    root["StoreName"] = store_mapping[store_id]
                else:
                    root["StoreName"] = "לא נמצא"

                # שימור סדר שדות והוספת Items
                price_data["Root"] = {key: root[key] for key in ["StoreId", "StoreName", "ChainId", "SubChainId", "BikoretNo", "DllVerNo"] if key in root}
                price_data["Root"]["Items"] = root.get("Items", {})

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(price_data, f, ensure_ascii=False, indent=4)

                print(f"✅ עודכן: {filename}")
            except json.JSONDecodeError:
                print(f"⚠️ שגיאת JSON בקובץ {filename}, מדלגים.")
            except Exception as e:
                print(f"⚠️ שגיאה בקובץ {filename}: {e}")

    print("🛑 התהליך הסתיים אוטומטית.\n")
    sys.exit()

# תזמון ל־07:00 בבוקר
schedule.every().day.at("11:01").do(update_price_files)

if __name__ == "__main__":
    print("⏳ ממתין ל־07:00 לעדכון קבצי Price עם שמות הסניפים...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הופסק ידנית.")
            break
