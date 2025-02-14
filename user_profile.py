import flet as ft
from datetime import datetime

def show_profile(page: ft.Page, user_data=None):
    # If user_data is not provided, use default values.
    if user_data is None:
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "date_joined": datetime.now().strftime("%Y-%m-%d")
        }
    
    profile_view = ft.Column(
        controls=[
            ft.Text("Profile Information", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"Name: {user_data.get('name', 'N/A')}", size=20),
            ft.Text(f"Email: {user_data.get('email', 'N/A')}", size=20),
            ft.Text(f"Date Joined: {user_data.get('date_joined', 'N/A')}", size=20),
            ft.ElevatedButton("Back to Home", on_click=lambda e: back_to_home(page))
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
    
    page.controls.clear()
    page.add(profile_view)
    page.update()

def back_to_home(page: ft.Page):
    import homepg
    homepg.main(page)
