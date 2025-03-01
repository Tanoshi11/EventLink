import flet as ft
import httpx
import threading
import time

# Global variable for the notifications popup
notif_popup = None

def get_regions():
    """Fetch regions from the server."""
    try:
        response = httpx.get("http://localhost:8000/regions")
        if response.status_code == 200:
            return response.json()["regions"]
    except Exception as ex:
        print("Error fetching regions:", ex)
    return []

def load_header(page: ft.Page):
    global notif_popup

    # ----------------- Header Functions -----------------
    def logout(e):
        def delayed_logout():
            time.sleep(0.6)
            if page.data is not None:
                page.data.clear()
            import login
            login.load_login(page)
        threading.Thread(target=delayed_logout).start()

    def show_profile_page(e):
        def delayed_profile():
            time.sleep(1)
            import user_profile
            user_profile.show_profile(page)
        threading.Thread(target=delayed_profile).start()

    def close_notifications(e):
        global notif_popup
        if notif_popup in page.overlay:
            page.overlay.remove(notif_popup)
        notif_popup = None
        page.update()

    def open_notifications(e):
        global notif_popup
        if notif_popup:
            close_notifications(e)
        else:
            show_notifications(e)

    def show_notifications(e):
        global notif_popup
        username = page.data.get("username")
        if not username:
            print("No username found!")
            return
        try:
            response = httpx.get(f"http://localhost:8000/notifications?username={username}")
            if response.status_code == 200:
                notifications_data = response.json()["notifications"]
            else:
                notifications_data = [{"message": "No notifications found."}]
        except Exception as ex:
            print("Error fetching notifications:", ex)
            notifications_data = [{"message": "Error fetching notifications."}]

        notif_controls = []
        for notif in notifications_data:
            notif_controls.append(
                ft.Container(
                    content=ft.Text(
                        notif.get("message", "No message"),
                        size=18,
                        color="white",
                        weight=ft.FontWeight.BOLD
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=15),
                    bgcolor="#4C7043",
                    border_radius=10,
                    margin=ft.margin.only(bottom=10)
                )
            )

        close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            on_click=close_notifications,
            icon_color="white",
            icon_size=30,
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
            shadow=ft.BoxShadow(blur_radius=10, color="gray", offset=ft.Offset(2, 2))
        )

        notif_popup = ft.AnimatedSwitcher(
            duration=500,
            content=ft.Container(
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=100, right=15),
                content=inner_popup,
            ),
        )

        page.overlay.append(notif_popup)
        page.update()

    def get_current_location(e):
        """Fetch user's current location using Geolocation API."""
        def on_success(position):
            lat = position.coords.latitude
            lon = position.coords.longitude
            page.data["location"] = f"{lat},{lon}"
            page.update()
            search_events(e)  # Trigger search with the new location

        def on_error(error):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Failed to get location. Please select a region manually."),
                open=True
            )
            page.update()

        page.window.navigator.geolocation.getCurrentPosition(on_success, on_error)

    # In header.py
    def search_events(e):
        """Trigger search when the user selects a region or presses Enter."""
        query = search_bar.value.strip() if search_bar.value else "All"
        location = region_dropdown.value

        # Debugging: Print the query and location
        print(f"Search triggered - Query: '{query}', Location: '{location}'")

        # Call load_search in search.py directly
        from search import load_search
        load_search(page, query, search_type="global", location=location)

    # ----------------- Build the Header UI -----------------
    regions = get_regions()
    region_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(region) for region in regions],
        hint_text="Select Location",
        expand=True,
        border_color="white",
        on_change=search_events  # Trigger search when region is selected
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
            # Clickable logo to go home
            ft.Container(
                content=ft.Image(src="images/eventlink.png", width=200, height=80, fit=ft.ImageFit.CONTAIN),
                margin=ft.margin.only(right=10),
                on_click=lambda e: __import__("homepg").load_homepage(page)
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
                        ft.IconButton(  # Add "Use My Location" button
                            icon=ft.icons.MY_LOCATION,
                            icon_color="white",
                            tooltip="Use my current location",
                            on_click=get_current_location,
                        )
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
            # Events Popup Menu: My Events, Create Event, Volunteer
            ft.Container(
                content=ft.PopupMenuButton(
                    tooltip="",
                    content=ft.Container(
                        content=ft.Text(
                            "Events",
                            style=ft.TextStyle(size=20, color="white", weight=ft.FontWeight.BOLD, letter_spacing=1.5)
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
                            on_click=lambda e: __import__("homepg").load_my_events(page)
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.EVENT_NOTE, color="white", size=15),
                                ft.Text("Create Event", style=ft.TextStyle(color="white", size=15))
                            ]),
                            on_click=lambda e: __import__("CreateEvents").load_create_event(page)
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
    return taskbar