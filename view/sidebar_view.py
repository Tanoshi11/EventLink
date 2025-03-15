import flet as ft
import time
import threading
from utils import clear_overlay

class SidebarView:
    def __init__(self, controller):
        self.controller = controller

    def create_item_row(self, icon_name: str, label: str, on_click):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=22),
                    ft.Text(label, style=ft.TextStyle(color="white", size=18))
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,  # Center horizontally
                vertical_alignment=ft.CrossAxisAlignment.CENTER  # Center vertically
            ),
            on_click=on_click,  # ✅ Use `Container` for click handling
            padding=ft.padding.all(5),
            border_radius=5,
            ink=True,  # ✅ Adds ripple effect on click
            bgcolor="#114f3e",  # Optional styling
            height=70
        )

    def open_volunteer_page(self, e):
        """Handles navigation to the Volunteer page."""
        from controller.volunteer_controller import VolunteerController  # ✅ Lazy import
        page = e.control.page
        volunteer_controller = VolunteerController(page)
        volunteer_controller.load_volunteer()

    def logout(self, e):
        """Handles logout functionality with a delay."""
        page = e.control.page  

        def delayed_logout():
            time.sleep(0.6)
            if page.data is not None:
                page.data.clear()

            from controller.login_controller import main as login_main  
            login_main(page)  

        threading.Thread(target=delayed_logout).start()

    def load_homepage(self, page):
        """Loads the homepage."""
        from controller.homepg_controller import load_homepage  
        load_homepage(page)

    def load_search(self, page):
        """Loads the 'Search Events' page."""
        from controller.search_controller import load_search  
        load_search(page)

    def load_my_events(self, page):
        """Loads the 'My Events' page."""
        from controller.homepg_controller import load_my_events  
        load_my_events(page)

    def load_create_event(self, page):
        """Loads the 'Create Event' page."""
        from CreateEvents import load_create_event  
        load_create_event(page)

    def handle_category_click(self, e, category_label):
        """Handles category selection in the sidebar."""
        from controller.search_controller import load_search  
        load_search(self.controller.page, query=category_label, search_type="category")

    def build(self, page: ft.Page):
        """Builds the sidebar UI."""
        from controller.search_controller import load_search
        items = self.controller.get_items()

        item_buttons = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(src="images/eventlink.png", width=200, height=80, fit=ft.ImageFit.CONTAIN),
                    margin=ft.margin.only(right=10),
                    on_click=lambda e: (clear_overlay(page), self.load_homepage(page))
                ),
                self.create_item_row(ft.Icons.SEARCH_ROUNDED, "Search Events", 
                     lambda e: (clear_overlay(page), load_search(page, query="All"))),
                self.create_item_row(ft.Icons.CALENDAR_TODAY, "My Events", 
                                     lambda e: (clear_overlay(page), self.load_my_events(page))),
                self.create_item_row(ft.Icons.EVENT_NOTE, "Create Event", 
                                     lambda e: (clear_overlay(page), self.load_create_event(page))),
                self.create_item_row(ft.Icons.VOLUNTEER_ACTIVISM, "Volunteer", 
                                     lambda e: (clear_overlay(page), self.open_volunteer_page(e))),
            ] + [
                self.create_item_row(item["icon"], item["label"], 
                                     lambda e, label=item["label"]: self.handle_category_click(e, label))
                for item in items
            ],
            spacing=20,
            alignment=ft.CrossAxisAlignment.CENTER
        )

        logout_button = self.create_item_row(
            icon_name=ft.Icons.EXIT_TO_APP,
            label="Logout",
            on_click=lambda e: (clear_overlay(page), self.logout(e))
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    item_buttons,
                    ft.Container(height=20),  
                    logout_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True  
            ),
            width=245,
            bgcolor="#0C3B2E",
            alignment=ft.alignment.top_left,
            padding=20,
            expand=True  
        )
