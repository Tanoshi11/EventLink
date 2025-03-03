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
    border_radius
)
import datetime
import httpx

PRIMARY_COLOR = "#6d9773"
SECONDARY_COLOR = "#0c3b2e"
ACCENT_COLOR = "#b46617"
HIGHLIGHT_COLOR = "#ffba00"

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
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

def validate_time(time_str):
    if not time_str:
        return "Time is required."
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return None
    except ValueError:
        return "Invalid time format. Use HH:MM (24-hour)."

def go_back(e, page):
    import homepg
    page.controls.clear()
    homepg.main(page)
    page.update()

def main(page: ft.Page):
    page.title = "Create Event"
    page.bgcolor = "#5F7755"

    # Back button
    back_button = ElevatedButton(
        text="Back",
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(e, page),
        bgcolor=HIGHLIGHT_COLOR,
        color=SECONDARY_COLOR
    )

    # Form fields
    event_name = TextField(label="Event Name", width=400)
    event_type = Dropdown(
        label="Event Type",
        width=400,
        options=[
            ft.dropdown.Option("Business"),
            ft.dropdown.Option("Food & Drink"),
            ft.dropdown.Option("Health"),
            ft.dropdown.Option("Travel"),
            ft.dropdown.Option("Music"),
            ft.dropdown.Option("Performing Arts"),
            ft.dropdown.Option("Fashion"),
            ft.dropdown.Option("Film & Media"),
            ft.dropdown.Option("Hobbies"),
            ft.dropdown.Option("Home & Lifestyle"),
            ft.dropdown.Option("Community"),
            ft.dropdown.Option("Charity & Causes"),
            ft.dropdown.Option("Government"),
        ]
    )
    event_date = TextField(label="Date (YYYY-MM-DD)", width=400)
    event_time = TextField(label="Time (HH:MM)", width=400)

    luzon_regions = fetch_regions()
    event_location = Dropdown(
        label="Location",
        width=400,
        options=[ft.dropdown.Option(region) for region in luzon_regions]
    )
    event_description = TextField(label="Description", multiline=True, width=400, height=80)

    def submit_form(e):
        error_found = False

        if not event_name.value:
            event_name.error_text = "Event Name is required."
            error_found = True
        else:
            event_name.error_text = None

        if not event_type.value:
            event_type.error_text = "Event Type is required."
            error_found = True
        else:
            event_type.error_text = None

        date_error = validate_date(event_date.value)
        if date_error:
            event_date.error_text = date_error
            error_found = True
        else:
            event_date.error_text = None

        time_error = validate_time(event_time.value)
        if time_error:
            event_time.error_text = time_error
            error_found = True
        else:
            event_time.error_text = None

        if not event_location.value:
            event_location.error_text = "Location is required."
            error_found = True
        else:
            event_location.error_text = None

        if not event_description.value:
            event_description.error_text = "Description is required."
            error_found = True
        else:
            event_description.error_text = None

        page.update()
        if error_found:
            return

        # Create event data payload
        event_data = {
            "name": event_name.value,
            "type": event_type.value,
            "date": event_date.value,
            "time": event_time.value,
            "location": event_location.value,
            "description": event_description.value,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        try:
            response = httpx.post("http://127.0.0.1:8000/create_event", json=event_data)
            if response.status_code == 200:
                print("Event created successfully!")
            else:
                print("Error creating event:", response.text)
        except Exception as ex:
            print("Exception while creating event:", ex)
        page.update()

    form_column = Column(
        controls=[
            Text("Create an Event", color="#F5E7C4", size=22, weight="bold"),
            event_name,
            event_type,
            event_date,
            event_time,
            event_location,
            event_description,
            ElevatedButton(
                "Submit",
                on_click=submit_form,
                bgcolor=HIGHLIGHT_COLOR,
                color=SECONDARY_COLOR
            ),
        ],
        spacing=15
    )

    right_container = Container(
        content=form_column,
        bgcolor=SECONDARY_COLOR,
        padding=20,
        border_radius=border_radius.all(10),
        alignment=ft.alignment.center
    )

    left_image = Image(
        src="images/eventlink.png",  # Ensure the image path is correct
        width=300,
        height=300,
        fit="contain"
    )
    left_container = Container(
        content=left_image,
        padding=20,
        alignment=ft.alignment.center
    )

    main_row = Row(
        controls=[left_container, right_container],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Use a Column layout to place the Back button at the top and the main content centered below
    final_layout = Column(
        controls=[
            Container(
                content=back_button,
                alignment=ft.alignment.top_left,
                padding=ft.padding.all(20)
            ),
            Container(
                content=main_row,
                expand=True,
                alignment=ft.alignment.center
            )
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.controls.clear()
    page.add(final_layout)
    page.update()

def load_create_event(page):
    main(page)
