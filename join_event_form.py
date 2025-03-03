import flet as ft

def load_join_event_form(page, event_id, title, date, time, back_callback):
    # Clear the current controls or open a modal dialog
    page.controls.clear()
    
   
    event_attend_name = ft.TextField(label="Name", width=400)
    
    event_ticket_tobuy = ft.TextField(label="Number of tickets", width=400, keyboard_type=ft.KeyboardType.NUMBER)
    
    def submit_form(e):
        error_found = False
        # Validate the name field.
        if not event_attend_name.value:
            event_attend_name.error_text = "Name is required."
            error_found = True
        else:
            event_attend_name.error_text = None
        
        # Validate the number of tickets: must be non-empty and numeric.
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
    
    # Build the join event form with Back and Submit buttons.
    form = ft.Column(
        controls=[
            ft.ElevatedButton("Back", on_click=lambda e: back_callback(page)),
            ft.Text(f"Join Event: {title}", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(f"Date: {date}"),
            ft.Text(f"Time: {time}"),
            event_attend_name,
            event_ticket_tobuy,
            ft.ElevatedButton("Submit", on_click=submit_form),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Wrap the form in a container to center it on the page.
    container = ft.Container(
        content=form,
        alignment=ft.alignment.center,
        expand=True,
    )
    
    page.add(container)
    page.update()

# Optional testing main function
if __name__ == "__main__":
    def back_callback(page):
        page.controls.clear()
        page.add(ft.Text("Back button pressed. Returning to previous page..."))
        page.update()
    
    def main(page: ft.Page):
        page.title = "Join the Event"
        page.bgcolor = "#5F7755"
        load_join_event_form(page, event_id=123, title="Test Event", date="2025-03-03", time="18:00", back_callback=back_callback)
    
    ft.app(target=main)
