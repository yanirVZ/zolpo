from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os

# הנתיב הסופי
output_path = r"C:\zolpo\shufersal\shufersal_mapping_stores.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# הפעלת דפדפן וטעינת האתר
driver = webdriver.Chrome()
driver.get("https://prices.shufersal.co.il/")

# איתור dropdown של הסניפים
store_select = driver.find_element(By.ID, "ddlStore")
options = store_select.find_elements(By.TAG_NAME, "option")

# חילוץ המידע
store_list = []
for opt in options:
    value = opt.get_attribute("value")
    name = opt.text.strip()
    if value != "0":  # דלג על All
        store_list.append({
            "StoreID": int(value),
            "StoreName": name
        })

driver.quit()

# כתיבה לקובץ JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(store_list, f, ensure_ascii=False, indent=2)

print(f"✅ נשמרו {len(store_list)} סניפים אל: {output_path}")
