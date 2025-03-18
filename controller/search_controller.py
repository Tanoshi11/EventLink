import threading
import time
import flet as ft
from datetime import datetime
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

    sidebar_controller = SidebarController(page)
    sidebar = sidebar_controller.build()

    def format_event(event):
        """Convert event API data into a proper format for the frontend."""
        title = event.get("title", "No Title")
        venue = event.get("venue", "No Venue")
        full_address = event.get("full_address", "No Address")
        location = venue  # Use venue instead of full address.

        date = event.get("date", "No Date")
        time_ = event.get("time", "No Time")
        event_id = event.get("_id", "No ID")
        link = event.get("link", "No Link")
        image = event.get("image", "No Image")
        available_slots = event.get("available_slots", 10000)

        return {
            "title": title,
            "venue": venue,  # Display venue instead of location
            "date": date,
            "time": time_,
            "event_id": str(event_id),
            "link": link,
            "image": image,
            "available_slots": available_slots,
        }   


    def load_events():
        time.sleep(0.2)
        events = fetch_events(query, search_type, location)
        results_list.controls.clear()

        if events:
            for ev in events:
                # Format the event data
                formatted_event = format_event(ev)

                # Determine event status
                event_date_str = formatted_event.get("date", None)
                event_time_str = formatted_event.get("time", None)
                available_slots = formatted_event.get("available_slots", 0)

                if event_date_str:
                    try:
                        event_datetime = datetime.strptime(event_date_str, "%Y-%m-%d")
                        is_past_event = event_datetime.date() < datetime.now().date()
                    except ValueError:
                        is_past_event = False
                else:
                    is_past_event = False

                is_closed = is_past_event or available_slots <= 0
                status_text = "Closed" if is_closed else "Open"

                # Create an event container with all details
                event_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(formatted_event["title"], size=22, color="white", weight=ft.FontWeight.BOLD),
                            ft.Divider(color="white"),
                            ft.Row(
                                controls=[
                                    ft.Image(src=formatted_event["image"], width=400, height=200),
                                    ft.Column(
                                        controls=[
                                            ft.Text(f"Date: {formatted_event['date']}", color="white"),
                                            ft.Text(f"Time: {formatted_event['time']}", color="white"),
                                            ft.Text(f"Venue: {formatted_event['venue']}", color="white"),  # Display venue
                                            ft.Text(f"Status: {status_text}", color="red" if is_closed else "green"),  # Display status
                                            ft.TextButton("Event Link", url=formatted_event["link"], icon_color="blue"),
                                        ],
                                        spacing=5
                                    )
                                ],
                                spacing=10
                            )
                        ],
                        spacing=10
                    ),
                    padding=10,
                    border_radius=10,
                    bgcolor="#105743",
                    ink=True,
                    on_click=lambda e, ev=ev: load_event_details(page, ev)
                )
                # Append the container to the results list
                results_list.controls.append(event_container)
                results_list.controls.append(ft.Divider(color="white"))
        else:
            # If no events are found, display a message
            results_list.controls.append(ft.Text("No events found.", size=20, color="white"))

        # Update the page to reflect changes
        page.update()


    main_stack = create_main_stack(header, sidebar, results_title, heading_divider, results_list)
    page.controls.clear()
    page.add(main_stack)
    page.update()

    threading.Thread(target=load_events, daemon=True).start()
