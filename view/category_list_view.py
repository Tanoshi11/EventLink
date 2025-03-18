import flet as ft

class CategoryListView:
    def __init__(self, controller):
        self.controller = controller

    def create_category_row(self, icon_name: str, label: str, on_click):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=15),
                    ft.Text(label, style=ft.TextStyle(color="white", size=15))
                ],
                spacing=5
            ),
            on_click=on_click,  # ✅ `Container` supports `on_click`
            padding=ft.padding.all(5),
            border_radius=5,
            ink=True,  # Enables ripple effect when clicked
            bgcolor="#2c6e49"  # Optional: Background color for better visibility
        )


    def build(self, page: ft.Page):
        categories = self.controller.get_categories()
        category_buttons = ft.Column(
            controls=[
                ft.Text("Filters", color="white", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Category", color="white", size=16, weight=ft.FontWeight.W_600),
            ] + [
                self.create_category_row(category["icon"], category["label"], lambda e, label=category["label"]: self.controller.on_category_click(e, label))
                for category in categories
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.START
        )

        return ft.Container(
            content=category_buttons,
            width=245,
            bgcolor="#1d572c",
            alignment=ft.alignment.top_left,
            padding=20,
            margin=ft.margin.only(top=100)
        )