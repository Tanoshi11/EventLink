import flet as ft
import httpx

# Global variable for the notifications popup
notif_popup = None

def clear_overlay(page: ft.Page):
    """Clear the overlay (e.g., join event form) from the page."""
    if page.overlay:
        page.overlay.clear()
        page.update()
        

def show_profile_page(e):
    page = e.control.page
    from controller.user_profile_controller import UserProfileController  
    profile_controller = UserProfileController(page, page.data.get("username"))
    profile_controller.show_profile()


def get_regions():
    """Fetch regions from the server."""
    try:
        response = httpx.get("http://localhost:8000/regions")
        if response.status_code == 200:
            regions = response.json()["regions"]
            print("Fetched regions:", regions)  # Debug print
            return regions
    except Exception as ex:
        print("Error fetching regions:", ex)
    return []

def load_header(page: ft.Page):
    global notif_popup

    # ----------------- Header Functions -----------------

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

    def search_events(e):
        """Trigger search when the user selects a region or presses Enter."""
        query = search_bar.value.strip() if search_bar.value else "All"
        location = region_dropdown.value

        # Debugging: Print the query and location
        print(f"Search triggered - Query: '{query}', Region: '{location}'")

        # Call load_search in search.py directly
        from controller.search_controller import load_search
        load_search(page, query, search_type="global", location=location)

    # ----------------- Build the Header UI -----------------
    # Fetch regions from the server
    regions = get_regions()

    # Create the dropdown with all regions
    region_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(region) for region in regions],
        hint_text="Select Region",
        hint_style=ft.TextStyle(size=17, color="white"),
        expand=True,
        border_color="white",
        bgcolor="#a8730a", 
        color="white",  # White text
        menu_height=320,
    )

    search_bar = ft.TextField(
        hint_text="Search events",
        border=None,
        expand=True,
        text_style=ft.TextStyle(size=17, color="white"),
        hint_style=ft.TextStyle(size=17, color="white"),
        border_radius=5,
        border_color="white",
        on_submit=search_events  # Trigger search when pressing Enter
    )

    header = ft.Row(
        controls=[
            ft.Container(width=15),
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
                bgcolor="#a8730a",
                margin=ft.margin.only(top=16, bottom=16, right=30)
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
                border=ft.border.all(2, "#FFBA00"),
                border_radius=30
            ),

            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.PERSON_ROUNDED,
                    on_click=lambda e: (clear_overlay(page), show_profile_page(e)),
                    icon_color="#FFBA00",
                    icon_size=40,
                    tooltip="Profile",
                    width=60
                ),
                margin=ft.margin.only(left=40, right=10),
                border=ft.border.all(2, "#FFBA00"),
                border_radius=30
            ),
        ]
    )

    taskbar = ft.Container(
        content=header,
        height=100,
        bgcolor="#4d3a17",
        alignment=ft.alignment.center_right,
        padding=ft.padding.symmetric(horizontal=10),
        margin=ft.margin.only(left=240)
    )
    return taskbar