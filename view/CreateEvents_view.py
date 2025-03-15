
import flet as ft
from flet import Row, Column, Container, Text, TextField, ElevatedButton, Image, Dropdown, border_radius
import datetime

def create_event_view(page, controller):
    # Header and Back Button (controller's go_back is attached)
    back_button = ElevatedButton(
        text="Back",
        icon=ft.icons.ARROW_BACK,
        on_click=controller.go_back,
        bgcolor=controller.HIGHLIGHT_COLOR,
        color=controller.SECONDARY_COLOR
    )

    # Date Picker TextField with its suffix IconButton
    controller.event_date = TextField(
        label="Selected Date",
        hint_text="Pick or Type a date (YYYY-MM-DD)",
        width=400,
        suffix=ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime.now(),
                    last_date=datetime.datetime(year=3000, month=12, day=31),
                    on_change=controller.handle_date_change,
                    on_dismiss=controller.handle_date_dismissal,
                )
            )
        )
    )

    # Time Picker TextFields
    controller.time_start_field = TextField(
        label="Start Time",
        hint_text="Pick or Type Time (HH:MM)",
        width=195,
        suffix=ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=lambda e: page.open(
                ft.TimePicker(
                    on_change=controller.handle_start_time_change
                )
            )
        )
    )

    controller.time_end_field = TextField(
        label="End Time",
        hint_text="Pick or Type Time (HH:MM)",
        width=195,
        suffix=ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=lambda e: page.open(
                ft.TimePicker(
                    on_change=controller.handle_end_time_change
                )
            )
        )
    )

    time_row = Row(
        controls=[controller.time_start_field, controller.time_end_field],
        spacing=10
    )

    # Other form fields
    controller.event_name = TextField(label="Event Name", width=400)
    controller.event_type = Dropdown(
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

    # Use the model function to fetch regions
    regions = controller.model_fetch_regions()
    controller.event_location = Dropdown(
        label="Location",
        width=400,
        options=[ft.dropdown.Option(region) for region in regions]
    )
    controller.event_attendees = TextField(label="Guest Limit", width=400)
    controller.event_ticket_price = TextField(label="Ticket Price", width=400)
    controller.event_description = TextField(label="Description", multiline=True, width=400, height=100)

    # Submit Button (calls controller.submit_form)
    submit_button = ElevatedButton(
        "Submit",
        on_click=controller.submit_form,
        bgcolor=controller.HIGHLIGHT_COLOR,
        color=controller.SECONDARY_COLOR
    )

    # Form layout column
    form_column = Column(
        controls=[
            Text("Create an Event", color="#F5E7C4", size=22, weight="bold"),
            controller.event_name,
            controller.event_type,
            controller.event_date,
            time_row,
            controller.event_attendees,
            controller.event_ticket_price,
            controller.event_location,
            controller.event_description,
            submit_button,
        ],
        spacing=15
    )


    right_container = Container(
        content=form_column,
        bgcolor=controller.SECONDARY_COLOR,
        padding=20,
        border_radius=border_radius.all(10),
        alignment=ft.alignment.center,
        height=page.height * 1.09
    )

    main_row = Row(
        controls=[ right_container],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Final layout including header and back button
    layout = Column(
        controls=[
            controller.header,  # assume controller.header is set up (e.g., via a header controller)
            Container(
                content=back_button,
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=20, top=20)
            ),
            Container(
                content=main_row,
                alignment=ft.alignment.center,
                expand=True
            ),
        ],
        expand=True
    )
    return layout
