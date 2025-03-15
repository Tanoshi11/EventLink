import flet as ft

class JoinEventView:
    def __init__(self, model, submit_callback, close_callback):
        self.model = model
        self.submit_callback = submit_callback
        self.close_callback = close_callback

        self.event_attend_name = ft.TextField(
            label="Name",
            width=300,
            text_style=ft.TextStyle(color="#FDF7E3"),
            label_style=ft.TextStyle(color="#FDF7E3"),
            border_color="#D4A937",
            hint_text="Enter your name"
        )

        self.event_ticket_tobuy = ft.TextField(
            label="Number of tickets",
            width=300,
            text_style=ft.TextStyle(color="#FDF7E3"),
            label_style=ft.TextStyle(color="#FDF7E3"),
            border_color="#D4A937",
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="Enter a number"
        )

        self.form = ft.Column(
            controls=[
                ft.Text(f"Join Event: {model.title}", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
                ft.Text(f"Date: {model.date}", color="#FDF7E3"),
                ft.Text(f"Time: {model.time}", color="#FDF7E3"),
                ft.Text(f"Available slots: {model.available_slots}", color="#FDF7E3"),
                self.event_attend_name,
                self.event_ticket_tobuy,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Submit",
                            on_click=self.submit_callback,
                            bgcolor="#C77000",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        ),
                        ft.ElevatedButton(
                            "Back",
                            on_click=self.close_callback,
                            bgcolor="#C77000",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.popup = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=380,
                        height=480,
                        padding=ft.padding.all(20),
                        border_radius=10,
                        bgcolor="#406157",
                        border=ft.border.all(3, "white"),
                        content=self.form,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            top=230,
            left=630,
        )

    def get_view(self):
        return self.popup
