import flet as ft
from header import load_header
from datetime import datetime
import pymongo

# Define Colors
BACKGROUND_COLOR = "#c69c5d"
DARK_RED = "#d9534f"
GREEN = "#5cb85c"
MUSTARD_YELLOW = "#f0ad4e"
WHITE = "#ffffff"
DARK_TEXT = "#333333"

# MongoDB Connection
MONGO_URI = "mongodb+srv://samanthaangelacrn:eventlink@eventlink.1hfcs.mongodb.net/?retryWrites=true&w=majority&appName=EventLink"
client = pymongo.MongoClient(MONGO_URI)
db = client["EventLink"]
collection = db["events"]

def fetch_events():
    """Fetch events from MongoDB."""
    try:
        events = list(collection.find({}, {"_id": 0, "name": 1, "date": 1}))
        return events
    except Exception as ex:
        print("Error fetching events:", ex)
        return []

def load_my_events(page: ft.Page):
    """Load the My Events page."""
    page.title = "My Events"
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0  

    events = fetch_events()
    current_date = datetime.now().date()

    past_events, current_events, upcoming_events = [], [], []
    for event in events:
        try:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            event_text = ft.Text(event['name'], size=16, color=WHITE, weight=ft.FontWeight.BOLD)

            if event_date < current_date:
                past_events.append(event_text)
            elif event_date == current_date:
                current_events.append(event_text)
            else:
                upcoming_events.append(event_text)
        except Exception as e:
            print(f"Error parsing event date: {e}")

    taskbar = load_header(page)  # Load the header

    my_events_header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.EVENT, color=WHITE, size=30),
            ft.Text("My Events", size=28, weight=ft.FontWeight.BOLD, color=WHITE)
        ], spacing=15, alignment=ft.MainAxisAlignment.START),
        margin=ft.margin.only(left=30, top=20)
    )

    divider_line = ft.Divider(color=WHITE, thickness=2)

    def event_section(title, events, bg_color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color=WHITE, text_align=ft.TextAlign.CENTER),
                ft.Column(events if events else [ft.Text("No events", color=WHITE, text_align=ft.TextAlign.CENTER)],
                          alignment=ft.MainAxisAlignment.CENTER, expand=True),
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, expand=True),
            bgcolor=bg_color,
            border_radius=15,
            padding=20,
            expand=True
        )

    events_container = ft.Row([
        event_section("Past Events", past_events, DARK_RED),
        event_section("Current Events", current_events, GREEN),
        event_section("Upcoming Events", upcoming_events, MUSTARD_YELLOW),
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER, expand=True)

    content_container = ft.Container(
        content=events_container,
        bgcolor=WHITE,
        border_radius=15,
        padding=30,
        width=950,
        height=500,
        alignment=ft.alignment.center,
        margin=ft.margin.only(left=30, top=20)
    )

    stats_buttons = ft.Column([
        ft.ElevatedButton(
            "Event Stats", 
            on_click=lambda e: go_event_stats(page), 
            bgcolor=WHITE, 
            color=DARK_TEXT,
            width=220,
            height=60,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        ft.ElevatedButton(
            "Volunteer Stats", 
            on_click=lambda e: go_volunteer_stats(page), 
            bgcolor=WHITE, 
            color=DARK_TEXT,
            width=220,
            height=60,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
    ], spacing=10, alignment=ft.MainAxisAlignment.START)

    page.add(
        taskbar,
        my_events_header,
        divider_line,
        ft.Row([
            content_container,
            stats_buttons
        ], alignment=ft.MainAxisAlignment.START, spacing=10)
    )
    page.update()

def go_home(page):
    import header
    page.controls.clear()
    header.main(page)
    page.update()

def go_event_stats(page):
    import event_stats
    page.controls.clear()
    event_stats.main(page)
    page.update()

def go_volunteer_stats(page):
    import volunteer_stats
    page.controls.clear()
    volunteer_stats.main(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=load_my_events)
