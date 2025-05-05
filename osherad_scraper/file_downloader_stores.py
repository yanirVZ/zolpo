import os
import json
import requests
import urllib3
import schedule
import sys
import time
from urllib.parse import urlparse
from datetime import datetime

# ביטול אזהרות SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIES_FILE = "cookies_auto.json"
LINKS_FILE = "valid_links_stores_osherad.txt"  # לינקים של יוחננוף
DOWNLOAD_FOLDER = r"C:\zolpo\osherad\osherad_prices_stores_auto"  # תיקיית הורדה ליוחננוף

def load_cookies():
    """ טוען את ה-cookies שנשמרו """
    with open(COOKIES_FILE, "r") as f:
        raw = json.load(f)
    cookies = {cookie["name"]: cookie["value"] for cookie in raw}
    return cookies

def download_all_stores():
    """ מוריד את כל קבצי ה-XML של ה-Stores """
    print(f"\n🌅 התחלת הורדה ב־{datetime.now().strftime('%H:%M:%S')}...")
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
            content_type = resp.headers.get('Content-Type', '')
            if 'xml' in content_type.lower():
                with open(dest, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ הורד: {filename}")
                count += 1
            else:
                print(f"❌ נכשל: {filename} (Content-Type: {content_type})")
        except Exception as e:
            print(f"⚠️ שגיאה בקובץ {filename}: {e}")

    print(f"\n📦 הסתיים. הורדו {count} קבצים.")
    print("🛑 התכנית הסתיימה אוטומטית.")
    sys.exit()

# תזמון משימה יומית ל־10:49
schedule.every().day.at("13:30").do(download_all_stores)

if __name__ == "__main__":
    print("⏳ ממתין ל־10:49 לביצוע הורדת קבצי Stores...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הפעולה הופסקה ידנית.")
            break
