import requests
from bs4 import BeautifulSoup

# 🌍 כתובת האתר שמכיל את רשימת הקבצים
URL = "https://url.retail.publishedprices.co.il/file"

# ⛔ עקיפת אזהרות SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# רשימת קבצים תקפים
just_url_list = []

try:
    print("🔎 ניגש לשרת רמי לוי ומושך קבצים...")
    response = requests.get(URL, verify=False)

    if response.status_code != 200:
        print(f"❌ שגיאה: קיבלתי קוד {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = link["href"]
            if href.endswith(".gz"):
                full_url = f"{URL}/{href}" if not href.startswith("http") else href
                store_id_match = next((part for part in href.split("-") if part.isdigit() and len(part) == 3), "000")
                just_url_list.append((store_id_match, "pricefull", full_url))
                print(f"✅ סניף {store_id_match} | {full_url}")

except Exception as e:
    print(f"❌ שגיאה כללית: {e}")

print(f"\n🧾 נמצאו {len(just_url_list)} קבצים.")
print(response.text[:1000]) 
# לשימוש חיצוני (כמו file_downloader)
if __name__ == "__main__":
    print("🔚 הסקרייפר סיים.")
