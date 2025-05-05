import os
import json
import requests
from urllib.parse import urlparse
import urllib3

# ביטול אזהרות SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIES_FILE = "cookies.json"
LINKS_FILE = "valid_links.txt"
DOWNLOAD_FOLDER = r"C:\zolpo\rami_levi_prices"

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
        except Exception as e:
            print(f"⚠️ שגיאה עם {filename}: {e}")

    print(f"\n📦 הסתיים. הורדו {count} קבצים.")

if __name__ == "__main__":
    download_all()
