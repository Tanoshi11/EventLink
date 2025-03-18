import httpx
from datetime import datetime
class VolunteerModel:
    def fetch_joined_events(self, username, category=None):
        """Fetch events based on the selected category."""
        try:
            url = f"http://localhost:8000/my_events?username={username}"
            if category:
                url += f"&category={category}"
            response = httpx.get(url)
            if response.status_code == 200:
                return response.json().get("events", [])
        except Exception as ex:
            print("Error fetching events:", ex)
        return []

    @staticmethod
    def update_volunteer_status(username: str, event_id: str) -> bool:
        """
        Update user to 'Volunteer' for an event.

        Args:
            username (str): The username of the logged-in user.
            event_id (str): The ID of the event to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            if not username or not event_id:
                print("⚠️ Username or event ID is missing.")
                return False

            # Update the user's status to "Volunteer"
            response = httpx.patch(
                f"http://localhost:8000/update_user?username={username}",
                json={"status": "Volunteer"},
                timeout=10  # Add timeout for better reliability
            )

            # Debugging output
            print("Update Response Status:", response.status_code)
            print("Update Response Content:", response.text)

            return response.status_code == 200
        except httpx.RequestError as ex:
            print(f"⚠️ Network Error: {ex}")
            return False
        except Exception as ex:
            print(f"⚠️ Error updating status: {ex}")
            return False

    @staticmethod
    def get_event_status(event_date: str, event_time: str) -> str:
        """
        Calculate the status of an event based on the current date and time.

        Args:
            event_date (str): The date of the event in "YYYY-MM-DD" format.
            event_time (str): The time of the event (can be a range like "18:00 - 22:00").

        Returns:
            str: The status of the event ("Available" or "Closed").
        """
        try:
            # Extract the start time from the time range (e.g., "18:00 - 22:00" -> "18:00")
            start_time = event_time.split(" - ")[0].strip()

            # Construct a clean datetime string
            event_datetime_str = f"{event_date} {start_time}"

            # Convert string to datetime
            event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")

            # Get the current datetime
            current_datetime = datetime.now()

            # Determine the event status
            if current_datetime > event_datetime:
                return "Closed"
            else:
                return "Available"
        except Exception as e:
            print(f"⚠️ Error calculating event status: {e}")
            return "Closed"  # Fallback status if parsing fails