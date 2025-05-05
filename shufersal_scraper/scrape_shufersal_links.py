import requests
from bs4 import BeautifulSoup
import html5lib
import re
from collections import defaultdict

BASE_URL = "https://prices.shufersal.co.il/?page={}"
MAX_PAGES = 30
LINKS_OUTPUT_FILE = "valid_links.txt"

just_url_list = []

for page in range(1, MAX_PAGES + 1):
    print(f"🔎 סורק עמוד {BASE_URL.format(page)}")
    try:
        r = requests.get(BASE_URL.format(page))
        soup = BeautifulSoup(r.content, 'html5lib')
        rows = soup.find_all('tr', class_='webgrid-row-style')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 6:
                continue

            name_field = cols[6].text.strip() if len(cols) > 6 else ""
            match = re.search(r'-(\d{3})-', name_field)
            if not match:
                continue
            store_id = match.group(1)

            category = cols[4].text.strip().lower()
            if category not in ["pricefull", "price"]:
                continue

            link_tag = cols[0].find('a', href=True)
            if link_tag:
                url = link_tag['href'].replace(";", "&")
                if url.startswith("http"):
                    just_url_list.append((store_id, category, url))
                    print(f"✅ סניף {store_id} | קטגוריה: {category} | כתובת: {url}")

    except Exception as e:
        print(f"❌ שגיאה בעמוד {page}: {e}")

# קיבוץ ומיון הקישורים
store_files = defaultdict(list)
for store_id, category, url in just_url_list:
    store_files[store_id].append((category, url))

sorted_links = []
for store_id in sorted(store_files.keys()):
    for category, url in sorted(store_files[store_id], key=lambda x: x[0]):
        sorted_links.append(url)

# כתיבה לקובץ טקסט
with open(LINKS_OUTPUT_FILE, "w", encoding="utf-8") as f:
    for url in sorted_links:
        f.write(url + "\n")

print(f"\n💾 נשמרו {len(sorted_links)} קישורים לקובץ {LINKS_OUTPUT_FILE}")
