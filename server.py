from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
import bcrypt
import httpx
from datetime import datetime
from typing import Optional

app = FastAPI()

client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/")
db = client["EventLink"]
users_collection = db["users"]
regions_collection = db["regions"]
events_collection = db["events"]

# Updated Luzon regions list
Luzon_regions = [
    "Ilocos/Ilocandia",
    "Cagayan Valley/Northern Luzon",
    "Cordillera Administrative Region (CAR)",
    "Central Luzon",
    "National Capital Region (NCR)",
    "Southern Tagalog Regions-4A (Cavite, Laguna, Batangas, Rizal, and Quezon)",
    "Southern Tagalog Regions-4B (Mindoro, Marinduque, Romblon, and Palawan)",
    "Bicol/Bicolandia"
]

# Force update regions collection on server start
regions_collection.delete_many({})
regions_collection.insert_many([{"name": region} for region in Luzon_regions])

@app.get("/regions")
def get_regions():
    """Fetch all Luzon regions"""
    regions = [region["name"] for region in regions_collection.find()]
    return {"regions": regions}

@app.get("/search_events")
def search_events(region: str):
    """Search events by location"""
    events = list(events_collection.find({"location": region}, {"_id": 0}))
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this location.")
    return {"events": events}

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    contact: str
    password: str
    gender: Optional[str] = "N/A"

class UserLogin(BaseModel):
    identifier: str
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
    username_exists = users_collection.find_one({"username": user.username})
    email_exists = users_collection.find_one({"email": user.email})

    if username_exists and email_exists:
        raise HTTPException(status_code=400, detail="Username and Email already exist")
    elif username_exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    elif email_exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "contact": user.contact,
        "password": hashed_password.decode(),
        "gender": user.gender,
        "date_joined": datetime.now().strftime("%Y-%m-%d")
    })
    return {"message": "Registration successful"}

@app.get("/get_user")
def get_user(username: str):
    doc = users_collection.find_one({"username": username})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": doc["username"],
        "email": doc["email"],
        "contact": doc["contact"],
        "backup_email": doc.get("backup_email", "N/A"),
        "backup_number": doc.get("backup_number", "N/A"),
        "address": doc.get("address", "N/A"),
        "gender": doc.get("gender", "N/A"),
        "date_joined": doc.get("date_joined", "N/A")
    }

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    backup_email: Optional[str] = None
    contact: Optional[str] = None
    backup_number: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None

@app.patch("/update_user")
def update_user(username: str, updates: UserUpdate):
    doc = users_collection.find_one({"username": username})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = updates.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    result = users_collection.update_one({"username": username}, {"$set": update_data})
    if result.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        return {"message": "No changes made"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
