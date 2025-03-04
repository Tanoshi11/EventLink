import flet as ft
import httpx
import threading
import time
from search import load_search
from header import load_header
import join_event_form  # Import the join_event_form module
from datetime import datetime

def load_event_details(page: ft.Page, event: dict, search_context: dict):
    """
    Load detailed information about the event when the user clicks on an event container.
    """
    if page.data is None:
        page.data = {}

    page.data["search_context"] = search_context
    page.controls.clear()

    # ----------------- Taskbar (Header) -----------------
    def go_homepage(e):
        import homepg
        homepg.load_homepage(page)

    def open_notifications(e):
        print("Notifications clicked (placeholder).")

    def close_notifications(e):
        print("Close notifications (placeholder).")

    def show_profile_page(e):
        print("Show profile page (placeholder).")

    def logout(e):
        print("Logout user (placeholder).")

    def load_my_events(page: ft.Page):
        try:
            username = page.data.get("username")
            response = httpx.get(f"http://localhost:8000/my_events?username={username}")
            if response.status_code == 200:
                events = response.json().get("events", [])
                load_search(page, query="My Events", search_type="my_events")
            else:
                print("Error fetching user's events:", response.status_code)
        except Exception as ex:
            print("Error loading my events:", ex)

    def load_create_event(page: ft.Page):
        import CreateEvents
        CreateEvents.load_create_event(page)

    def get_regions():
        try:
            response = httpx.get("http://localhost:8000/regions")
            if response.status_code == 200:
                return response.json()["regions"]
        except Exception as ex:
            print("Error fetching regions:", ex)
        return []

    regions = get_regions()

    def search_events(e):
        query = search_bar.value.strip() if search_bar.value else "All"
        location = region_dropdown.value
        load_search(page, query, search_type="global", location=location)

    region_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(region) for region in regions],
        hint_text="Select Location",
        expand=True,
        on_change=search_events,
        border_color="white"
    )

    search_bar = ft.TextField(
        hint_text="Search events",
        border=None,
        expand=True,
        text_style=ft.TextStyle(size=18, color="white"),
        border_radius=20,
        border_color="white",
        on_submit=search_events
    )

    header = ft.Row(
        controls=[
            ft.Container(width=15),
            ft.Container(
                content=ft.Image(src="images/eventlink.png", width=200, height=80, fit=ft.ImageFit.CONTAIN),
                margin=ft.margin.only(right=10),
                on_click=go_homepage
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SEARCH, color="white", size=30),
                        search_bar,
                        ft.VerticalDivider(width=1, color="white"),
                        ft.Icon(name=ft.Icons.LOCATION_ON, color="white", size=30),
                        region_dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                border_radius=15,
                border=ft.border.all(1, "white"),
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                expand=True,
                bgcolor="#105743",
                margin=ft.margin.only(top=16, bottom=16, right=30)
            ),
            ft.VerticalDivider(width=1, color="white", leading_indent=30, trailing_indent=30),
            ft.Container(
                content=ft.PopupMenuButton(
                    tooltip="",
                    content=ft.Container(
                        content=ft.Text(
                            "Events",
                            style=ft.TextStyle(
                                size=20,
                                color="white",
                                weight=ft.FontWeight.BOLD,
                                letter_spacing=1.5
                            )
                        ),
                        alignment=ft.alignment.center
                    ),
                    height=55,
                    width=175,
                    bgcolor="#B46617",
                    menu_position=ft.PopupMenuPosition.UNDER,
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row([ft.Icon(name=ft.Icons.CALENDAR_TODAY, color="white", size=15),
                                            ft.Text("My Events", style=ft.TextStyle(color="white", size=15))]),
                            on_click=lambda e: load_my_events(page)
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([ft.Icon(name=ft.Icons.EVENT_NOTE, color="white", size=15),
                                            ft.Text("Create Event", style=ft.TextStyle(color="white", size=15))]),
                            on_click=lambda e: load_create_event(page)
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[ft.Icon(name=ft.Icons.SENTIMENT_SATISFIED, color="white", size=15),
                                          ft.Text("Volunteer", style=ft.TextStyle(color="white", size=15))],
                                spacing=5
                            ),
                            on_click=lambda e: print("Volunteer clicked")
                        )
                    ]
                ),
                margin=ft.margin.only(left=3, right=3)
            ),
            ft.VerticalDivider(width=1, color="white", leading_indent=30, trailing_indent=30),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.NOTIFICATIONS,
                    on_click=open_notifications,
                    icon_color="#FFBA00",
                    icon_size=40,
                    tooltip="Notifications",
                    width=60
                ),
                margin=ft.margin.only(left=40, right=10),
                border=ft.border.all(2, "#105743"),
                border_radius=30
            ),
            ft.Container(
                content=ft.PopupMenuButton(
                    tooltip="Profile",
                    content=ft.Container(
                        content=ft.Icon(name=ft.Icons.PERSON_ROUNDED, color="#FFBA00", size=40),
                        alignment=ft.alignment.center
                    ),
                    height=55,
                    width=60,
                    bgcolor="#B46617",
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[ft.Icon(name=ft.Icons.PERSON_ROUNDED, color="white", size=15),
                                          ft.Text("Profile", style=ft.TextStyle(color="white", size=15))],
                                spacing=5
                            ),
                            on_click=show_profile_page
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[ft.Icon(name=ft.Icons.EXIT_TO_APP, color="white", size=15),
                                          ft.Text("Logout", style=ft.TextStyle(color="white", size=15))],
                                spacing=5
                            ),
                            on_click=logout
                        )
                    ]
                ),
                margin=ft.margin.only(left=50, right=20),
                border=ft.border.all(2, "#105743"),
                border_radius=30
            )
        ]
    )

    taskbar = load_header(page)

    # ----------------- Sidebar (Categories) -----------------
    def handle_category_click(e, category_label: str):
        load_search(page, query=category_label, search_type="category")

    def category_row(icon_name: str, label: str):
        return ft.Container(
            content=ft.Row(
                controls=[ft.Icon(name=icon_name, color="white", size=20),
                          ft.Text(label, color="white", size=16)],
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.all(5),
            on_click=lambda e: handle_category_click(e, label),
            ink=True,
            border_radius=ft.border_radius.all(5),
        )

    category_buttons = ft.Column(
        controls=[
            ft.Text("Filters", color="white", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Category", color="white", size=16, weight=ft.FontWeight.W_600),
            category_row(ft.Icons.BUSINESS_CENTER, "Business"),
            category_row(ft.Icons.RESTAURANT, "Food & Drink"),
            category_row(ft.Icons.CHILD_CARE, "Family & Education"),
            category_row(ft.Icons.HEALTH_AND_SAFETY, "Health"),
            category_row(ft.Icons.DIRECTIONS_BOAT, "Travel"),
            category_row(ft.Icons.MUSIC_NOTE, "Music"),
            category_row(ft.Icons.THEATER_COMEDY, "Performing Arts"),
            category_row(ft.Icons.STYLE, "Fashion"),
            category_row(ft.Icons.MOVIE, "Film & Media"),
            category_row(ft.Icons.COLOR_LENS, "Hobbies"),
            category_row(ft.Icons.HOME, "Home & Lifestyle"),
            category_row(ft.Icons.GROUP, "Community"),
            category_row(ft.Icons.VOLUNTEER_ACTIVISM, "Charity & Causes"),
            category_row(ft.Icons.ACCOUNT_BALANCE, "Government"),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START
    )

    side_taskbar = ft.Container(
        content=category_buttons,
        width=245,
        bgcolor="#1d572c",
        alignment=ft.alignment.top_left,
        padding=20,
        margin=ft.margin.only(top=100)
    )

    # ----------------- Event Details Content -----------------
    event_title = ft.Text(
        event.get("name", "Unnamed Event"),
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.LEFT
    )

    title_divider = ft.Divider(color="white", thickness=1)

    event_image = ft.Image(
        src=event.get("image_url", "default_event_image.jpg"),
        width=300,
        height=200,
        fit=ft.ImageFit.COVER,
        border_radius=20
    )

    def get_event_status(event_date, event_time):
        """Determine the status of the event based on the current date and time."""
        event_datetime_str = f"{event_date} {event_time}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if current_datetime > event_datetime:
            return "Closed"
        elif current_datetime.date() == event_datetime.date():
            return "Ongoing"
        else:
            return "Upcoming"

    event_status = get_event_status(event.get("date", ""), event.get("time", ""))
    status_color = {
        "Upcoming": "#4CAF50",
        "Ongoing": "#FFEB3B",
        "Closed": "#FF5252"
    }.get(event_status, "white")

    event_details = ft.Column(
        controls=[
            ft.Text(f"Host: {event.get('username', 'Unknown')}", size=20, color="white"),  # Add the username of the event creator
            ft.Text(f"Date: {event.get('date', 'N/A')}", size=20, color="white"),
            ft.Text(f"Time: {event.get('time', 'N/A')}", size=20, color="white"),
            ft.Text(f"Location: {event.get('location', 'N/A')}", size=20, color="white"),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )

    image_details_row = ft.Row(
        controls=[event_image, event_details],
        spacing=20,
        alignment=ft.MainAxisAlignment.START
    )

    event_description = ft.Column(
        controls=[
            ft.Text("Description:", size=20, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text(
                event.get("description", "No description available."),
                size=18,
                color="white",
                text_align=ft.TextAlign.LEFT
            )
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.START
    )

    def join_event(e):
        """Open the join event form."""
        join_event_form.load_join_event_form(
            page,
            title=event.get("name", "Unnamed Event"),
            date=event.get("date", "N/A"),
            time=event.get("time", "N/A"),
            event_id=event.get("id", "N/A"),
            back_callback=lambda e: close_popup(),  # Close the popup without refreshing the page
            join_callback=update_join_button  # Pass the callback to update the button text
        )

    def close_popup():
        if page.overlay:
            page.overlay.pop()
        page.update()

    def update_join_button():
        join_event_button.text = "Joined Event"
        join_event_button.disabled = True
        page.data["joined_event"] = True  # Mark the event as joined in page data
        page.update()

    # Determine if the user has already joined the event
    username = page.data.get("username")
    if username in event.get("participants", []) or page.data.get("joined_event"):
        join_event_button = ft.Text("Joined Event", size=15, color="white", weight="bold")
    else:
        join_event_button = ft.ElevatedButton(
            text="Join Event",
            on_click=join_event,
            bgcolor="#C77000",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )

    back_to_search_button = ft.ElevatedButton(
        text="Back to Search",
        on_click=lambda e: go_back_to_search(page),
        bgcolor="#C77000",
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    back_to_home_button = ft.ElevatedButton(
        text="Back to Home",
        on_click=lambda e: go_back_to_homepage(page),
        bgcolor="#C77000",
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    container_color = "#21582F"  # Taskbar green color
    button_color = "#C77000"

    buttons_row = ft.Row(
        controls=[
            back_to_search_button,
            back_to_home_button
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.END
    )

    if event_status != "Closed":
        buttons_row.controls.insert(0, join_event_button)

    event_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(event.get("name", "Unnamed Event"), size=24, weight="bold", color="white"),
                ft.Text(f"Status: {event_status}", color=status_color,size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(color="white"),
                image_details_row,
                ft.Divider(color="white"),
                event_description,
                ft.Container(
                    content=buttons_row,
                    margin=ft.margin.only(top=20)
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO  # Make the column scrollable if content overflows
        ),
        bgcolor=container_color,
        padding=20,
        border_radius=10,
        expand=True,
        height=page.height * 0.8  # Limit the height to 80% of the page height
    )

    main_content = ft.Container(
        content=event_container,
        margin=ft.margin.only(left=270, top=120, right=40),
        expand=True
    )

    main_stack = ft.Stack(
        controls=[
            main_content,
            taskbar,
            side_taskbar,
        ],
        expand=True
    )

    page.add(main_stack)
    page.update()

def go_back_to_search(page: ft.Page):
    search_context = page.data.get("search_context", {})
    query = search_context.get("query", "All")
    search_type = search_context.get("search_type", "global")
    location = search_context.get("location", None)
    import search
    search.load_search(page, query=query, search_type=search_type, location=location)

def go_back_to_homepage(page: ft.Page):
    import homepg
    homepg.load_homepage(page)
