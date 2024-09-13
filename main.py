import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from models.user_model import User


# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\Harshit Joshi\RestApi\firebase-service-account.json")
# firebase_admin.initialize_app(cred)

# Firestore database
db = firestore.client()

app = FastAPI()

# Pydantic models for request bodies
class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str


@app.get("/")
def hellyeah():
    return {"messge":"hello"}

@app.post("/register")
async def register(user: RegisterUser):
    # Check if username or email already exists
    username_check = User.find_by_username(user.username)
    # username_check=True
    if username_check:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    email_check = User.find_by_email(user.email)
    # email_check=True
    if email_check:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create new user with hashed password
    User.create_user(user.username, user.email, user.password)
    return {"msg": "User registered successfully", "status": True}


@app.post("/login")
async def login(user: LoginUser):
    # Find user by username
    user_query = User.find_by_username(user.username)
    
    if not user_query:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Get the user data from Firestore
    user_data = user_query.to_dict()
    
    # Verify the password using bcrypt
    if not User.verify_password(user_data["password"], user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"msg": "Login successful", "user": user_data, "status": True}
