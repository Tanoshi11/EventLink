import flet as ft
import threading
import time
import httpx
from utils import clear_overlay
from model.volunteer_model import VolunteerModel
from view.volunteer_view import VolunteerView
from controller.volunteer_form_controller import VolunteerFormController
from controller.sidebar_controller import SidebarController

class VolunteerController:
    def __init__(self, page: ft.Page):
        if page is None:
            raise ValueError("Page cannot be None in VolunteerController")
        self.page = page
        self.model = VolunteerModel()
        self.view = VolunteerView(self)
        self.volunteer_form_controller = VolunteerFormController(page)

        if self.page.data is None:
            self.page.data = {}

        print("✅ VolunteerController initialized")  # Debugging print

    def fetch_joined_events(self):
        """Fetch events from API and return the JSON response."""
        try:
            username = self.page.data.get("username", None)
            if not username:
                print("⚠️ Error: No username found in session!")
                return []

            url = f"http://localhost:8000/my_events?username={username}"
            print(f"Fetching events from URL: {url}")  # Debugging print
            response = httpx.get(url)  

            if response.status_code == 200:
                print("✅ Successfully fetched events from API.")  # Debugging print
                events = response.json().get("events", [])
                print(f"Fetched events: {events}")  # Debugging print
                return events
            else:
                print(f"⚠️ API Error: {response.status_code} - {response.text}")
                return []

        except Exception as ex:
            print("❌ Error fetching events:", ex)
            return []

    def load_volunteer(self):
        """Loads the Volunteer page."""
        print("Loading Volunteer page...")  # Debugging print
        if hasattr(self.page, "overlay"):
            clear_overlay(self.page)

        if self.page.data is None:
            self.page.data = {}

        self.page.title = "Volunteer Opportunities"
        self.page.bgcolor = "#d6aa54"

        sidebar_controller = SidebarController(self.page)
        sidebar = sidebar_controller.build()

        volunteer_view = VolunteerView(self)

        main_stack = ft.Stack(
            controls=[
                sidebar,
                volunteer_view.build(self.page)  # ✅ No "Back to Home" button
            ],
            expand=True,
        )

        self.page.controls.clear()
        self.page.add(main_stack)
        self.page.update()

        print("Starting thread to load events...")  # Debugging print
        threading.Thread(target=self.load_events, daemon=True).start()

    def load_events(self):
        try:
            print("Fetching joined events...")  # Debugging print
            self.view.scrollable_results.controls.clear()
            self.view.scrollable_results.controls.append(ft.Text("Fetching events...", size=20, color="white"))
            self.page.update()

            events = self.fetch_joined_events()  
            print(f"✅ Debug: Loaded events: {events}")  # Debug print

            if not events:
                print("⚠️ No events found after fetching.")  # Debugging print
                time.sleep(1)  

            # Ensure UI updates happen on the main thread
            self.page.run_task(self.view.update_event_list, self.page, events)

        except Exception as e:
            print(f"❌ Error loading events: {e}")
            print(f"Error details: {e.__class__.__name__}: {str(e)}")  # Detailed error logging
            self.view.scrollable_results.controls.clear()
            self.view.scrollable_results.controls.append(ft.Text("Failed to load events.", size=20, color="red"))
            self.page.update()

    def update_volunteer_status(self, e, event_id: str):
        """Updates the user status to 'Volunteer' for an event."""
        try:
            username = self.page.data.get("username")
            if not username:
                print("⚠️ No username found in session!")
                return
            
            print(f"Updating volunteer status for event: {event_id}")  # Debugging print
            response = httpx.patch(
                f"http://localhost:8000/update_user?username={username}",
                json={"status": "Volunteer"}
            )
            
            if response.status_code == 200:
                print("✅ Successfully updated volunteer status.")  # Debugging print
                self.page.snack_bar.content = ft.Text("You are now a volunteer!")
                self.page.snack_bar.bgcolor = "#4CAF50"
                self.page.snack_bar.open = True

                e.control.text = "Volunteering!"
                e.control.bgcolor = "#4CAF50"
                e.control.disabled = True
                e.control.update()

        except Exception as ex:
            print(f"❌ Error updating status: {ex}")  # Debugging print
            self.page.snack_bar.content = ft.Text(f"Error updating status: {ex}")
            self.page.snack_bar.bgcolor = "red"
            self.page.snack_bar.open = True
        
        finally:
            self.page.update()

def main(page: ft.Page):
    """Main entry point for the Flet app."""
    print("Starting Flet app...")  # Debugging print
    controller = VolunteerController(page)
    controller.load_volunteer()

if __name__ == "__main__":
    ft.app(target=main)