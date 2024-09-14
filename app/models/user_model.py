import bcrypt
import firebase_admin
from firebase_admin import firestore,credentials

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\Harshit Joshi\RestApi\firebase-service-account.json")
firebase_admin.initialize_app(cred)

# Firestore database
db = firestore.client()

users_collection = db.collection('users')  # Firestore collection for users

class User:
    @staticmethod
    def create_user(username: str, email: str, password: str):
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = {
            "username": username,
            "email": email,
            "password": hashed_password,  # Store the hashed password
        }
        return users_collection.add(user)

    @staticmethod
    def find_by_username(username: str):
        user_query = users_collection.where("username", "==", username).get()
        return user_query[0] if user_query else None

    @staticmethod
    def find_by_email(email: str):
        email_query = users_collection.where("email", "==", email).get()
        return email_query[0] if email_query else None

    @staticmethod
    def verify_password(stored_password: str, provided_password: str):
        # Verify hashed password
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
