# homepg_view.py
import flet as ft
from controller.category_list_controller import CategoryListController

def create_slider(slider_images, slider_descriptions):
    """Create the slider for the homepage."""
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

    return animated_slider, animated_text

def create_floating_slider(animated_slider, animated_text):
    """Create the floating slider container."""
    discover_text = ft.Text(
        "Discover New Events!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.CENTER
    )

    floating_slider_content = ft.Container(
        width=420,
        height=1000,
        bgcolor="#1D572C",
        border_radius=20,
        padding=15,
        content=ft.Column(
            controls=[discover_text, animated_slider, animated_text],
            spacing=15,
            alignment=ft.alignment.center_right,
        ),
    )

    return ft.Container(
        content=floating_slider_content,
        alignment=ft.alignment.center_right,
        margin=ft.margin.only(right=20, top=60,bottom=30),
    )

def create_category_row(icon_name: str, label: str, on_click):
    """Create a clickable category row."""
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
        on_click=on_click,
        ink=True,
        border_radius=ft.border_radius.all(5),
    )

def create_event_highlights(events):
    """Create 6 event highlight containers with real event data."""
    
    # Ensure at least 6 events, or fallback to placeholders
    event_data = events[:6] + [{"image": "images/default_event.jpg", "date": "TBD", "time": "TBD"}] * (6 - len(events))

    event_containers = []
    positions = [
        (100, 300), (100, 700), (100, 1100),  # Top row
        (500, 300), (500, 700), (500, 1100)   # Bottom row
    ]
    colors = ["#a63b0a", "#a6750a", "#0a9135", "#b6dbf2", "#5D3FD3", "#FF5733"]  # Different background colors

    for i in range(6):
        event = event_data[i]

        container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(src=event.get("image", "images/default_event.jpg"), width=400, height=230, fit=ft.ImageFit.CONTAIN, border_radius=20),
                    ft.Text(event.get("venue", "No Venue"), size=16, color="white", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text(event.get("date_time", "No Date"), size=16, color="white", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.TextButton(
                        "More Details",
                        url=event.get("link", "#"),
                        style=ft.ButtonStyle(
                            bgcolor="white",  # Button background color
                            color="black",    # Text color
                        ),
                    )
                ],
                alignment=ft.alignment.center,
                spacing=10
            ),
            width=390,
            height=390,
            bgcolor=colors[i % len(colors)],  # Rotate colors
            alignment=ft.alignment.top_center,
            padding=20,
            border_radius=20,
            expand=True,
            margin=ft.margin.only(top=positions[i][0], left=positions[i][1], bottom=20),
        )

        event_containers.append(container)

    return event_containers
