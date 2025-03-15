import flet as ft
from model.sidebar_model import SidebarModel
from view.sidebar_view import SidebarView

class SidebarController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = SidebarModel()
        self.view = SidebarView(self)

    def get_items(self):
        return self.model.get_items()

    def on_item_click(self, e, item_label: str):
        print(f"Item clicked: {item_label}")
        # Handle item click logic here

    def build(self):
        return self.view.build(self.page)