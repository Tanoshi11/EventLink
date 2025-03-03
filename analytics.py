import flet as ft
import pymongo
import matplotlib.pyplot as plt
import io
import base64
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
BACKGROUND_COLOR = SECONDARY_COLOR  # Dark green background
CHART_BG_COLOR = "#f7f5ed"  # Soft background for charts

# MongoDB Connection
MONGO_URI = "mongodb+srv://samanthaangelacrn:eventlink@eventlink.1hfcs.mongodb.net/?retryWrites=true&w=majority&appName=EventLink"
client = pymongo.MongoClient(MONGO_URI)
db = client["EventLink"]
collection = db["events"]

def fetch_available_years():
    """Fetch distinct years available in the database."""
    years = collection.distinct("date")
    years = sorted(set(date[:4] for date in years if len(date) >= 4), reverse=True)
    return years

def fetch_event_data(selected_year):
    """Fetch events and participants per month for the given year."""
    pipeline = [
        {"$addFields": {
            "event_year": {"$substr": ["$date", 0, 4]},  # Extract YYYY
            "event_month": {"$substr": ["$date", 5, 2]}  # Extract MM
        }},
        {"$match": {"event_year": str(selected_year)}},  # Filter by selected year
        {"$group": {
            "_id": "$event_month",  # Group by MM (01–12)
            "total_participants": {"$sum": "$participants"},
            "total_events": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}  # Sort by month
    ]

    data = list(collection.aggregate(pipeline))
    months = [item["_id"] for item in data]  # Only MM
    participants = [item["total_participants"] for item in data]
    events = [item["total_events"] for item in data]

    return months, participants, events

def create_chart(months, data, title):
    """Generate a Matplotlib line chart with months formatted as 01-12."""
    fig, ax = plt.subplots()
    ax.plot(months, data, marker="o", linestyle="-", color=ACCENT_COLOR, label=title)

    ax.set_xticks(range(1, 13))  # Set x-axis ticks for 01-12
    ax.set_xticklabels([f"{i:02}" for i in range(1, 13)])  # Ensure labels show only numbers

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

    available_years = fetch_available_years()
    selected_year = available_years[0] if available_years else str(datetime.now().year)

    # Dropdown to select year
    year_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(year) for year in available_years],
        value=selected_year,
        on_change=lambda e: update_graphs(e.control.value, page),
    )

    def update_graphs(year, page):
        """Update graphs when a new year is selected."""
        months, participants, events = fetch_event_data(year)

        # Generate new charts
        participants_chart = create_chart(months, participants, "Monthly Event Participation")
        events_chart = create_chart(months, events, "Monthly Events Creation")

        # Convert images for Flet display
        participants_img.src_base64 = participants_chart
        events_img.src_base64 = events_chart

        page.update()

    # Fetch initial data
    months, participants, events = fetch_event_data(selected_year)

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
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=SECONDARY_COLOR, icon_size=24, on_click=lambda e: load_my_events(e)),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=WHITE,
        padding=15,  
        border_radius=30
    )

    spacing = ft.Container(height=20)  # Adds space between header and graphs

    # Year selection dropdown
    year_selection = ft.Container(
        content=ft.Row(
            [
                ft.Text("Select Year:", size=18, weight="bold", color=WHITE),
                year_dropdown
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=10
    )

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
    page.add(year_selection)
    page.add(graph_section)

ft.app(target=main)
