import gzip
import xmltodict
import json
import os

# נתיבים
GZ_PATH = r"C:\zolpo\shufersal\stores\shufersal_stores.gz"
JSON_FOLDER = r"C:\zolpo\shufersal\stores_json"
JSON_OUTPUT = os.path.join(JSON_FOLDER, "shufersal_stores.json")
MAPPING_OUTPUT = r"C:\zolpo\shufersal\store_id_to_name.json"

def extract_and_convert_store_file():
    if not os.path.exists(JSON_FOLDER):
        os.makedirs(JSON_FOLDER)

    # פתיחת GZ וקריאה
    try:
        with gzip.open(GZ_PATH, 'rb') as f_in:
            xml_data = f_in.read().decode('utf-8')
            data_dict = xmltodict.parse(xml_data)

        # שמירת JSON מלא
        with open(JSON_OUTPUT, "w", encoding="utf-8") as json_out:
            json.dump(data_dict, json_out, indent=2, ensure_ascii=False)
        print(f"✅ JSON נשמר: {JSON_OUTPUT}")

    except Exception as e:
        print(f"❌ שגיאה בקריאת או המרת GZ: {e}")
        return

    # יצירת מיפוי StoreId → StoreName
    try:
        store_mapping = {}
        stores = data_dict.get("root", {}).get("Store", [])
        if not isinstance(stores, list):
            stores = [stores]

        for store in stores:
            sid = store.get("StoreId")
            name = store.get("StoreName")
            if sid and name:
                store_mapping[sid] = name

        with open(MAPPING_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(store_mapping, f, indent=2, ensure_ascii=False)
        print(f"📦 מיפוי {len(store_mapping)} סניפים נשמר: {MAPPING_OUTPUT}")

    except Exception as e:
        print(f"❌ שגיאה ביצירת מיפוי: {e}")

if __name__ == "__main__":
    extract_and_convert_store_file()
