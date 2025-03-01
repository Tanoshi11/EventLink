import flet as ft
import time
import threading
import httpx
from search import load_search

# Global variable to store the notification popup overlay
notif_popup = None
events_text = ft.Text("", color="white")

def main(page: ft.Page):
    if page.data is None:
        page.data = {}
    page.title = "Home"
    page.bgcolor = "#d6aa54"
    page.padding = 0  # Ensure no extra padding at the edges

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

    def open_notifications(e):
        global notif_popup
        if notif_popup:
            close_notifications(e)
        else:
            show_notifications(e)

    def show_notifications(e):
        global notif_popup

        # Ensure page.data is a dict
        if page.data is None:
            page.data = {}

        # Get the username
        username = page.data.get("username", None)
        if not username:
            print("No username found in page data! User might not be logged in.")
            return

        # Fetch notifications from server
        try:
            response = httpx.get(f"http://localhost:8000/notifications?username={username}")
            if response.status_code == 200:
                notifications_data = response.json()["notifications"]
            else:
                notifications_data = [{"message": "No notifications found."}]
        except Exception as ex:
            print("Error fetching notifications:", ex)
            notifications_data = [{"message": "Error fetching notifications."}]

        # Build notification items
        notif_controls = []
        for notif in notifications_data:
            notif_controls.append(
                ft.Container(
                    content=ft.Text(
                        notif["message"],
                        size=18,
                        color="white",
                        weight=ft.FontWeight.BOLD,
                        no_wrap=False  # Allow text to wrap to multiple lines
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=15),
                    bgcolor="#4C7043",
                    border_radius=10,
                    margin=ft.margin.only(bottom=10),
                    on_click=lambda e, msg=notif["message"]: print(f"Notification clicked: {msg}"),
                )
            )

        # Close button
        close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            on_click=close_notifications,
            icon_color="white",
            icon_size=30,
            style=ft.ButtonStyle(overlay_color=ft.colors.TRANSPARENT),
            tooltip=None,
            alignment=ft.alignment.top_right
        )

        # Scrollable ListView for notifications
        list_view = ft.ListView(
            controls=notif_controls,
            expand=True,      # Fill remaining space
            auto_scroll=False # Keep a scroll bar if items exceed the container's height
        )

        # Create a column with the close button on top and the scrollable list beneath
        content_column = ft.Column(
            controls=[
                close_button,
                list_view
            ],
            spacing=10,
            expand=True
        )

        # The main popup container
        inner_popup = ft.Container(
            content=content_column,
            width=400,          # Keep it narrow enough for easy reading
            height=300,         # Short container height
            bgcolor="#6D9773",
            padding=10,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color="gray", offset=ft.Offset(2, 2)),
            on_click=lambda e: e.stop_propagation() if hasattr(e, "stop_propagation") else None,
        )

        # Wrap in an AnimatedSwitcher for a nice show/hide transition
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



    def close_notifications(e):
        global notif_popup
        if notif_popup in page.overlay:
            page.overlay.remove(notif_popup)
        notif_popup = None
        page.update()

    def handle_click_outside(e):
        if notif_popup and notif_popup in page.overlay:
            close_notifications(e)
    
    def store_previous_page_context(page: ft.Page, previous_page: str):
        """Store the previous page context in page.data."""
        if page.data is None:
            page.data = {"username": user.username}
        page.data["previous_page"] = previous_page

    # ----------------- Taskbar (Header) -----------------
    def get_regions():
        try:
            response = httpx.get("http://localhost:8000/regions")
            if response.status_code == 200:
                return response.json()["regions"]
        except Exception as ex:
            print("Error fetching regions:", ex)
        return []

    # Function to search events based on the selected region
    def search_events(e):
        region = region_dropdown.value
        if region:
            try:
                response = httpx.get(f"http://localhost:8000/search_events?region={region}")
                if response.status_code == 200:
                    events = response.json()["events"]
                    # For demonstration, update a text control with the events data
                    events_text.value = f"Events in {region}: {events}"
                else:
                    events_text.value = f"No events found for {region}"
            except Exception as ex:
                events_text.value = f"Error: {ex}"
            page.update()

    # Retrieve regions from your server database (populated in server.py, :contentReference[oaicite:1]{index=1})
    regions = get_regions()
    # Create a dropdown using the retrieved regions
    region_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(region) for region in regions],
        hint_text="Select Location",
        expand=True,
        on_change=search_events,  # triggers the search when a region is selected
        border_color="white"
    )

    header = ft.Row(
        controls=[
            ft.Container(width=15),
            ft.Container(
                content=ft.Image(src="images/eventlink.png", width=200, height=80, fit=ft.ImageFit.CONTAIN),
                margin=ft.margin.only(right=10)
            ),
            # Search and Location Fields
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SEARCH, color="white", size=30),
                        ft.TextField(
                            hint_text="Search events",
                            border=None,
                            expand=True,
                            text_style=ft.TextStyle(size=18, color="white"),
                            border_radius=20,
                            border_color="white",
                            on_submit=lambda e: load_search(page, e.control.value.strip() or "All", search_type="global")
                        ),
                        ft.VerticalDivider(width=1, color="white"),
                        ft.Icon(name=ft.Icons.LOCATION_ON, color="white", size=30),
                        # Use the dropdown in place of the TextField
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
                            on_click=lambda e: load_my_events(page)  # Call the function to load My Events
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.EVENT_NOTE, color="white", size=15),
                                ft.Text("Create Event", style=ft.TextStyle(color="white", size=15))
                            ]),
                            on_click=lambda e: load_create_event(page)  # Call the function to load Create Events
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
            # Notifications Icon Container with a border overlay
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
            # Profile Popup Menu Container with a border overlay
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

    # The taskbar container sits at the very top.
    taskbar = ft.Container(
        content=header,
        height=100,  # Adjust height as needed
        bgcolor="#0C3B2E",
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=10)
    )

    # ----------------- Other Main Content -----------------
    top_left_text = ft.Container(
        content=ft.Text(
            "Upcoming Events 🎉",
            size=30,
            weight=ft.FontWeight.BOLD,
            color="#faf9f7",
            text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.top_left,
        margin=ft.margin.only(top=100, left=250),
        padding=20
    )

    # ======== FLOATING DISCOVER & SLIDER ========

    # 1) "Discover" text remains unchanged (you can also adjust its font size if desired)
    # Headline text at the top of the slider
    discover_text = ft.Text(
        "Discover New Events!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.CENTER
    )

    # Slider images
    slider_images = [
        "images/eventsample_img1.jpg",
        "images/eventsample_img2.png",
        "images/eventsample_img3.jpg",
    ]

    # Corresponding descriptions for each image
    slider_descriptions = [
        "Description for Image 1: A fantastic outdoor event you won't want to miss!",
        "Description for Image 2: Join us and help the people in need!",
        "Description for Image 3: Volunteer opportunities to make a positive impact!",
    ]

    # Create an AnimatedSwitcher for the images
    animated_slider = ft.AnimatedSwitcher(
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=1000,
        content=ft.Image(
            src=slider_images[0],
            width=600,
            height=300,
            fit=ft.ImageFit.FIT_WIDTH,
            border_radius=20
        )
    )

    # Create a second AnimatedSwitcher for the text descriptions
    animated_text = ft.AnimatedSwitcher(
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=1000,
        content=ft.Text(
            slider_descriptions[0],
            color="white",
            size=14,
            text_align=ft.TextAlign.CENTER
        )
    )

    # Loop that periodically switches both the image and the description
    def slider_loop():
        current_index = 0
        while True:
            time.sleep(8)  # Wait 8 seconds before switching
            current_index = (current_index + 1) % len(slider_images)
            # Update the image
            animated_slider.content = ft.Image(
                src=slider_images[current_index],
                width=600,
                height=300,
                fit=ft.ImageFit.FIT_WIDTH,
                border_radius=20
            )
            # Update the text
            animated_text.content = ft.Text(
                slider_descriptions[current_index],
                color="white",
                size=14,
                text_align=ft.TextAlign.CENTER
            )
            page.update()

    # Start the slider in a background thread
    threading.Thread(target=slider_loop, daemon=True).start()

    # Combine the "Discover" text, the image, and the description in one column
    floating_slider_content = ft.Container(
        width=420,                # Adjust width to suit your design
        height=page.height *1.5,
        bgcolor="#1D572C",
        border_radius=20,
        padding=15,
        content=ft.Column(
            controls=[
                discover_text,
                animated_slider,
                animated_text
            ],
            spacing=15,
            alignment=ft.alignment.top_center,
        ),
    )

    # Place the slider container on the right side of the screen
    floating_slider_container = ft.Container(
        content=floating_slider_content,
        alignment=ft.alignment.center_right,
        margin=ft.margin.only(right=20, top=120, bottom=10),
    )

    # ======== END FLOATING DISCOVER & SLIDER ========

    # 5) Minimal "homepage_view" with only top_left_text
    homepage_view = ft.Container(
        content=top_left_text,
        expand=True
    )

    # ----------------- Category Icons Section -----------------
     # Text control to display which category was clicked
    selected_category_text = ft.Text("Selected Category: None", size=20, color="white")

    # Click handler: updates the visible text and prints to console
    def handle_category_click(e, category_label: str):
        load_search(page, query=category_label, search_type="category")
        print(f"{category_label} quick search triggered!")



    # Helper function: returns a clickable row with an icon and label
    def category_row(icon_name: str, label: str):
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
            ink=True,  # adds a ripple effect when clicked
            border_radius=ft.border_radius.all(5),
        )

    # Header texts for the sidebar
    filters_text = ft.Text("Filters", color="white", size=20, weight=ft.FontWeight.BOLD)
    category_text = ft.Text("Category", color="white", size=16, weight=ft.FontWeight.W_600)

    # Build the list of category items
    category_buttons = ft.Column(
        controls=[
            filters_text,
            category_text,
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

    # Create the sidebar container
    side_taskbar = ft.Container(
        content=ft.Container(
            content=category_buttons,
            width=245,             # adjust as needed
            bgcolor="#1d572c",     # your desired sidebar color
            alignment=ft.alignment.top_left,
            padding=20
        ),
        alignment=ft.alignment.top_left,
        margin=ft.margin.only(top=100)
    )

    event1_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#a63b0a",
            alignment=ft.alignment.top_center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=178, right=620)
    )

    event2_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#a6750a",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=178, right= -220)
    )

    event3_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#0a9135",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=530, right=620)
    )

    event4_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#b6dbf2",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=530, right=-220)
    )

    # Place the floating slider LAST so it appears on top
    main_stack = ft.Stack(
        controls=[
            homepage_view,
            event1_highlight,
            event2_highlight,
            event3_highlight,
            event4_highlight,
            floating_slider_container,
            taskbar,
            side_taskbar,  # Move the sidebar to the last element so it's on top
        ],
        expand=True,
    )


    page.controls.clear()
    page.add(main_stack)
    page.update()


def load_homepage(page):
    page.controls.clear()
    main(page)

def load_login(page):
    page.floating_action_button = None
    pass

def load_my_events(page):
    import my_events
    page.controls.clear()
    my_events.load_my_events(page)  # Calls the function without restarting the app
    page.update()

def load_create_event(page):
    import CreateEvents
    page.controls.clear()
    CreateEvents.load_create_event(page)  # Calls the function without re-running ft.app()
    page.update()


def load_profile(page):
    page.floating_action_button = None
    pass

if __name__ == "__main__":
    ft.app(target=main)
