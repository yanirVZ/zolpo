import os
import gzip
import json
import xmltodict

INPUT_FOLDER = r"C:\zolpo\shufersal\gz_files_names"
OUTPUT_FOLDER = r"C:\zolpo\shufersal\json_files_names"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def is_gzip(path):
    with open(path, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'

def extract_and_convert():
    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".gz")]
    print(f"📂 נמצאו {len(files)} קבצים בתיקייה.")

    for fname in files:
        gz_path = os.path.join(INPUT_FOLDER, fname)
        out_path = os.path.join(OUTPUT_FOLDER, fname.replace(".gz", ".json"))

        try:
            # פתיחה לפי סוג הקובץ
            if is_gzip(gz_path):
                with gzip.open(gz_path, 'rt', encoding='utf-8-sig') as f:
                    text = f.read()
                print(f"📦 {fname} — פורמט GZIP מזוהה")
            else:
                with open(gz_path, 'r', encoding='utf-8-sig') as f:
                    text = f.read()
                print(f"📝 {fname} — לא דחוס (נקרא כקובץ טקסט רגיל)")

            # ניסיון להמיר מ־XML ל־dict
            try:
                data = xmltodict.parse(text)
                print(f"🔁 הומר מ־XML")
            except:
                data = json.loads(text)
                print(f"🔁 הומר מ־JSON")

            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ נשמר: {out_path}")

        except Exception as e:
            print(f"❌ שגיאה בקובץ {fname}: {e}")

if __name__ == "__main__":
    extract_and_convert()
