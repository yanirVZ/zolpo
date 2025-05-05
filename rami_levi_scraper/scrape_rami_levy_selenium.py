import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "https://url.retail.publishedprices.co.il/file"
COOKIES_PATH = "cookies.json"
OUTPUT_PATH = "valid_links.txt"

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
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_links():
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
        if href and href.endswith(".gz") and "Price" in href:
            valid.append(href)
            print(f"✅ נמצא קובץ: {href}")

    print(f"\n🔗 נמצאו {len(valid)} קבצים.")
    with open(OUTPUT_PATH, "w") as f:
        for line in valid:
            f.write(line + "\n")

    driver.quit()

if __name__ == "__main__":
    scrape_links()
