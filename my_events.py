import flet as ft
from datetime import datetime
import pymongo
from controller.sidebar_controller import SidebarController

# Define Colors
BACKGROUND_COLOR = "#d6aa54"
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

def load_my_events(page: ft.Page):
    """Load the My Events page with hardcoded event data."""
    page.title = "My Events"
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0  

    # Load Sidebar
    if "sidebar" not in page.data:
        sidebar_controller = SidebarController(page)
        sidebar = sidebar_controller.build()
        page.data["sidebar"] = sidebar
    else:
        sidebar = page.data["sidebar"]

    # Hardcoded Events
    joined_events = [
        "Podfest Asia 2025 (April 1)",
        "Iron Fist Tournament (March 29)",
        "200 Cities Project: Fighting Loneliness (March 20)"
    ]
    volunteered_events = [
        "LUNCH & LEARN: #makersmeetup - [Davao City] (March 29)",
        "The Corp Comm Crash Course (March 22)",
        "Sales Workshop: Creating Effective Sales Presentations (March 29)"
    ]
    created_events = [
        "Fortifying Data with AI: A New Era for the Philippines’ Security (April 11)",
        "Basic PowerBI (April 1)",
        "Negotiation Skills Workshop (April 1)"
    ]
    
    def event_section(title, events, bg_color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color=WHITE, text_align=ft.TextAlign.CENTER),
                ft.Column([ft.Text(event, size=16, color=WHITE, weight=ft.FontWeight.BOLD) for event in events],
                          alignment=ft.MainAxisAlignment.CENTER, expand=True),
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, expand=True),
            bgcolor=bg_color,
            border_radius=15,
            padding=20,
            expand=True
        )

    events_container = ft.Row([
        event_section("Joined Events", joined_events, MUSTARD_YELLOW),
        event_section("Volunteered Events", volunteered_events, MUSTARD_YELLOW),
        event_section("My Created Events", created_events, MUSTARD_YELLOW),
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER, expand=True)

    my_events_header = ft.Row(
        [
            ft.Icon(name=ft.icons.CALENDAR_MONTH, color=WHITE, size=30),
            ft.Text("My Events", size=30, weight=ft.FontWeight.BOLD, color="#faf9f7"),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    divider_line = ft.Divider(color="white", thickness=1)

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

    main_content = ft.Container(
        content=ft.Column([
            my_events_header,
            divider_line,
            ft.Row([
                content_container,
                stats_buttons
            ], alignment=ft.MainAxisAlignment.START, spacing=10)
        ], spacing=15, expand=True),
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
