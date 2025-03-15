import flet as ft
import httpx

# Global variable for the notifications popup
notif_popup = None

def clear_overlay(page: ft.Page):
    """Clear the overlay (e.g., join event form) from the page."""
    if page.overlay:
        page.overlay.clear()
        page.update()

def get_regions():
    """Fetch regions from the server."""
    try:
        response = httpx.get("http://localhost:8000/regions")
        if response.status_code == 200:
            regions = response.json()["regions"]
            print("Fetched regions:", regions)  # Debug print
            return regions
    except Exception as ex:
        print("Error fetching regions:", ex)
    return []

def load_header(page: ft.Page):
    global notif_popup

    # ----------------- Header Functions -----------------

    def search_events(e):
        """Trigger search when the user selects a region or presses Enter."""
        query = search_bar.value.strip() if search_bar.value else "All"
        location = region_dropdown.value

        # Debugging: Print the query and location
        print(f"Search triggered - Query: '{query}', Region: '{location}'")

        # Call load_search in search.py directly
        from controller.search_controller import load_search
        load_search(page, query, search_type="global", location=location)

    # ----------------- Build the Header UI -----------------
    # Fetch regions from the server
    regions = get_regions()

    # Create the dropdown with all regions
    region_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(region) for region in regions],
        hint_text="Select Region",
        hint_style=ft.TextStyle(size=17, color="white"),
        expand=True,
        border_color="white",
        bgcolor="#a8730a", 
        color="white",  # White text
        #menu_height=320,
    )

    search_bar = ft.TextField(
        hint_text="Search events",
        border=None,
        expand=True,
        text_style=ft.TextStyle(size=17, color="white"),
        hint_style=ft.TextStyle(size=17, color="white"),
        border_radius=5,
        border_color="white",
        on_submit=search_events  # Trigger search when pressing Enter
    )

    header = ft.Row(
        controls=[
            ft.Container(width=15),
            # Search & Location container
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SEARCH, color="white", size=30),
                        search_bar,
                        ft.VerticalDivider(width=1, color="white"),
                        ft.Icon(name=ft.Icons.LOCATION_ON, color="white", size=30),
                        region_dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                border_radius=15,
                border=ft.border.all(1, "white"),
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                expand=True,
                bgcolor="#a8730a",
                margin=ft.margin.only(top=16, bottom=16, right=30)
            ),
        ]
    )

    taskbar = ft.Container(
        content=header,
        height=100,
        bgcolor="#4d3a17",
        alignment=ft.alignment.center_right,
        padding=ft.padding.symmetric(horizontal=10),
        margin=ft.margin.only(left=240)
    )
    return taskbar