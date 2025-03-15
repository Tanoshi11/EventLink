import httpx
from datetime import datetime

class JoinEventModel:
    def __init__(self, event_id, title, date, time, available_slots):
        self.event_id = event_id
        self.title = title
        self.date = date
        self.time = time
        self.available_slots = available_slots

    def join_event(self, username):
        """Send a request to join the event."""
        join_data = {"username": username, "event_name": self.title}
        response = httpx.post("http://localhost:8000/join_event", json=join_data)

        if response.status_code == 200:
            joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {"success": True, "message": f"You have joined the event: {self.title}", "date": joined_date}
        else:
            return {"success": False, "error": response.json()}
