import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
import re

# נתיב לתיקיית קבצי JSON
FOLDER = r"C:\zolpo\Prices"

# התחברות ל-Firebase
cred = credentials.Certificate("C:/Users/user/zolpo/shufersal_scraper/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# מיפוי store_id -> store_name
store_name_map = {
    "001": "שלי ת\"א - בן יהודה",
    "002": "שלי ירושלים - אגרון",
    "003": "שלי גבעתיים - סירקין",
    "004": "שלי חיפה - כרמל",
    "005": "שלי ירושלים - יובל",
    "006": "שלי ת\"א - ארלוזורוב",
    "007": "שלי נתניה - ויצמן"
}

def upload_to_firebase():
    # מיון קבצים לפי מספר מתוך שם הקובץ
    json_files = sorted(
        [f for f in os.listdir(FOLDER) if f.endswith(".json")],
        key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0
    )

    for json_file in json_files:
        path = os.path.join(FOLDER, json_file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                print(f"⚠️ {json_file} לא תקין - לא קובץ JSON רגיל.")
                continue

            root = data.get("root", {})
            store_id = root.get("StoreId")
            items = root.get("Items", {}).get("Item")

            if not store_id or not items:
                print(f"⚠️ {json_file} חסר שדות נדרשים.")
                continue

            # הפוך לפריט בודד אם יש רק מוצר אחד
            if isinstance(items, dict):
                items = [items]

            count = 0
            for item in items:
                product_id = f"{store_id}_{item.get('ItemCode')}"
                db.collection("products").document(product_id).set({
                    "store_id": store_id,
                    "store_name": store_name_map.get(store_id, "לא ידוע"),
                    "name": item.get("ItemName", "לא ידוע"),
                    "price": float(item.get("ItemPrice", 0)),
                    "quantity": float(item.get("Quantity", 1)),
                })
                count += 1

            print(f"✅ הועלו {count} מוצרים מ-{json_file} (חנות {store_id})")

        except Exception as e:
            print(f"❌ שגיאה בקובץ {json_file}: {e}")

if __name__ == "__main__":
    upload_to_firebase()
