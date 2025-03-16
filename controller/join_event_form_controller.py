import flet as ft
from model.join_event_form_model import JoinEventModel
from view.join_event_form_view import JoinEventView

class JoinEventController:
    def __init__(self, page, event_id, title, date, time, available_slots, join_callback):
        self.page = page
        self.model = JoinEventModel(event_id, title, date, time, available_slots)
        self.join_callback = join_callback
        self.view = JoinEventView(self.model, self.submit_form, self.close_join_popup)

    def submit_form(self, e):
        error_found = False

        # Validate name
        if not self.view.event_attend_name.value:
            self.view.event_attend_name.error_text = "Name is required."
            error_found = True
        else:
            self.view.event_attend_name.error_text = None

        # Validate tickets
        if not self.view.event_ticket_tobuy.value:
            self.view.event_ticket_tobuy.error_text = "Number of tickets is required."
            error_found = True
        elif not self.view.event_ticket_tobuy.value.isdigit():
            self.view.event_ticket_tobuy.error_text = "Please enter a valid number."
            error_found = True
        elif int(self.view.event_ticket_tobuy.value) > int(self.model.available_slots):
            self.view.event_ticket_tobuy.error_text = "Not enough slots available."
            error_found = True
        else:
            self.view.event_ticket_tobuy.error_text = None

        self.page.update()

        if error_found:
            return

        username = self.page.data.get("username")
        response = self.model.join_event(username)

        if response["success"]:
            self.page.snack_bar = ft.SnackBar(
                ft.Column([
                    ft.Text(response["message"], color="white"),
                    ft.Text(f"Date: {response['date']}", size=12, color="white")
                ])
            )
            self.page.snack_bar.open = True
            self.page.update()
            self.join_callback()
        else:
            print("Error joining event:", response["error"])

        self.close_join_popup()

    def close_join_popup(self, e=None):
        """Close the join event form and clear the overlay."""
        if self.page.overlay:
            self.page.overlay.clear()
            self.page.update()

    def show_form(self):
        self.page.overlay.append(self.view.get_view())
        self.page.update()
