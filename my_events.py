import flet as ft
import httpx
from datetime import datetime

# Define theme colors
PRIMARY_COLOR = "#6d9773"       # Accent green
SECONDARY_COLOR = "#0c3b2e"     # Dark green (used for headers/forms)
ACCENT_COLOR = "#b46617"        # Warm accent (for text or titles)
HIGHLIGHT_COLOR = "#ffba00"     # Highlight yellow
WHITE = "#ffffff"
DARK_RED = "#8B0000"
MUSTARD_YELLOW = "#B8860B"
GREEN = "#008000"

def load_my_events(page: ft.Page):
    
    page.title = "My Events"
    page.bgcolor = SECONDARY_COLOR
    page.padding = 20

    # Fetch events from API
    def fetch_events():
        try:
            response = httpx.get("http://127.0.0.1:8000/my_events")
            response.raise_for_status()
            return response.json()
        except Exception as ex:
            print("Error fetching events:", ex)
            return []

    events = fetch_events()
    current_date = datetime.now().date()

    past_events, current_events, upcoming_events = [], [], []

    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        event_text = ft.Text(event['title'], size=16, color=WHITE, weight=ft.FontWeight.BOLD)

        if event_date < current_date:
            past_events.append(event_text)
        elif event_date == current_date:
            current_events.append(event_text)
        else:
            upcoming_events.append(event_text)

    # Header 
    header = ft.Container(
        content=ft.Row([
            ft.Text("My Events", size=30, weight=ft.FontWeight.BOLD, color=SECONDARY_COLOR, expand=True),
            ft.IconButton(icon=ft.icons.HOME, icon_color=SECONDARY_COLOR, icon_size=30, on_click=lambda e: go_back(e, page),),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=WHITE,
        padding=20,
        border_radius=30
    )

    def go_back(e, page):
        import homepg
        page.controls.clear()
        homepg.main(page)
        page.update()
    
    # Event Card Function 
    def event_section(title, events, bg_color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=WHITE),
                ft.Column(events if events else [ft.Text("No events", color=WHITE)]),
            ], spacing=10),
            bgcolor=bg_color,
            border_radius=15,
            padding=15,
            expand=True
        )

    # Event Sections
    event_container = ft.Container(
        content=ft.Column([
            ft.Row([  
                event_section("Current Events", current_events, GREEN),
            ], spacing=10, expand=True),
            ft.Row([
                event_section("Upcoming Events", upcoming_events, MUSTARD_YELLOW),
                event_section("Past Events", past_events, DARK_RED),
            ], spacing=10, expand=True)
        ], spacing=10),
        bgcolor=WHITE,
        border_radius=15,
        padding=15,
        expand=True
    )

    CONTAINER_WIDTH = 350  

# Calendar Section
    calendar = ft.Container(
        content=ft.Text("📅 Calendar (Placeholder)", size=18, weight=ft.FontWeight.BOLD, color="black"),
        bgcolor=WHITE,
        padding=15,
        border_radius=15,
        width=CONTAINER_WIDTH  
    )

# Volunteer Analytics Button
    volunteer_button = ft.Container(
        content=ft.Text("Volunteer Analytics", size=18, weight=ft.FontWeight.BOLD, color="black"),
        bgcolor=WHITE,
        padding=15,
        border_radius=30,
        alignment=ft.alignment.center,
        width=CONTAINER_WIDTH  
    )

    # Layout
    page.add(
        header,
        ft.Row([event_container, ft.Column([calendar, volunteer_button], spacing=15, expand=True)], spacing=15, expand=True)
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=load_my_events)
