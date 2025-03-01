import flet as ft
import httpx
import threading
import time
from search import load_search

def load_event_details(page: ft.Page, event: dict, search_context: dict):
    """
    Load detailed information about the event when the user clicks on an event container.
    """
    # Initialize page.data as a dictionary
    if page.data is None:
        page.data = {}

    # Store the search context in page.data
    page.data["search_context"] = search_context

    # Clear the existing content on the page
    page.controls.clear()

    # ----------------- Taskbar (Header) -----------------
    def go_homepage(e):
        """Navigate back to homepage."""
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
        """Load the user's events."""
        try:
            # Fetch the user's events from the backend
            username = page.data.get("username")  # Assuming the username is stored in page.data
            response = httpx.get(f"http://localhost:8000/my_events?username={username}")
            if response.status_code == 200:
                events = response.json().get("events", [])
                load_search(page, query="My Events", search_type="my_events")
            else:
                print("Error fetching user's events:", response.status_code)
        except Exception as ex:
            print("Error loading my events:", ex)

    def load_create_event(page: ft.Page):
        """Load the create event page."""
        import CreateEvents
        CreateEvents.load_create_event(page)

    def get_regions():
        """Fetch regions from the server."""
        try:
            response = httpx.get("http://localhost:8000/regions")
            if response.status_code == 200:
                return response.json()["regions"]
        except Exception as ex:
            print("Error fetching regions:", ex)
        return []

    regions = get_regions()

    def search_events(e):
        """Trigger search when the user selects a region or presses Enter."""
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
        on_submit=search_events  # Trigger search when pressing Enter
    )

    header = ft.Row(
        controls=[
            ft.Container(width=15),
            # Clickable EventLink logo -> goes home
            ft.Container(
                content=ft.Image(src="images/eventlink.png", width=200, height=80, fit=ft.ImageFit.CONTAIN),
                margin=ft.margin.only(right=10),
                on_click=go_homepage
            ),
            # Search & Location container
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
            # Events Popup Menu
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
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.CALENDAR_TODAY, color="white", size=15),
                                ft.Text("My Events", style=ft.TextStyle(color="white", size=15))
                            ]),
                            on_click=lambda e: load_my_events(page)
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.EVENT_NOTE, color="white", size=15),
                                ft.Text("Create Event", style=ft.TextStyle(color="white", size=15))
                            ]),
                            on_click=lambda e: load_create_event(page)
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.SENTIMENT_SATISFIED, color="white", size=15),
                                    ft.Text("Volunteer", style=ft.TextStyle(color="white", size=15))
                                ],
                                spacing=5
                            ),
                            on_click=lambda e: print("Volunteer clicked")
                        )
                    ]
                ),
                margin=ft.margin.only(left=3, right=3)
            ),
            ft.VerticalDivider(width=1, color="white", leading_indent=30, trailing_indent=30),
            # Notifications Icon
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
            # Profile Popup
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
                                controls=[
                                    ft.Icon(name=ft.Icons.PERSON_ROUNDED, color="white", size=15),
                                    ft.Text("Profile", style=ft.TextStyle(color="white", size=15))
                                ],
                                spacing=5
                            ),
                            on_click=show_profile_page
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.EXIT_TO_APP, color="white", size=15),
                                    ft.Text("Logout", style=ft.TextStyle(color="white", size=15))
                                ],
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

    taskbar = ft.Container(
        content=header,
        height=100,
        bgcolor="#0C3B2E",
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=10)
    )

    # ----------------- Sidebar (Categories) -----------------
    def handle_category_click(e, category_label: str):
        """Handle category search."""
        load_search(page, query=category_label, search_type="category")

    def category_row(icon_name: str, label: str):
        """Create a clickable category row."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=20),
                    ft.Text(label, color="white", size=16),
                ],
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
            ft.Text("Categories", color="white", size=20, weight=ft.FontWeight.BOLD),
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
    # Event title at the top left
    event_title = ft.Text(
        event.get("name", "Unnamed Event"),
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.LEFT
    )

    # Divider below the title
    title_divider = ft.Divider(color="white", thickness=1)

    # Image and details row (aligned to the left)
    event_image = ft.Image(
        src=event.get("image_url", "default_event_image.jpg"),  # Use image_url
        width=300,
        height=200,
        fit=ft.ImageFit.COVER,
        border_radius=20
    )

    event_details = ft.Column(
        controls=[
            ft.Text(f"Date: {event.get('date', 'N/A')}", size=20, color="white"),
            ft.Text(f"Time: {event.get('time', 'N/A')}", size=20, color="white"),
            ft.Text(f"Location: {event.get('location', 'N/A')}", size=20, color="white")
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )

    image_details_row = ft.Row(
        controls=[event_image, event_details],
        spacing=20,
        alignment=ft.MainAxisAlignment.START
    )

    # Event description with a label
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

    # Join Event button
    join_event_button = ft.ElevatedButton(
        text="Join Event",
        on_click=lambda e: print("Join Event clicked"),  # Placeholder for join event logic
        bgcolor="#105743",
        color="white"
    )

    # Back to Search button
    back_to_search_button = ft.ElevatedButton(
        text="Back to Search",
        on_click=lambda e: go_back_to_search(page),  # Placeholder for back to search logic
        bgcolor="#105743",
        color="white"
    )

    # Back to Home button
    back_to_home_button = ft.ElevatedButton(
        text="Back to Home",
        on_click=lambda e: go_back_to_homepage(page),  # Placeholder for back to home logic
        bgcolor="#105743",
        color="white"
    )

    # Combine all elements into a column
    event_details_column = ft.Column(
        controls=[
            event_title,    # Event title at the top left
            title_divider,  # Divider below the title
            image_details_row,  # Image and details aligned to the left
            event_description,  # Description with a label
            join_event_button,  # Join Event button
            ft.Row(  # Back to Search and Back to Home buttons at the bottom right
                controls=[back_to_search_button, back_to_home_button],
                alignment=ft.MainAxisAlignment.END
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START
    )

    # Main content container
    main_content = ft.Container(
        content=event_details_column,
        margin=ft.margin.only(left=270, top=120, right=40),
        expand=True
    )

    # ----------------- Stack Layout -----------------
    main_stack = ft.Stack(
        controls=[
            main_content,  # Event details in the middle
            taskbar,       # Taskbar at the top
            side_taskbar,  # Sidebar on the left
        ],
        expand=True
    )

    # Add the stack to the page
    page.add(main_stack)
    page.update()

def go_back_to_search(page: ft.Page):
    """Navigate back to the search results using the stored search context."""
    search_context = page.data.get("search_context", {})
    query = search_context.get("query", "All")
    search_type = search_context.get("search_type", "global")
    location = search_context.get("location", None)

    import search
    search.load_search(page, query=query, search_type=search_type, location=location)

def go_back_to_homepage(page: ft.Page):
    """Navigate back to the homepage."""
    import homepg
    homepg.load_homepage(page)