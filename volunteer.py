import flet as ft
import threading
import time
from datetime import datetime
from header import load_header
from volunteer_form import fetch_joined_events, show_volunteer_popup
import httpx

def clear_overlay(page: ft.Page):
    """Clear the overlay (e.g., volunteer popup) from the page."""
    if page.overlay:
        page.overlay.clear()
        page.update()

def load_volunteer(page: ft.Page):
    if page.data is None:
        page.data = {}

    # Set flag to track volunteer form activity
    page.data["volunteer_form_active"] = True


    page.controls.clear()
    page.bgcolor = "#d6aa54"

    # Load header (DO NOT REMOVE)
    taskbar = load_header(page)

    def get_event_status(event_date, event_time):
        """Determine the status of the event based on the current date and time."""
        event_datetime_str = f"{event_date} {event_time}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        if current_datetime > event_datetime:
            return "Closed"
        else:
            return "Available"

    def load_events():
        """Fetch events and update the UI."""
        results_list.controls.clear()
        results_list.controls.append(ft.Text("Loading Results...", size=20, color="white"))
        page.update()

        time.sleep(0.5)
        events = fetch_joined_events(page)

        results_list.controls.clear()
        if not events:
            results_list.controls.append(
                ft.Text("You haven't joined any events.", size=20, color="white")
            )
        else:
            for event in events:
                event_status = get_event_status(event.get("date", ""), event.get("time", ""))
                status_color = {
                    "Available": "#4CAF50",
                    "Closed": "#FF5252"
                }.get(event_status, "white")
                
                text_color = "white" if event_status == "Available" else "#B0B0B0"  # Gray color for closed events

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
                                    ft.Text(f"Date Joined: {event.get('joined', 'N/A').split(' ')[0]}", color=text_color)  # Removed alignment arg
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
                    on_click=lambda e, ev=event: show_volunteer_popup(page, ev) if get_event_status(ev.get("date", ""), ev.get("time", "")) == "Available" else None  # Only Available if status is "Available"
                )
                results_list.controls.append(event_container)

                # Add a divider between events
                results_list.controls.append(ft.Divider(color="white", thickness=1, height=10))

        page.update()

    # Volunteer Dashboard centered with 80% width
    status_header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.VOLUNTEER_ACTIVISM, color="white", size=30),
            ft.Text("Volunteer Dashboard", size=28, weight=ft.FontWeight.BOLD, color="white")
        ], spacing=15),
        padding=ft.padding.only(top=20),  # Keep spacing from top
        width=page.width * 0.8,  # 80% width
        alignment=ft.alignment.center  # Center it properly
    )

    # Divider below header (also centered)
    header_divider = ft.Container(
        content=ft.Divider(color="white", thickness=2),
        width=page.width * 0.8,  # Match width with header
        alignment=ft.alignment.center
    )

    # Main content centered with 70% width
    results_list = ft.ListView(expand=True, spacing=10)

    # Wrap the results_list in a Container with a fixed height to make it scrollable
    scrollable_results = ft.Container(
        content=results_list,
        height=page.height * 0.73,  # Adjust the height as needed
        width=page.width * 0.8,
        alignment=ft.alignment.center
    )

    main_content = ft.Container(
        content=ft.Column([
            status_header,
            header_divider,
            scrollable_results  # Use the scrollable container here
        ], spacing=25, alignment=ft.alignment.center),  # Center column
        width=page.width * 0.8,  # Set width to 70%
        alignment=ft.alignment.center  # Center it properly
    )

    # Assemble the page (KEEP THE HEADER)
    page.add(
        ft.Column([
            taskbar,  # Header remains at the top
            ft.Container(  # Center everything properly
                content=ft.Column([
                    main_content
                ], alignment=ft.alignment.center),
                alignment=ft.alignment.center
            )
        ])
    )
    page.update()

    threading.Thread(target=load_events, daemon=True).start()