import flet as ft
import httpx
from datetime import datetime

def main(page: ft.Page):
    page.title = "My Events"
    page.bgcolor = "#0C3B2E"
    
    def fetch_events():
        try:
            response = httpx.get("http://127.0.0.1:8000/my_events")
            response.raise_for_status()
            return response.json()
        except Exception as ex:
            return []
    
    events = fetch_events()
    current_date = datetime.now().date()
    
    past_events = []
    current_events = []
    upcoming_events = []
    
    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        if event_date < current_date:
            past_events.append(ft.Text(event['title'], size=18, color="gray"))
        elif event_date == current_date:
            current_events.append(ft.Text(event['title'], size=18, color="white"))
        else:
            upcoming_events.append(ft.Text(event['title'], size=18, color="lightgreen"))
    
    # Header (Navigation Bar)
    header = ft.Container(
        content=ft.Row([
            ft.Text("My Events", size=30, weight=ft.FontWeight.BOLD, color="white")
        ]),
        bgcolor="#2C6D4F",
        padding=10
    )
    
    # Events List
    events_section = ft.Container(
        content=ft.Column([
            ft.Text("Past Events", size=22, weight=ft.FontWeight.BOLD, color="red"),
            ft.Column(past_events if past_events else [ft.Text("No past events", color="gray")]),
            ft.Text("Current Events", size=22, weight=ft.FontWeight.BOLD, color="yellow"),
            ft.Column(current_events if current_events else [ft.Text("No current events", color="gray")]),
            ft.Text("Upcoming Events", size=22, weight=ft.FontWeight.BOLD, color="green"),
            ft.Column(upcoming_events if upcoming_events else [ft.Text("No upcoming events", color="gray")]),
        ], spacing=15),
        padding=20
    )
    
    # Footer Button
    footer_button = ft.Container(
        content=ft.ElevatedButton(
            text="Back to Home",
            bgcolor="#6D9773",
            color="white",
            on_click=lambda _: print("Back to home clicked"),
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(vertical=15, horizontal=30),
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
            ),
        ),
        alignment=ft.alignment.center,
        padding=20
    )
    
    # Main Layout
    my_events_view = ft.Column(
        controls=[
            header,
            events_section,
            footer_button
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
    
    page.controls.clear()
    page.add(my_events_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
