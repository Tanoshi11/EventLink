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
        
        # ✅ Fix: Define snack bar early so it doesn't crash
        self.page.snack_bar = ft.SnackBar(ft.Text(""), bgcolor="#4CAF50")

    def fetch_joined_events(self):
        """Fetch events from API and return the JSON response."""
        try:
            username = self.page.data.get("username", None)
            if not username:
                print("⚠️ Error: No username found in session!")
                return []

            url = f"http://localhost:8000/my_events?username={username}"
            response = httpx.get(url)  
            
            if response.status_code == 200:
                return response.json().get("events", [])
            else:
                print(f"⚠️ API Error: {response.status_code} - {response.text}")
                return []

        except Exception as ex:
            print("❌ Error fetching events:", ex)
            return []

    def load_volunteer(self):
        """Loads the volunteer page and ensures sidebar is displayed first."""
        print("✅ load_volunteer() called")

        if self.page.data is None:
            self.page.data = {}

        self.page.data["volunteer_form_active"] = True

        # ✅ Preserve sidebar instead of reloading it
        if "sidebar" not in self.page.data:
            sidebar_controller = SidebarController(self.page)
            self.page.data["sidebar"] = sidebar_controller.build()  # Store sidebar

        sidebar = self.page.data["sidebar"]  # Reuse existing sidebar

        # ✅ Clear volunteer content but keep sidebar
        self.page.controls.clear()

        # ✅ Build volunteer content correctly
        volunteer_content = self.view.build(self.page)  
        if volunteer_content is None:
            print("⚠️ Error: Volunteer view returned None!")
            return  

        self.page.add(sidebar)  # ✅ Sidebar stays in place
        self.page.add(volunteer_content)  # ✅ Add volunteer content below sidebar

        # ✅ Load events in the background
        threading.Thread(target=self.load_events, daemon=True).start()
        self.page.update()  # Force UI refresh

    def load_events(self):
        """Fetches joined events and updates the UI properly."""
        try:
            # ✅ Clear event list before loading
            self.view.scrollable_results.controls.clear()
            self.view.scrollable_results.controls.append(ft.Text("Loading Events...", size=20, color="white"))
            self.page.update()

            # ✅ Fetch events using API
            events = self.fetch_joined_events()  # ✅ Now uses the correct function

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
                print("⚠️ No username found in session!")
                return
            
            response = httpx.patch(
                f"http://localhost:8000/update_user?username={username}",
                json={"status": "Volunteer"}
            )
            
            if response.status_code == 200:
                # ✅ Fix: Use pre-defined snackbar, not create a new one
                self.page.snack_bar.content = ft.Text("You are now a volunteer!")
                self.page.snack_bar.bgcolor = "#4CAF50"
                self.page.snack_bar.open = True

                # ✅ Update button state
                e.control.text = "Volunteering!"
                e.control.bgcolor = "#4CAF50"
                e.control.disabled = True
                e.control.update()

        except Exception as ex:
            # ✅ Fix: Use pre-defined snackbar for error
            self.page.snack_bar.content = ft.Text(f"Error updating status: {ex}")
            self.page.snack_bar.bgcolor = "red"
            self.page.snack_bar.open = True
        
        finally:
            self.page.update()

def main(page: ft.Page):
    """Main entry point for the Flet app."""
    controller = VolunteerController(page)
    controller.load_volunteer()

if __name__ == "__main__":
    ft.app(target=main)
