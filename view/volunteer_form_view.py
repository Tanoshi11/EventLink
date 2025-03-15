import flet as ft

class VolunteerFormView:
    def __init__(self, controller):
        self.controller = controller

    def show_volunteer_popup(self, page, event):
        """Show a popup with event details and options to Volunteer or Back."""
        def close_popup(e):
            if page.overlay:
                for control in page.overlay:
                    if isinstance(control, ft.Container) and control.bgcolor == ft.colors.with_opacity(0.5, ft.colors.BLACK):
                        page.overlay.remove(control)
                        break
                page.overlay.pop()
            page.update()

        def volunteer(e):
            self.controller.update_volunteer_status(page)
            close_popup(e)

        form = ft.Column(
            controls=[
                ft.Text(f"Volunteer for: {event.get('name', 'Unnamed Event')}", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
                ft.Text(f"Date: {event.get('date', 'N/A')}", color="#FDF7E3"),
                ft.Text(f"Region: {event.get('location', 'N/A')}", color="#FDF7E3"),
                ft.Text(f"Category: {event.get('type', 'Unknown')}", color="#FDF7E3"),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Volunteer", on_click=volunteer, bgcolor="#C77000", color="white"),
                        ft.ElevatedButton("Back", on_click=close_popup, bgcolor="#C77000", color="white"),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )

        popup = ft.Container(
            alignment=ft.alignment.center,
            bgcolor="rgba(0,0,0,0.5)",
            width=page.width,
            height=page.height - 100,
            top=100,
            content=ft.Container(
                width=380,
                height=400,
                padding=ft.padding.all(20),
                border_radius=10,
                bgcolor="#406157",
                border=ft.border.all(3, "white"),
                content=form,
            ),
        )

        blur_overlay = ft.Container(
            bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            width=page.width,
            height=page.height - 100,
            top=100,
            left=0,
            on_click=close_popup
        )

        page.overlay.append(blur_overlay)
        page.overlay.append(popup)
        page.update()
