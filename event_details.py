import flet as ft
import httpx
from datetime import datetime
from controller.search_controller import load_search
from header import load_header
from view.sidebar_view import SidebarView  # Import SidebarView
from controller.sidebar_controller import SidebarController  # Import SidebarController
from utils import clear_overlay
from controller.join_event_form_controller import JoinEventController
def load_event_details(page: ft.Page, event: dict, search_context: dict):
    if page.data is None:
        page.data = {}
    page.data["search_context"] = search_context
    page.controls.clear()

    # ----------------- Taskbar (Header) -----------------
    taskbar = load_header(page)

    # ----------------- Sidebar (Categories) -----------------
    sidebar_controller = SidebarController(page)  # ✅ Pass the page correctly
    sidebar = SidebarView(controller=sidebar_controller)  # Initialize SidebarView with the controller
    sidebar_content = sidebar.build(page)  # Build the sidebar content

    # ----------------- Event Details Content -----------------
    event_title_text = event.get("title", "Unnamed Event")
    event_date = event.get("date_time", "N/A")
    event_time = event.get("time", "N/A")
    date_time = event.get("date_time", "N/A")
    event_venue = event.get("venue", "N/A")
    event_description_text = event.get("description", "No description available.")

    # Determine event status
    event_status_text = "Unknown"
    status_color = "white"
    if event_date and event_time:
        try:
            event_datetime_str = f"{event_date} {event_time}"
            event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %I:%M %p")
            now = datetime.now()

            if event_datetime < now:
                event_status_text = "Closed"
                status_color = "#FF5252"
            elif event_datetime.date() == now.date():
                event_status_text = "Ongoing"
                status_color = "#FFEB3B"
            else:
                event_status_text = "Upcoming"
                status_color = "#4CAF50"
        except ValueError as e:
            print(f"Error parsing date or time: {e}")
            event_status_text = "Invalid Date/Time"
    
    event_title = ft.Text(
        event_title_text,
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.LEFT,
    )

    title_divider = ft.Divider(color="white", thickness=1)

    event_image = ft.Image(
        src=event.get("image", "default_event_image.jpg"),
        width=300,
        height=200,
        fit=ft.ImageFit.COVER,
        border_radius=20,
    )

    event_details = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Date & Time:", size=20, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(date_time, size=20, color="white"),
                ],
                spacing=5,
            ),
            ft.Row(
                controls=[
                    ft.Text("Venue:", size=20, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(event_venue, size=20, color="white"),
                ],
                spacing=5,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )


    image_details_row = ft.Row(
        controls=[event_image, event_details],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    event_description = ft.Column(
        controls=[
            ft.Text("Description:", size=20, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text(
                event_description_text,
                size=18,
                color="white",
                text_align=ft.TextAlign.LEFT,
            ),
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.START,
    )


    def join_event(e):
        """Open the join event form."""
        print("🔍 Opening join event form...")  # Debugging

        # Ensure overlay isn't duplicated
        blur_overlay = ft.Container(
            bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            expand=True
        )
        page.overlay.append(blur_overlay)

        # ✅ Correct way to open the Join Event form
        join_controller = JoinEventController(
            page,
            event_id=event.get("id", "N/A"),
            title=event.get("title", "Unnamed Event"),
            date=event.get("date", "N/A"),
            time=event.get("time", "N/A"),
            available_slots=event.get("guest_limit", "N/A"),
            join_callback=update_join_button
        )
        join_controller.show_form()  # ✅ This properly displays the form

        page.update()


    def close_popup(page_instance=None):
        if page.overlay:
            for control in page.overlay:
                if isinstance(control, ft.Container) and control.bgcolor == ft.colors.with_opacity(
                    0.5, ft.colors.BLACK
                ):
                    page.overlay.remove(control)
                    break
        JoinEventController.close_join_popup(page)
        page.update()

    def update_join_button():
        buttons_row.controls.remove(join_event_button)
        joined_text = ft.Text("Joined Event", size=15, color="white", weight="bold")
        buttons_row.controls.insert(0, joined_text)
        page.data["joined_event"] = True
        page.update()

    username = page.data.get("username")
    response = httpx.get(f"http://localhost:8000/my_events?username={username}")
    if response.status_code == 200:
        user_events = response.json().get("events", [])
        if any(event.get("name") == e.get("name") for e in user_events):
            join_event_button = ft.Text("Joined Event", size=15, color="white", weight="bold")
        else:
            join_event_button = ft.ElevatedButton(
                text="Join Event",
                on_click=join_event,
                bgcolor="#C77000",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            )
    else:
        join_event_button = ft.ElevatedButton(
            text="Join Event",
            on_click=join_event,
            bgcolor="#C77000",
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )

    back_to_search_button = ft.ElevatedButton(
        text="Back to Search",
        on_click=lambda e: go_back_to_search(page),
        bgcolor="#C77000",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    # back_to_home_button = ft.ElevatedButton(
    #     text="Back to Home",
    #     on_click=lambda e: go_back_to_homepage(page),
    #     bgcolor="#C77000",
    #     color="white",
    #     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    # )

    container_color = "#21582F"
    button_color = "#C77000"
    buttons_row = ft.Row(
        controls=[
            back_to_search_button,
            # back_to_home_button
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.END
    )

    if event_status_text != "Closed":
        buttons_row.controls.insert(0, join_event_button)

    event_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(event.get("title", "Unnamed Event"), size=24, weight="bold", color="white"),
                ft.Divider(color="white"),
                image_details_row,
                ft.Divider(color="white"),
                event_description,
                ft.Container(
                    content=buttons_row,
                    margin=ft.margin.only(top=20)
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        bgcolor=container_color,
        padding=20,
        border_radius=10,
        expand=True,
        height=page.height * 0.8
    )

    main_content = ft.Container(
        content=event_container,
        margin=ft.margin.only(left=270, top=120, right=40),
        expand=True
    )

    main_stack = ft.Stack(
        controls=[
            main_content,
            taskbar,
            sidebar_content,  # Use the sidebar content here
        ],
        expand=True
    )

    page.add(main_stack)
    page.update()

def go_back_to_search(page: ft.Page):
    """Go back to the search page and clear the overlay."""
    clear_overlay(page)  # Clear the overlay before navigating
    search_context = page.data.get("search_context", {})
    query = search_context.get("query", "All")
    search_type = search_context.get("search_type", "global")
    location = search_context.get("location", None)
    import controller.search_controller as search
    search.load_search(page, query=query, search_type=search_type, location=location)

# def go_back_to_homepage(page: ft.Page):
#     """Go back to the homepage and clear the overlay."""
#     clear_overlay(page)  # Clear the overlay before navigating
#     import controller.homepg_controller as homepg
#     homepg.load_homepage(page)