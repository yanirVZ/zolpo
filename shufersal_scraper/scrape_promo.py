import requests
from bs4 import BeautifulSoup
import html5lib
import re

BASE_URL = "https://prices.shufersal.co.il/?page={}"
START_PAGE = 45
END_PAGE = 80
OUTPUT_PROMO = "promo_price_links_45_80.txt"

just_promo_urls = []

for page in range(START_PAGE, END_PAGE + 1):
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

            if link_tag and category in ["promo", "promofull"]:
                url = link_tag['href'].replace(";", "&")
                if url.startswith("http"):
                    just_promo_urls.append(url)
                    print(f"🟨 [Promo] סניף {store_id} | {category} | {url}")

    except Exception as e:
        print(f"❌ שגיאה בעמוד {page}: {e}")

# כתיבה לקובץ promo בלבד
with open(OUTPUT_PROMO, "w", encoding="utf-8") as f:
    for url in just_promo_urls:
        f.write(url + "\n")

print(f"\n💾 נשמרו {len(just_promo_urls)} קישורים לקובץ {OUTPUT_PROMO}")
