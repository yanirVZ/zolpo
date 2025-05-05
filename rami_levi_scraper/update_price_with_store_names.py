import json
import os

# פונקציה לקרוא את המיפוי מקבצי ה-JSON של הסניפים
def load_store_mapping():
    store_mapping = {}
    folder = r"C:\zolpo\rami_levi_prices_stores"  # הנתיב לקבצי ה-JSON של הסניפים
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    store_data = json.load(f)
                    for store in store_data:
                        if isinstance(store, dict) and "StoreID" in store:
                            store_mapping[store["StoreID"]] = store["StoreName"]
                        else:
                            print(f"Warning: Store format incorrect in {filename}")
            except json.JSONDecodeError:
                print(f"⚠️ Error decoding JSON in file {filename}, skipping this file.")
            except Exception as e:
                print(f"⚠️ Error processing file {filename}: {e}")
    
    return store_mapping

# פונקציה לעדכן את קבצי ה-Price ו-PriceFull עם ה-StoreID ו-StoreName
def update_price_files():
    store_mapping = load_store_mapping()  # טוען את המיפוי
    print(f"Loaded store mapping: {store_mapping}")  # הדפסת המיפוי שהתקבל
    price_folder = r"C:\zolpo\rami_levi_json"  # תיקיית קבצי ה-Price
    for filename in os.listdir(price_folder):
        if filename.endswith(".json") and ("Price" in filename or "PriceFull" in filename):  # כולל קבצי price ו-priceFull
            file_path = os.path.join(price_folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    price_data = json.load(f)
                
                # ווידוא שהנתונים מצויים במבנה הנכון
                root = price_data.get("Root", {})
                store_id = root.get("StoreId", None)

                # הוספת StoreName ישירות אחרי StoreId
                if store_id and store_id in store_mapping:
                    root["StoreName"] = store_mapping[store_id]  # מוסיף את שם הסניף מתחת לשדה storeId
                else:
                    root["StoreName"] = "לא נמצא"  # אם אין מיפוי לשם סניף

                # שימור סדר השדות כך ש-StoreName יהיה הראשון
                price_data["Root"] = {key: root[key] for key in ["StoreId", "StoreName", "ChainId", "SubChainId", "BikoretNo", "DllVerNo"] if key in root}
                price_data["Root"]["Items"] = root.get("Items", {})

                # שמירת הקובץ עם המידע המעודכן
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(price_data, f, ensure_ascii=False, indent=4)

                print(f"✅ קובץ {filename} עודכן עם שמות הסניפים")
            except json.JSONDecodeError:
                print(f"⚠️ Error decoding JSON in file {filename}, skipping this file.")
            except Exception as e:
                print(f"⚠️ Error processing file {filename}: {e}")

if __name__ == "__main__":
    update_price_files()
