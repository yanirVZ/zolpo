import requests
import os
import re

# נתיב שמירה
FOLDER = r"C:\zolpo\shufersal\gz_files_names"
LINKS_FILE = "valid_links.txt"

def extract_info_from_url(url):
    # זיהוי הקטגוריה
    category = "unknown"
    if "pricefull" in url.lower():
        category = "pricefull"
    elif "price" in url.lower():
        category = "price"

    # חילוץ מספר הסניף - שלוש ספרות אחרי המינוס הראשון
    match = re.search(r'-0*(\d{1,3})-', url)
    store_id = match.group(1).zfill(3) if match else "unknown"

    return category, store_id

def file_downloader(urls):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    for i, url in enumerate(urls, start=1):
        category, store_id = extract_info_from_url(url)
        filename = f"price_file_{i}_{category}_{store_id}.gz"
        gz_file = os.path.join(FOLDER, filename)

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
