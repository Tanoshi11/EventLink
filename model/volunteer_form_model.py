import httpx

class VolunteerFormModel:
    @staticmethod
    def fetch_joined_events(username):
        """Fetch events where the user has already joined."""
        try:
            url = f"http://localhost:8000/my_events?username={username}"
            response = httpx.get(url)
            if response.status_code == 200:
                return response.json().get("events", [])
        except Exception as ex:
            print("Error fetching events:", ex)
        return []

    @staticmethod
    def update_volunteer_status(username):
        """Update user to 'Volunteer' for an event."""
        try:
            if not username:
                return False
            response = httpx.patch(
                f"http://localhost:8000/update_user?username={username}",
                json={"status": "Volunteer"}
            )
            return response.status_code == 200
        except Exception as ex:
            print(f"Error updating status: {ex}")
            return False
