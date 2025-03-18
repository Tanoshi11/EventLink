import threading
import time
import flet as ft
from model.search_model import fetch_events, get_event_status
from view.search_view import create_results_view, create_main_stack, clear_overlay, load_event_details
# from controller.category_list_controller import CategoryListController
from controller.sidebar_controller import SidebarController

def get_header_controller():
    from header import load_header  
    return load_header

def load_search(page, query, search_type="global", location=None):
    clear_overlay(page)
    if page.data is None:
        page.data = {}

    page.data["query"] = query
    page.data["search_type"] = search_type
    page.data["location"] = location

    if search_type == "category":
        heading_text = f"Category: {query}"
    elif location:
        heading_text = f"Search Results: {query} ; Region: {location}"
    else:
        heading_text = f"Search Results: {query}"

    page.title = heading_text
    page.bgcolor = "#d6aa54"

    results_title, heading_divider, results_list = create_results_view(heading_text)
    header = get_header_controller()(page)  

    # ✅ Initialize sidebar and category list inside function
    sidebar_controller = SidebarController(page)
    sidebar = sidebar_controller.build()

    # category_list_controller = CategoryListController(page)
    # categories = category_list_controller.build()

    def load_events():
        time.sleep(0.2)
        events = fetch_events(query, search_type, location)
        results_list.controls.clear()

        if events:
            for ev in events:
                event_status = get_event_status(ev.get("date", ""), ev.get("time", ""))
                status_color = {
                    "Upcoming": "#4CAF50",
                    "Ongoing": "#FFEB3B",
                    "Closed": "#FF5252"
                }.get(event_status, "white")

                event_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(ev.get("name", "Unnamed Event"), size=22, color="white", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Status: {event_status}", color=status_color, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Date: {ev.get('date', '')}", color="white"),
                            ft.Text(f"Time: {ev.get('time', '')}", color="white"),
                            ft.Text(f"Region: {ev.get('location', '')}", color="white"),
                            ft.Text(f"Category: {ev.get('type', 'Unknown')}", color="white"),
                        ],
                        spacing=5
                    ),
                    padding=10,
                    border_radius=10,
                    bgcolor="#105743",
                    ink=True,
                    on_click=lambda e, ev=ev: load_event_details(page, ev)
                )
                results_list.controls.append(event_container)
                results_list.controls.append(ft.Divider(color="white"))
        else:
            results_list.controls.append(ft.Text("No events found.", size=20, color="white"))

        page.update()

    main_stack = create_main_stack(header, sidebar, results_title, heading_divider, results_list) # no categories
    page.controls.clear()
    page.add(main_stack)
    page.update()

    threading.Thread(target=load_events, daemon=True).start()