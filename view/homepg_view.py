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

def create_event_highlights():
    """Create the event highlight containers."""
    event1_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=440,
            bgcolor="#a63b0a",
            alignment=ft.alignment.top_center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=110, right=620,bottom=418)
    )

    event2_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=440,
            bgcolor="#a6750a",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=110, right=-220,bottom=418)
    )

    event3_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=440,
            bgcolor="#0a9135",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=482, right=620,bottom=30)
    )

    event4_highlight = ft.Container(
        content=ft.Container(
            width=410,
            height=440,
            bgcolor="#b6dbf2",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=482, right=-220,bottom=30)
    )

    return event1_highlight, event2_highlight, event3_highlight, event4_highlight