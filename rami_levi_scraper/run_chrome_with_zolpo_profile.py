import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# נתיב מותאם אישית לפרופיל חדש
USER_PROFILE_PATH = "C:/zolpo/profile_data"
URL = "https://url.publishedprices.co.il/file"

def setup_driver_with_custom_profile():
    print(f"⚙️ פותח דפדפן עם פרופיל מותאם: {USER_PROFILE_PATH}")
    options = Options()
    options.add_argument(f"user-data-dir={USER_PROFILE_PATH}")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    return driver

def main():
    driver = setup_driver_with_custom_profile()
    print(f"🌍 טוען את הדף: {URL}")
    driver.get(URL)

    print("⏳ נמתין 60 שניות כדי שתוכל להתחבר...")
    time.sleep(60)

    print("🍪 מנסה לאסוף cookies:")
    cookies = driver.get_cookies()
    for c in cookies:
        print(f"  - {c['name']} = {c['value']} (domain: {c['domain']})")

    driver.quit()
    print("🛑 סיום פעולה.")

if __name__ == "__main__":
    main()
