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

PRIMARY_COLOR = "#6d9773"
SECONDARY_COLOR = "#0c3b2e"
ACCENT_COLOR = "#b46617"
HIGHLIGHT_COLOR = "#ffba00"

notif_popup = None
events_text = ft.Text("", color="white")

def get_header_controller():
    from header import load_header  # Delayed import
    return load_header


def get_load_search():
    from controller.search_controller import load_search
    return load_search


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


def go_back(e, page):
    import controller.homepg_controller as homepg
    page.controls.clear()
    homepg.main(page)
    page.update()


def main(page: ft.Page):
    page.title = "Create Event"
    page.bgcolor = "#5F7755"
    page.padding =0

  #Header area
    HeaderController = get_header_controller()
    header = HeaderController()
    taskbar = header.header_view  # Extract the UI component
    page.add(taskbar)  # Now add only the UI


    # Back button
    back_button = ElevatedButton(
        text="Back",
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(e, page),
        bgcolor=HIGHLIGHT_COLOR,
        color=SECONDARY_COLOR
    )

    # Date picker
    event_date = ft.TextField(
        label="Selected Date",
        hint_text="Pick or Type a date YY-MM-DD",
        width=400,
        suffix=ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime.now(),
                    last_date=datetime.datetime(year=3000, month=12, day=31),
                    on_change=handle_change,
                    on_dismiss=handle_dismissal,
                )
            )
        )
    )

    def handle_change(e):
        selected_date = e.control.value
        event_date.value = selected_date.strftime('%Y-%m-%d')
        page.update()

    def handle_dismissal(e):
        page.update()

    # Time picker
    def handle_start_time_change(e):
        selected_time = e.control.value 
        if selected_time:
            time_start_field.value = selected_time.strftime("%H:%M")
            page.update()

    def handle_end_time_change(e):
        selected_time = e.control.value
        if selected_time:
            time_end_field.value = selected_time.strftime("%H:%M")
            page.update()

    time_start_field = ft.TextField(
        label="Start Time",
        hint_text="Pick or Type Time HH-MM",
        width=195,
        suffix=ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=lambda e: page.open(
                ft.TimePicker(
                    on_change=handle_start_time_change
                )
            )
        )
    )

    time_end_field = ft.TextField(
        label="End Time",
        hint_text="Pick or type time",
        width=195,
        suffix=ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=lambda e: page.open(
                ft.TimePicker(
                    on_change=handle_end_time_change
                )
            )
        )
    )

    time_row = ft.Row(
        controls=[time_start_field, time_end_field],
        spacing=10
    )

    # Form fields
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
    event_ticket_price = TextField(label ="Ticket Price ", width=400)
    event_description = TextField(label="Description", multiline=True, width=400, height=100)

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
        
        #-----attendees error handle
        if not event_attendees.value:
            event_attendees.error_text = "Guest Limit is required."
            error_found = True
        else:
            try:
                guest_limit = int(event_attendees.value)
                event_attendees.error_text = None
            except ValueError:
                event_attendees.error_text = "Guest Limit must be a number."
                error_found = True
        
        #--- ticket price error handle
       
        if not event_ticket_price.value:
            event_ticket_price.error_text = "Ticket Price is required."
            error_found = True
        else:
            try:
                ticket_price = int(event_ticket_price.value)
                event_ticket_price.error_text = None
            except ValueError:
                event_ticket_price.error_text = "Ticket must be a number."
                error_found = True


        #------time start error
        time_start_error = validate_time(time_start_field.value)
        if time_start_error:
            time_start_field.error_text = time_start_error
            error_found = True
        else:
            time_start_field.error_text = None

        #----time end error
        time_end_error = validate_time(time_end_field.value)
        if time_end_error:
            time_end_field.error_text = time_end_error
            error_found = True
        else:
            time_end_field.error_text = None

        page.update()
        if error_found:
            return



        username = page.data.get("username")
       
        # Create event data payload
        event_data = {
            "host": username, 
            "name": event_name.value,
            "type": event_type.value,
            "date": event_date.value,
            "time": f"{time_start_field.value} - {time_end_field.value}",
            "guest_limit": guest_limit,
            "ticket_price": ticket_price,
            "location": event_location.value,
            "description": event_description.value,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        try:
            response = httpx.post("http://127.0.0.1:8000/create_event", json=event_data)
            if response.status_code == 200:
                event_name.value = ""
                event_date.value = ""
                time_start_field.value = ""
                time_end_field.value = ""
                event_attendees.value = ""
                event_ticket_price.value = ""
                event_description.value = ""
                event_type.value = ""
                event_location.value = ""

                page.snack_bar = ft.SnackBar(Text("Event created successfully!"))
                page.snack_bar.open = True
               
            else:
                page.snack_bar = ft.SnackBar(Text("Error creating event: " + response.text))
                page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(Text("Exception while creating event: " + str(ex)))
            page.snack_bar.open = True
            print("Exception while creating event:", ex)
        page.update()

    form_column = Column(
        controls=[
            Text("Create an Event", color="#F5E7C4", size=22, weight="bold"),
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
        alignment=ft.alignment.center,
        height=page.height * 1.09
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

    # --- Final Layout with a Stack ---
    final_layout = Column(
        controls=[
            taskbar,
            Container(
                content=back_button,
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=20, top=20), 
                expand=False
            ),
            Container(
                content=main_row,
                alignment=ft.alignment.center,
                expand=True
            ),
           
        ],
        
        expand=True
    )

    page.controls.clear()
    page.add(final_layout)
    page.update()


# Only one definition for load_create_event is needed.
def load_create_event(page):
    main(page)


def load_homepage(page):
    page.controls.clear()
    main(page)


def load_login(page):
    page.floating_action_button = None
    # Add login logic here if needed.
    pass


def load_my_events(page):
    import my_events
    page.controls.clear()
    my_events.load_my_events(page)  # Calls the function without restarting the app
    page.update()


def load_profile(page):
    page.floating_action_button = None
    # Add profile loading logic here if needed.
    pass


if __name__ == "__main__":
    ft.app(target=main)