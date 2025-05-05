import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# נתיב לקובץ העוגיות
COOKIES_FILE = "cookies.json"
# נתיב יעד להורדות
DOWNLOAD_FOLDER = r"C:\zolpo\rami_levy_prices"

# יצירת תיקיית יעד אם לא קיימת
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# פתיחת דפדפן
options = Options()
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)

# גישה לדף של רמי לוי
url = "https://url.retail.publishedprices.co.il"
driver.get(url)

# טעינת עוגיות
with open(COOKIES_FILE, "r", encoding="utf-8") as f:
    cookies = json.load(f)

for cookie in cookies:
    driver.add_cookie(cookie)

# טען מחדש את הדף לאחר טעינת עוגיות
driver.get(url)
time.sleep(3)  # זמן לטעינה

# מציאת קישורים לקבצי .gz
links = driver.find_elements(By.TAG_NAME, "a")
gz_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and link.get_attribute("href").endswith(".gz")]

print(f"\n🧲 נמצאו {len(gz_links)} קישורים להורדה.\n")

# שלב ההורדה
downloaded = 0
for i, link in enumerate(gz_links):
    store_id = link.split("-")[-2]
    filename = f"rami_levy_{store_id}_{i+1}.gz"
    path = os.path.join(DOWNLOAD_FOLDER, filename)

    try:
        print(f"⬇️ מוריד {filename}")
        r = requests.get(link, verify=False, timeout=20)
        if r.ok and b"<html" not in r.content[:50]:  # הגנה מקבצי HTML שגויים
            with open(path, "wb") as f:
                f.write(r.content)
            downloaded += 1
        else:
            print(f"❌ קובץ לא תקין: {link}")

    except Exception as e:
        print(f"⚠️ שגיאה בהורדה: {e}")

driver.quit()
print(f"\n✅ הסתיים. הותקנו {downloaded} קבצים תקינים מתוך {len(gz_links)}.\n")
