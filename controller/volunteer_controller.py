import flet as ft
import threading
from model.volunteer_model import VolunteerModel
from view.volunteer_view import VolunteerView
from controller.volunteer_form_controller import VolunteerFormController
from controller.sidebar_controller import SidebarController  # ✅ Import SidebarController

class VolunteerController:
    def __init__(self, page: ft.Page):
        if page is None:
            raise ValueError("Page cannot be None in VolunteerController")
        self.page = page
        self.model = VolunteerModel()
        self.view = VolunteerView(self)

    def get_event_status(self, event_date: str, event_time: str) -> str:
        return self.model.get_event_status(event_date, event_time)

    def load_header(self, page):
        from header import load_header  # ✅ Lazy import to prevent circular import issues
        return load_header(page)

    def show_volunteer_popup(self, page, event):
        """Displays the volunteer form popup for the given event."""
        volunteer_form_controller = VolunteerFormController(page)
        volunteer_form_controller.show_volunteer_popup(page, event)

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
        self.page.add(sidebar)  # Sidebar remains

        # ✅ Build volunteer content correctly
        volunteer_content = self.view.build(self.page)  
        if volunteer_content is None:
            print("⚠️ Error: Volunteer view returned None!")
            return  # Exit early to prevent adding None to page

        self.page.add(volunteer_content)  # Add volunteer content after sidebar
        self.page.update()  # Force UI refresh

        # ✅ Load events in the background
        threading.Thread(target=self.load_events, daemon=True).start()

    def load_events(self):
        """Loads events the user has joined and updates the event list."""
        try:
            self.view.results_list.controls.clear()
            self.view.results_list.controls.append(ft.Text("Loading Results...", size=20, color="white"))
            self.page.update()

            username = self.page.data.get("username")
            if not username:
                print("⚠️ No username found, cannot fetch events.")
                self.view.results_list.controls.append(ft.Text("Error: No user logged in.", size=20, color="red"))
                self.page.update()
                return

            events = self.model.fetch_joined_events(username)
            print("Fetched events:", events)  # Debugging output

            self.view.update_event_list(self.page, events)
        except Exception as e:
            print(f"Error loading events: {e}")
            self.view.results_list.controls.clear()
            self.view.results_list.controls.append(ft.Text("Failed to load events.", size=20, color="red"))
            self.page.update()

def main(page: ft.Page):
    """Main entry point for the Flet app."""
    controller = VolunteerController(page)
    controller.load_volunteer()

if __name__ == "__main__":
    ft.app(target=main)
