from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
import bcrypt
import re
from datetime import datetime
from typing import Optional

app = FastAPI()

client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/")
db = client["EventLink"]
users_collection = db["users"]
regions_collection = db["regions"]
events_collection = db["events"]
notifications_collection = db["notifications"]

print(list(events_collection.find({})))

# Updated Luzon, Visayas, and Mindanao regions list
regions = [
    "National Capital Region (NCR)",
    "Cordillera Administrative Region (CAR)",
    "Ilocos Region (Region I)",
    "Cagayan Valley (Region II)",
    "Central Luzon (Region III)",
    "CALABARZON (Region IV-A)",
    "MIMAROPA (Region IV-B)",
    "Bicol Region (Region V)",
    "Western Visayas (Region VI)",
    "Negros Island Region (NIR)",
    "Central Visayas (Region VII)",
    "Eastern Visayas (Region VIII)",
    "Zamboanga Peninsula (Region IX)",
    "Northern Mindanao (Region X)",
    "Davao Region (Region XI)",
    "Soccsksargen (Region XII)",
    "Caraga (Region XIII)",
    "Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)"
]

print("All regions:", regions)  # Debug print

# Force update regions collection on server start
regions_collection.delete_many({})
regions_collection.insert_many([{"name": region} for region in regions])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/get_user")
def get_user(username: str):
    user = users_collection.find_one({"username": username}, {"_id": 0})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/regions")
def get_regions():
    """Fetch all regions (Luzon, Visayas, and Mindanao)"""
    return {"regions": regions}

@app.get("/search_events")
def search_events(query: str = Query(...), region: str = None):
    """
    Search events by query and optionally by region.
    - If query is 'All', return all events (or all events for the provided region).
    - Otherwise, search events where the name or description contains the query (case-insensitive),
      and if region is provided, also filter by location.
    """
    print(f"Searching events - Query: '{query}', Region: '{region}'")  # Debugging

    # If the query is "All", ignore text filtering.
    if query.lower() == "all":
        if region:
            # Escape special characters in the region for regex
            escaped_region = re.escape(region)
            events = list(events_collection.find(
                {"location": {"$regex": escaped_region, "$options": "i"}},
                {"_id": 0}
            ))
        else:
            events = list(events_collection.find({}, {"_id": 0}))
    else:
        # Build a filter to search in 'name' or 'description'
        filter_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }
        if region:
            # Escape special characters in the region for regex
            escaped_region = re.escape(region)
            filter_query["location"] = {"$regex": escaped_region, "$options": "i"}
        events = list(events_collection.find(filter_query, {"_id": 0}))

    # Add event status based on the current date and time
    for event in events:
        event_datetime_str = f"{event['date']} {event['time']}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if current_datetime > event_datetime:
            event["status"] = "Closed"
        elif current_datetime.date() == event_datetime.date():
            event["status"] = "Ongoing"
        else:
            event["status"] = "Upcoming"

    print(f"Found {len(events)} events.")  # Debugging
    if not events:
        raise HTTPException(status_code=404, detail="No events found matching the criteria.")
    return {"events": events}

@app.get("/search_events_by_category")
def search_events_by_category(category: str):
    """Search events by category (using the 'type' field)"""
    events = list(events_collection.find(
        {"type": {"$regex": f"^{category}$", "$options": "i"}},  # Case-insensitive exact match
        {"_id": 0}
    ))

    # Add event status based on the current date and time
    for event in events:
        event_datetime_str = f"{event['date']} {event['time']}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if current_datetime > event_datetime:
            event["status"] = "Closed"
        elif current_datetime.date() == event_datetime.date():
            event["status"] = "Ongoing"
        else:
            event["status"] = "Upcoming"

    if not events:
        raise HTTPException(status_code=404, detail="No events found for this category.")
    return {"events": events}

