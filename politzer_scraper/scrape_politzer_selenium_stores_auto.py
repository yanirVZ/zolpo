import time
import json
import schedule
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# פרטי האתר והקבצים
URL = "https://url.publishedprices.co.il/file"
COOKIES_PATH = "cookies.json"
OUTPUT_PATH = "valid_links_stores_politzer.txt"  # שם קובץ מעודכן ל-politzer
USER_NAME = "politzer"
PASSWORD = "politzer"  # בהנחה שאין סיסמה שונה, אם כן תגיד לי ואעדכן

# הגדרת הדרייבר במצב Headless
def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# התחברות אוטומטית
def login(driver):
    try:
        driver.get(URL)
        time.sleep(2)
        user_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        user_field.send_keys(USER_NAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)

        time.sleep(3)
        print("🔒 התחברות הושלמה.")
    except Exception as e:
        print(f"⚠️ שגיאה בהתחברות: {e}")

# טעינת cookies שמורות
def load_cookies(driver):
    try:
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("🍪 Cookies loaded.")
    except Exception as e:
        print(f"⚠️ Couldn't load cookies: {e}")

# כתיבת קישור לקובץ
def add_link_to_file(url):
    with open(OUTPUT_PATH, "a") as f:
        f.write(url + "\n")
    print(f"✅ קישור נוסף לקובץ: {url}")

# הסקרייפינג עצמו
def scrape_stores():
    print("🌅 התחלת סקרייפינג לקבצי Stores...")
    driver = setup_driver()
    login(driver)

    try:
        load_cookies(driver)
        driver.refresh()
        time.sleep(5)
    except Exception as e:
        print(f"⚠️ שגיאה בטעינת cookies או רענון: {e}")

    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        valid = []

        for link in links:
            href = link.get_attribute("href")
            if href and "Stores" in href and href.endswith(".xml"):
                valid.append(href)
                print(f"✅ נמצא קובץ Store: {href}")
                add_link_to_file(href)

        print(f"\n🔗 נמצאו {len(valid)} קישורים ל-Stores.")
    except Exception as e:
        print(f"⚠️ שגיאה בסריקת הקישורים: {e}")

    driver.quit()
    print("✔️ סיום התהליך.")
    print("🛑 התכנית הסתיימה אוטומטית.")
    sys.exit()

# משימה מתוזמנת
def job():
    print("🕖 בוקר טוב! מתחיל סקרייפינג ב־10:47 בדיוק...")
    scrape_stores()

# תזמון יומי
schedule.every().day.at("14:04").do(job)

# הפעלה תמידית
if __name__ == "__main__":
    print("⏳ ממתין ל־10:47 להפעלת הסקרייפינג...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 הופסק ידנית.")
            break
