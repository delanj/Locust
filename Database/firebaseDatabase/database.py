import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/Users/nick/Desktop/Locust/Database/firebaseDatabase/locUst_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()