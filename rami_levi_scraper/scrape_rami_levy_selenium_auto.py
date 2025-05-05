import time
import json
import schedule
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# פרטי האתר
URL = "https://url.retail.publishedprices.co.il/file"
COOKIES_PATH = "cookies.json"
OUTPUT_PATH = "valid_links_updated_auto.txt"  # עדכון שם הקובץ
USER_NAME = "RamiLevi"  # שם המשתמש שלך

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
    options.add_argument("--headless")  # הוספת מצב Headless (ללא דפדפן גרפי)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# התחברות אוטומטית לאתר עם שם המשתמש בלבד
def login(driver):
    try:
        driver.get(URL)
        # מציאת שדות שם המשתמש והסיסמה
        user_field = driver.find_element(By.ID, "username")  # או לפי ה-ID של שדה שם המשתמש
        password_field = driver.find_element(By.ID, "password")  # שדה הסיסמה

        # הזנת שם המשתמש והשארת סיסמה ריקה
        user_field.send_keys(USER_NAME)
        password_field.send_keys("")  # אם אין סיסמה
        password_field.send_keys(Keys.RETURN)  # שליחה של הטופס
        time.sleep(3)  # המתן מעט לעיבוד ההתחברות
        print("🔒 התחברות הושלמה.")
    except Exception as e:
        print(f"⚠️ שגיאה בהתחברות: {e}")

# הפונקציה לסקרייפינג של הקישורים
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
        with open(OUTPUT_PATH, "w") as f:  # עדכון שם הקובץ
            for line in valid:
                f.write(line + "\n")

    except Exception as e:
        print(f"⚠️ Error scraping links: {e}")

    driver.quit()
    print("✔️ Task Completed Successfully")
    time.sleep(10)  # המתן 10 שניות אחרי שההודעה נשלחה
    
    # הוספת הודעה לאחר סיום ריצה
    print("🛑 התכנית הסתיימה אוטומטית.")  # הודעת סיום
    sys.exit()  # יציאה מהתוכנית

# הגדרת משימה שתופעל כל 24 שעות בשעה 7:00 בבוקר
def job():
    print("🌅 התחלת סקרייפינג ב-7:00 בבוקר...")
    scrape_links()

# תזמון המשימה לשעה 7:00 בבוקר
schedule.every().day.at("10:30").do(job)

# שמירה על הפעלת התוכנית כל הזמן
if __name__ == "__main__":
    print("⏳ מתכנן את המשימה שתופעל כל יום בשעה 11:37.")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("🔴 משימה בוטלה ידנית.")
            break
