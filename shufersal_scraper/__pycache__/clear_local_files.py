import os

FOLDER = r"C:\zolpo\Prices"

def delete_all_files():
    if not os.path.exists(FOLDER):
        print("❌ תיקייה לא קיימת.")
        return

    files = os.listdir(FOLDER)
    for file in files:
        path = os.path.join(FOLDER, file)
        try:
            os.remove(path)
            print(f"🗑️ נמחק: {file}")
        except Exception as e:
            print(f"⚠️ שגיאה במחיקת {file}: {e}")

if __name__ == "__main__":
    delete_all_files()
