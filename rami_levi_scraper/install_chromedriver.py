import requests
import zipfile
import io
import os
import shutil
import subprocess
import re

def get_chrome_version():
    """Get the installed version of Chrome on Windows"""
    try:
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            shell=True
        )
        version = re.search(r"(\d+\.\d+\.\d+\.\d+)", output.decode()).group(1)
        return version
    except Exception as e:
        print("❌ לא ניתן למצוא את גרסת כרום:", e)
        return None

def download_chromedriver(version):
    """Download the appropriate ChromeDriver for the detected Chrome version"""
    major_version = version.split('.')[0]
    url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/win64/chromedriver-win64.zip"
    
    try:
        print(f"🔽 מוריד ChromeDriver לגרסה {version}...")
        r = requests.get(url)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("chromedriver_extracted")
        shutil.move("chromedriver_extracted/chromedriver-win64/chromedriver.exe", "chromedriver.exe")
        shutil.rmtree("chromedriver_extracted")
        print("✅ הקובץ chromedriver.exe הותקן בהצלחה בתיקייה הנוכחית.")
    except Exception as e:
        print("❌ שגיאה בהורדה:", e)

if __name__ == "__main__":
    chrome_version = get_chrome_version()
    if chrome_version:
        download_chromedriver(chrome_version)
    else:
        print("⚠️ לא ניתן לאתר את גרסת כרום שלך. ודא שכרום מותקן.")
