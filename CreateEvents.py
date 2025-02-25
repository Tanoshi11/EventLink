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
import httpx  # Import httpx

# Define theme colors
PRIMARY_COLOR = "#6d9773"       # Accent green
SECONDARY_COLOR = "#0c3b2e"     # Dark green (used for headers/forms)
ACCENT_COLOR = "#b46617"        # Warm accent (for text or titles)
HIGHLIGHT_COLOR = "#ffba00"     # Highlight yellow

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

    # --- Back Button (top-left) ---
    back_button = ElevatedButton(
        text="Back",
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(e, page),
        bgcolor=HIGHLIGHT_COLOR,
        color=SECONDARY_COLOR
    )

    # --- Event Form Fields ---
    event_name = TextField(label="Event Name", width=400)
    event_type = Dropdown(
        label="Event Type",
        width=400,
        options=[
            ft.dropdown.Option("Music"),
            ft.dropdown.Option("Art and Cultural Events"),
            ft.dropdown.Option("Sports"),
            ft.dropdown.Option("Workshops"),
            ft.dropdown.Option("Seminars"),
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

        print("Form submitted!")
        print("Event Name:", event_name.value)
        print("Event Type:", event_type.value)
        print("Date:", event_date.value)
        print("Time:", event_time.value)
        print("Location:", event_location.value)
        print("Description:", event_description.value)

    # Column for the form
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

    # Right container (dark green)
    right_container = Container(
        content=form_column,
        bgcolor=SECONDARY_COLOR,
        padding=20,
        border_radius=border_radius.all(10),
        alignment=ft.alignment.center,
        height=page.height * 0.9
    )

    # Left container (image)
    left_image = Image(
        src="images/eventlink.png",  # Make sure this path is correct
        width=500,
        height=500,
        fit="contain"
    )
    left_container = Container(
        content=left_image,
        padding=20,
        alignment=ft.alignment.center
    )

    # Row with image (left) and form (right)
    main_row = Row(
        controls=[left_container, right_container],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # We'll just center the row itself in the stack
    main_content = main_row

    # --- Final Layout with a Stack ---
    # 1) Pin back_button in top-left
    # 2) Center main_content in the remaining space
    final_layout = Column(
        controls=[
            # Centered main content
            Container(
                

                content = back_button,
                alignment = ft.alignment.top_left,
                padding=ft.padding.only(left=20, top=20), 
                expand= False
            ),
            # Top-left back button
            Container(
                content=main_content,
                alignment=ft.alignment.center,
                expand=True

            ),
        ],
        expand=True
    )

    page.controls.clear()
    page.add(final_layout)
    page.update()

def load_create_event(page):
    main(page)

if __name__ == "__main__":
    ft.app(target=main)
