from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
import bcrypt

app = FastAPI()

client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/")
db = client["EventLink"]
users_collection = db["users"]

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    contact: str
    password: str

class UserLogin(BaseModel):
    identifier: str  # Username or email
    password: str

@app.post("/login")
def login(user: UserLogin):
    found = users_collection.find_one({
        "$or": [
            {"username": user.identifier},
            {"email": user.identifier}
        ]
    })
    if not found:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    stored_password = found["password"].encode()
    if bcrypt.checkpw(user.password.encode(), stored_password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/register")
def register(user: UserRegister):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "contact": user.contact,
        "password": hashed_password.decode()
    })
    return {"message": "Registration successful"}

@app.get("/check-username")
def check_username(username: str):
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "Username available"}

@app.get("/check-email")
def check_email(email: str):
    if users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"message": "Email available"}

@app.get("/events")
def get_events():
    return [
        {"title": "Operating Systems"},
        {"title": "Software Design"},
        {"title": "Electronics Lecture"},
    ]
