import flet as ft
import pymongo
from datetime import datetime, timedelta

# Define theme colors
PRIMARY_COLOR = "#6d9773"
SECONDARY_COLOR = "#0c3b2e"
ACCENT_COLOR = "#b46617"
HIGHLIGHT_COLOR = "#ffba00"
WHITE = "#ffffff"
DARK_RED = "#8B0000"
MUSTARD_YELLOW = "#B8860B"
GREEN = "#008000"

# MongoDB Connection
MONGO_URI = "mongodb+srv://samanthaangelacrn:eventlink@eventlink.1hfcs.mongodb.net/?retryWrites=true&w=majority&appName=EventLink"
client = pymongo.MongoClient(MONGO_URI)
db = client["EventLink"]
collection = db["events"]

def fetch_events():
    """Fetch events from MongoDB and return them as a list of dictionaries."""
    try:
        events = list(collection.find({}, {"_id": 0, "name": 1, "date": 1}))
        return events
    except Exception as ex:
        print("Error fetching events:", ex)
        return []

def load_my_events(page: ft.Page):
    """Load the My Events page with categorized event listings."""
    page.title = "My Events"
    page.bgcolor = SECONDARY_COLOR
    page.padding = 20

    events = fetch_events()
    current_date = datetime.now().date()

    three_months_ago = current_date - timedelta(days=90)
    three_months_later = current_date + timedelta(days=90)

    past_events, current_events, upcoming_events = [], [], []

    for event in events:
        try:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            event_text = ft.Text(event['name'], size=16, color=WHITE, weight=ft.FontWeight.BOLD)

            if event_date < three_months_ago:
                past_events.append(event_text)
            elif three_months_ago <= event_date <= three_months_later:
                current_events.append(event_text)
            else:
                upcoming_events.append(event_text)
        except Exception as e:
            print(f"Error parsing event date: {e}")

    header = ft.Container(
        content=ft.Row([
            ft.Text("My Events", size=30, weight=ft.FontWeight.BOLD, color=SECONDARY_COLOR, expand=True),
            ft.IconButton(icon=ft.icons.HOME, icon_color=SECONDARY_COLOR, icon_size=30, 
                          on_click=lambda e: go_back(e, page)),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=WHITE,
        padding=20,
        border_radius=30,
    )

    def go_back(e, page):
        import homepg
        page.controls.clear()
        homepg.main(page)
        page.update()
    
    def event_section(title, events, bg_color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=WHITE),
                ft.Column(events if events else [ft.Text("No events", color=WHITE)]),
            ], spacing=10),
            bgcolor=bg_color,
            border_radius=15,
            padding=15,
            expand=True,
        )

    event_container = ft.Container(
        content=ft.Column([
            ft.Row([
                event_section("Current Events", current_events, GREEN),
            ], spacing=10, expand=True),
            ft.Row([
                event_section("Upcoming Events", upcoming_events, MUSTARD_YELLOW),
                event_section("Past Events", past_events, DARK_RED),
            ], spacing=10, expand=True)
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=WHITE,
        border_radius=15,
        padding=15,
        width=600,
        height=400,
    )

    def go_stats(e, page):
        import analytics
        page.controls.clear()
        analytics.main(page)
        page.update()

    stats_button = ft.Container(
        content=ft.Text("Event Stats", size=18, weight=ft.FontWeight.BOLD, color=SECONDARY_COLOR),
        bgcolor=WHITE,
        padding=15,
        border_radius=30,
        alignment=ft.alignment.center,
        width=200,
        on_click=lambda e: go_stats(e, page),
    )

    calendar = ft.Container(
        content=ft.Text("📅 Calendar (Placeholder)", size=18, weight=ft.FontWeight.BOLD, color="black"),
        bgcolor=WHITE,
        padding=15,
        border_radius=15,
        width=350  
    )

    volunteer_button = ft.Container(
        content=ft.Text("Volunteer Analytics", size=18, weight=ft.FontWeight.BOLD, color="black"),
        bgcolor=WHITE,
        padding=15,
        border_radius=30,
        alignment=ft.alignment.center,
        width=350  
    )

    centered_layout = ft.Column([
        event_container,
        stats_button
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(
        header,
        ft.Container(
            content=ft.Row([centered_layout, ft.Column([calendar, volunteer_button], spacing=15, expand=True)], spacing=15, expand=True),
            alignment=ft.alignment.center,
            expand=True,
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=load_my_events)