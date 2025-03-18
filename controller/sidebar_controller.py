import flet as ft
from model.sidebar_model import SidebarModel
from view.sidebar_view import SidebarView

class SidebarController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = SidebarModel()
        self.view = SidebarView(self)

    def sidebar_button_click(self, e):
        print(f"Sidebar Button Clicked: {e.control.text}")
        
        # Remove volunteer container if it exists
        volunteer_container = self.page.data.get("volunteer_container")
        if volunteer_container and volunteer_container in self.page.controls:
            self.page.controls.remove(volunteer_container)
            self.page.data["volunteer_container"] = None
            print("Volunteer container removed.")
        
        # Clear page (optionally preserve sidebar)
        # For example, if sidebar is stored as well:
        sidebar = self.page.data.get("sidebar")
        self.page.controls.clear()
        if sidebar:
            self.page.controls.append(sidebar)
        
        self.page.route = e.control.data
        self.page.update()
        self.page.go(self.page.route)




    def get_items(self):
        return self.model.get_items()

    def on_item_click(self, e, item_label: str):
        print(f"Item clicked: {item_label}")

    def build(self):
        return self.view.build(self.page)
    
    def create_item_row(self, icon_name: str, label: str, on_click):
        return ft.Container(
            content=ft.Row([
                ft.Icon(name=icon_name, color="white", size=22),
                ft.Text(label, style=ft.TextStyle(color="white", size=18))
            ]),
            on_click=lambda e: self.sidebar_button_click(e),  # ✅ Call button click
            padding=ft.padding.all(5),
            border_radius=5,
            ink=True,
            bgcolor="#114f3e",
            height=70
        )
