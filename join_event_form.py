import flet as ft
import httpx

def load_join_event_form(page, event_id, title, date, time, back_callback):
    # Check if the user is logged in by checking if username is stored in page.data.
    username = page.data.get("username") if page.data else None
    if not username:
        # Redirect to login if no user is logged in.
        import login
        login.load_login(page)
        return

    # Create a read-only field for the user's name.
    event_attend_name = ft.TextField(
        label="Name",
        width=300,
        value=username,
        read_only=True,
        text_style=ft.TextStyle(color="#FDF7E3"),
        label_style=ft.TextStyle(color="#FDF7E3"),
        border_color="#D4A937"
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

    join_button = ft.ElevatedButton(
        "Join Event",
        bgcolor="#C77000",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    def submit_form(e):
        if not event_ticket_tobuy.value or not event_ticket_tobuy.value.isdigit():
            event_ticket_tobuy.error_text = "Please enter a valid number."
            page.update()
            return

        # Prepare the data to send
        data = {
            "event_id": event_id,
            "title": title,
            "date": date,
            "time": time,
            "username": username
        }

        try:
            response = httpx.post(
                "http://127.0.0.1:8000/join_event",
                json=data,
                timeout=10.0
            )
            response.raise_for_status()

            # Hide the join button after successful join.
            join_button.visible = False
            page.update()

            # Show success notification.
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Successfully joined {title}!"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()

        except httpx.HTTPStatusError as exc:
            error_msg = exc.response.json().get("detail", "Error joining event.")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {error_msg}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    # Assign the submit_form function to the join button.
    join_button.on_click = submit_form

    form = ft.Column(
        controls=[
            ft.Text(f"Join Event: {title}", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
            ft.Text(f"Date: {date}", color="#FDF7E3"),
            ft.Text(f"Time: {time}", color="#FDF7E3"),
            event_attend_name,
            event_ticket_tobuy,
            ft.Row([join_button], alignment=ft.MainAxisAlignment.CENTER)  # Centered button row.
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    popup = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="rgba(0,0,0,0.5)",  # Semi‐transparent overlay
        content=ft.Container(
            width=500,
            height=480,
            padding=ft.padding.all(20),
            border_radius=10,
            bgcolor="#406157",  # Matching popup background color
            border=ft.border.all(3, "white"),
            content=form,
        ),
    )

    page.overlay.append(popup)
    page.update()

def close_join_popup(page, back_callback):
    if page.overlay:
        page.overlay.pop()
    page.update()
    back_callback(page)
