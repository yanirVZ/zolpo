import os
import json
import requests
import urllib3
import sys
import time
import schedule
from urllib.parse import urlparse

# ביטול אזהרות SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIES_FILE = "cookies_auto.json"
LINKS_FILE = "valid_links_politzer.txt"  # הקובץ שהפקנו בסקרייפר
DOWNLOAD_FOLDER = r"C:\zolpo\politzer\politzerprices_auto"  # תיקיית הורדה ליוחננוף

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
            resp = session.get(url, verify=False, stream=True)
            if resp.ok and resp.headers.get("Content-Type", "").startswith("application"):
                with open(dest, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ הורד: {filename}")
                count += 1
            else:
                print(f"❌ נכשל: {filename} (HTML במקום GZIP?)")
                print("Response content:", resp.text[:500])
        except Exception as e:
            print(f"⚠️ שגיאה עם {filename}: {e}")

    print(f"\n📦 הסתיים. הורדו {count} קבצים.")
    print("🛑 התכנית הסתיימה אוטומטית.\n")
    sys.exit()

# הגדרת משימה מתוזמנת ל־10:32 בבוקר
def job():
    print("🌅 התחלת הורדה אוטומטית ב-10:32...")
    download_all()

# תזמון הרצה כל יום בשעה 10:32
schedule.every().day.at("13:54").do(job)

# הרצה תמידית ברקע
if __name__ == "__main__":
    print("⏳ ממתין לשעה 10:32 לביצוע הורדה יומית...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 המשימה בוטלה ידנית.")
            break
