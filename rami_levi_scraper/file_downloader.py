import requests
import gzip
import shutil
import json
import xmltodict
import os

from scrape_rami_levy_selenium import scrape_rami_levy, just_url_list

FOLDER = r"C:\zolpo\rami_levi_prices"

def is_valid_gzip(file_path):
    try:
        with open(file_path, 'rb') as f:
            signature = f.read(2)
            return signature == b'\x1f\x8b'
    except:
        return False

def is_html_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read(300).lower()
            return b'<!doctype html' in content or b'<html' in content
    except:
        return False

def file_downloader(urls):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    for i, (store_id, category, url) in enumerate(urls, start=1):
        gz_file = os.path.join(FOLDER, f"rami_levy_{store_id}_{i}.gz")
        xml_file = gz_file.replace(".gz", ".xml")
        json_file = gz_file.replace(".gz", ".json")

        try:
            print(f"📥 מוריד: {url}")
            r = requests.get(url, verify=False)
            with open(gz_file, "wb") as f:
                f.write(r.content)

            if not is_valid_gzip(gz_file) or is_html_file(gz_file):
                print(f"❌ קובץ שגוי (לא GZIP או HTML) → נמחק: {gz_file}")
                os.remove(gz_file)
                continue

            with gzip.open(gz_file, 'rb') as file_in:
                with open(xml_file, 'wb') as file_out:
                    shutil.copyfileobj(file_in, file_out)

            with open(xml_file, encoding='utf-8') as xml_in:
                data_dict = xmltodict.parse(xml_in.read())
                json_data = json.dumps(data_dict, indent=2)

            with open(json_file, "w", encoding="utf-8") as json_out:
                json_out.write(json_data)

            print(f"✅ נשמר: {json_file}")

        except Exception as e:
            print(f"❌ שגיאה בהורדה או עיבוד {url}: {e}")

if __name__ == "__main__":
    print("🔍 סורק עם Selenium...")
    scrape_rami_levy()

    if just_url_list:
        print(f"\n📦 מתחיל הורדה של {len(just_url_list)} קבצים...\n")
        file_downloader(just_url_list)
    else:
        print("⚠️ לא נמצאו קישורים להורדה.")
