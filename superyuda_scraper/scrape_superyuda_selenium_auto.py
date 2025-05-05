import time
import json
import schedule
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# פרטי האתר
URL = "https://url.publishedprices.co.il/file"
COOKIES_PATH = "cookies.json"
OUTPUT_PATH = "valid_links_superyuda.txt"
USER_NAME = "yuda_ho"
PASSWORD = "Yud@147"  # עדכן כאן את הסיסמה אם תשתנה

def load_cookies(driver):
    try:
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("🍪 Cookies loaded.")
    except Exception as e:
        print(f"⚠️ Couldn't load cookies: {e}")

def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def login(driver):
    try:
        driver.get(URL)
        user_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        user_field.send_keys(USER_NAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)
        print("🔒 התחברות הושלמה.")
    except Exception as e:
        print(f"⚠️ שגיאה בהתחברות: {e}")

def scrape_links():
    driver = setup_driver()
    login(driver)

    try:
        # כניסה לתיקיית Yuda
        yuda_folder_link = driver.find_element(By.LINK_TEXT, "Yuda")
        yuda_folder_link.click()
        time.sleep(3)
        print("📁 נכנס לתיקיית Yuda.")
    except Exception as e:
        print(f"⚠️ לא הצליח להיכנס לתיקיית Yuda: {e}")

    try:
        load_cookies(driver)
        driver.refresh()
        time.sleep(5)
    except Exception as e:
        print(f"⚠️ Error loading cookies or refreshing: {e}")

    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        valid = []

        for link in links:
            href = link.get_attribute("href")
            if href and href.endswith(".gz") and "Price" in href:
                valid.append(href)
                print(f"✅ נמצא קובץ: {href}")

        print(f"\n🔗 נמצאו {len(valid)} קבצים.")
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            for line in valid:
                f.write(line + "\n")

    except Exception as e:
        print(f"⚠️ Error scraping links: {e}")

    driver.quit()
    print("✔️ Task Completed Successfully")
    time.sleep(10)
    print("🛑 התכנית הסתיימה אוטומטית.")
    sys.exit()

def job():
    print("🌅 התחלת סקרייפינג ב-10:30 בבוקר...")
    scrape_links()

schedule.every().day.at("17:15").do(job)

if __name__ == "__main__":
    print("⏳ מתכנן את המשימה שתופעל כל יום בשעה 10:30.")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 משימה בוטלה ידנית.")
            break
