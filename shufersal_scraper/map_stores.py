import os
import json

def create_flat_store_mapping():
    input_path = r"C:\zolpo\shufersal\shufersal_mapping_stores.json"
    output_path = r"C:\zolpo\shufersal\flat_store_mapping_shufersal.json"

    if not os.path.exists(input_path):
        print(f"❌ קובץ המקור לא נמצא: {input_path}")
        return

    flat_mapping = {}

    with open(input_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)
        for store in stores:
            store_id = str(store.get("StoreID"))
            store_name = store.get("StoreName")
            if store_id and store_name:
                flat_mapping[store_id.zfill(3)] = store_name

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(flat_mapping, f, ensure_ascii=False, indent=4)

    print(f"📦 מיפוי סניפים שטוח נשמר ב: {output_path}")

# קריאה ישירה
if __name__ == "__main__":
    create_flat_store_mapping()
