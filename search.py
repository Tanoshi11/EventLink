import flet as ft
import httpx
import threading
import time

def load_event_details(page, event):
    """Load event details when an event container is clicked."""
    import event_details
    # Pass the search context (query, search_type, location) to the event details page
    search_context = {
        "query": page.data.get("query", "All"),
        "search_type": page.data.get("search_type", "global"),
        "location": page.data.get("location", None)
    }
    event_details.load_event_details(page, event, search_context)

def load_search(page, query, search_type="global", location=None):
    # Initialize page.data as a dictionary
    if page.data is None:
        page.data = {}

    # Store the search context in page.data
    page.data["query"] = query
    page.data["search_type"] = search_type
    page.data["location"] = location
    # Update the heading text based on the search type and location
    if search_type == "category":
        heading_text = f"Category: {query}"
    elif location:
        heading_text = f"Search Results: {query} ; Location: {location}"
    else:
        heading_text = f"Search Results: {query}"

    page.title = heading_text
    page.bgcolor = "#d6aa54"

    # Create a persistent search result heading
    results_title = ft.Text(
        heading_text,
        size=30,
        weight=ft.FontWeight.BOLD,
        color="#faf9f7"
    )

    # Divider for styling
    heading_divider = ft.Divider(color="white", thickness=1)

    # Keep the search results visible
    results_list = ft.ListView(expand=True, spacing=10)
    results_list.controls.append(ft.Text("Loading Results...", size=20, color="white"))

    # ------------------------------------------------------------------
    # 1) TASKBAR (HEADER) - same as in homepg.py, plus clickable logo
    # ------------------------------------------------------------------

    def go_homepage(e):
        """Navigate back to homepage."""
        import homepg  # inline import to avoid circular references
        homepg.load_homepage(page)

    def open_notifications(e):
        """Display real notifications."""
        global notif_popup
        if notif_popup:
            close_notifications(e)
        else:
            try:
                # Fetch notifications from the backend
                response = httpx.get("http://localhost:8000/notifications")
                if response.status_code == 200:
                    notifications = response.json().get("notifications", [])
                    show_notifications(e, notifications)
                else:
                    print("Error fetching notifications:", response.status_code)
            except Exception as ex:
                print("Error opening notifications:", ex)

    def close_notifications(e):
        """Close the notifications popup."""
        global notif_popup
        if notif_popup in page.overlay:
            page.overlay.remove(notif_popup)
        notif_popup = None
        page.update()

    def show_notifications(e, notifications):
        """Display notifications in a popup."""
        global notif_popup
        notif_controls = []
        for notif in notifications:
            notif_controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[ft.Text(notif.get("message", "No message"), size=18, color="white", weight=ft.FontWeight.BOLD)],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=15),
                    bgcolor="#4C7043",
                    border_radius=10,
                    margin=ft.margin.only(bottom=10),
                    on_click=lambda e, notif_id=notif.get("id"): handle_notification_click(notif_id),
                )
            )

        close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            on_click=close_notifications,
            icon_color="white",
            icon_size=30,
            tooltip=None,
            width=30,
            height=30,
            alignment=ft.alignment.top_right,
            style=ft.ButtonStyle(overlay_color=ft.colors.TRANSPARENT)
        )

        list_view = ft.ListView(
            controls=notif_controls,
            height=300,
            expand=True,
        )

        inner_popup = ft.Container(
            content=ft.Column(
                controls=[close_button, list_view],
                spacing=20,
            ),
            bgcolor="#6D9773",
            padding=10,
            border_radius=10,
            width=400,
            height=400,
            shadow=ft.BoxShadow(blur_radius=10, color="gray", offset=ft.Offset(2, 2)),
            on_click=lambda e: e.stop_propagation() if hasattr(e, "stop_propagation") else None,
        )

        notif_popup = ft.AnimatedSwitcher(
            duration=500,
            content=ft.Container(
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=100, bottom=300, right=15),
                content=inner_popup,
            ),
        )

        page.overlay.append(notif_popup)
        page.update()

    def handle_notification_click(notif_id):
        """Handle notification click."""
        print(f"Notification clicked: {notif_id}")
        # You can add logic to mark the notification as read or navigate to a specific page

    def show_profile_page(e):
        """Display the user's profile."""
        try:
            # Fetch the user's profile from the backend
            response = httpx.get("http://localhost:8000/profile")
            if response.status_code == 200:
                profile = response.json()
                import user_profile
                user_profile.load_profile(page, profile)
            else:
                print("Error fetching profile:", response.status_code)
        except Exception as ex:
            print("Error loading profile:", ex)

    def logout(e):
        """Log out the user."""
        try:
            # Send a logout request to the backend
            response = httpx.post("http://localhost:8000/logout")
            if response.status_code == 200:
                print("Logout successful")
                import login
                login.load_login(page)
            else:
                print("Error logging out:", response.status_code)
        except Exception as ex:
            print("Error logging out:", ex)

    def load_my_events(page: ft.Page):
        """Load the user's events."""
        try:
            # Fetch the user's events from the backend
            response = httpx.get("http://localhost:8000/my_events")
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

    def volunteer(e):
        """Redirect users to volunteer opportunities."""
        print("Redirecting to volunteer opportunities...")
        # You can replace this with a URL or page navigation
        page.launch_url("https://example.com/volunteer")

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

    # ------------------------------------------------------------------
    # 2) SIDEBAR (Categories)
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # 3) MAIN CONTENT: SEARCH RESULTS
    # ------------------------------------------------------------------

    def fetch_events():
        try:
            # 1) If user picks a category:
            if search_type == "category":
                url = f"http://localhost:8000/search_events_by_category?category={query}"

            # 2) If user wants to see *all* events (with or without a region):
            elif query == "All":
                if location:
                    url = f"http://localhost:8000/search_events?region={location}"
                else:
                    url = "http://localhost:8000/all_events"

            # 3) Otherwise, user typed something (like "Event"):
            else:
                # If there is a location, include it:
                if location:
                    url = f"http://localhost:8000/search_events?query={query}&region={location}"
                else:
                    url = f"http://localhost:8000/search_events?query={query}"

            print("Fetching events from:", url)
            resp = httpx.get(url)
            
            if resp.status_code == 200:
                events = resp.json().get("events", [])
                return events
            else:
                print("Error: Received status code", resp.status_code)
                return []
        except Exception as ex:
            print("Error fetching events:", ex)
            return []


    def load_events():
        """Background thread to load events from the server."""
        time.sleep(0.5)  # optional slight delay
        events = fetch_events()

        results_list.controls.clear()

        if events:
            for i, ev in enumerate(events):
                event_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(ev.get("name", "Unnamed Event"), size=22, color="white", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Date: {ev.get('date', '')}", color="white"),
                            ft.Text(f"Location: {ev.get('location', '')}", color="white"),
                            ft.Text(ev.get("description", ""), color="white"),
                        ],
                        spacing=5
                    ),
                    padding=10,
                    border_radius=10,
                    bgcolor="#105743",
                    ink=True,
                    on_click=lambda e, ev=ev: load_event_details(page, ev)  # Make the container clickable
                )
                results_list.controls.append(event_container)

                if i < len(events) - 1:
                    results_list.controls.append(ft.Divider(color="white"))
        else:
            results_list.controls.append(ft.Text("No events found.", size=20, color="white"))

        page.update()

    threading.Thread(target=load_events, daemon=True).start()

    # ------------------------------------------------------------------
    # 4) STACK LAYOUT
    # ------------------------------------------------------------------
    main_stack = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[results_title, heading_divider, results_list],
                    spacing=20,
                    expand=True
                ),
                margin=ft.margin.only(left=270, top=120, right=40),
                expand=True
            ),
            taskbar,
            side_taskbar,
        ],
        expand=True
    )

    page.controls.clear()
    page.add(main_stack)
    page.update()


# For quick testing: flet run search.py
if __name__ == "__main__":
    ft.app(target=lambda page: load_search(page, query="All", search_type="global", location="New York"))