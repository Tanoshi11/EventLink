# controllers/CreateEvents_controller.py
import flet as ft
from flet import (
    Row,
    Column,
    Container,
    Text,
    TextField,
    ElevatedButton,
    Image,
    Dropdown,
    border_radius,
    Alignment
)
import datetime
import httpx
from controller.sidebar_controller import SidebarController

# Color constants (adjust as needed)
PAGE_BG_COLOR = "#0C3B2E"
HEADER_BG_COLOR = "#A8730A"
CONTAINER_BG_COLOR = "#5F7755"
TEXT_COLOR = "#FDF7E3"
ACCENT_COLOR = "#ffba00"
SECONDARY_COLOR = "#0c3b2e"

def get_header_controller():
    from header import load_header  # Delayed import
    return load_header

def fetch_regions():
    try:
        response = httpx.get("http://127.0.0.1:8000/regions")
        response.raise_for_status()
        return response.json()["regions"]
    except:
        return []

def validate_date(date_str):
    if not date_str:
        return "Date is required."
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."
    if dt.date() < datetime.date.today():
        return "Date must be today or later."
    return None

def validate_time(time_str):
    if not time_str:
        return "Time is required."
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return None
    except ValueError:
        return "Invalid time format. Use HH:MM (24-hour)."

class CreateEventsController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "EventLink - Create Event"
        self.page.bgcolor = PAGE_BG_COLOR
        self.page.padding = 0

    def show_create_event_form(self):
        """Build and display the Create Event form with a fixed-width sidebar."""
      
        HeaderController = get_header_controller()
        header_container = HeaderController(self.page)

       
        sidebar_controller = SidebarController(self.page)
        sidebar_view = sidebar_controller.build()
        sidebar_container = Container(
            content=sidebar_view,
            width=250,         
            expand=False,      
            bgcolor=PAGE_BG_COLOR
        )

      
        def handle_date_pick(e):
            selected_date = e.control.value
            event_date.value = selected_date.strftime('%Y-%m-%d')
            self.page.update()

        def dismiss_date_picker(e):
            self.page.update()

        event_date = TextField(
            label="Event Date (YYYY-MM-DD)",
            width=400,
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: self.page.open(
                    ft.DatePicker(
                        first_date=datetime.datetime.now(),
                        last_date=datetime.datetime(year=3000, month=12, day=31),
                        on_change=handle_date_pick,
                        on_dismiss=dismiss_date_picker,
                    )
                )
            )
        )

        def handle_start_time(e):
            selected_time = e.control.value
            if selected_time:
                time_start_field.value = selected_time.strftime("%H:%M")
                self.page.update()

        def handle_end_time(e):
            selected_time = e.control.value
            if selected_time:
                time_end_field.value = selected_time.strftime("%H:%M")
                self.page.update()

        time_start_field = TextField(
            label="Start Time (HH:MM)",
            width=195,
            suffix=ft.IconButton(
                icon=ft.icons.ACCESS_TIME,
                on_click=lambda e: self.page.open(
                    ft.TimePicker(on_change=handle_start_time)
                )
            )
        )

        time_end_field = TextField(
            label="End Time (HH:MM)",
            width=195,
            suffix=ft.IconButton(
                icon=ft.icons.ACCESS_TIME,
                on_click=lambda e: self.page.open(
                    ft.TimePicker(on_change=handle_end_time)
                )
            )
        )

        time_row = Row(controls=[time_start_field, time_end_field], spacing=10)

        # Other form fields
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
            ]
        )
        luzon_regions = fetch_regions()
        event_location = Dropdown(
            label="Location",
            width=400,
            options=[ft.dropdown.Option(region) for region in luzon_regions]
        )
        event_attendees = TextField(label="Guest Limit", width=400)
        event_ticket_price = TextField(label="Ticket Price", width=400)
        event_description = TextField(label="Description", multiline=True, width=400, height=120)

        def submit_form(e):
            # Validate and submit logic
            # ...
            self.page.update()

        # 4. Build form layout
        form_column = Column(
            controls=[
                Text("Create Event", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
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
                    width=120
                ),
            ],
            spacing=12
        )

        form_container = Container(
            content=form_column,
            bgcolor="#D6AA54",  
            padding=20,
            border_radius=10,
            expand=True  
        )

       
        main_content = Row(
            controls=[sidebar_container, form_container],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

        
        final_layout = Column(
            controls=[
                header_container,   
                main_content        
            ],
            expand=True
        )

        # Clear and add
        self.page.controls.clear()
        self.page.add(final_layout)
        self.page.update()

#
# Helper functions
#
def load_create_event(page: ft.Page):
    controller = CreateEventsController(page)
    controller.show_create_event_form()

def load_homepage(page: ft.Page):
    page.controls.clear()
    import controller.homepg_controller as homepg
    homepg.main(page)

def load_login(page: ft.Page):
    page.floating_action_button = None
    # ...
    pass

def load_my_events(page: ft.Page):
    import my_events
    page.controls.clear()
    my_events.load_my_events(page)
    page.update()

def load_profile(page: ft.Page):
    page.floating_action_button = None
    pass

if __name__ == "__main__":
    ft.app(target=load_create_event)
