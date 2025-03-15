import flet as ft
import threading
import httpx
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
        self.volunteer_form_controller = VolunteerFormController(page)  # Instantiate VolunteerFormController

    def fetch_joined_events(self):
        """Fetch events from API and return the JSON response."""
        try:
            username = self.page.data.get("username", "default_user")  # ✅ Ensure username is retrieved
            category = self.page.data.get("category", None)
            url = f"http://localhost:8000/my_events?username={username}"
            if category:
                url += f"&category={category}"
                
            response = httpx.get(url)  # ✅ Make API request
            if response.status_code == 200:
                return response.json().get("events", [])
        except Exception as ex:
            print("⚠️ Error fetching events:", ex)
        return []

    def load_volunteer(self):
        """Loads the volunteer page and ensures sidebar is displayed first."""
        print("✅ load_volunteer() called")  # Debugging output

        if self.page.data is None:
            self.page.data = {}

        self.page.data["volunteer_form_active"] = True

        # ✅ Load sidebar first
        sidebar_controller = SidebarController(self.page)
        sidebar = sidebar_controller.build()

        # ✅ Clear only volunteer-related content, not the sidebar
        self.page.controls.clear()

        # ✅ Build volunteer content correctly
        volunteer_content = self.view.build(self.page)  
        if volunteer_content is None:
            print("⚠️ Error: Volunteer view returned None!")
            return  # Exit early to prevent adding None to page

        self.page.add(volunteer_content)  # Add volunteer content after sidebar

        # ✅ Load events in the background
        threading.Thread(target=self.load_events, daemon=True).start()
        self.page.update()  # Force UI refresh

    def load_events(self):
        """Fetches joined events and updates the UI properly."""
        try:
            # ✅ Clear the event list before loading
            self.view.scrollable_results.controls.clear()
            self.view.scrollable_results.controls.append(ft.Text("Loading Events...", size=20, color="white"))
            self.page.update()

            # ✅ Fetch events using API
            username = self.page.data.get("username")  # ✅ Get username
            if not username:
                print("⚠️ No username found, cannot fetch events.")
                self.view.scrollable_results.controls.append(ft.Text("Error: No user logged in.", size=20, color="red"))
                self.page.update()
                return

            events = self.model.fetch_joined_events(username)  # ✅ Correctly pass username

            # ✅ Update UI with event list
            self.view.update_event_list(self.page, events)

        except Exception as e:
            print(f"❌ Error loading events: {e}")
            self.view.scrollable_results.controls.clear()
            self.view.scrollable_results.controls.append(ft.Text("Failed to load events.", size=20, color="red"))
            self.page.update()

    def update_volunteer_status(self, e, event_id: str):
        """Updates the user status to 'Volunteer' for an event."""
        try:
            username = self.page.data.get("username")
            if not username:
                return
            response = httpx.patch(
                f"http://localhost:8000/update_user?username={username}",
                json={"status": "Volunteer"}
            )
            if response.status_code == 200:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text("You are now a volunteer!"),
                    bgcolor="#4CAF50"
                )
                e.control.text = "Volunteering!"
                e.control.bgcolor = "#4CAF50"
                e.control.disabled = True
                e.control.update()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Error updating status: {ex}"),
                bgcolor="red"
            )
        finally:
            self.page.snack_bar.open = True
            self.page.update()

def main(page: ft.Page):
    """Main entry point for the Flet app."""
    controller = VolunteerController(page)
    controller.load_volunteer()

if __name__ == "__main__":
    ft.app(target=main)