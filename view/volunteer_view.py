import flet as ft
from datetime import datetime
from model.volunteer_model import VolunteerModel  
from controller.sidebar_controller import SidebarController
from controller.volunteer_form_controller import VolunteerFormController

class VolunteerView:
    def __init__(self, controller):
        self.controller = controller
        self.page = controller.page  # ✅ Store reference to page
        self.scrollable_results = ft.ListView(expand=True, spacing=10)  # Ensure expand=True
        print("✅ VolunteerView initialized")  # Debugging print

    def get_event_status(self, event_date, event_time):
        """Determine the status of the event based on the current date and time."""
        try:
            if not event_date or not event_time:
                print("⚠️ Event date or time is missing.")
                return "Unknown"
                
            event_time = event_time.split(" - ")[0] if " - " in event_time else event_time  # ✅ Fix time extraction
            event_datetime_str = f"{event_date} {event_time}"
            print("Parsed datetime string:", event_datetime_str)  # ✅ Debugging print

            event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
            return "Closed" if datetime.now() > event_datetime else "Available"
        except ValueError as e:
            print("❌ Error parsing date/time:", e)  # ✅ Debugging print
            return "Unknown"

    def update_event_list(self, page, events):
        print("✅ Updating event list with", len(events), "events")
        self.scrollable_results.controls.clear()  # Clear old data
        page.update()  # Force refresh before adding new elements

        if not events:
            print("⚠️ No events found to display.")
            self.scrollable_results.controls.append(
                ft.Text("You haven't joined any events.", size=20, color="white")
            )
        else:
            print(f"Processing {len(events)} events")  # Debugging print
            for event in events:
                print(f"Processing event: {event.get('name', 'Unnamed')}")  # Debugging print
                print(f"Event data: {event}")  # Debugging print
                
                event_status = self.get_event_status(event.get("date", ""), event.get("time", ""))
                print(f"Event status: {event_status}")  # Debugging print
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
                    on_click=lambda e, ev=event: self.controller.update_volunteer_status(e, ev.get("name")) if event_status == "Available" else None
                )
                
                self.scrollable_results.controls.append(event_container)
                self.scrollable_results.controls.append(ft.Divider(color="white", thickness=1, height=10))

        # Debugging: Print the controls in scrollable_results
        print(f"Controls in scrollable_results: {self.scrollable_results.controls}")

        page.update()  # Ensure this is called after all events are added
        print("Event list updated!")  # Debugging print
        
    def build(self, page: ft.Page): 
        print("Building VolunteerView UI...")  # Debugging print
        page.bgcolor = "#d6aa54"

        if "sidebar" not in page.data:
            print("Building sidebar...")  # Debugging print
            sidebar_controller = SidebarController(page)
            sidebar = sidebar_controller.build()
            page.data["sidebar"] = sidebar
        else:
            sidebar = page.data["sidebar"]
            
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
                self.scrollable_results,  # Ensure this is included
                ft.Container(alignment=ft.alignment.center)  # Add back button
            ], spacing=20, expand=True),
            margin=ft.margin.only(left=270, top=30, right=40),
            expand=True
        )

        layout = ft.Stack(
            controls=[sidebar, main_content],
            expand=True
        )

        page.controls.clear()
        page.add(layout)
        page.update()

        print("VolunteerView UI built successfully.")  # Debugging print
        return layout