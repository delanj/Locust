import os

import firebase_admin
from firebase_admin import credentials, firestore

current_file_directory = os.path.dirname(os.path.abspath(__file__))
locust_directory = os.path.abspath(os.path.join(current_file_directory, '..', '..'))
file_path = os.path.join(locust_directory, "Database", "firebaseDatabase", "locUst_key.json")


cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred)

db = firestore.client()