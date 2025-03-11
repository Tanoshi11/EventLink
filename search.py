import flet as ft
import httpx
import threading
import time
from datetime import datetime
from header import load_header  # Import the header

def clear_overlay(page: ft.Page):
    """Clear the overlay (e.g., join event form) from the page."""
    if page.overlay:
        page.overlay.clear()
        page.update()


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

def load_search(page, query, search_type="global", location=None):
    clear_overlay(page)  # Clear the overlay before loading the search page
    # Initialize page.data as a dictionary
    if page.data is None:
        page.data = {}

    # Store the search context in page.data
    page.data["query"] = query
    page.data["search_type"] = search_type
    page.data["location"] = location

    # Update the heading text based on the search type and location
    if search_type == "category":
        heading_text = f"Category: {query}"
    elif location:
        heading_text = f"Search Results: {query} ; Region: {location}"
    else:
        heading_text = f"Search Results: {query}"

    page.title = heading_text
    page.bgcolor = "#d6aa54"

    # Create a persistent search result heading
    results_title = ft.Text(
        heading_text,
        size=30,
        weight=ft.FontWeight.BOLD,
        color="#faf9f7"
    )

    # Divider for styling
    heading_divider = ft.Divider(color="white", thickness=1)

    # Keep the search results visible
    results_list = ft.ListView(expand=True, spacing=10)
    results_list.controls.append(ft.Text("Loading Results...", size=20, color="white"))

    # ------------------------------------------------------------------
    # 1) TASKBAR (HEADER) - Load from header.py
    # ------------------------------------------------------------------
    taskbar = load_header(page)  # Load the header

    # ------------------------------------------------------------------
    # 2) SIDEBAR (Categories)
    # ------------------------------------------------------------------

    def handle_category_click(e, category_label: str):
        """Handle category search."""
        load_search(page, query=category_label, search_type="category")

    def category_row(icon_name: str, label: str):
        """Create a clickable category row."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=20),
                    ft.Text(label, color="white", size=16),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.all(5),
            on_click=lambda e: handle_category_click(e, label),
            ink=True,
            border_radius=ft.border_radius.all(5),
        )

    category_buttons = ft.Column(
        controls=[
            ft.Text("Filters", color="white", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Category", color="white", size=16, weight=ft.FontWeight.W_600),
            category_row(ft.Icons.BRUSH, "Arts"),
            category_row(ft.Icons.BUSINESS_CENTER, "Business"),
            category_row(ft.Icons.FAVORITE, "Charity"),
            category_row(ft.Icons.LOCAL_LIBRARY, "Community"),
            category_row(ft.Icons.SCHOOL, "Education"),
            category_row(ft.Icons.THEATER_COMEDY, "Entertainment"),
            category_row(ft.Icons.ECO, "Environment"),
            category_row(ft.Icons.RESTAURANT, "Food"),
            category_row(ft.Icons.GAMES, "Gaming"),
            category_row(ft.Icons.HEALTH_AND_SAFETY, "Health"),
            category_row(ft.Icons.MUSIC_NOTE, "Music"),
            category_row(ft.Icons.GAVEL, "Politics"),
            category_row(ft.Icons.SPORTS_SOCCER, "Sports"),
            category_row(ft.Icons.DEVICES, "Technology"),
            category_row(ft.Icons.FLIGHT, "Travel"),
        ],
        spacing=12,
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

    # ------------------------------------------------------------------
    # 3) MAIN CONTENT: SEARCH RESULTS
    # ------------------------------------------------------------------

    def fetch_events():
        try:
            query = page.data.get("query", "All")
            search_type = page.data.get("search_type", "global")
            location = page.data.get("location")

            # Debugging: Print the current search context
            print(f"Fetching events - Query: '{query}', Type: '{search_type}', Region: '{location}'")

            # Build the URL
            if search_type == "category":
                url = f"http://localhost:8000/search_events_by_category?category={query}"
            else:
                if location:
                    url = f"http://localhost:8000/search_events?query={query}&region={location}"
                else:
                    url = f"http://localhost:8000/search_events?query={query}"

            print(f"Calling backend URL: {url}")
            resp = httpx.get(url)
            
            if resp.status_code == 200:
                events = resp.json().get("events", [])
                print(f"Received {len(events)} events.")
                print("Events data:", events)  # Debugging: Print the events data
                return events
            else:
                print(f"Backend error: {resp.status_code}")
                print(f"Backend response: {resp.text}")  # Print the backend response for debugging
                return []
        except Exception as ex:
            print(f"Error in fetch_events: {ex}")
            return []

    def get_event_status(event_date, time_range):
        """Determine the status of the event based on the current date and time."""
        try:
            #--------2

            if isinstance(time_range, list):
                time_range = time_range[0]

            if " - " in time_range:
                start_time_str, end_time_str = [s.strip() for s in time_range.split(" - ", 1)]
            else:
            
                start_time_str = time_range
                end_time_str = time_range

            start_dt_str = f"{event_date} {start_time_str}"
            end_dt_str   = f"{event_date} {end_time_str}"

            start_dt = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M")
            end_dt   = datetime.strptime(end_dt_str, "%Y-%m-%d %H:%M")

            now = datetime.now()




            #----------
            if now < start_dt:
                return "Upcoming"
            elif start_dt <= now <= end_dt:
                return "Ongoing"
            else:
                return "Closed"
        
        except Exception as ex:
            print(f"Error in get_event_status: {ex}")
            return "Unknown"

            #start_time = event_time.split(" - ")[0] if " - " in event_time else event_time
            #event_datetime_str = f"{event_date} {start_time}"
            #event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
           # current_datetime = datetime.now()
            
    

    def load_events():
        time.sleep(0.2)  # Optional delay
        events = fetch_events()

        # Debugging: Print the number of events fetched
        print(f"Number of events fetched: {len(events)}")

        # Clear existing results
        results_list.controls.clear()

        if events:
            for ev in events:
                # Debugging: Print each event's data
                print("Event data:", ev)

                #----------


                time_value = ev["time"]
                if " - " in time_value:
                    start_time = time_value.split(" - ",1)
                else:
                    start_time = time_value
                    

                #time_range = (f"{start_time} - {end_time}") if start_time and end_time else (start_time or end_time)

                #--------


                event_status = get_event_status(ev.get("date", ""), ev.get("time", ""))
                status_color = {
                    "Upcoming": "#4CAF50",
                    "Ongoing": "#FFEB3B",
                    "Closed": "#FF5252"
                }.get(event_status, "white")

                event_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(ev.get("name", "Unnamed Event"), size=22, color="white", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Status: {event_status}", color=status_color, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Date: {ev.get('date', '')}", color="white"),
                            ft.Text(f"Time: {ev.get('time', '')}", color="white"),
                            #------
                            ft.Text(f"Region: {ev.get('location', '')}", color="white"),
                            #-------
                            ft.Text(f"Category: {ev.get('type', 'Unknown')}", color="white"),  # Use 'type' instead of 'category'
                        ],
                        spacing=5
                    ),
                    padding=10,
                    border_radius=10,
                    bgcolor="#105743",
                    ink=True,
                    on_click=lambda e, ev=ev: load_event_details(page, ev)  # Make the container clickable
                )
                results_list.controls.append(event_container)

                # Add a divider between events
                results_list.controls.append(ft.Divider(color="white"))
        else:
            results_list.controls.append(ft.Text("No events found.", size=20, color="white"))

        # Force UI update
        page.update()
        print("UI updated with new results!")

    # ------------------------------------------------------------------
    # 4) STACK LAYOUT
    # ------------------------------------------------------------------
    main_stack = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[results_title, heading_divider, results_list],
                    spacing=20,
                    expand=True
                ),
                margin=ft.margin.only(left=270, top=120, right=40),
                expand=True
            ),
            taskbar,  # Header loaded from header.py
            side_taskbar,  # Sidebar with categories
        ],
        expand=True
    )

    page.controls.clear()
    page.add(main_stack)
    page.update()

    # Call load_events() in a separate thread to avoid blocking the UI
    threading.Thread(target=load_events, daemon=True).start()

# For quick testing: flet run search.py
if __name__ == "__main__":
    ft.app(target=lambda page: load_search(page, query="All", search_type="global", location="New York"))