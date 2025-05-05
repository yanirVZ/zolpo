import xml.etree.ElementTree as ET
import os
import json

# פונקציה לקרוא את XML ולהמיר אותו ל-JSON
def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # יצירת מילון לשמירת הנתונים
        store_data = []

        # חיפוש בתוך Root ולא בתוך Store
        for store in root.findall('.//Store'):
            store_info = {}
            store_id_elem = store.find('StoreID')
            store_name_elem = store.find('StoreName')

            # אם אלמנטים קיימים, נוסיף את הערכים
            if store_id_elem is not None and store_name_elem is not None:
                store_info["StoreID"] = store_id_elem.text
                store_info["StoreName"] = store_name_elem.text
                store_data.append(store_info)

        # שמירה כקובץ JSON
        json_file_path = file_path.replace('.xml', '.json')
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(store_data, json_file, ensure_ascii=False, indent=4)

        print(f"✅ המרת {file_path} ל-JSON הצליחה")
        return json_file_path  # מחזירים את נתיב הקובץ המומר

    except Exception as e:
        print(f"⚠️ שגיאה בהמרת {file_path}: {e}")
        return None

# פונקציה להמיר את כל הקבצים בנתיב
def convert_all_xml_to_json():
    folder = r"C:\zolpo\rami_levi_prices_stores"  # תיקיית ה-XML
    for filename in os.listdir(folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder, filename)
            parse_xml(file_path)  # השתמש ב-parse_xml במקום xml_to_json

# קריאה להמיר את כל קבצי ה-XML
convert_all_xml_to_json()
