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
    
    # Image for the logo
    logo_image = ft.Image(
        src="eventlink.png",  
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

    # Header (Navigation Bar)
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
                    icon_color="white",  
                    icon_size=30
                ),
                border_color="white",
                border_radius=10,
                text_style=ft.TextStyle(color="white", size=20),
                cursor_color="white",
                label_style=ft.TextStyle(color="white", size=20)
            ),
            ft.IconButton(
                icon=ft.Icons.SAVINGS,
                on_click=lambda: print("Savings Clicked"),
                icon_color="#FFBA00",
                icon_size=40, 
                width=100,
                tooltip="",
            ),
            ft.PopupMenuButton(
                icon=ft.Icons.EVENT_AVAILABLE_SHARP,
                icon_color="#FFBA00",
                icon_size=40, 
                width=100,
                tooltip="",
                # items=[
                #     ft.PopupMenuItem(
                #         text="Organize Event",
                #         on_click=lambda e: print("Organize clicked"),
                #     ),
                #     ft.PopupMenuItem(
                #         text="Volunteer Event",
                #         on_click=lambda e: print("Volunteer clicked"),
                #     )
                # ]
            ),
            ft.PopupMenuButton(
                icon=ft.Icons.PERSON_ROUNDED,
                icon_color="#FFBA00",
                icon_size=40,
                width=100,
                bgcolor="#B46617",
                tooltip="",
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
        padding=5,
        expand=False  
    )

    # Welcome Section 
    welcome_section = ft.Container(
        content=ft.Text(
            "Your Personalized Event Experience Starts Here!",
            size=50,
            weight=ft.FontWeight.BOLD,
            color="white",
            text_align=ft.TextAlign.CENTER 
        ),
        alignment=ft.alignment.center,
        padding=20,
        expand=True  
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
                padding=ft.padding.symmetric(vertical=20, horizontal=40),
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD) 
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
        alignment=ft.MainAxisAlignment.START,  
        expand=True
    )

    page.controls.clear()
    page.add(homepage_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
