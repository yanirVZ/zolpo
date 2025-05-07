import requests
from bs4 import BeautifulSoup
import html5lib
import re
from collections import defaultdict

BASE_URL = "https://prices.shufersal.co.il/?page={}"
MAX_PAGES = 85
LINKS_OUTPUT_PRICE = "valid_links.txt"
LINKS_OUTPUT_PROMO = "promo_price_links.txt"

just_price_urls = []
just_promo_urls = []

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
            link_tag = cols[0].find('a', href=True)

            if link_tag:
                url = link_tag['href'].replace(";", "&")
                if url.startswith("http"):
                    if category in ["price", "pricefull"]:
                        just_price_urls.append(url)
                        print(f"✅ [Price] סניף {store_id} | {category} | {url}")
                    elif category in ["promo", "promofull"]:
                        just_promo_urls.append(url)
                        print(f"🟨 [Promo] סניף {store_id} | {category} | {url}")

    except Exception as e:
        print(f"❌ שגיאה בעמוד {page}: {e}")

# כתיבה לקבצים
with open(LINKS_OUTPUT_PRICE, "w", encoding="utf-8") as f:
    for url in just_price_urls:
        f.write(url + "\n")

with open(LINKS_OUTPUT_PROMO, "w", encoding="utf-8") as f:
    for url in just_promo_urls:
        f.write(url + "\n")

print(f"\n💾 נשמרו {len(just_price_urls)} קישורים לקובץ {LINKS_OUTPUT_PRICE}")
print(f"💾 נשמרו {len(just_promo_urls)} קישורים לקובץ {LINKS_OUTPUT_PROMO}")
