from fastapi import FastAPI, HTTPException, Query , WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
import bcrypt
import re
import asyncio
from datetime import datetime
from typing import Optional, List

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

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Send notification and broadcast via WebSocket
def send_notification(username: str, message: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notification = {"username": username, "message": message, "date": current_time}
    notifications_collection.insert_one(notification)

    formatted_message = f"{username}: {message}"

    # Ensure WebSocket messages are sent correctly
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    asyncio.run_coroutine_threadsafe(manager.broadcast(formatted_message), loop)
    print(f"📢 WebSocket Notification Sent: {formatted_message}")  # Debugging print


@app.get("/get_user")
def get_user(username: str):
    user = users_collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}}, {"_id": 0})
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
    print(f"🔍 Searching events - Query: '{query}', Region: '{region}'")  # Debugging

    try:
        if query.lower() == "all":
            if region:
                escaped_region = re.escape(region)
                events = list(events_collection.find(
                    {"location": {"$regex": escaped_region, "$options": "i"}},
                    {"_id": 0}
                ))
            else:
                events = list(events_collection.find({}, {"_id": 0}))
        else:
            filter_query = {
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ]
            }
            if region:
                escaped_region = re.escape(region)
                filter_query["location"] = {"$regex": escaped_region, "$options": "i"}
            events = list(events_collection.find(filter_query, {"_id": 0}))

        print(f"✅ Found {len(events)} events.")  # Debugging
        current_datetime = datetime.now()

        for event in events:
            try:
                print(f"🔹 Processing event: {event}")  # Log each event before processing

                if "date" not in event or "time" not in event:
                    print("⚠️ Event missing 'date' or 'time':", event)
                    continue  # Skip this event to prevent crashing

                time_value = event["time"].strip()  # Remove extra spaces
    
                # Extract only the start time (before " - ") if a range exists
                start_time = time_value.split(" - ")[0]  

                # Construct a clean datetime string
                event_datetime_str = f"{event['date']} {start_time}"

                # Debugging print to verify the extracted datetime string
                print(f"✅ Cleaned event_datetime_str: {event_datetime_str}")

                # Convert string to datetime
                event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")

                # Assign event status
                if current_datetime > event_datetime:
                    event["status"] = "Closed"
                elif current_datetime.date() == event_datetime.date():
                    event["status"] = "Ongoing"
                else:
                    event["status"] = "Upcoming"

            except ValueError as e:
                print(f"❌ ValueError: {e} - Event data: {event}")  # Log parsing issues

        if not events:
            raise HTTPException(status_code=404, detail="No events found matching the criteria.")

        return {"events": events}

    except Exception as e:
        print(f"🔥 Internal Server Error: {e}")  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/search_events_by_category")
def search_events_by_category(category: str):
    """Search events by category (using the 'type' field)"""
    events = list(events_collection.find(
        {"type": {"$regex": f"^{category}$", "$options": "i"}},  # Case-insensitive exact match
        {"_id": 0}
    ))

    current_datetime = datetime.now()

    for event in events:
        time_value = event["time"].strip()  # Remove extra spaces
    
        # Extract only the start time (before " - ") if a range exists
        start_time = time_value.split(" - ")[0]  

        # Construct a clean datetime string
        event_datetime_str = f"{event['date']} {start_time}"

        # Debugging print to verify the extracted datetime string
        print(f"✅ Cleaned event_datetime_str: {event_datetime_str}")

        # Convert string to datetime
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")

        # Assign event status
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
    
    if username_exists or email_exists:
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    user_data = {"username": user.username, "email": user.email, "password": hashed_password}
    users_collection.insert_one(user_data)
    
    send_notification(user.username, "Welcome to EventLink! Thank you for signing up.")
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
        try:
            # Extract the start time from the time range (e.g., "18:00 - 22:00" -> "18:00")
            start_time = event["time"].split(" - ")[0].strip()

            # Construct a clean datetime string
            event_datetime_str = f"{event['date']} {start_time}"

            # Debugging print to verify the extracted datetime string
            print(f"✅ Cleaned event_datetime_str: {event_datetime_str}")

            # Convert string to datetime
            event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")

            # Assign event status
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

        except Exception as e:
            print(f"❌ Error processing event {event.get('name')}: {e}")
            event["status"] = "Unknown"  # Fallback status if parsing fails

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
    description: Optional[str] = None  # Added field

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
    host: str
    name: str
    type: str
    date: str
    ticket_price: int
    time: str
    guest_limit: int
    location: str
    description: str
    created_at: str

@app.post("/create_event")
def create_event(event: BaseModel):
    event_data = event.dict()
    event_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events_collection.insert_one(event_data)
    
    send_notification(event.host, f"Your event '{event.name}' has been created!")
    return {"message": "Event created successfully"}


from pydantic import BaseModel

class JoinEventRequest(BaseModel):
    username: str
    event_name: str

@app.post("/join_event")
def join_event(request: JoinEventRequest):
    event = events_collection.find_one({"name": request.event_name})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    
    events_collection.update_one(
        {"name": request.event_name},
        {"$push": {"participants": request.username}}
    )
    
    send_notification(request.username, f"You have joined the event '{request.event_name}'!")
    return {"message": "Event joined successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)