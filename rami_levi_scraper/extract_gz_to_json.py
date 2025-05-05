import os
import gzip
import json
import xmltodict

input_folder = r"C:\zolpo\rami_levi_prices"
output_folder = r"C:\zolpo\rami_levi_json"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".gz"):
        gz_path = os.path.join(input_folder, filename)
        json_path = os.path.join(output_folder, filename.replace(".gz", ".json"))

        try:
            with gzip.open(gz_path, 'rt', encoding='utf-8-sig') as f:
                xml_text = f.read()
                data = xmltodict.parse(xml_text)  # המרה מ־XML לדיקט

            with open(json_path, 'w', encoding='utf-8') as out_f:
                json.dump(data, out_f, indent=2, ensure_ascii=False)

            print(f"✅ הומר: {filename}")
        except Exception as e:
            print(f"⚠️ שגיאה ב־{filename}: {e}")
