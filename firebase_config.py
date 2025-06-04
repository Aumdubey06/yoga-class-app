import firebase_admin
from firebase_admin import credentials, firestore

# Only initialize if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
