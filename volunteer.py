import flet as ft
import httpx
import threading
import time
from header import load_header

def load_volunteer(page: ft.Page):
    # Initialize page.data if needed
    if page.data is None:
        page.data = {}

    # Clear previous UI
    page.controls.clear()
    
    # Set page background color
    page.bgcolor = "#d6aa54"
    
    # Load header
    taskbar = load_header(page)

    # ----------------- Helper Functions -----------------
    def fetch_joined_events():
        """Fetch events based on the selected category."""
        try:
            username = page.data.get("username", "default_user")
            category = page.data.get("category", None)
            url = f"http://localhost:8000/my_events?username={username}"
            if category:
                url += f"&category={category}"
            response = httpx.get(url)
            if response.status_code == 200:
                return response.json().get("events", [])
        except Exception as ex:
            print("Error fetching events:", ex)
        return []

    def update_volunteer_status(e, event_id: str):
        """Update user to 'Volunteer' for an event."""
        try:
            username = page.data.get("username")
            if not username:
                return
            response = httpx.patch(
                f"http://localhost:8000/update_user?username={username}",
                json={"status": "Volunteer"}
            )
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(
                    ft.Text("You are now a volunteer!"),
                    bgcolor="#4CAF50"
                )
                e.control.text = "Volunteering!"
                e.control.bgcolor = "#4CAF50"
                e.control.disabled = True
                e.control.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error updating status: {ex}"),
                bgcolor="red"
            )
        finally:
            page.snack_bar.open = True
            page.update()

    def load_events():
        """Fetch events and update the UI quickly."""
        # Display a loading message while waiting for results
        results_list.controls.clear()
        results_list.controls.append(ft.Text("Loading Results...", size=20, color="white"))
        page.update()

        time.sleep(0.5)  # Optional delay
        events = fetch_joined_events()

        results_list.controls.clear()
        if not events:
            results_list.controls.append(
                ft.Text("No volunteer events found.", size=20, color="white")
            )
        else:
            for event in events:
                # Placeholder: Check if the user has joined the event.
                # For now, we'll assume they have joined (set joined=True).
                # Later, you can replace this with a real check from your endpoint.
                joined = event.get("joined", True)
                volunteer_button = ft.ElevatedButton(
                    "Volunteer" if joined else "Join Event First",
                    icon=ft.icons.VOLUNTEER_ACTIVISM,
                    on_click=lambda e, ev=event: update_volunteer_status(e, ev.get("id")) if joined else None,
                    bgcolor="#105743",
                    color="white",
                    disabled=not joined
                )
                results_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(
                                    event.get("name", "Unnamed Event"),
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color="white"
                                ),
                                volunteer_button
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Date: {event.get('date', 'N/A')}", color="white"),
                            ft.Text(f"Location: {event.get('location', 'N/A')}", color="white"),
                            ft.Divider(color="white")
                        ]),
                        bgcolor="#1d572c",
                        border_radius=10,
                        margin=ft.margin.only(bottom=10)
                    )
                )
        page.update()

    def handle_category_click(e, category_label: str):
        """Handle category selection and immediately fetch new events."""
        page.data["category"] = category_label
        threading.Thread(target=load_events, daemon=True).start()

    def category_row(icon_name: str, label: str):
        """Create a category button."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=20),
                    ft.Text(label, color="white", size=16)
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.all(5),
            on_click=lambda e: handle_category_click(e, label),
            ink=True,
            border_radius=ft.border_radius.all(5)
        )

    # ----------------- Sidebar (Categories) -----------------
    category_buttons = ft.Column(
        controls=[
            ft.Text("Filters", color="white", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Category", color="white", size=16, weight=ft.FontWeight.W_600),
            category_row(ft.Icons.BUSINESS_CENTER, "Business"),
            category_row(ft.Icons.RESTAURANT, "Food & Drink"),
            category_row(ft.Icons.CHILD_CARE, "Family & Education"),
            category_row(ft.Icons.HEALTH_AND_SAFETY, "Health"),
            category_row(ft.Icons.DIRECTIONS_BOAT, "Travel"),
            category_row(ft.Icons.MUSIC_NOTE, "Music"),
            category_row(ft.Icons.THEATER_COMEDY, "Performing Arts"),
            category_row(ft.Icons.STYLE, "Fashion"),
            category_row(ft.Icons.MOVIE, "Film & Media"),
            category_row(ft.Icons.COLOR_LENS, "Hobbies"),
            category_row(ft.Icons.HOME, "Home & Lifestyle"),
            category_row(ft.Icons.GROUP, "Community"),
            category_row(ft.Icons.VOLUNTEER_ACTIVISM, "Charity & Causes"),
            category_row(ft.Icons.ACCOUNT_BALANCE, "Government"),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START
    )

    side_taskbar = ft.Container(
        content=category_buttons,
        width=245,
        bgcolor="#1d572c",
        alignment=ft.alignment.top_left,
        padding=20,
        margin=ft.margin.only(top=100)
    )

    # ----------------- Main Content -----------------
    results_list = ft.ListView(expand=True, spacing=10)

    status_header = ft.Row([
        ft.Icon(ft.icons.VOLUNTEER_ACTIVISM, color="white", size=30),
        ft.Text("Volunteer Dashboard", size=28, weight=ft.FontWeight.BOLD, color="white")
    ], spacing=15)

    main_content = ft.Container(
        content=ft.Column([
            status_header,
            ft.Divider(color="white"),
            results_list
        ], spacing=25),
        margin=ft.margin.only(left=270, top=120, right=40),
        expand=True
    )

    # ----------------- Assemble Page -----------------
    page.add(
        ft.Stack([
            main_content,
            taskbar,
            side_taskbar,
        ], expand=True)
    )
    page.update()

    # Load events immediately at startup
    threading.Thread(target=load_events, daemon=True).start()
