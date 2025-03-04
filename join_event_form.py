import flet as ft
import httpx
from datetime import datetime

def load_join_event_form(page, event_id, title, date, time, back_callback, join_callback):
    # Text fields with styling to match user_profile.py
    event_attend_name = ft.TextField(
        label="Name",
        width=300,
        text_style=ft.TextStyle(color="#FDF7E3"),
        label_style=ft.TextStyle(color="#FDF7E3"),
        border_color="#D4A937",
        hint_text="Enter your name"
    )
    event_ticket_tobuy = ft.TextField(
        label="Number of tickets",
        width=300,
        text_style=ft.TextStyle(color="#FDF7E3"),
        label_style=ft.TextStyle(color="#FDF7E3"),
        border_color="#D4A937",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="Enter a number"
    )

    def submit_form(e):
        error_found = False
        # Validate name
        if not event_attend_name.value:
            event_attend_name.error_text = "Name is required."
            error_found = True
        else:
            event_attend_name.error_text = None

        # Validate tickets
        if not event_ticket_tobuy.value:
            event_ticket_tobuy.error_text = "Number of tickets is required."
            error_found = True
        elif not event_ticket_tobuy.value.isdigit():
            event_ticket_tobuy.error_text = "Please enter a valid number."
            error_found = True
        else:
            event_ticket_tobuy.error_text = None

        page.update()
        if error_found:
            return

        print("Submitting join request for:", event_attend_name.value, event_ticket_tobuy.value)
        
        # Send join event API request
        username = page.data.get("username")
        join_data = {"username": username, "event_name": title}
        response = httpx.post("http://localhost:8000/join_event", json=join_data)
        if response.status_code == 200:
            joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            page.snack_bar = ft.SnackBar(
                ft.Column([
                    ft.Text(f"You have joined the event: {title}", color="white"),
                    ft.Text(f"Date: {joined_date}", size=12, color="white")
                ])
            )
            page.snack_bar.open = True
            page.update()
            # Call the join_callback to update the button text
            join_callback()
        else:
            print("Error joining event:", response.json())

        # Close the join event popup and trigger the back callback
        close_join_popup(page, back_callback)

    # Build the form layout
    form = ft.Column(
        controls=[
            ft.Text(f"Join Event: {title}", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
            ft.Text(f"Date: {date}", color="#FDF7E3"),
            ft.Text(f"Time: {time}", color="#FDF7E3"),
            event_attend_name,
            event_ticket_tobuy,
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Submit",
                        on_click=submit_form,
                        bgcolor="#C77000",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                    ),
                    ft.ElevatedButton(
                        "Back",
                        on_click=lambda e: close_join_popup(page, back_callback),
                        bgcolor="#C77000",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Create a popup overlay container (similar to user_profile edit popups)
    popup = ft.AnimatedSwitcher(
        duration=500,
        content=ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor="rgba(0,0,0,0.5)",  # semi‐transparent overlay
            content=ft.Container(
                width=380,
                height=480,
                padding=ft.padding.all(20),
                border_radius=10,
                bgcolor="#406157",  # match your profile popup color
                border=ft.border.all(3, "white"),
                content=form,
            ),
        ),
    )

    # Add the popup to the page overlay so it appears on top of existing content
    page.overlay.append(popup)
    page.update()

def close_join_popup(page, back_callback):
    # Remove this popup from the overlay (assumes it is the last added)
    if page.overlay:
        page.overlay.pop()
    page.update()

    # Call the back_callback with the page argument
    back_callback(page) if back_callback else None  # Ensures 'Back' only works if properly set

