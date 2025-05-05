import xml.etree.ElementTree as ET
import os
import json
import schedule
import time
import sys
from datetime import datetime

FOLDER = r"C:\zolpo\osherad\osherad_prices_stores_auto"  # תיקיית קבצי ה-XML

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        store_data = []

        # גישה למסלול הנכון: Root > SubChains > SubChain > Stores > Store
        for subchain in root.findall('.//SubChain'):
            stores = subchain.find('Stores')
            if stores is not None:
                for store in stores.findall('Store'):
                    store_info = {}
                    store_id_elem = store.find('StoreId')
                    store_name_elem = store.find('StoreName')

                    if store_id_elem is not None and store_name_elem is not None:
                        store_info["StoreID"] = store_id_elem.text
                        store_info["StoreName"] = store_name_elem.text
                        store_data.append(store_info)

        json_file_path = file_path.replace('.xml', '.json')
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(store_data, json_file, ensure_ascii=False, indent=4)

        print(f"✅ המרת {file_path} ל-JSON הצליחה")
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

schedule.every().day.at("13:32").do(convert_all_xml_to_json)

if __name__ == "__main__":
    print("⏳ ממתין להפעלה יומית ב־10:53...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הופסק ידנית.")
            break
