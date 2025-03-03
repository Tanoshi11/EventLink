import flet as ft
import pymongo
import matplotlib.pyplot as plt
import io
import base64

# Define theme colors
PRIMARY_COLOR = "#6d9773"       # Accent green
SECONDARY_COLOR = "#0c3b2e"     # Dark green (used for headers/forms)
ACCENT_COLOR = "#b46617"        # Warm accent (for text or titles)
HIGHLIGHT_COLOR = "#ffba00"     # Highlight yellow
WHITE = "#ffffff"
DARK_RED = "#8B0000"
MUSTARD_YELLOW = "#B8860B"
GREEN = "#008000"
BACKGROUND_COLOR = SECONDARY_COLOR  # Dark green background
CHART_BG_COLOR = "#f7f5ed"  # Soft background for charts

# MongoDB Connection
MONGO_URI = "mongodb+srv://samanthaangelacrn:eventlink@eventlink.1hfcs.mongodb.net/?retryWrites=true&w=majority&appName=EventLink"
client = pymongo.MongoClient(MONGO_URI)
db = client["EventLink"]
collection = db["events"]

def fetch_event_data():
    """Fetch events and participants per month from MongoDB."""
    pipeline = [
        {"$group": {
            "_id": {"month": {"$substr": ["$date", 0, 7]}},  # Extract YYYY-MM
            "total_participants": {"$sum": "$participants"},
            "total_events": {"$sum": 1}
        }},
        {"$sort": {"_id.month": 1}}
    ]

    data = list(collection.aggregate(pipeline))
    months = [item["_id"]["month"] for item in data]
    participants = [item["total_participants"] for item in data]
    events = [item["total_events"] for item in data]

    return months, participants, events

def create_chart(months, data, title):
    """Generate a Matplotlib line chart and return as base64."""
    fig, ax = plt.subplots()
    ax.plot(months, data, marker="o", linestyle="-", color=ACCENT_COLOR, label=title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.grid(True)

    # Save chart to memory
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight", facecolor=CHART_BG_COLOR)
    img_buffer.seek(0)

    # Convert image to base64
    return base64.b64encode(img_buffer.getvalue()).decode("utf-8")

def main(page: ft.Page):
    page.bgcolor = BACKGROUND_COLOR
    page.title = "Event Analytics"

    # Fetch event data
    months, participants, events = fetch_event_data()

    # Generate charts
    participants_chart = create_chart(months, participants, "Monthly Event Participation")
    events_chart = create_chart(months, events, "Monthly Events Creation")

    # Convert images for Flet display
    participants_img = ft.Image(src_base64=participants_chart, width=400, height=300)
    events_img = ft.Image(src_base64=events_chart, width=400, height=300)

    def load_my_events(e):
        import my_events
        page.controls.clear()
        my_events.load_my_events(page)  # Navigate back to my_events.py
        page.update()

    # Header 
    header = ft.Container(
        content=ft.Row([
            ft.Text("Event Stats", size=24, weight=ft.FontWeight.BOLD, color=SECONDARY_COLOR, expand=True),
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=SECONDARY_COLOR, icon_size=24, on_click=lambda e: load_my_events(e, page)),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=WHITE,
        padding=15,  
        border_radius=30
    )

    spacing = ft.Container(height=30)  # Adds space between header and graphs

    # Graph Section 
    graph_section = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Monthly Event Participation", size=20, weight="bold", color=SECONDARY_COLOR, text_align=ft.TextAlign.CENTER),
                        participants_img
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=CHART_BG_COLOR,
                    padding=20,
                    border_radius=15,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Monthly Events Creation", size=20, weight="bold", color=SECONDARY_COLOR, text_align=ft.TextAlign.CENTER),
                        events_img
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=CHART_BG_COLOR,
                    padding=20,
                    border_radius=15,
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center 
    )

    # Add components to the page
    page.add(header)
    page.add(spacing)  
    page.add(graph_section)

ft.app(target=main)
