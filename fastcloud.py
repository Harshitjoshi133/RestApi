from fastapi import FastAPI,Body
import httpx
import firebase_admin
from firebase_admin import credentials,firestore

app = FastAPI()


@app.get("/")
async def start():
    return {"message":"Hello"}
