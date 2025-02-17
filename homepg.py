import flet as ft
import httpx
from datetime import datetime

def main(page: ft.Page):
    page.title = "Home"
    page.bgcolor = "#0C3B2E"
    
    def logout(e):
         import login
         login.load_login(page)
    
    def show_profile_page(page: ft.Page):
         import user_profile
         user_profile.show_profile(page)
    
    logo_image = ft.Image(
        src="logo1.png",  # Ensure this image file is in your project directory
        width=200,
        height=80,
        fit=ft.ImageFit.CONTAIN 
    )
    
    # Fetch events from FastAPI
    try:
        response = httpx.get("http://127.0.0.1:8000/events")
        response.raise_for_status()
        events = response.json()
        event_widgets = [ft.Text(event["title"], size=18, color="white") for event in events]
    except Exception as ex:
        event_widgets = [ft.Text("Failed to fetch events", color="red")]

    # Header 
    header = ft.Container(
        content=ft.Row([
            ft.Container(width=15),
            ft.Container(content=logo_image, margin=ft.margin.only(right=10)),
            ft.TextField(
                label="Search Events",
                expand=True,
                height=50,
                suffix=ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    on_click=lambda e: print("Search clicked"),
                    icon_color="#FFBA00",  # Yellow accent color
                    icon_size=30
                ),
                border_color="white",
                border_radius=10,
                text_style=ft.TextStyle(color="white", size=20),
                cursor_color="white",
                label_style=ft.TextStyle(color="white", size=20)
            ),
            ft.IconButton(
                icon=ft.Icons.EVENT,
                on_click=lambda e: print("Event clicked"),
                icon_color="#FFBA00",
                icon_size=40,
                bgcolor="#B46617"  # Burnt orange
            ),
            ft.PopupMenuButton(
                icon=ft.Icons.PERSON,
                icon_color="#FFBA00",
                icon_size=40,
                bgcolor="#B46617",
                items=[
                    ft.PopupMenuItem(
                        text="Info",
                        on_click=lambda e: show_profile_page(page)
                    ),
                    ft.PopupMenuItem(
                        text="Logout",
                        on_click=lambda e: logout(e)
                    )
                ]
            )
        ]),
        bgcolor="#2C6D4F", 
        padding=5
    )

    # Welcome Section
    welcome_section = ft.Container(
        content=ft.Text(
            "Your Personalized Event Experience Starts Here.",
            size=50,
            weight=ft.FontWeight.BOLD,
            color="white"
        ),
        alignment=ft.alignment.center,
        padding=20
    )

    # Events List
    events_section = ft.Container(
        content=ft.Column(event_widgets, alignment=ft.MainAxisAlignment.CENTER),
        padding=20
    )

    # Footer Button with adjustments
    footer_button = ft.Container(
        content=ft.ElevatedButton(
            text="Explore Events",
            bgcolor="#6D9773",  # Soft green button
            color="white",
            on_click=lambda _: print("Explore clicked"),
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(vertical=20, horizontal=40),  # Larger padding for bigger button
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)  # Larger text size
            ),
        ),
        alignment=ft.alignment.center,
        padding=20
    )

    # Main Layout
    homepage_view = ft.Column(
        controls=[
            header,
            welcome_section,
            events_section,
            footer_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    page.controls.clear()
    page.add(homepage_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
