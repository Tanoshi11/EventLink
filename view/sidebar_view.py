import flet as ft
import httpx
from utils import clear_overlay

class SidebarView:
    def __init__(self, controller):
        self.controller = controller
        self.bottom_spacing = 20  # Default spacing for bottom buttons
        self.bottom_section_height = 200  # Default height of the bottom section box
        self.bottom_row_height = 50  # Default height of bottom item rows
        self.notif_popup = None
        self.page = None  # Store page reference when build() is called

    def set_bottom_spacing(self, spacing):
        self.bottom_spacing = spacing

    def set_bottom_section_height(self, height):
        self.bottom_section_height = height

    def set_bottom_row_height(self, height):
        self.bottom_row_height = height

    def create_item_row(self, icon_name: str, label: str, on_click, height=70):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=22),
                    ft.Text(label, style=ft.TextStyle(color="white", size=18))
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            on_click=on_click,
            padding=ft.padding.all(5),
            border_radius=5,
            ink=True,
            bgcolor="#114f3e",
            height=height
        )

    def load_profile_page(self, e):
        """Navigates to the profile page."""
        from controller.user_profile_controller import UserProfileController
        username = self.page.data.get("username")
        if not username:
            print("No username found!")
            return
        profile_controller = UserProfileController(self.page, username)
        profile_controller.show_profile()

    def load_homepage(self, e):
        """Loads the homepage."""
        from controller.homepg_controller import load_home
        clear_overlay(self.page)
        load_home(self.page)

    def load_my_events(self, e):
        """Loads the user's events page."""
        from my_events import load_my_events
        clear_overlay(self.page)
        load_my_events(self.page)

    def load_create_event(self, e):
        """Loads the event creation page."""
        from CreateEvents import load_create_event
        clear_overlay(self.page)
        load_create_event(self.page)

    def open_volunteer_page(self, e):
        """Opens the volunteer page."""
        from controller.volunteer_controller import load_volunteer
        clear_overlay(self.page)
        load_volunteer(self.page)

    def logout(self, e):
        """Logs out the user and redirects to the login screen."""
        try:
            from controller.login_controller import handle_logout  # Import inside function
            handle_logout(self.page)  # Call the function
        except ImportError:
            print("Error: handle_logout() is missing in login_controller.py")



    def close_notifications(self, e):
        if self.notif_popup and self.notif_popup in self.page.overlay:
            self.page.overlay.remove(self.notif_popup)
            self.notif_popup = None
            self.page.update()

    def open_notifications(self, e):
        if self.notif_popup:
            self.close_notifications(e)
        else:
            self.show_notifications(e)

    def show_notifications(self, e):
        username = self.page.data.get("username")
        if not username:
            print("No username found!")
            return
        try:
            response = httpx.get(f"http://localhost:8000/notifications?username={username}")
            notifications_data = response.json().get("notifications", [{"message": "No notifications found."}]) if response.status_code == 200 else [{"message": "No notifications found."}]
        except Exception as ex:
            print("Error fetching notifications:", ex)
            notifications_data = [{"message": "Error fetching notifications."}]

        notif_controls = [ft.Container(
            content=ft.Text(notif.get("message", "No message"), size=18, color="white", weight=ft.FontWeight.BOLD),
            padding=ft.padding.symmetric(horizontal=15, vertical=15),
            bgcolor="#4C7043",
            border_radius=10,
            margin=ft.margin.only(bottom=10)
        ) for notif in notifications_data]

        close_button = ft.IconButton(icon=ft.Icons.CLOSE, on_click=self.close_notifications, icon_color="white", icon_size=30)

        self.notif_popup = ft.AnimatedSwitcher(
            duration=500,
            content=ft.Container(
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=100, right=15),
                content=ft.Container(
                    content=ft.Column(controls=[close_button, ft.ListView(controls=notif_controls, height=300, expand=True)], spacing=20),
                    bgcolor="#6D9773",
                    padding=10,
                    border_radius=10,
                    width=400,
                    height=400,
                ),
            ),
        )

        self.page.overlay.append(self.notif_popup)
        self.page.update()

    def build(self, page: ft.Page):
        self.page = page  # Store the page reference
        from controller.search_controller import load_search
        items = self.controller.get_items()

        top_section = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(src="images/eventlink.png", width=200, height=80, fit=ft.ImageFit.CONTAIN),
                    margin=ft.margin.only(right=10),
                    on_click=self.load_homepage
                ),
                self.create_item_row(ft.Icons.SEARCH_ROUNDED, "Search Events", lambda e: (clear_overlay(page), load_search(page, query="All"))),
                self.create_item_row(ft.Icons.CALENDAR_TODAY, "My Events", self.load_my_events),
                self.create_item_row(ft.Icons.EVENT_NOTE, "Create Event", self.load_create_event),
                self.create_item_row(ft.Icons.VOLUNTEER_ACTIVISM, "Volunteer", self.open_volunteer_page)
            ] + [
                self.create_item_row(item["icon"], item["label"], lambda e, label=item["label"]: self.handle_category_click(e, label))
                for item in items
            ],
            spacing=22,
            alignment=ft.MainAxisAlignment.START
        )

        bottom_section = ft.Container(
            content=ft.Column(
                controls=[
                    self.create_item_row(ft.Icons.PERSON_ROUNDED, "Profile", self.load_profile_page, height=self.bottom_row_height),
                    ft.Container(height=self.bottom_spacing),
                    self.create_item_row(ft.Icons.NOTIFICATIONS, "Notifications", self.open_notifications, height=self.bottom_row_height),
                    ft.Container(height=self.bottom_spacing),
                    self.create_item_row(ft.Icons.EXIT_TO_APP, "Logout", self.logout, height=self.bottom_row_height)
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=5
            ),
            height=300
        )

        return ft.Container(
            content=ft.Column(
                controls=[top_section, ft.Container(expand=True), bottom_section],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True
            ),
            width=245,
            bgcolor="#0C3B2E",
            alignment=ft.alignment.top_left,
            padding=20,
            expand=True
        )
