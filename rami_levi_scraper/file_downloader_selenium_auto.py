import os
import json
import requests
from urllib.parse import urlparse
import urllib3
import time
import schedule

# ביטול אזהרות SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIES_FILE = "cookies.json"
LINKS_FILE = "valid_links_updated_auto.txt"  # עדכון שם הקובץ
DOWNLOAD_FOLDER = r"C:\zolpo\ramilevi\rami_levi_prices"

def load_cookies():
    with open(COOKIES_FILE, "r") as f:
        raw = json.load(f)
    cookies = {}
    for cookie in raw:
        cookies[cookie["name"]] = cookie["value"]
    return cookies

def download_all():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    cookies = load_cookies()
    session = requests.Session()
    session.cookies.update(cookies)

    with open(LINKS_FILE, "r") as f:
        links = [line.strip() for line in f if line.strip()]

    count = 0
    for url in links:
        filename = os.path.basename(urlparse(url).path)
        dest = os.path.join(DOWNLOAD_FOLDER, filename)

        try:
            # הוספת הדפסות לצורך מעקב
            print(f"⬇️ מתחילים להוריד את הקובץ: {filename}")
            resp = session.get(url, verify=False, stream=True)

            # אם התגובה היא HTML במקום GZIP
            if resp.ok and "text/html" in resp.headers.get("Content-Type", ""):
                print(f"❌ נכשל: {filename} (קיבלנו HTML במקום GZIP)")
                print(f"סטטוס: {resp.status_code}")
                print(f"תוכן: {resp.text[:500]}")  # הצגת חלק מהתוכן אם זה HTML
                continue

            if resp.ok and resp.headers.get("Content-Type", "").startswith("application"):
                with open(dest, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ הורד: {filename}")
                count += 1
            else:
                print(f"❌ נכשל: {filename} (לא GZIP)")

        except Exception as e:
            print(f"⚠️ שגיאה בהורדת {filename}: {e}")

    print(f"\n📦 הסתיים. הורדו {count} קבצים.")

# הגדרת משימה שתופעל כל 24 שעות בשעה 7:00 בבוקר
def job():
    print("🌅 התחלת סקרייפינג והורדה ב-7:00 בבוקר...")
    download_all()

# תזמון המשימה לשעה 7:00 בבוקר
schedule.every().day.at("14:44").do(job)

# שמירה על הפעלת התוכנית כל הזמן
if __name__ == "__main__":
    print("⏳ מתכנן את המשימה שתופעל כל יום בשעה 7:00 בבוקר.")
    while True:
        schedule.run_pending()
        time.sleep(1)
