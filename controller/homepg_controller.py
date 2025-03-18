import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
import flet as ft
import time
import threading
from pymongo import MongoClient
from header import load_header
from controller.search_controller import load_search
from controller.category_list_controller import CategoryListController
from controller.sidebar_controller import SidebarController
from view.homepg_view import create_event_highlights

client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/")
db = client["EventLink"]
collection = db["events"]


def handle_category_click(page, category_label):
    """Handle category click events."""
    load_search(page, query=category_label, search_type="category")
    print(f"{category_label} quick search triggered!")

def slider_loop(page, animated_slider, animated_text, slider_images, slider_descriptions):
    """Loop through the slider images and descriptions."""
    current_index = 0
    while True:
        time.sleep(5)  # Wait 8 seconds before switching
        current_index = (current_index + 1) % len(slider_images)
        animated_slider.content = ft.Image(
            src=slider_images[current_index],
            width=600,
            height=300,
            fit=ft.ImageFit.FIT_WIDTH,
            border_radius=20
        )
        animated_text.content = ft.Text(
            slider_descriptions[current_index],
            color="white",
            size=14,
            text_align=ft.TextAlign.CENTER
        )
        page.update()

def get_random_events():
    """Fetch up to 4 random events from MongoDB."""
    events = list(collection.aggregate([{"$sample": {"size": 4}}]))  # Get 4 random events
    return events if events else [{"image": "images/default_event.jpg", "date": "TBD", "time": "TBD"}] * 4  # Fallback

def load_homepage(page: ft.Page):
    """Load the homepage."""
    main(page)

def main(page: ft.Page):
    """Main function to load the homepage."""
    if page.data is None:
        page.data = {}
    page.title = "Home"
    page.bgcolor = "#d6aa54"
    page.padding = 0

    # Load header and sidebar
    header = load_header(page)
    sidebar_controller = SidebarController(page)
    sidebar_list = sidebar_controller.build()

    # Fetch 4 random events from MongoDB
    events = get_random_events()

    # Create event highlights with actual event data
    event1_highlight, event2_highlight, event3_highlight, event4_highlight = create_event_highlights(events)

    # Main layout
    main_stack = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Text(
                    "UPCOMING EVENTS 🎉",
                    size=35,
                    weight=ft.FontWeight.BOLD,
                    color="#faf9f7",
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.top_left,
                margin=ft.margin.only(top=10, left=250),
                padding=20
            ),
            event1_highlight,
            event2_highlight,
            event3_highlight,
            event4_highlight,
            sidebar_list,
        ],
        expand=True,
    )

    page.controls.clear()
    page.add(main_stack)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)