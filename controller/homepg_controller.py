# homepg_controller.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import flet as ft
import time
import threading
from header import load_header
from controller.search_controller import load_search
from controller.category_list_controller import CategoryListController
from controller.sidebar_controller import SidebarController
from view.homepg_view import create_slider, create_floating_slider, create_event_highlights



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

def load_homepage(page: ft.Page):
    """Load the homepage."""
    main(page)  # Call the main function to load the homepage

def main(page: ft.Page):
    """Main function to load the homepage."""
    if page.data is None:
        page.data = {}
    page.title = "Home"
    page.bgcolor = "#d6aa54"
    page.padding = 0

    # Load the header
    header = load_header(page)

    #category_list
    category_list_controller = CategoryListController(page)
    category_list = category_list_controller.build()

    #sidebar list
    sidebar_controller = SidebarController(page)
    sidebar_list = sidebar_controller.build()

    # Create the slider
    slider_images = [
        "images/eventsample_img1.jpg",
        "images/eventsample_img2.png",
        "images/eventsample_img3.jpg",
    ]
    slider_descriptions = [
        "A fantastic outdoor event you won't want to miss!",
        "Join us and help the people in need!",
        "Volunteer opportunities to make a positive impact!",
    ]
    animated_slider, animated_text = create_slider(slider_images, slider_descriptions)
    floating_slider_container = create_floating_slider(animated_slider, animated_text)

    # Start the slider loop in a background thread
    threading.Thread(target=slider_loop, args=(page, animated_slider, animated_text, slider_images, slider_descriptions), daemon=True).start()

    # Create event highlights
    event1_highlight, event2_highlight, event3_highlight, event4_highlight = create_event_highlights()

    # Main stack layout
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
            floating_slider_container,
            # header,
            sidebar_list,
            # category_list,
        ],
        expand=True,
    )

    page.controls.clear()
    page.add(main_stack)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)