import os
import json

# === שלב 1: מיפוי ItemCode ל־ItemName ===
def build_itemcode_to_name_map(folder_path):
    code_to_name = {}
    for fname in os.listdir(folder_path):
        if fname.endswith(".json"):
            with open(os.path.join(folder_path, fname), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    items = data.get("root", {}).get("Items", {}).get("Item", [])
                    if isinstance(items, dict):
                        items = [items]
                    for item in items:
                        code = item.get("ItemCode")
                        name = item.get("ItemName")
                        if code and name:
                            code_to_name[code] = name
                except Exception as e:
                    print(f"שגיאה בקובץ {fname}: {e}")
    print(f"✅ נבנה מיפוי של {len(code_to_name)} מוצרים.")
    return code_to_name

# === שלב 2: הוספת ItemName לכל Item בקבצי promo ===
def add_names_to_promos(promo_folder, output_folder, itemcode_to_name):
    os.makedirs(output_folder, exist_ok=True)
    updated = 0

    for fname in os.listdir(promo_folder):
        if fname.endswith(".json"):
            with open(os.path.join(promo_folder, fname), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    promos = data.get("root", {}).get("Promotions", {}).get("Promotion", [])
                    if isinstance(promos, dict):
                        promos = [promos]
                    for promo in promos:
                        items = promo.get("PromotionItems", {}).get("Item", [])
                        if isinstance(items, dict):  # מקרה של פריט יחיד
                            items = [items]
                        for item in items:
                            code = item.get("ItemCode")
                            if code and code in itemcode_to_name:
                                item["ItemName"] = itemcode_to_name[code]
                    with open(os.path.join(output_folder, fname), 'w', encoding='utf-8') as out_f:
                        json.dump(data, out_f, ensure_ascii=False, indent=2)
                    updated += 1
                except Exception as e:
                    print(f"שגיאה בעיבוד {fname}: {e}")
    print(f"\n📦 עודכנו {updated} קבצי promo.")

# === שלב 3: הרצה ===
if __name__ == "__main__":
    price_folder = r"C:\zolpo\shufersal\json_files_updated"
    promo_folder = r"C:\zolpo\shufersal\promo_json_files_updated"
    output_folder = r"C:\zolpo\shufersal\promo_json_with_names"

    item_map = build_itemcode_to_name_map(price_folder)
    add_names_to_promos(promo_folder, output_folder, item_map)
