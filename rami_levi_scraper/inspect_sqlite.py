import sqlite3

def list_tables(file_path):
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        if not tables:
            print("❌ לא נמצאו טבלאות בקובץ.")
        else:
            print(f"📦 נמצאו {len(tables)} טבלאות:")
            for table in tables:
                print(f"  - {table[0]}")

    except Exception as e:
        print("❌ שגיאה:", e)

# קריאה
list_tables("temp_test.sqlite")