@app.get("/display_events")
def display_events():
    """Fetch all available events"""
    events = list(events_collection.find({}, {"_id": 0}))

    # Add event status based on the current date and time
    for event in events:
        event_datetime_str = f"{event['date']} {event['time']}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if current_datetime > event_datetime:
            event["status"] = "Closed"
        elif current_datetime.date() == event_datetime.date():
            event["status"] = "Ongoing"
        else:
            event["status"] = "Upcoming"

    if not events:
        raise HTTPException(status_code=404, detail="No events found.")
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

    # Delete existing notifications for the username
    notifications_collection.delete_many({"username": user.username})

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_data = {
        "username": user.username,
        "email": user.email,
        "contact": user.contact,
        "password": hashed_password.decode(),
        "gender": user.gender,
        "date_joined": datetime.now().strftime("%Y-%m-%d")
    }
    users_collection.insert_one(user_data)
    
    # Create a welcome notification with date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    welcome_notification = {
        "username": user.username,
        "message": f"Welcome to EventLink! Thank you for signing up.\n------------------------\n{current_time}",
        "date": current_time
    }
    notifications_collection.insert_one(welcome_notification)

    return {"message": "Registration successful"}

@app.get("/all_events")
def get_all_events():
    """Fetch all events"""
    events = list(events_collection.find({}, {"_id": 0}))

    # Add event status based on the current date and time
    for event in events:
        event_datetime_str = f"{event['date']} {event['time']}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if current_datetime > event_datetime:
            event["status"] = "Closed"
        elif current_datetime.date() == event_datetime.date():
            event["status"] = "Ongoing"
        else:
            event["status"] = "Upcoming"

    return {"events": events}

@app.get("/my_events")
def get_my_events(username: str):
    """Fetch events the user has joined"""
    events = list(events_collection.find(
        {"participants.username": username},  # Ensure this matches the structure used in join_event
        {"_id": 0}
    ))

    # Add event status based on the current date and time
    for event in events:
        event_datetime_str = f"{event['date']} {event['time']}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if current_datetime > event_datetime:
            event["status"] = "Closed"
        elif current_datetime.date() == event_datetime.date():
            event["status"] = "Ongoing"
        else:
            event["status"] = "Upcoming"

        # Retrieve joined date for the current user from participants
        for participant in event.get("participants", []):
            if isinstance(participant, dict) and participant.get("username") == username:
                event["joined"] = participant.get("joined")
                break
        else:
            event["joined"] = "N/A"

    if not events:
        raise HTTPException(404, "No joined events found")
    return {"events": events}

@app.get("/notifications")
def get_notifications(username: str):
    """Fetch the user's notifications, sorted by date in descending order."""
    notifications = list(notifications_collection.find({"username": username}, {"_id": 0}).sort("date", -1))
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for this user.")
    return {"notifications": notifications}

@app.get("/profile")
def get_profile(username: str):
    """Fetch the user's profile."""
    profile = users_collection.find_one({"username": username}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="User not found.")
    return profile

class UpdateUserRequest(BaseModel):
    gender: Optional[str] = None
    backup_email: Optional[str] = None
    backup_number: Optional[str] = None
    address: Optional[str] = None

@app.patch("/update_user")
def update_user(username: str, update_data: UpdateUserRequest):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_values = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_values:
        raise HTTPException(status_code=400, detail="No fields to update")

    users_collection.update_one({"username": username}, {"$set": update_values})
    return {"message": "User updated successfully"}

@app.post("/logout")
def logout(username: str):
    """Log out the user."""
    return {"message": "Logout successful"}

class Notification(BaseModel):
    username: str
    message: str
    date: str

@app.post("/create_notification")
def create_notification(notification: Notification):
    notifications_collection.insert_one(notification.dict())
    return {"message": "Notification created"}

class Event(BaseModel):
    name: str
    type: str
    date: str
    time: str
    location: str
    description: str
    created_at: str

@app.post("/create_event")
def create_event(event: Event):
    try:
        event_data = event.dict()
        event_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        events_collection.insert_one(event_data)
        return {"message": "Event created successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error creating event: {ex}")

from pydantic import BaseModel

class JoinEventRequest(BaseModel):
    username: str
    event_name: str

@app.post("/join_event")
def join_event(request: JoinEventRequest):
    event = events_collection.find_one({"name": request.event_name})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    participants = event.get("participants", [])
    if any(isinstance(p, dict) and p.get("username") == request.username for p in participants):
        raise HTTPException(status_code=400, detail="User already joined this event.")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events_collection.update_one(
        {"name": request.event_name},
        {"$push": {"participants": {"username": request.username, "joined": current_time}}}
    )

    notification = {
        "username": request.username,
        "message": f"You have joined the event: {request.event_name}\n------------------------\n{current_time}",
        "date": current_time
    }
    notifications_collection.insert_one(notification)
    print(f"Notification created: {notification}")  # Debug print

    return {"message": "Event joined successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
