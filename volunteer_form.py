import flet as ft
import httpx

def fetch_joined_events(page):
    """Fetch events where the user has already joined."""
    try:
        username = page.data.get("username", "default_user")
        url = f"http://localhost:8000/my_events?username={username}"
        response = httpx.get(url)
        if response.status_code == 200:
            return response.json().get("events", [])
    except Exception as ex:
        print("Error fetching events:", ex)
    return []

def update_volunteer_status(page, event_id: str):
    """Update user to 'Volunteer' for an event."""
    try:
        username = page.data.get("username")
        if not username:
            return
        response = httpx.patch(
            f"http://localhost:8000/update_user?username={username}",
            json={"status": "Volunteer"}
        )
        if response.status_code == 200:
            page.snack_bar = ft.SnackBar(
                ft.Text("You are now a volunteer!", color="white"),
                bgcolor="#4CAF50"
            )
            page.snack_bar.open = True
            page.update()
    except Exception as ex:
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Error updating status: {ex}", color="white"),
            bgcolor="red"
        )
        page.snack_bar.open = True
        page.update()

def show_volunteer_popup(page, event):
    """Show a popup with event details and options to Volunteer or Back."""

    def close_popup(e):
        if page.overlay:
            # Remove the blur overlay and the popup
            for control in page.overlay:
                if isinstance(control, ft.Container) and control.bgcolor == ft.colors.with_opacity(0.5, ft.colors.BLACK):
                    page.overlay.remove(control)
                    break
            page.overlay.pop()  # Remove the popup
        page.update()

    def volunteer(e):
        update_volunteer_status(page, event.get("id"))
        close_popup(e)

    # Form layout matching join_event_form.py
    form = ft.Column(
        controls=[
            ft.Text(f"Volunteer for: {event.get('name', 'Unnamed Event')}", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
            ft.Text(f"Date: {event.get('date', 'N/A')}", color="#FDF7E3"),
            ft.Text(f"Region: {event.get('location', 'N/A')}", color="#FDF7E3"),
            ft.Text(f"Category: {event.get('type', 'Unknown')}", color="#FDF7E3"),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Volunteer",
                        on_click=volunteer,
                        bgcolor="#C77000",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        )
                    ),
                    ft.ElevatedButton(
                        "Back",
                        on_click=close_popup,
                        bgcolor="#C77000",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        )
                    )
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    header_height = 100  # Height of your header
    popup = ft.Container(
        alignment=ft.alignment.center,
        bgcolor="rgba(0,0,0,0.5)",  # Semi-transparent overlay background
        width=page.width,
        height=page.height - header_height,  # Only cover below the header
        top=header_height,  # Position overlay below the header
        content=ft.Container(
            width=380,
            height=400,
            padding=ft.padding.all(20),
            border_radius=10,
            bgcolor="#406157",  # Matching popup color
            border=ft.border.all(3, "white"),
            content=form,
        ),
    )


    # Add a blur overlay that starts below the header
    header_height = 100  # Height of the header
    blur_overlay = ft.Container(
        bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
        width=page.width,
        height=page.height - header_height,  # Adjust height to not cover the header
        top=header_height,  # Position the overlay below the header
        left=0,
        on_click=close_popup  # Close popup when clicking outside
    )

    # Add the blur overlay and popup to the page overlay
    page.overlay.append(blur_overlay)
    page.overlay.append(popup)
    page.update()