import flet as ft
import httpx

def show_profile(page: ft.Page):
    """
    Fetch user data from MongoDB via FastAPI, based on the username in page.data["username"].
    """
    username = page.data.get("username") if page.data else None

    if not username:
        # If no username is present, show an error
        error_view = ft.Column(
            controls=[
                ft.Text("User not logged in.", color="red", size=20),
                ft.ElevatedButton("Back to Login", on_click=lambda e: back_to_login(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.controls.clear()
        page.add(error_view)
        page.update()
        return

    try:
        # Fetch user data from the FastAPI endpoint
        response = httpx.get(f"http://127.0.0.1:8000/get_user?username={username}", timeout=10.0)
        response.raise_for_status()
        doc = response.json()
        
        # Build user data from the DB
        user_data = {
            "username": doc.get("username", "N/A"),
            "email": doc.get("email", "N/A"),
            "contact": doc.get("contact", "N/A"),
            "status": "Customer",  # default
            "date_joined": doc.get("date_joined", "N/A")
        }
    except Exception as e:
        # If there's an error retrieving data, show an error
        error_view = ft.Column(
            controls=[
                ft.Text("Error retrieving user data.", color="red", size=20),
                ft.Text(str(e), color="red"),
                ft.ElevatedButton("Back to Login", on_click=lambda e: back_to_login(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.controls.clear()
        page.add(error_view)
        page.update()
        return

    # Display the user data in the UI
    profile_view = ft.Column(
        controls=[
            ft.Text("Profile Information", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"Username: {user_data['username']}", size=20),
            ft.Text(f"Email: {user_data['email']}", size=20),
            ft.Text(f"Contact: {user_data['contact']}", size=20),
            ft.Text(f"Status: {user_data['status']}", size=20),
            ft.Text(f"Date Joined: {user_data['date_joined']}", size=20),
            ft.ElevatedButton("Back to Home", on_click=lambda e: back_to_home(page),bgcolor="#B46617", color = "white", style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ))
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

def back_to_login(page: ft.Page):
    import login
    login.load_login(page)
