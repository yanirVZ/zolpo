import requests
import os

# נתיב שמירה
FOLDER = r"C:\zolpo\shufersal\promo_gz_files"
LINKS_FILE = "promo_price_links.txt"

def file_downloader(urls):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    for i, url in enumerate(urls, start=1):
        gz_file = os.path.join(FOLDER, f"promo_file_{i}.gz")

        try:
            print(f"📥 מוריד: {url}")
            response = requests.get(url, timeout=30)
            with open(gz_file, "wb") as f:
                f.write(response.content)
            print(f"✅ נשמר: {gz_file}")

        except Exception as e:
            print(f"❌ שגיאה בהורדת {url}: {e}")

if __name__ == "__main__":
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"🔗 נטענו {len(urls)} קישורים מתוך {LINKS_FILE}")
        file_downloader(urls)
    else:
        print(f"⚠️ קובץ הקישורים {LINKS_FILE} לא נמצא")
