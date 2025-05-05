import os
import json
import requests
from urllib.parse import urlparse
import urllib3
import gzip

# ביטול אזהרות SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIES_FILE = "cookies.json"
LINKS_FILE = "valid_links.txt"
DOWNLOAD_FOLDER = r"C:\zolpo\rami_levi_prices"
STORE_MAP = {}

def load_cookies():
    with open(COOKIES_FILE, "r") as f:
        raw = json.load(f)
    cookies = {}
    for cookie in raw:
        cookies[cookie["name"]] = cookie["value"]
    return cookies

def load_store_map():
    """ טוען את המיפוי של הסניפים מ־Stores.json """
    store_file = "Stores7290058140886-001-202504101000.json.gz"  # יש להוריד את קובץ ה־Stores
    if os.path.exists(store_file):
        with gzip.open(store_file, 'rt', encoding='utf-8-sig') as f:
            store_data = json.load(f)
            for store in store_data.get("Stores", []):
                store_id = store["StoreId"]
                store_name = store["StoreName"]
                STORE_MAP[store_id] = store_name
        print("🍪 מיפוי סניפים נטען בהצלחה.")
    else:
        print("⚠️ לא נמצא קובץ Stores, הורד אותו קודם.")

def download_all():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    cookies = load_cookies()
    session = requests.Session()
    session.cookies.update(cookies)

    # קריאה לקובץ ה־Stores אם הוא לא טוען כבר
    load_store_map()

    with open(LINKS_FILE, "r") as f:
        links = [line.strip() for line in f if line.strip()]

    count = 0
    for url in links:
        filename = os.path.basename(urlparse(url).path)
        dest = os.path.join(DOWNLOAD_FOLDER, filename)

        # אם זה קישור ל- Stores, נוריד אותו
        if "Stores" in url:
            try:
                print(f"📥 מוריד קובץ Store: {url}")
                resp = session.get(url, verify=False, stream=True)
                with open(dest, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ הורד: {filename}")
                load_store_map()  # נטעין את מיפוי הסניפים אחרי הורדת ה-Store
                count += 1
            except Exception as e:
                print(f"⚠️ שגיאה בהורדת {filename}: {e}")
        elif "Price" in url:
            try:
                print(f"📥 מוריד קובץ מחיר: {url}")
                resp = session.get(url, verify=False, stream=True)
                if resp.ok and resp.headers.get("Content-Type", "").startswith("application"):
                    with open(dest, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"✅ הורד: {filename}")
                    count += 1
                else:
                    print(f"❌ נכשל: {filename} (HTML במקום GZIP?)")
            except Exception as e:
                print(f"⚠️ שגיאה בהורדת {filename}: {e}")

    print(f"\n📦 סיימנו. הורדו {count} קבצים.")

if __name__ == "__main__":
    download_all()
