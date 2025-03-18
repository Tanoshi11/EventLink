# controllers/CreateEvents_controller.py
import flet as ft
from flet import (
    Row,
    Column,
    Container,
    Text,
    TextField,
    ElevatedButton,
    Dropdown,
    Alignment
)
import datetime
import httpx
from controller.sidebar_controller import SidebarController

PAGE_BG_COLOR = "#0C3B2E"    # Dark green (used for page & sidebar)
TEXT_COLOR = "#FDF7E3"
ACCENT_COLOR = "#ffba00"
SECONDARY_COLOR = "#0c3b2e"
WHITE = "#ffffff"
DARK_TEXT = "#333333"

def fetch_regions():
    try:
        response = httpx.get("http://127.0.0.1:8000/regions")
        response.raise_for_status()
        return response.json()["regions"]
    except:
        return []

class CreateEventsController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "EventLink - Create Event"
        self.page.bgcolor = PAGE_BG_COLOR
        self.page.padding = 0

    def show_create_event_form(self):

        # -- SIDEBAR (CACHED) --
        if "sidebar" not in self.page.data:
            sidebar_controller = SidebarController(self.page)
            sidebar = sidebar_controller.build()
            self.page.data["sidebar"] = sidebar
        else:
            sidebar = self.page.data["sidebar"]

        sidebar_container = Container(
            content=sidebar,
            width=250,
            bgcolor=PAGE_BG_COLOR,
            expand=False,
        )

        # -- FORM FIELDS --
        event_name = TextField(label="Event Name", width=400)
        event_type = Dropdown(
            label="Event Type",
            width=400,
            options=[
            ft.dropdown.Option("Arts"),
            ft.dropdown.Option("Business"),
            ft.dropdown.Option("Charity"),
            ft.dropdown.Option("Community"),
            ft.dropdown.Option("Education"),
            ft.dropdown.Option("Entertainment"),
            ft.dropdown.Option("Environment"),
            ft.dropdown.Option("Food"),
            ft.dropdown.Option("Gaming"),
            ft.dropdown.Option("Health"),
            ft.dropdown.Option("Music"),
            ft.dropdown.Option("Politics"),
            ft.dropdown.Option("Sports"),
            ft.dropdown.Option("Technology"),
            ft.dropdown.Option("Travel"),
            ],
        )
        event_date = TextField(label="Event Date (YYYY-MM-DD)", width=400)
        time_start_field = TextField(label="Start Time (HH:MM)", width=195)
        time_end_field = TextField(label="End Time (HH:MM)", width=195)

        time_row = ft.Row(
            controls=[time_start_field, time_end_field],
            spacing=10
        )

        event_attendees = TextField(label="Guest Limit", width=400)
        event_ticket_price = TextField(label="Ticket Price", width=400)

        luzon_regions = fetch_regions()
        event_location = Dropdown(
            label="Location",
            width=400,
            options=[ft.dropdown.Option(region) for region in luzon_regions],
        )
        event_description = TextField(
            label="Description",
            multiline=True,
            width=400,
            height=120
        )

        def submit_form(e):
            # Validate and submit logic
            # ...
            self.page.update()

        # -- FORM LAYOUT --
        form_column = Column(
            controls=[
                Text("Create Event", size=24, weight=ft.FontWeight.BOLD, color=WHITE),
                event_name,
                event_type,
                event_date,
                time_row,
                event_attendees,
                event_ticket_price,
                event_location,
                event_description,
                ElevatedButton(
                    "Submit",
                    on_click=submit_form,
                    bgcolor=ACCENT_COLOR,
                    color=SECONDARY_COLOR,
                    width=120,
                ),
            ],
            spacing=12,
            alignment="center"
        )

        # Inner container (the form "card") with rounded borders, padding, and green background.
        form_container = Container(
            content=form_column,
            alignment=ft.alignment.center,
            border_radius=20,
            padding=20,
            width=500,
            bgcolor=PAGE_BG_COLOR,
        )

        # Main container that fills the available area to the right and bottom.
        content_container = Container(
            content=form_container,
            bgcolor="#D6AA54",
            border_radius=0,
            padding=20,
            expand=True,
            alignment=ft.alignment.center,
        )

        # Offset container so it doesn't overlap the sidebar & header.
        main_content = Container(
            content=content_container,
            margin=ft.margin.only(left=250, top=80),
            expand=True,
            alignment=ft.alignment.center,
        )

        # -- STACK LAYOUT (HEADER, SIDEBAR, MAIN CONTENT) --
        final_layout = ft.Stack(
            controls=[
                sidebar_container,
                main_content,
            ],
            expand=True
        )

        self.page.controls.clear()
        self.page.add(final_layout)
        self.page.update()

#
# Helper functions
#
def load_create_event(page: ft.Page):
    controller = CreateEventsController(page)
    controller.show_create_event_form()

if __name__ == "__main__":
    ft.app(target=load_create_event)
