import os
import gzip
import json
import xmltodict
import schedule
import time
import sys
from datetime import datetime

# נתיבי קלט ופלט
input_folder = r"C:\zolpo\tivtaam\tivtaamprices_auto"
output_folder = r"C:\zolpo\tivtaam\tivtaamprices_auto_json"
os.makedirs(output_folder, exist_ok=True)

def convert_gz_to_json():
    print(f"\n🌅 התחלת המרה אוטומטית בשעה {datetime.now().strftime('%H:%M:%S')}...")
    count = 0

    for filename in os.listdir(input_folder):
        if filename.endswith(".gz"):
            gz_path = os.path.join(input_folder, filename)
            json_path = os.path.join(output_folder, filename.replace(".gz", ".json"))

            try:
                with gzip.open(gz_path, 'rt', encoding='utf-8-sig') as f:
                    xml_text = f.read()
                    data = xmltodict.parse(xml_text)

                with open(json_path, 'w', encoding='utf-8') as out_f:
                    json.dump(data, out_f, indent=2, ensure_ascii=False)

                print(f"✅ הומר: {filename}")
                count += 1
            except Exception as e:
                print(f"⚠️ שגיאה ב־{filename}: {e}")

    print(f"\n📦 הסתיים. הומרו {count} קבצים.")
    print("🛑 התכנית הסתיימה אוטומטית.\n")
    sys.exit()

# תזמון משימה יומית לשעה 10:36 בבוקר
schedule.every().day.at("10:01").do(convert_gz_to_json)

# הרצה תמידית של הבדיקה
if __name__ == "__main__":
    print("⏳ ממתין ל־10:36 לביצוע המרה יומית מ־GZ ל־JSON...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 בוצעה יציאה ידנית.")
            break
