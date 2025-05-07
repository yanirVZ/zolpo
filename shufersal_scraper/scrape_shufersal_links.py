import requests
from bs4 import BeautifulSoup
import html5lib
import re
from collections import defaultdict

BASE_URL = "https://prices.shufersal.co.il/?page={}"
MAX_PAGES = 45
LINKS_OUTPUT_FILE = "valid_links.txt"

just_url_list = []

for page in range(1, MAX_PAGES + 1):
    print(f"🔎 דורס עמוד {page}")
    try:
        r = requests.get(BASE_URL.format(page))
        soup = BeautifulSoup(r.content, 'html5lib')
        rows = soup.find_all('tr')  # הסרנו את הסינון לפי class

        for row in rows:
            cols = row.find_all('td')
            if not cols:
                continue

            link_tag = cols[0].find('a', href=True)
            if not link_tag:
                continue  # דלג אם אין קישור

            url = link_tag['href'].replace(";", "&")
            if not url.startswith("http"):
                continue

            text_fields = [col.text.strip() for col in cols]
            category = text_fields[4].lower() if len(text_fields) > 4 else "unknown"

            # הוצאת מספר סניף מהשם (col[6] אם קיים, או מה-url)
            name_field = text_fields[6] if len(text_fields) > 6 else url
            match = re.search(r'-(\d{3})-', name_field)
            store_id = match.group(1) if match else "000"

            if category in ["price", "pricefull"]:
                just_url_list.append((store_id, category, url))
                print(f"✅ {store_id} | {category} | {url}")

    except Exception as e:
        print(f"❌ שגיאה בעמוד {page}: {e}")

# קיבוץ ומיון
sorted_links = sorted(just_url_list, key=lambda x: (int(x[0]), x[1]))

# כתיבה לקובץ
with open(LINKS_OUTPUT_FILE, "w", encoding="utf-8") as f:
    for store_id, category, url in sorted_links:
        f.write(url + "\n")

print(f"\n💾 נשמרו {len(sorted_links)} קישורים לקובץ {LINKS_OUTPUT_FILE}")
