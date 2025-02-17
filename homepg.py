import flet as ft
import httpx
from datetime import datetime

def main(page: ft.Page):
    page.title = "EventLink Homepage"
    
    def logout(e):
         import login
         login.load_login(page)
    
    def show_profile_page(page: ft.Page):
         import user_profile
         user_profile.show_profile(page)
    
    # Use the downloaded image as the logo
    logo_image = ft.Image(
        src="logo1.png",  # Ensure this image file is in your project directory
        width=200,
        height=60,
        fit=ft.ImageFit.CONTAIN 
    )
    
    # Optionally fetch events from FastAPI.
    try:
         response = httpx.get("http://127.0.0.1:8000/events")
         response.raise_for_status()
         events = response.json()
         event_widgets = [ft.Text(event["title"], size=18) for event in events]
    except Exception as ex:
         event_widgets = [ft.Text("Failed to fetch events", color="red")]
    
    homepage_view = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.Container(width=15),
                    # Display the logo image
                    ft.Container(
                        content=logo_image,
                        margin=ft.margin.only(right=10)
                    ),
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
                        icon=ft.Icons.EVENT, 
                        on_click=lambda e: print("Event clicked"), 
                        icon_color="white", 
                        icon_size=40, 
                        bgcolor="5d0f28"
                    ),
                    ft.PopupMenuButton(
                        icon=ft.Icons.PERSON,
                        icon_color="white",
                        icon_size=40,
                        bgcolor="5d0f28",
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
                bgcolor="#560419",
                padding=5
            ),
            ft.Container(
                content=ft.Text("Welcome to EventLink!", size=50, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                expand=True
            ),
            ft.Column(event_widgets, alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )
    
    page.controls.clear()
    page.add(homepage_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
