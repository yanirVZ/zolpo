import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "https://url.retail.publishedprices.co.il/file"
COOKIES_PATH = "cookies.json"
OUTPUT_PATH = "valid_links_stores.txt"

def load_cookies(driver):
    """ טוען עוגיות מתוך הקובץ """
    try:
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("🍪 Cookies loaded.")
    except Exception as e:
        print(f"⚠️ Couldn't load cookies: {e}")

def setup_driver():
    """ הכנה של דפדפן Chrome עם האפשרויות המתאימות """
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def add_link_to_file(url):
    """ פונקציה להוסיף קישור לקובץ valid_links_stores.txt """
    with open(OUTPUT_PATH, "a") as f:
        f.write(url + "\n")
    print(f"✅ קישור נוסף לקובץ: {url}")

def scrape_stores():
    """ פונקציה לסרוק קישורים לסניפים (Stores) """
    driver = setup_driver()
    driver.get(URL)

    # ⏸️ מחכה שתסיים התחברות ידנית
    input("🔐 התחבר ידנית לדף ואז לחץ Enter להמשך...")

    try:
        load_cookies(driver)
        driver.refresh()
        time.sleep(5)
    except:
        pass

    links = driver.find_elements(By.TAG_NAME, "a")
    valid = []

    for link in links:
        href = link.get_attribute("href")
        if href:
            # חיפוש קישורים שמכילים "Stores" וסיומת XML
            if "Stores" in href and href.endswith(".xml"):
                valid.append(href)
                print(f"✅ נמצא קובץ Store: {href}")
                add_link_to_file(href)  # הוסף את הקישור ל-valid_links_stores.txt

    print(f"\n🔗 נמצאו {len(valid)} קישורים ל-Stores.")
    driver.quit()

if __name__ == "__main__":
    scrape_stores()
