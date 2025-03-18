import flet as ft 
import matplotlib.pyplot as plt
import io
import base64
import pymongo
from datetime import datetime
from controller.sidebar_controller import SidebarController

# Define theme colors
BACKGROUND_COLOR = "#d6aa54"
DARK_RED = "#d9534f"
WHITE = "#ffffff"
DARK_TEXT = "#333333"
CHART_BG_COLOR = "#f7f5ed"

# MongoDB Connection
MONGO_URI = "mongodb+srv://samanthaangelacrn:eventlink@eventlink.1hfcs.mongodb.net/?retryWrites=true&w=majority&appName=EventLink"
client = pymongo.MongoClient(MONGO_URI)
db = client["EventLink"]
collection = db["events"]

def main(page: ft.Page):
    page.title = "Volunteer Stats"
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0

    if "sidebar" not in page.data:
        sidebar_controller = SidebarController(page)
        sidebar = sidebar_controller.build()
        page.data["sidebar"] = sidebar
    else:
        sidebar = page.data["sidebar"]

    volunteer_stats_header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.INSIGHTS, color=WHITE, size=30),
            ft.Text("Volunteer Stats", size=28, weight=ft.FontWeight.BOLD, color=WHITE)
        ], spacing=15, alignment=ft.MainAxisAlignment.START),
        margin=ft.margin.only(left=30, top=40)
    )

    divider_line = ft.Divider(color=WHITE, thickness=2)

    participants_chart = create_chart()
    participants_img = ft.Image(src_base64=participants_chart, width=400, height=300)

    graph_section = ft.Container(
        content=ft.Column([
            ft.Text("Monthly Volunteer Participation", size=20, weight="bold", color=DARK_TEXT, text_align=ft.TextAlign.CENTER),
            participants_img
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=CHART_BG_COLOR,
        padding=20,
        border_radius=15,
        alignment=ft.alignment.center,
        width=600,
        height=400
    )

    main_content = ft.Container(
        content=ft.Column([
            volunteer_stats_header,
            divider_line,
            ft.Row([graph_section], alignment=ft.MainAxisAlignment.CENTER)
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

def create_chart():
    fig, ax = plt.subplots()
    ax.plot([], [], marker="o", linestyle="-", color=DARK_RED, label="No Data")
    ax.set_xlabel("Month")
    ax.set_ylabel("Count")
    ax.set_title("Monthly Volunteer Participation")
    ax.grid(True)
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight", facecolor=CHART_BG_COLOR)
    img_buffer.seek(0)
    return base64.b64encode(img_buffer.getvalue()).decode("utf-8")

if __name__ == "__main__":
    ft.app(target=main)
