import firebase_admin
from firebase_admin import credentials, firestore
import os

firebase_creds = os.getenv("ServiceKey")
if firebase_creds is None:
    raise ValueError("Firebase service account key path not found in 'ServiceKey' environment variable.")
cred = credentials.Certificate(firebase_creds)

firebase_admin.initialize_app(cred)

db = firestore.client()