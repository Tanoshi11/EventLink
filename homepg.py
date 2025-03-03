import flet as ft
import time
import threading
from header import load_header  # Import the header
from search import load_search

# Global variable to store the notification popup overlay
notif_popup = None
events_text = ft.Text("", color="white")

def main(page: ft.Page):
    if page.data is None:
        page.data = {}
    page.title = "Home"
    page.bgcolor = "#d6aa54"
    page.padding = 0  # Ensure no extra padding at the edges

    # ----------------- Taskbar (Header) -----------------
    taskbar = load_header(page)  # Load the header from header.py

    # ----------------- Other Main Content -----------------
    top_left_text = ft.Container(
        content=ft.Text(
            "Upcoming Events 🎉",
            size=30,
            weight=ft.FontWeight.BOLD,
            color="#faf9f7",
            text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.top_left,
        margin=ft.margin.only(top=100, left=250),
        padding=20
    )

    # ======== FLOATING DISCOVER & SLIDER ========

     # 1) "Discover" text remains unchanged (you can also adjust its font size if desired)
    # Headline text at the top of the slider
    discover_text = ft.Text(
        "Discover New Events!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.CENTER
    )

    # Slider images
    slider_images = [
        "images/eventsample_img1.jpg",
        "images/eventsample_img2.png",
        "images/eventsample_img3.jpg",
    ]

    # Corresponding descriptions for each image
    slider_descriptions = [
        "Description for Image 1: A fantastic outdoor event you won't want to miss!",
        "Description for Image 2: Join us and help the people in need!",
        "Description for Image 3: Volunteer opportunities to make a positive impact!",
    ]

    # Create an AnimatedSwitcher for the images
    animated_slider = ft.AnimatedSwitcher(
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=1000,
        content=ft.Image(
            src=slider_images[0],
            width=600,
            height=300,
            fit=ft.ImageFit.FIT_WIDTH,
            border_radius=20
        )
    )

    # Create a second AnimatedSwitcher for the text descriptions
    animated_text = ft.AnimatedSwitcher(
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=1000,
        content=ft.Text(
            slider_descriptions[0],
            color="white",
            size=14,
            text_align=ft.TextAlign.CENTER
        )
    )

    # Loop that periodically switches both the image and the description
    def slider_loop():
        current_index = 0
        while True:
            time.sleep(8)  # Wait 8 seconds before switching
            current_index = (current_index + 1) % len(slider_images)
            # Update the image
            animated_slider.content = ft.Image(
                src=slider_images[current_index],
                width=600,
                height=300,
                fit=ft.ImageFit.FIT_WIDTH,
                border_radius=20
            )
            # Update the text
            animated_text.content = ft.Text(
                slider_descriptions[current_index],
                color="white",
                size=14,
                text_align=ft.TextAlign.CENTER
            )
            page.update()

    # Start the slider in a background thread
    threading.Thread(target=slider_loop, daemon=True).start()

    # Combine the "Discover" text, the image, and the description in one column
    floating_slider_content = ft.Container(
        width=420,                # Adjust width to suit your design
        height=page.height *1.5,
        bgcolor="#1D572C",
        border_radius=20,
        padding=15,
        content=ft.Column(
            controls=[
                discover_text,
                animated_slider,
                animated_text
            ],
            spacing=15,
            alignment=ft.alignment.top_center,
        ),
    )

    # Place the slider container on the right side of the screen
    floating_slider_container = ft.Container(
        content=floating_slider_content,
        alignment=ft.alignment.center_right,
        margin=ft.margin.only(right=20, top=120, bottom=10),
    )


    # ======== END FLOATING DISCOVER & SLIDER ========

    homepage_view = ft.Container(
        content=top_left_text,
        expand=True
    )

    # ----------------- Category Icons Section -----------------
    selected_category_text = ft.Text("Selected Category: None", size=20, color="white")

    # Click handler: updates the visible text and prints to console
    def handle_category_click(e, category_label: str):
        load_search(page, query=category_label, search_type="category")
        print(f"{category_label} quick search triggered!")

    # Helper function: returns a clickable row with an icon and label
    def category_row(icon_name: str, label: str):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon_name, color="white", size=20),
                    ft.Text(label, color="white", size=16),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.all(5),
            on_click=lambda e: handle_category_click(e, label),
            ink=True,  # adds a ripple effect when clicked
            border_radius=ft.border_radius.all(5),
        )

    # Header texts for the sidebar
    filters_text = ft.Text("Filters", color="white", size=20, weight=ft.FontWeight.BOLD)
    category_text = ft.Text("Category", color="white", size=16, weight=ft.FontWeight.W_600)

    # Build the list of category items
    category_buttons = ft.Column(
        controls=[
            filters_text,
            category_text,
            category_row(ft.Icons.BUSINESS_CENTER, "Business"),
            category_row(ft.Icons.RESTAURANT, "Food & Drink"),
            category_row(ft.Icons.CHILD_CARE, "Family & Education"),
            category_row(ft.Icons.HEALTH_AND_SAFETY, "Health"),
            category_row(ft.Icons.DIRECTIONS_BOAT, "Travel"),
            category_row(ft.Icons.MUSIC_NOTE, "Music"),
            category_row(ft.Icons.THEATER_COMEDY, "Performing Arts"),
            category_row(ft.Icons.STYLE, "Fashion"),
            category_row(ft.Icons.MOVIE, "Film & Media"),
            category_row(ft.Icons.COLOR_LENS, "Hobbies"),
            category_row(ft.Icons.HOME, "Home & Lifestyle"),
            category_row(ft.Icons.GROUP, "Community"),
            category_row(ft.Icons.VOLUNTEER_ACTIVISM, "Charity & Causes"),
            category_row(ft.Icons.ACCOUNT_BALANCE, "Government"),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START
    )

    # Create the sidebar container
    side_taskbar = ft.Container(
        content=ft.Container(
            content=category_buttons,
            width=245,             # adjust as needed
            bgcolor="#1d572c",     # your desired sidebar color
            alignment=ft.alignment.top_left,
            padding=20
        ),
        alignment=ft.alignment.top_left,
        margin=ft.margin.only(top=100)
    )

    event1_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#a63b0a",
            alignment=ft.alignment.top_center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=178, right=620)
    )

    event2_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#a6750a",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=178, right= -220)
    )

    event3_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#0a9135",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=530, right=620)
    )

    event4_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=340,
            bgcolor="#b6dbf2",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=530, right=-220)
    )

    # Place the floating slider LAST so it appears on top
    main_stack = ft.Stack(
        controls=[
            homepage_view,
            event1_highlight,
            event2_highlight,
            event3_highlight,
            event4_highlight,
            floating_slider_container,
            taskbar,  # Header loaded from header.py
            side_taskbar,  # Move the sidebar to the last element so it's on top
        ],
        expand=True,
    )

    page.controls.clear()
    page.add(main_stack)
    page.update()


def load_homepage(page):
    page.controls.clear()
    main(page)

def load_login(page):
    page.floating_action_button = None
    pass

def load_my_events(page):
    import my_events
    page.controls.clear()
    my_events.load_my_events(page)  # Calls the function without restarting the app
    page.update()

def load_create_event(page):
    import CreateEvents
    page.controls.clear()
    CreateEvents.load_create_event(page)  # Calls the function without re-running ft.app()
    page.update()


def load_profile(page):
    page.floating_action_button = None
    pass

if __name__ == "__main__":
    ft.app(target=main)
