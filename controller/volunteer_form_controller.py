import flet as ft
from model.volunteer_form_model import VolunteerFormModel
from view.volunteer_form_view import VolunteerFormView

class VolunteerFormController:
    def __init__(self, page):
        self.page = page
        self.view = VolunteerFormView(self)
        self.username = page.data.get("username", "default_user")

    def fetch_joined_events(self):
        events = VolunteerFormModel.fetch_joined_events(self.username)
        print("Fetched events:", events)
        return events

    def update_volunteer_status(self, page):
        success = VolunteerFormModel.update_volunteer_status(self.username)
        page.snack_bar = ft.SnackBar(
            ft.Text("You are now a volunteer!" if success else "Error updating status", color="white"),
            bgcolor="#4CAF50" if success else "red"
        )
        page.snack_bar.open = True
        page.update()

    def show_volunteer_popup(self, page, event):
        self.view.show_volunteer_popup(page, event)