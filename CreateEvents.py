import flet as ft
from flet import Page, Row, Column, Container, Text, TextField, ElevatedButton, Image, Dropdown, alignment, border_radius, colors
import datetime

# Define theme colors
PRIMARY_COLOR = "#6d9773"      
SECONDARY_COLOR = "#0c3b2e"    
ACCENT_COLOR = "#b46617"        
HIGHLIGHT_COLOR = "#ffba00"     

def validate_date(date_str):
    if not date_str:
        return "Date is required."
    try:
        # Expecting date format: YYYY-MM-DD
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

def validate_time(time_str):
    if not time_str:
        return "Time is required."
    try:
        # Expecting time format: HH:MM (24-hour)
        datetime.datetime.strptime(time_str, "%H:%M")
        return None
    except ValueError:
        return "Invalid time format. Use HH:MM (24-hour)."

def main(page: ft.Page):
    page.title = "EventLink"
    page.bgcolor = PRIMARY_COLOR  # Fill background with primary color so no white border is seen
    page.window_width = 1200
    page.window_height = 700

    
    def go_back(e):
        print("Back button clicked!")
        # Add your navigation logic here

   
    back_button = ElevatedButton(
        "Back",
        icon=ft.icons.ARROW_BACK,
        on_click=go_back,
        bgcolor=HIGHLIGHT_COLOR,
        color=SECONDARY_COLOR
    )
    back_button_row = Row(
        controls=[back_button],
        alignment=ft.MainAxisAlignment.START
    )

    
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
        ],
    )
    event_date = TextField(label="Date (YYYY-MM-DD)", width=400)
    event_time = TextField(label="Time (HH:MM)", width=400)
    event_location = TextField(label="Location", width=400)
    event_description = TextField(label="Description", multiline=True, width=400, height=80)

    def submit_form(e):
        error_found = False

        if not event_name.value:
            event_name.error_text = "Event Name is required."
            error_found = True
        else:
            event_name.error_text = None

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

        if not event_type.value:
            event_type.error_text = "Event Type is required."
            error_found = True
        else:
            event_type.error_text = None

        page.update()

        if error_found:
            return

        print("Form submitted!")
        page.update()


    form_column = Column(
        controls=[
            Text("Create an Event", color=ACCENT_COLOR, size=18, weight="bold"),
            event_name,
            event_type,
            event_date,
            event_time,
            event_location,
            event_description,
            ElevatedButton("Submit", on_click=submit_form, bgcolor=HIGHLIGHT_COLOR, color=SECONDARY_COLOR),
        ],
        spacing=10,
    )

  
    right_container = Container(
        content=form_column,
        bgcolor=SECONDARY_COLOR,
        padding=20,
        border_radius=border_radius.all(10)
    )

   
    left_image = Image(
        src="eventlink.png",  
        width=500,
        height=500,
        fit="contain"
    )
    left_container = Container(
        content=left_image,
        expand=True,
        padding=20
    )

   
    layout = Row(
        controls=[
            left_container,
            right_container
        ],
        expand=True
    )

   
    final_layout = Column(
        controls=[
            back_button_row,
            layout
        ],
        expand=True
    )

    page.add(final_layout)

ft.app(target=main)