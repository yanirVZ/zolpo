from save_cookies import get_raw_cookie
import requests

cookie = get_raw_cookie(
    r"C:\zolpo\profile_data\Default",
    "cftpSID",
    "publishedprices.co.il"
)

if not cookie:
    print("❌ הקוקי לא נמצא או לא תקין.")
    exit(1)

headers = {
    "Cookie": f"cftpSID={cookie}"
}

url = "https://url.publishedprices.co.il/file"
response = requests.get(url, headers=headers)

print(f"Status code: {response.status_code}")
print(response.text[:300])

# שמירת הקוקי
with open("cftpSID.txt", "w") as f:
    f.write(cookie)
    print("✅ הקוקי נשמר לקובץ cftpSID.txt")
