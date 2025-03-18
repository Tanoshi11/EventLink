import flet as ft
import pymongo
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from controller.sidebar_controller import SidebarController
from header import load_header  # Import the header function

# Define theme colors
BACKGROUND_COLOR = "#c69c5d"
DARK_RED = "#d9534f"
GREEN = "#5cb85c"
MUSTARD_YELLOW = "#f0ad4e"
WHITE = "#ffffff"
DARK_TEXT = "#333333"
CHART_BG_COLOR = "#f7f5ed"

# MongoDB Connection
MONGO_URI = "mongodb+srv://samanthaangelacrn:eventlink@eventlink.1hfcs.mongodb.net/?retryWrites=true&w=majority&appName=EventLink"
client = pymongo.MongoClient(MONGO_URI)
db = client["EventLink"]
collection = db["events"]

def fetch_available_years():
    years = collection.distinct("date")
    years = sorted(set(date[:4] for date in years if len(date) >= 4), reverse=True)
    return years

def fetch_event_data(selected_year):
    pipeline = [
        {"$addFields": {
            "event_year": {"$substr": ["$date", 0, 4]},
            "event_month": {"$substr": ["$date", 5, 2]}
        }},
        {"$match": {"event_year": str(selected_year)}},
        {"$group": {
            "_id": "$event_month",
            "total_participants": {"$sum": "$participants"},
            "total_events": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    data = list(collection.aggregate(pipeline))
    months = [item["_id"] for item in data]
    participants = [item["total_participants"] for item in data]
    events = [item["total_events"] for item in data]
    return months, participants, events

def main(page: ft.Page):
    page.title = "Event Stats"
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0

    # Load Sidebar
    if "sidebar" not in page.data:
        sidebar_controller = SidebarController(page)
        sidebar = sidebar_controller.build()
        page.data["sidebar"] = sidebar
    else:
        sidebar = page.data["sidebar"]

    taskbar = load_header(page)  # Load the header

    event_stats_header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.INSIGHTS, color=WHITE, size=30),
            ft.Text("Event Stats", size=28, weight=ft.FontWeight.BOLD, color=WHITE)
        ], spacing=15, alignment=ft.MainAxisAlignment.START),
        margin=ft.margin.only(left=30, top=40)
    )

    divider_line = ft.Divider(color=WHITE, thickness=2)

    available_years = fetch_available_years()
    selected_year = available_years[0] if available_years else str(datetime.now().year)

    months, participants, events = fetch_event_data(selected_year)
    participants_chart = create_chart(months, participants, "Monthly Event Participation")
    events_chart = create_chart(months, events, "Monthly Events Creation")

    participants_img = ft.Image(src_base64=participants_chart, width=400, height=300)
    events_img = ft.Image(src_base64=events_chart, width=400, height=300)

    graph_section = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("Monthly Event Participation", size=20, weight="bold", color=DARK_TEXT, text_align=ft.TextAlign.CENTER),
                participants_img
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=CHART_BG_COLOR,
            padding=20,
            border_radius=15,
            alignment=ft.alignment.center
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Monthly Events Creation", size=20, weight="bold", color=DARK_TEXT, text_align=ft.TextAlign.CENTER),
                events_img
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=CHART_BG_COLOR,
            padding=20,
            border_radius=15,
            alignment=ft.alignment.center
        )
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

    stats_button = ft.Container(
        content=ft.ElevatedButton(
            "Back", 
            on_click=lambda e: go_my_events(page), 
            bgcolor=WHITE, 
            color=DARK_TEXT,
            width=220,
            height=60,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=20)
    )

    main_content = ft.Container(
        content=ft.Column([
            event_stats_header,
            divider_line,
            graph_section,
            stats_button
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        margin=ft.margin.only(left=270, top=30, right=40),
        expand=True
    )

    layout = ft.Stack(
        controls=[taskbar, sidebar, main_content],
        expand=True
    )

    page.controls.clear()
    page.add(layout)
    page.update()

def go_my_events(page):
    import my_events
    page.controls.clear()
    my_events.load_my_events(page)
    page.update()

def create_chart(months, data, title):
    fig, ax = plt.subplots()
    ax.plot(months, data, marker="o", linestyle="-", color=DARK_RED, label=title)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([f"{i:02}" for i in range(1, 13)])
    ax.set_xlabel("Month")
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.grid(True)
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight", facecolor=CHART_BG_COLOR)
    img_buffer.seek(0)
    return base64.b64encode(img_buffer.getvalue()).decode("utf-8")

if __name__ == "__main__":
    ft.app(target=main)
