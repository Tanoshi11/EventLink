import flet as ft
import httpx
from datetime import datetime, timedelta

def load_my_events(page: ft.Page):
    page.title = "My Events"
    page.bgcolor = "#0C3B2E"
    page.padding = 20

    def fetch_events():
        try:
            response = httpx.get("http://127.0.0.1:8000/my_events")
            response.raise_for_status()
            return response.json()
        except Exception as ex:
            print("Error fetching events:", ex)
            return []

    events = fetch_events()
    current_date = datetime.now().date()
    past_events, current_events, upcoming_events = [], [], []
    event_dates = {datetime.strptime(event["date"], "%Y-%m-%d").date(): event["title"] for event in events}

    for event_date, title in event_dates.items():
        event_text = ft.Text(title, size=16, weight=ft.FontWeight.MEDIUM)
        event_container = ft.Container(
            content=ft.ListTile(title=event_text, bgcolor="#4F4F4F"),
            border_radius=10,
            padding=5
        )

        if event_date < current_date:
            past_events.append(event_container)
        elif event_date == current_date:
            event_container.content.bgcolor = "#FFD700"
            current_events.append(event_container)
        else:
            event_container.content.bgcolor = "#32CD32"
            upcoming_events.append(event_container)

    def create_event_section(title, events_list, color):
        return ft.Column([
            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=color),
            ft.Column(events_list if events_list else [ft.Text("No events", color="gray")], spacing=5)
        ], spacing=10)

    sidebar = ft.Container(
        content=ft.Column([
            ft.Text("My Events", size=22, weight=ft.FontWeight.BOLD, color="white"),
            ft.Divider(height=5, color="gray"),
            ft.Text("Event Categories", size=16, weight=ft.FontWeight.BOLD, color="white"),
            ft.Container(content=ft.ListTile(title=ft.Text("Past Events")), bgcolor="#4F4F4F", border_radius=10, padding=5),
            ft.Container(content=ft.ListTile(title=ft.Text("Current Events")), bgcolor="#FFD700", border_radius=10, padding=5),
            ft.Container(content=ft.ListTile(title=ft.Text("Upcoming Events")), bgcolor="#32CD32", border_radius=10, padding=5)
        ], spacing=10),
        width=250,
        bgcolor="#1E4D3D",
        padding=15,
        border_radius=12
    )

    def show_selected_date(date):
        if date in event_dates:
            page.dialog = ft.AlertDialog(title=ft.Text(f"Event on {date}: {event_dates[date]}"))
            page.dialog.open = True
            page.update()

    def create_calendar():
        today = datetime.now().date()
        first_day = today.replace(day=1)
        start_weekday = first_day.weekday()
        days_in_month = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day
        
        dates = []
        for i in range(start_weekday):
            dates.append(ft.Container())
        for day in range(1, days_in_month + 1):
            date = first_day.replace(day=day)
            event_indicator = "🔴" if date in event_dates else ""
            dates.append(
                ft.Container(
                    content=ft.Text(f"{day}{event_indicator}", size=16, weight=ft.FontWeight.BOLD, color="white"),
                    alignment=ft.alignment.center,
                    padding=10,
                    bgcolor="#2C6D4F" if date in event_dates else "#1E4D3D",
                    border_radius=5,
                    on_click=lambda e, d=date: show_selected_date(d)
                )
            )
        
        return ft.GridView(
            runs_count=7,
            controls=dates,
            spacing=5,
            run_spacing=5
        )
    
    calendar_section = ft.Column([
        ft.Text("Calendar", size=18, weight=ft.FontWeight.BOLD, color="white"),
        create_calendar()
    ], spacing=10)

    main_content = ft.Column([
        ft.Text("Good Afternoon.\nWhat's your plan for today?", size=24, weight=ft.FontWeight.BOLD, color="white"),
        create_event_section("Past Events", past_events, "#FF6347"),
        create_event_section("Current Events", current_events, "#FFD700"),
        create_event_section("Upcoming Events", upcoming_events, "#32CD32")
    ], spacing=15, expand=True)

    sidebar_layout = ft.Row([
        sidebar,
        ft.VerticalDivider(width=5, color="gray"),
        main_content,
        ft.VerticalDivider(width=5, color="gray"),
        calendar_section
    ], expand=True)

    def go_back(e):
        from homepg import load_homepage
        load_homepage(page)

    footer_button = ft.Container(
        content=ft.ElevatedButton(
            text="Back to Home",
            bgcolor="#FFD700",
            color="black",
            on_click=go_back,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(vertical=10, horizontal=20),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        ),
        alignment=ft.alignment.center,
        padding=10
    )

    page.controls.clear()
    page.add(ft.Column([
        sidebar_layout,
        footer_button
    ], alignment=ft.MainAxisAlignment.START, expand=True))
    page.update()

if __name__ == "__main__":
    ft.app(target=load_my_events)
