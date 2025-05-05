from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("user-data-dir=C:/zolpo/profile_data")
options.add_argument("--profile-directory=Default")
driver = webdriver.Chrome(options=options)

driver.get("https://url.publishedprices.co.il/file")
time.sleep(5)

cookies = driver.get_cookies()
for c in cookies:
    if c["name"] == "cftpSID":
        print("✅ הקוקי נמצא:", c["value"])
        with open("cftpSID.txt", "w") as f:
            f.write(c["value"])
driver.quit()
