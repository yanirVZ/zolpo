import firebase_admin
from firebase_admin import credentials, firestore

# נתיב לקובץ המפתח
cred = credentials.Certificate("C:/Users/user/zolpo/shufersal_scraper/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def delete_all_supermarkets():
    supermarkets_ref = db.collection("products")
    docs = supermarkets_ref.stream()
    deleted = 0

    for doc in docs:
        supermarkets_ref.document(doc.id).delete()
        deleted += 1

    print(f"✅ נמחקו {deleted} חנויות מהאוסף 'supermarkets'.")

if __name__ == "__main__":
    delete_all_supermarkets()
