import requests
import os

LINK_FILE = "stores_links.txt"
OUTPUT_PATH = r"C:\zolpo\shufersal\shufersal_stores.gz"

def download_store_file():
    folder = os.path.dirname(OUTPUT_PATH)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(LINK_FILE):
        print(f"❌ הקובץ {LINK_FILE} לא נמצא")
        return

    with open(LINK_FILE, "r", encoding="utf-8") as f:
        url = f.readline().strip()

    if not url.startswith("http"):
        print(f"❌ הקישור בקובץ אינו תקין: {url}")
        return

    try:
        print(f"📥 מוריד את הקובץ מ: {url}")
        response = requests.get(url, timeout=30)

        with open(OUTPUT_PATH, "wb") as f_out:
            f_out.write(response.content)

        print(f"✅ הקובץ נשמר: {OUTPUT_PATH}")

    except Exception as e:
        print(f"❌ שגיאה בהורדה: {e}")

if __name__ == "__main__":
    download_store_file()
