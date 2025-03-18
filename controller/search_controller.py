import threading
import time
import re
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
        formatted_event = {
            "title": event.get("title", "No Title"),
            "venue": event.get("venue") or "No Venue",
            "date": event.get("date"),  # Keep as is (might be None)
            "time": event.get("time"),  # Keep as is (might be None)
            "date_time": event.get("date_time"),  # Get the original date_time string
            "event_id": str(event.get("_id", "No ID")),
            "link": event.get("link") or "No Link",
            "image": event.get("image") or "No Image",
            "available_slots": event.get("available_slots", 10000),
            "location": event.get("location") or "No Location" #add this in
        }

        # Extract date and time from the date_time string if date/time are None
        if formatted_event["date_time"]:
            # Use regular expression to extract date and time
            match = re.match(r"^(.*?)(\d{1,2}:\d{2} [AP]M)$", formatted_event["date_time"])
            if match:
                extracted_date = match.group(1).strip()
                extracted_time = match.group(2).strip()

                # Update date and time only if they are currently None
                if formatted_event["date"] is None:
                    formatted_event["date"] = extracted_date
                if formatted_event["time"] is None:
                    formatted_event["time"] = extracted_time

                formatted_event["date_time"] = f"{extracted_date} {extracted_time}" #recreate the field
            else:
                formatted_event["date_time"] = "Date/Time Not Available" # if all else fails

        else:
            formatted_event["date_time"] = "Date/Time Not Available"

        return formatted_event



    def load_events():
        time.sleep(0.2)
        events = fetch_events(query, search_type, location)
        
        print("Fetched Events:", events)  # Debugging statement
        
        results_list.controls.clear()

        if events:
            for ev in events:
                formatted_event = format_event(ev)
                print("Formatted Event:", formatted_event)  # Debugging statement

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
                                        ft.Text(f"Status: {status_text}", color="red" if is_closed else "green"),
                                        ft.Text(f"Date & Time: {formatted_event['date_time']}", color="white"),
                                        ft.Text(f"Venue: {formatted_event['venue']}", color="white"),
                                        ft.TextButton(
                                            "More Details",
                                            url=formatted_event["link"],
                                            style=ft.ButtonStyle(
                                                bgcolor="white",  # Button background color
                                                color="black",    # Text color
                                            ),
                                        )
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
