import os
import gzip
import json
import xmltodict
from datetime import datetime

# נתיבי קלט ופלט
input_folder = r"C:\zolpo\shufersal\promo_gz_files"
output_folder = r"C:\zolpo\shufersal\promo_json_files"
os.makedirs(output_folder, exist_ok=True)

def convert_promo_gz_to_json():
    print(f"\n🌀 התחלת המרת promo.gz ל־JSON בשעה {datetime.now().strftime('%H:%M:%S')}...")
    converted = 0

    for filename in os.listdir(input_folder):
        if filename.endswith(".gz"):
            gz_path = os.path.join(input_folder, filename)
            json_path = os.path.join(output_folder, filename.replace(".gz", ".json"))

            try:
                with gzip.open(gz_path, 'rt', encoding='utf-8-sig') as f:
                    xml_text = f.read()
                    data = xmltodict.parse(xml_text)

                with open(json_path, 'w', encoding='utf-8') as out_f:
                    json.dump(data, out_f, indent=2, ensure_ascii=False)

                print(f"✅ הומר: {filename}")
                converted += 1
            except Exception as e:
                print(f"⚠️ שגיאה ב־{filename}: {e}")

    print(f"\n📦 הסתיים. הומרו {converted} קבצים.")
    print("🛑 סיום המרה.\n")

if __name__ == "__main__":
    convert_promo_gz_to_json()
