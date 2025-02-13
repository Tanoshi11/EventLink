import flet as ft
import httpx

def main(page: ft.Page):
    page.title = "EventLink Homepage"

    # Logout: returns user to login screen (via your login module)
    def logout(e):
         import login
         login.load_login(page)
    
    # Optionally: Fetch events from your FastAPI endpoint.
    # If you have an endpoint (e.g., GET /events) that returns a list of events,
    # you can display them here. Otherwise, you may omit this section.
    try:
        response = httpx.get("http://127.0.0.1:8000/events")
        response.raise_for_status()
        events = response.json()  # Expected format: a list of dicts with at least a "title" key.
        event_widgets = [ft.Text(event["title"], size=18) for event in events]
    except Exception as ex:
        event_widgets = [ft.Text("Failed to fetch events", color="red")]

    homepage_view = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Container(width=15),
                ft.Text("EventLink 🎉", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(width=5),
                ft.TextField(
                    label="Search Events", 
                    expand=True,
                    height=50, 
                    suffix=ft.IconButton(icon=ft.Icons.SEARCH, on_click=lambda e: print("Search clicked"), icon_color="white", icon_size=30),
                    border_color="white",
                    border_radius=10,
                    text_style=ft.TextStyle(color="white", size=20),
                    cursor_color="white",
                    label_style=ft.TextStyle(color="white", size=20)
                ),
                ft.IconButton(icon=ft.Icons.EVENT, on_click=lambda e: print("Event clicked"), icon_color="white", icon_size=40, bgcolor="5d0f28"),
                ft.PopupMenuButton(
                    icon=ft.Icons.PERSON,
                    icon_color="white",
                    icon_size=40,
                    bgcolor="5d0f28",
                    items=[
                        ft.PopupMenuItem(text="Info", on_click=lambda e: print("Info clicked")),
                        ft.PopupMenuItem(text="Logout", on_click=logout)
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
        # Optionally list events below the welcome message:
        ft.Column(event_widgets, alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
    
    page.controls.clear()
    page.add(homepage_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
