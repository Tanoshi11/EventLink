from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import bcrypt

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/")
db = client["EventLink"]
users_collection = db["users"]

class User(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(user: User):
    found = users_collection.find_one({"username": user.username})
    if not found:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    stored_password = found["password"].encode()
    if bcrypt.checkpw(user.password.encode(), stored_password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/register")
def register(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_collection.insert_one({"username": user.username, "password": hashed_password.decode()})
    return {"message": "Registration successful"}

@app.get("/events")
def get_events():
    # Return dummy events for now
    return [
        {"title": "Operating Systems"},
        {"title": "Software Design"},
        {"title": "Electronics Lecture"},
    ]
