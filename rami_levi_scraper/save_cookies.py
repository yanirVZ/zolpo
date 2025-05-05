import sqlite3
from pathlib import Path
import shutil

def get_raw_cookie(profile_path, cookie_name, domain_filter):
    original_path = Path(profile_path) / "Network" / "Cookies"
    temp_path = Path("temp_raw_cookie.sqlite")

    if not original_path.exists():
        raise FileNotFoundError(f"❌ לא נמצא קובץ cookies: {original_path}")

    shutil.copyfile(original_path, temp_path)

    conn = sqlite3.connect(str(temp_path))
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT name, value, host_key FROM cookies
        WHERE name = '{cookie_name}' AND host_key LIKE '%{domain_filter}%'
    """)

    result = cursor.fetchone()
    conn.close()
    temp_path.unlink()

    if result:
        name, value, host_key = result
        return value  # לא מוצפן – נחזיר אותו ישירות

    print("❌ לא נמצא קוקי בשם הזה.")
    return None
