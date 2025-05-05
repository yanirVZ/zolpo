import os
import json

# פונקציה לקרוא את המיפוי מקבצי ה-JSON של הסניפים ולשמור אותו בקובץ stores_mapping.json
def create_stores_mapping():
    stores_mapping = {}
    folder = r"C:\zolpo\ramilevi\rami_levi_prices_stores"  # תיקיית ה-JSON של הסניפים
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    store_data = json.load(f)
                    
                    # אם הנתונים הם בתוך רשימה, אז נעבור עליהם
                    if isinstance(store_data, list):
                        for store in store_data:
                            store_id = store.get("StoreID")
                            store_name = store.get("StoreName")
                            if store_id and store_name:
                                stores_mapping[store_id] = store_name
                    # אם הנתונים הם במבנה של מילון, ניגש אליהם ישירות
                    elif isinstance(store_data, dict):
                        store_id = store_data.get("StoreID")
                        store_name = store_data.get("StoreName")
                        if store_id and store_name:
                            stores_mapping[store_id] = store_name
                except Exception as e:
                    print(f"⚠️ שגיאה בקובץ {file_path}: {e}")
    
    # שמור את המיפוי בקובץ stores_mapping.json
    with open(r"C:\zolpo\rami_levi_prices_stores\stores_mapping.json", 'w', encoding='utf-8') as f:
        json.dump(stores_mapping, f, ensure_ascii=False, indent=4)

    print(f"📦 מיפוי הסניפים נשמר ב-stores_mapping.json")

# קריאה לפונקציה
create_stores_mapping()
