from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import os
import requests
from urllib.parse import urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def save_cookies_after_login():
    options = Options()
    options.add_argument("--user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data")
    options.add_argument("--profile-directory=Default")

    # הגדרה תקינה של WebDriver עם Service (Selenium 4)
    chrome_path = r"C:\Users\user\zolpo\rami_levi_scraper\chromedriver.exe"
    service = Service(executable_path=chrome_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://url.retail.publishedprices.co.il/")

    print("🔒 נא התחבר עם שם משתמש (ואם צריך – סיסמה), ואז לחץ Enter להמשך...")
    input("↩️ Enter כשסיימת ⤵️ ")

    cookies = driver.get_cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f, indent=2)

    print("🍪 Cookies saved ל-cookies.json")
    driver.quit()

def load_cookies_to_requests(session, cookies_file):
    with open(cookies_file, "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain"))

def download_files(links, download_folder, cookies_file):
    os.makedirs(download_folder, exist_ok=True)
    session = requests.Session()
    load_cookies_to_requests(session, cookies_file)

    count = 0
    for url in links:
        try:
            filename = os.path.basename(urlparse(url).path)
            dest_path = os.path.join(download_folder, filename)
            r = session.get(url, stream=True, verify=False)
            if r.ok and r.headers.get("Content-Type", "").startswith("application"):
                with open(dest_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ הורד: {filename}")
                count += 1
            else:
                print(f"❌ נכשל {filename} (HTML או שגיאה אחרת)")
        except Exception as e:
            print(f"⚠️ שגיאה בהורדת {url}: {e}")
    print(f"📦 סיימנו. הורדו {count} קבצים.")

if __name__ == "__main__":
    save_cookies_after_login()

    links = [
        "https://url.retail.publishedprices.co.il/file/d/Price7290058140886-001-202504100700.gz",
        "https://url.retail.publishedprices.co.il/file/d/Price7290058140886-001-202504100800.gz",
    ]

    download_folder = r"C:\zolpo\rami_levi_prices"
    download_files(links, download_folder, "cookies.json")
