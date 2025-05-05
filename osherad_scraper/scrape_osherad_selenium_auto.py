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
OUTPUT_PATH = "valid_links_osherad.txt"  # עדכון שם הקובץ
USER_NAME = "osherad"  # שם המשתמש של יוחננוף

# פונקציה להורדת ה-cookies ששמורים
def load_cookies(driver):
    try:
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("🍪 Cookies loaded.")
    except Exception as e:
        print(f"⚠️ Couldn't load cookies: {e}")

# הגדרת הדרייבר של Selenium ב-Headless Mode (ללא דפדפן גרפי)
def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# התחברות אוטומטית לאתר
def login(driver):
    try:
        driver.get(URL)
        user_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        user_field.send_keys(USER_NAME)
        password_field.send_keys("")  # אין סיסמה
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)
        print("🔒 התחברות הושלמה.")
    except Exception as e:
        print(f"⚠️ שגיאה בהתחברות: {e}")

# פונקציה לסקרייפינג של הקישורים
def scrape_links():
    driver = setup_driver()

    login(driver)  # התחברות אוטומטית

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

# הגדרת משימה שתופעל כל 24 שעות בשעה 10:30 בבוקר
def job():
    print("🌅 התחלת סקרייפינג ב-10:30 בבוקר...")
    scrape_links()

# תזמון המשימה לשעה 10:30 בבוקר
schedule.every().day.at("13:08").do(job)

# שמירה על הפעלת התוכנית כל הזמן
if __name__ == "__main__":
    print("⏳ מתכנן את המשימה שתופעל כל יום בשעה 10:30.")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 משימה בוטלה ידנית.")
            break
