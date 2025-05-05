import os
import json
import schedule
import time
import sys
from datetime import datetime

FOLDER = r"C:\zolpo\ramilevi\rami_levi_prices_stores_auto"  # תיקיית קבצי ה-JSON
OUTPUT_FILE = "stores_mapping_auto.json"

def map_stores():
    print(f"\n🗺️ התחלת מיפוי סניפים ב־{datetime.now().strftime('%H:%M:%S')}...")
    stores_mapping = {}

    for filename in os.listdir(FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(FOLDER, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    store_data = json.load(f)
                    stores_mapping[filename] = store_data
            except Exception as e:
                print(f"⚠️ שגיאה בקריאת {filename}: {e}")

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(stores_mapping, f, ensure_ascii=False, indent=4)
        print(f"✅ מיפוי נשמר ב־{OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ שגיאה בשמירה לקובץ {OUTPUT_FILE}: {e}")

    print("🛑 התהליך הסתיים אוטומטית.\n")
    sys.exit()

# תזמון ל־07:00
schedule.every().day.at("10:58").do(map_stores)

if __name__ == "__main__":
    print("⏳ ממתין להפעלת מיפוי סניפים ב־07:00...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הופסק ידנית.")
            break
