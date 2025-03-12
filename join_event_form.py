import flet as ft
import httpx
from datetime import datetime

def load_join_event_form(page, event_id, title, date, time, available_slots,back_callback, join_callback):
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


        #slots
        if event_ticket_tobuy.value.isdigit() and int(event_ticket_tobuy.value)> available_slots:
            event_ticket_tobuy.error_text = "Not enough slots available"
            error_found = True

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

        close_join_popup(page)

    # Build the form layout
    form = ft.Column(
        controls=[
            ft.Text(f"Join Event: {title}", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
            ft.Text(f"Date: {date}", color="#FDF7E3"),
            ft.Text(f"Time: {time}", color="#FDF7E3"),
            ft.Text(f"Available slots: {available_slots}", color="#FDF7E3"),
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
                        on_click=lambda e: close_join_popup(page),
                        bgcolor="#C77000",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Create the popup container
    popup = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    width=380,
                    height=480,
                    padding=ft.padding.all(20),
                    border_radius=10,
                    bgcolor="#406157",  # Match your profile popup color
                    border=ft.border.all(3, "white"),
                    content=form,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        top=230,  # Adjust the top position to avoid covering the header
        left=630,  # Adjust the left position to avoid covering the side taskbar
    )

    # Add the popup to the page overlay so it appears on top of existing content
    page.overlay.append(popup)
    page.update()

def close_join_popup(page):
    """Close the join event form and clear the overlay."""
    if page.overlay:
        page.overlay.clear()
        page.update()
