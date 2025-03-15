import flet as ft
import threading
import httpx
from model.volunteer_model import VolunteerModel
from view.volunteer_view import VolunteerView
from controller.sidebar_controller import SidebarController

class VolunteerController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = VolunteerModel()
        self.view = VolunteerView(self)

        self.page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor="#4CAF50")

        # Store references to components for proper removal
        self.volunteer_content = None
        self.sidebar = None

    def load_volunteer(self):
        """Loads the volunteer page and ensures sidebar is displayed first."""
        print("✅ load_volunteer() called")  # Debugging output

        if self.page.data is None:
            self.page.data = {}

        self.page.data["volunteer_form_active"] = True

        # Load sidebar first
        sidebar_controller = SidebarController(self.page)
        sidebar = sidebar_controller.build()

        # Clear only volunteer-related content, not the sidebar
        self.page.controls.clear()
        self.page.add(sidebar)  # Sidebar remains

        # Build volunteer content correctly
        volunteer_content = self.view.build(self.page)  
        if volunteer_content is None:
            print("⚠️ Error: Volunteer view returned None!")
            return  # Exit early to prevent adding None to page

        self.page.add(volunteer_content)  # Add volunteer content after sidebar
        self.page.update()  # Force UI refresh

        # Listen to route changes
        self.page.on_route_change = self.handle_route_change

    def handle_route_change(self, e):
        """Handles route changes and reloads the page."""
        print(f"Route changed to: {self.page.route}")
        # Rebuild the page based on the new route
        self.load_volunteer()


    def remove_volunteer_view(self):
        """Properly remove the volunteer UI if it exists."""
        volunteer_content = self.page.data.get("volunteer_content")
        if not volunteer_content:
            print("⚠️ No volunteer content to remove. Skipping.")
            return

        print("✅ Attempting to remove Volunteer Page...")

        if volunteer_content in self.page.controls:
            self.page.controls.remove(volunteer_content)
            self.page.update()
            print("✅ Volunteer Page Removed!")
        else:
            print("⚠️ Volunteer content exists but was not found in controls!")

        # Remove the stored reference
        self.page.data["volunteer_content"] = None







    def load_events(self):
        """Fetches joined events and updates the UI properly."""
        try:
            self.view.scrollable_results.controls.clear()
            self.view.scrollable_results.controls.append(ft.Text("Loading Events...", size=20, color="white"))
            self.page.update()

            username = self.page.data.get("username")
            if not username:
                self.view.scrollable_results.controls.append(ft.Text("Error: No user logged in.", size=20, color="red"))
                self.page.update()
                return

            events = self.model.fetch_joined_events(username, self.page.data.get("category"))
            self.view.update_event_list(self.page, events)

        except Exception as e:
            print(f"Error loading events: {e}")
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
                self.page.snack_bar.content = ft.Text("You are now a volunteer!")
                self.page.snack_bar.bgcolor = "#4CAF50"
                e.control.text = "Volunteering!"
                e.control.bgcolor = "#4CAF50"
                e.control.disabled = True
                e.control.update()
            else:
                self.page.snack_bar.content = ft.Text("Failed to update status!")
                self.page.snack_bar.bgcolor = "red"
        except Exception as ex:
            self.page.snack_bar.content = ft.Text(f"Error updating status: {ex}")
            self.page.snack_bar.bgcolor = "red"
        finally:
            self.page.snack_bar.open = True
            self.page.update()

def main(page: ft.Page):
    controller = VolunteerController(page)
    controller.load_volunteer()

if __name__ == "__main__":
    ft.app(target=main)
