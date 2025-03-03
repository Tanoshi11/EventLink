import flet as ft
from flet import (
    Row,
    Column,
    Container,
    Text,
    ListView,
    ScrollMode,
    padding,
    margin,
    border_radius,
    ElevatedButton,
)
import httpx
from header import load_header  # Import the header
from search import load_search

# Global variable to store the notification popup overlay
notif_popup = None
events_text = ft.Text("", color="white")

def load_event_details(page, event):
    """Load event details when an event container is clicked."""
    import event_details
    # Pass the search context (query, search_type, location) to the event details page
    search_context = {
        "query": page.data.get("query", "All"),
        "search_type": page.data.get("search_type", "global"),
        "location": page.data.get("location", None)
    }
    event_details.load_event_details(page, event, search_context)

def join_event(page, event_data):
    """Handle the join button click by opening join_event_form.py."""
    # Extract necessary data from the event
    event_id = event_data.get("id", None)
    title = event_data.get("name", "Untitled Event")
    date = event_data.get("date", "No date provided")
    time = event_data.get("time", "No time provided")
    
    # Import and call the join event form loader from join_event_form.py
    import join_event_form
    join_event_form.load_join_event_form(page, event_id, title, date, time, back_callback=load_bookevent)

def fetch_events(page):
    """
    Fetch events from FastAPI. 
    If query == "All" and no location is set, call /display_events.
    Otherwise, call your existing search endpoints.
    """
    try:
        query = page.data.get("query", "All")
        search_type = page.data.get("search_type", "global")
        location = page.data.get("location")

        # Debugging: Print the current search context
        print(f"Fetching events - Query: '{query}', Type: '{search_type}', Location: '{location}'")

        # 1) If user wants ALL events (and no specific location), call /display_events
        if query.lower() == "all" and not location:
            url = "http://localhost:8000/display_events"
        
        # 2) Otherwise, continue using your existing search endpoints
        else:
            if search_type == "category":
                url = f"http://localhost:8000/search_events_by_category?category={query}"
            else:
                # If location is provided, search by location
                if location:
                    url = f"http://localhost:8000/search_events?query={query}&region={location}"
                else:
                    url = f"http://localhost:8000/search_events?query={query}"

        print(f"Calling backend URL: {url}")
        resp = httpx.get(url)

        if resp.status_code == 200:
            events = resp.json().get("events", [])
            print(f"Received {len(events)} events.")
            print("Events data:", events)  # Debugging
            return events
        else:
            print(f"Backend error: {resp.status_code}")
            print(f"Backend response: {resp.text}")
            return []
    except Exception as ex:
        print(f"Error in fetch_events: {ex}")
        return []

def main(page: ft.Page):
    if page.data is None:
        page.data = {}
    page.title = "Register for an Event"
    page.bgcolor = "#d6aa54"
    page.padding = 0  # No extra padding at the edges

    # ----------------- Header (Taskbar) -----------------
    taskbar = load_header(page)  # Load the header from header.py

    # ----------------- Sidebar: Category Icons -----------------
    def handle_category_click(e, category_label: str):
        load_search(page, query=category_label, search_type="category")
        print(f"{category_label} quick search triggered!")

    def category_row(icon_name: str, label: str):
        return Container(
            content=Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=20),
                    Text(label, color="white", size=16),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=padding.all(5),
            on_click=lambda e: handle_category_click(e, label),
            ink=True,  # adds a ripple effect when clicked
            border_radius=border_radius.all(5),
        )

    filters_text = Text("Filters", color="white", size=20, weight=ft.FontWeight.BOLD)
    category_text = Text("Category", color="white", size=16, weight=ft.FontWeight.W_600)

    category_buttons = Column(
        controls=[
            filters_text,
            category_text,
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
        alignment=ft.MainAxisAlignment.START,
    )

    side_taskbar = Container(
        content=Container(
            content=category_buttons,
            width=245,
            bgcolor="#1d572c",
            alignment=ft.alignment.top_left,
            padding=20
        ),
        alignment=ft.alignment.top_left,
    )

    # ----------------- Main Events Container (Scrollable) -----------------
    def build_event_container(event_data):
        title = event_data.get("name", "Untitled Event")
        date = event_data.get("date", "No date provided")
        time = event_data.get("time", "No time provided")
        description = event_data.get("description", "No description provided")
        
        # Create a container for the event details and a join button.
        return Container(
            content=Column(
                controls=[
                    Text(title, size=20, weight=ft.FontWeight.BOLD, color="black"),
                    Text(date, size=16, color="black"),
                    Text(time, size=16, color="black"),
                    Text(description, size=16, color="black"),
                    # Join button for each event container.
                    ElevatedButton(
                        "Join",
                        on_click=lambda e: join_event(page, event_data)
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            bgcolor="white",
            border_radius=border_radius.all(8),
            margin=margin.only(bottom=10),
            on_click=lambda e: load_event_details(page, event_data),
        )

    # Fetch events (this will call either /display_events or /search_events, etc.)
    http_events = fetch_events(page)

    events_list = ListView(
        controls=[build_event_container(e) for e in http_events],
        spacing=10,
        padding=10,
        expand=True,  # Expands to fill available space
    )

    events_container = Column(
        controls=[
            Container(
                content=Text(
                    "Events 🎉",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#faf9f7",
                    text_align=ft.TextAlign.CENTER
                ),
                padding=20,
            ),
            events_list,
        ],
        expand=True,
        scroll=ScrollMode.ALWAYS,
    )

    main_content = ft.Row(
        controls=[
            side_taskbar,
            events_container,
        ],
        spacing=20,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
    )

    page.controls.clear()
    page.add(
        Column(
            controls=[
                taskbar,
                main_content,
            ],
            expand=True,
        )
    )
    page.add(events_text)  # Display any notification text if needed
    page.update()

def load_homepage(page):
    page.controls.clear()
    main(page)

def load_login(page):
    page.floating_action_button = None
    pass

def load_my_events(page):
    import my_events
    page.controls.clear()
    my_events.load_my_events(page)
    page.update()

def load_create_event(page):
    import CreateEvents
    page.controls.clear()
    CreateEvents.load_create_event(page)
    page.update()

def load_profile(page):
    page.floating_action_button = None
    pass


def load_bookevent(page):
    """Reload the events page."""
    page.controls.clear()
    main(page)

if __name__ == "__main__":
    ft.app(target=main)
