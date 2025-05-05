import xml.etree.ElementTree as ET
import os
import json
import schedule
import time
import sys
from datetime import datetime

FOLDER = r"C:\zolpo\tivtaam\tivtaam_prices_stores_auto"  # שים כאן את הנתיב שלך

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        store_data = []

        subchains_root = root.find('SubChains')
        if subchains_root is not None:
            for subchain in subchains_root.findall('SubChain'):
                stores = subchain.find('Stores')
                if stores is not None:
                    for store in stores.findall('Store'):
                        store_id_elem = store.find('StoreId')  # שים לב - לא StoreID אלא StoreId
                        store_name_elem = store.find('StoreName')

                        if store_id_elem is not None and store_name_elem is not None:
                            store_data.append({
                                "StoreID": store_id_elem.text.strip(),
                                "StoreName": store_name_elem.text.strip()
                            })

        json_file_path = file_path.replace('.xml', '.json')
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(store_data, json_file, ensure_ascii=False, indent=4)

        if store_data:
            print(f"✅ המרת {os.path.basename(file_path)} הצליחה ({len(store_data)} סניפים)")
        else:
            print(f"⚠️ לא נמצאו סניפים בקובץ: {os.path.basename(file_path)}")

        return json_file_path

    except Exception as e:
        print(f"⚠️ שגיאה בהמרת {os.path.basename(file_path)}: {e}")
        return None

def convert_all_xml_to_json():
    print(f"\n🌅 התחלת המרה ב־{datetime.now().strftime('%H:%M:%S')}...")
    count = 0
    for filename in os.listdir(FOLDER):
        if filename.endswith(".xml"):
            file_path = os.path.join(FOLDER, filename)
            if parse_xml(file_path):
                count += 1

    print(f"\n📁 הסתיים. הומרו {count} קבצים.")
    print("🛑 התכנית הסתיימה אוטומטית.")
    sys.exit()

# תזמון יומי
schedule.every().day.at("10:06").do(convert_all_xml_to_json)

if __name__ == "__main__":
    print("⏳ ממתין ל־14:47 לעיבוד קבצי סניפים...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הופסק ידנית.")
            break
