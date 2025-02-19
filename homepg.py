import flet as ft
import time
import threading

# Global variable to store the notification popup overlay
notif_popup = None

def main(page: ft.Page):
    page.title = "Home"
    page.bgcolor = "#5F7755"
    page.padding = 0  # Ensure no extra padding at the edges

    def logout(e):
        """
        Log the user out by clearing the username from page.data
        and navigating back to the login page after a 0.6-second delay.
        """
        def delayed_logout():
            time.sleep(0.6)
            if page.data is not None:
                page.data.clear()
            import login
            login.load_login(page)
        threading.Thread(target=delayed_logout).start()

    def show_profile_page(e):
        """
        Show the user profile page after a 2-second delay.
        """
        def delayed_profile():
            time.sleep(2)
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
        notifications = [
            "Notification 1: Event Update",
            "Notification 2: New Message",
            "Notification 3: System Maintenance",
            "Notification 4: Special Offer",
            "Notification 5: Reminder",
            "Notification 5: Reminder",
            "Notification 5: Reminder",
            "Notification 5: Reminder",
            # ... add more if needed ...
        ]

        def on_click_event(event_text):
            print(f"Event clicked: {event_text}")

        notif_controls = []
        for notif in notifications:
            notif_controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[ft.Text(notif, size=18, color="white", weight=ft.FontWeight.BOLD)],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=15),
                    bgcolor="#4C7043",
                    border_radius=10,
                    margin=ft.margin.only(bottom=10),
                    on_click=lambda e, notif_text=notif: on_click_event(notif_text),
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

        inner_popup_height = 400

        inner_popup = ft.Container(
            content=ft.Column(
                controls=[close_button, list_view],
                spacing=20,
            ),
            bgcolor="#6D9773",
            padding=10,
            border_radius=10,
            width=400,
            height=inner_popup_height,
            shadow=ft.BoxShadow(blur_radius=10, color="gray", offset=ft.Offset(2, 2)),
            on_click=lambda e: e.stop_propagation() if hasattr(e, "stop_propagation") else None,
        )

        notif_popup = ft.AnimatedSwitcher(
            duration=500,  # Duration in milliseconds
            content=ft.Container(
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=100, bottom=300, right=15),
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

    # ----------------- Taskbar (Header) -----------------
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
                        ft.Icon(ft.Icons.SEARCH, color="white", size=30),
                        ft.TextField(
                            hint_text="Search events",
                            border=None,
                            expand=True,
                            text_style=ft.TextStyle(size=18, color="white"),
                            border_radius=20,
                            border_color="#B46617"
                        ),
                        ft.VerticalDivider(width=1, color="white"),
                        ft.Icon(ft.Icons.LOCATION_ON, color="white", size=30),
                        ft.TextField(
                            hint_text="Select Location",
                            border=None,
                            expand=True,
                            text_style=ft.TextStyle(size=18, color="white"),
                            border_radius=20,
                            border_color="#B46617"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                border_radius=15,
                border=ft.border.all(1, "#B46617"),
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                expand=True,
                bgcolor="#105743",
                margin=ft.margin.only(top=16, bottom=16)
            ),
            # Shop Button
            ft.Container(
                content=ft.TextButton(
                    text="Shop",
                    on_click=lambda e: print("Shop clicked"),
                    style=ft.ButtonStyle(color="white", text_style=ft.TextStyle(size=20)),
                    height=55
                ),
                margin=ft.margin.only(left=50, right=10)
            ),
            # Events Popup Menu
            ft.Container(
                content=ft.PopupMenuButton(
                    content=ft.Text("Events", style=ft.TextStyle(size=20, color="white")),
                    bgcolor="#B46617",
                    items=[
                        ft.PopupMenuItem(text="My Events", on_click=lambda e: print("My Events clicked")),
                        ft.PopupMenuItem(text="Create Event", on_click=lambda e: print("Create Event clicked")),
                        ft.PopupMenuItem(text="Volunteer", on_click=lambda e: print("Volunteer clicked"))
                    ]
                ),
                margin=ft.margin.only(left=50, right=10)
            ),
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
                margin=ft.margin.only(left=50, right=10)
            ),
            # Profile Popup Menu
            ft.Container(
                content=ft.PopupMenuButton(
                    icon=ft.Icons.PERSON_ROUNDED,
                    icon_color="#FFBA00",
                    icon_size=40,
                    bgcolor="#B46617",
                    tooltip="Profile Menu",
                    width=60,
                    items=[
                        ft.PopupMenuItem(text="Profile", on_click=show_profile_page),
                        ft.PopupMenuItem(text="Logout", on_click=logout)
                    ]
                ),
                margin=ft.margin.only(left=50, right=20)
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
    welcome_section = ft.Container(
        content=ft.Text(
            "Your Personalized Event Experience Starts Here!",
            size=50,
            weight=ft.FontWeight.BOLD,
            color="white",
            text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.center,
        padding=20
    )

    slider_images = [
        "images/eventsample_img1.jpg",
        "images/eventsample_img2.png",
        "images/eventsample_img3.jpg",
    ]
    
    # AnimatedSwitcher for the slider image with a fade transition (default behavior)
    animated_slider = ft.AnimatedSwitcher(
        duration=500,  # Duration in milliseconds
        content=ft.Image(src=slider_images[0], width=600, height=300, fit=ft.ImageFit.FIT_WIDTH)
    )

    slider_image_container = ft.Container(
        content=animated_slider,
        width=500,
        height=400,
        padding=10,
        border=ft.border.all(5, "#FFBA00"),
        border_radius=10,
        margin=ft.margin.only(bottom=50, right=120)
    )

    slider_container = ft.Container(
        content=ft.Stack(
            controls=[slider_image_container],
            alignment=ft.alignment.center_right
        ),
        alignment=ft.alignment.center_right,
        margin=ft.margin.only(bottom=50, right=5)
    )

    def slider_loop():
        current_index = 0
        while True:
            time.sleep(8)
            current_index = (current_index + 1) % len(slider_images)
            animated_slider.content = ft.Image(
                src=slider_images[current_index],
                width=600,
                height=300,
                fit=ft.ImageFit.FIT_WIDTH
            )
            page.update()

    threading.Thread(target=slider_loop, daemon=True).start()

    homepage_view = ft.Column(
        controls=[welcome_section, slider_container],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )

    # Floating adjustable box (background element)
    floating_adjustable_box = ft.Container(
        content=ft.Container(
            content=ft.Text("Adjustable Box", size=24, weight=ft.FontWeight.BOLD, color="white"),
            width=300,
            height=200,
            bgcolor="#B46617",
            alignment=ft.alignment.center,
            border_radius=10,
            padding=20,
        ),
        expand=True,
        alignment=ft.alignment.center
    )

    # Main content area as a Stack (for overlapping the floating adjustable box)
    main_stack = ft.Stack(
        controls=[floating_adjustable_box, homepage_view],
        expand=True,
    )

    page_view = ft.Column(
        controls=[taskbar, main_stack],
        expand=True
    )

    page.controls.clear()
    page.add(page_view)
    page.on_click = handle_click_outside
    page.update()

def load_homepage(page):
    """A separate function to load homepage only."""
    page.controls.clear()
    main(page)

def load_login(page):
    """A separate function to load login page."""
    page.floating_action_button = None
    # Add your login page controls here
    pass

def load_profile(page):
    """A separate function to load profile page."""
    page.floating_action_button = None
    # Add your profile page controls here
    pass

if __name__ == "__main__":
    ft.app(target=main)
