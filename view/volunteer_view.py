import flet as ft
from controller.sidebar_controller import SidebarController  # ✅ Import SidebarController

class VolunteerView:
    def __init__(self, controller):
        self.controller = controller
        self.results_list = ft.ListView(expand=True, spacing=10)  # ✅ Expand for scrolling support

    def build(self, page: ft.Page):
        """
        Build the volunteer dashboard UI.
        """
        page.bgcolor = "#d6aa54"

        # # Load the header (taskbar)
        # taskbar = self.controller.load_header(page)

        # ✅ Load Sidebar
        sidebar_controller = SidebarController(page)
        sidebar = sidebar_controller.build()

        # Header for the volunteer dashboard
        status_header = ft.Text(
            "Volunteer Dashboard",
            size=30,
            weight=ft.FontWeight.BOLD,
            color="white"
        )

        header_divider = ft.Divider(color="white", thickness=1)

        # Container for the scrollable event results
        self.scrollable_results = ft.ListView(expand=True, spacing=10)
        self.scrollable_results.controls.append(
            ft.Text("Loading Events...", size=20, color="white")
        )

        # Main content container
        main_content = ft.Container(
            content=ft.Column([
                status_header,
                header_divider,
                self.scrollable_results
            ], spacing=20, expand=True),
            margin=ft.margin.only(left=270, top=30, right=40),  # ✅ Align with search page
            expand=True
        )

        # ✅ Wrap Sidebar and Content inside a Stack
        layout = ft.Stack(
            controls=[
                main_content,  # Main content
                # taskbar,       # Taskbar (on top)
                sidebar        # Sidebar (on the left)
            ],
            expand=True
        )

        # Clear the page and add the new layout
        page.controls.clear()
        page.add(layout)
        page.update()
