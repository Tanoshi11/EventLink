import flet as ft 
import matplotlib.pyplot as plt
import io
import base64
import random
import pymongo
from datetime import datetime
from controller.sidebar_controller import SidebarController

# Define theme colors
BACKGROUND_COLOR = "#d6aa54"
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
    current_year = datetime.now().year
    years = [str(year) for year in range(current_year - 5, current_year + 1)]
    return sorted(years, reverse=True)

def fetch_event_data(selected_year):
    months = [f"{i:02}" for i in range(1, 13)]
    event_counts = [random.randint(5, 50) for _ in range(12)]
    return months, event_counts

def create_chart(months, data, title):
    fig, ax = plt.subplots()
    month_labels = [datetime(2000, int(m), 1).strftime('%b') for m in months]
    ax.bar(month_labels, data, color=DARK_RED)
    
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Events")
    ax.set_title(title)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight", facecolor=CHART_BG_COLOR)
    img_buffer.seek(0)
    return base64.b64encode(img_buffer.getvalue()).decode("utf-8")

def main(page: ft.Page):
    page.title = "Event Stats"
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0

    if "sidebar" not in page.data:
        sidebar_controller = SidebarController(page)
        sidebar = sidebar_controller.build()
        page.data["sidebar"] = sidebar
    else:
        sidebar = page.data["sidebar"]

    event_stats_header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.INSIGHTS, color=WHITE, size=30),
            ft.Text("Event Stats", size=28, weight=ft.FontWeight.BOLD, color=WHITE)
        ], spacing=15, alignment=ft.MainAxisAlignment.START),
        margin=ft.margin.only(left=30, top=20)
    )

    divider_line = ft.Divider(color=WHITE, thickness=2)
    available_years = fetch_available_years()
    selected_year = available_years[0] if available_years else str(datetime.now().year)
    months, events = fetch_event_data(selected_year)
    events_chart = create_chart(months, events, "Number of Events Per Month")
    events_img = ft.Image(src_base64=events_chart, width=400, height=300)

    graph_section = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("Number of Events Per Month", size=20, weight="bold", color=DARK_TEXT, text_align=ft.TextAlign.CENTER),
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
        controls=[sidebar, main_content],
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

if __name__ == "__main__":
    ft.app(target=main)
