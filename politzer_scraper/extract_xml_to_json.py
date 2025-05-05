import xml.etree.ElementTree as ET
import os
import json
import schedule
import time
import sys
from datetime import datetime

FOLDER = r"C:\zolpo\politzer\politzer_prices_stores_auto"

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        store_data = []

        # גישה נכונה: Root > SubChains > SubChain > Stores > Store
        subchains_root = root.find('SubChains')
        if subchains_root is not None:
            for subchain in subchains_root.findall('SubChain'):
                stores = subchain.find('Stores')
                if stores is not None:
                    for store in stores.findall('Store'):
                        store_id_elem = store.find('StoreID')
                        store_name_elem = store.find('StoreName')

                        if store_id_elem is not None and store_name_elem is not None:
                            store_data.append({
                                "StoreID": store_id_elem.text.strip(),
                                "StoreName": store_name_elem.text.strip()
                            })

        # כתיבת JSON רק אם נמצא משהו
        json_file_path = file_path.replace('.xml', '.json')
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(store_data, json_file, ensure_ascii=False, indent=4)

        if store_data:
            print(f"✅ המרת {file_path} ל-JSON הצליחה ({len(store_data)} סניפים)")
        else:
            print(f"⚠️ לא נמצאו סניפים בקובץ: {file_path}")

        return json_file_path

    except Exception as e:
        print(f"⚠️ שגיאה בהמרת {file_path}: {e}")
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
schedule.every().day.at("14:50").do(convert_all_xml_to_json)

if __name__ == "__main__":
    print("⏳ ממתין להפעלה יומית ב־14:47...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הופסק ידנית.")
            break
