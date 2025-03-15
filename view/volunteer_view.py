import flet as ft
import threading
import time
from datetime import datetime
from model.volunteer_model import VolunteerModel
from controller.sidebar_controller import SidebarController
from controller.volunteer_form_controller import VolunteerFormController

class VolunteerView:
    def __init__(self, controller):
        self.controller = controller
        self.scrollable_results = ft.ListView(expand=True, spacing=10)

    def get_event_status(self, event_date, event_time):
        """Determine the status of the event based on the current date and time."""
        try:
            # ✅ Fix: Only use the first time value if it's a range (e.g., "04:30 - 22:00")
            event_time = event_time.split(" - ")[0]  # Extract only the start time

            event_datetime_str = f"{event_date} {event_time}"
            event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")  # ✅ Now it's valid
            current_datetime = datetime.now()

            return "Closed" if current_datetime > event_datetime else "Available"
        except ValueError:
            return "Unknown"  # ✅ If parsing fails, return "Unknown"

    def load_events(self, page):
        """Fetch events and update the UI."""
        self.scrollable_results.controls.clear()
        self.scrollable_results.controls.append(ft.Text("Loading Events...", size=20, color="white"))
        page.update()

        username = page.data.get("username")
        if not username:
            self.scrollable_results.controls.append(ft.Text("Error: No user logged in.", size=20, color="red"))
            page.update()
            return

        # ✅ Initialize the volunteer form controller
        form_controller = VolunteerFormController(page)
        events = form_controller.fetch_joined_events()  # ✅ Fetch events correctly

        self.scrollable_results.controls.clear()
        if not events:
            self.scrollable_results.controls.append(
                ft.Text("You haven't joined any events.", size=20, color="white")
            )
        else:
            for event in events:
                event_status = self.get_event_status(event.get("date", ""), event.get("time", ""))
                status_color = {"Available": "#4CAF50", "Closed": "#FF5252"}.get(event_status, "white")
                text_color = "white" if event_status == "Available" else "#B0B0B0"

                event_container = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(event.get("name", "Unnamed Event"), size=22, color=text_color, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Date: {event.get('date', 'N/A')}", color=text_color),
                                    ft.Text(f"Time: {event.get('time', 'N/A')}", color=text_color),
                                    ft.Text(f"Region: {event.get('location', 'N/A')}", color=text_color),
                                    ft.Text(f"Category: {event.get('type', 'Unknown')}", color=text_color),
                                    ft.Text(""),
                                    ft.Text(f"Date Joined: {event.get('joined', 'N/A').split(' ')[0]}", color=text_color)
                                ],
                                spacing=5
                            ),
                            ft.Container(
                                content=ft.Text(event_status, color="white", weight=ft.FontWeight.BOLD, size=18),
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=5,
                                bgcolor=status_color
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=10,
                    border_radius=10,
                    bgcolor="#105743",
                    ink=True,
                    on_click=lambda e, ev=event: form_controller.show_volunteer_popup(page, ev) if event_status == "Available" else None
                )
                self.scrollable_results.controls.append(event_container)
                self.scrollable_results.controls.append(ft.Divider(color="white", thickness=1, height=10))

        page.update()

    def build(self, page: ft.Page):
        """Builds the volunteer view UI."""
        page.bgcolor = "#d6aa54"

        sidebar_controller = SidebarController(page)
        sidebar = sidebar_controller.build()

        status_header = ft.Text(
            "Volunteer Dashboard",
            size=30,
            weight=ft.FontWeight.BOLD,
            color="white"
        )

        header_divider = ft.Divider(color="white", thickness=1)

        self.scrollable_results.controls.append(
            ft.Text("Loading Events...", size=20, color="white")
        )

        main_content = ft.Container(
            content=ft.Column([
                status_header,
                header_divider,
                self.scrollable_results
            ], spacing=20, expand=True),
            margin=ft.margin.only(left=270, top=30, right=40),
            expand=True
        )

        layout = ft.Stack(
            controls=[
                sidebar,  # Sidebar should be first so it's at the back
                main_content  # Main content should be on top, but not covering the sidebar
            ],
            expand=True
        )

        page.controls.clear()
        page.add(layout)
        page.update()

        # Start loading events in the background
        threading.Thread(target=self.load_events, args=(page,), daemon=True).start()

        return layout