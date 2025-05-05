import sqlite3

def list_cookies_from_temp(file_path, domain_filter):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT name, host_key FROM cookies
        WHERE host_key LIKE '%{domain_filter}%'
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("❌ לא נמצאו קוקיז עבור הדומיין.")
    else:
        print(f"🔍 נמצאו {len(rows)} קוקיז ב־{file_path}:")
        for name, host in rows:
            print(f"  - {name} (host: {host})")

# קריאה:
list_cookies_from_temp("temp_test.sqlite", "publishedprices.co.il")
