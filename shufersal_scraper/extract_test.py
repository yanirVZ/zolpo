import gzip
import json
import xml.etree.ElementTree as ET

gz_path = r"C:\zolpo\shufersal\test.gz"
json_path = r"C:\zolpo\shufersal\test.json"

def convert_gz_to_json(gz_path, json_path):
    try:
        # קריאת תוכן הקובץ
        with gzip.open(gz_path, 'rt', encoding='utf-8-sig') as f:
            content = f.read()
        
        stripped = content.lstrip()

        # זיהוי סוג התוכן
        if stripped.startswith('{') or stripped.startswith('['):
            print("🟢 זוהה תוכן מסוג JSON")
            data = json.loads(content)
        
        elif stripped.startswith('<?xml') or stripped.startswith('<'):
            print("🟡 זוהה תוכן מסוג XML")
            root = ET.fromstring(content)
            data = {child.tag: child.text for child in root}
        
        else:
            print("🔴 לא זוהה פורמט JSON או XML")
            return

        # שמירה כקובץ JSON
        with open(json_path, 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent=2)
        
        print(f"✅ הקובץ הומר ונשמר ב־ {json_path}")

    except Exception as e:
        print(f"❌ שגיאה: {e}")

# הפעלת הפונקציה
convert_gz_to_json(gz_path, json_path)
