import flet as ft

class LoginView:
    def __init__(self, controller):
        self.controller = controller

    def build(self, page: ft.Page):
        page.title = "EventLink - Login"
        page.bgcolor = "#0C3B2E"

        self.login_identifier = ft.TextField(
            label="Username or Email",
            label_style=ft.TextStyle(color="#EAE3D2"),
            text_style=ft.TextStyle(color="#F5E7C4"),
            width=500,
            border_color="#D4A937",
            border_radius=10,
            content_padding=ft.padding.all(10)
        )
        self.login_identifier_error = ft.Text("", color="red", size=12)

        self.login_password = ft.TextField(
            label="Password",
            label_style=ft.TextStyle(color="#EAE3D2"),
            text_style=ft.TextStyle(color="#F5E7C4"),
            width=500,
            password=True,
            border_color="#D4A937",
            border_radius=10,
            content_padding=ft.padding.all(10)
        )
        self.login_password_error = ft.Text("", color="red", size=12)

        self.login_message = ft.Text("", color="red")
        self.login_message_container = ft.Container(content=self.login_message, margin=ft.margin.only(top=5))

        self.login_button = ft.ElevatedButton(
            "Login",
            on_click=self.controller.login,
            bgcolor="#C77000",
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            width=100
        )

        self.login_to_signup = ft.TextButton(
            content=ft.Text(
                "Don't have an account? Sign up here",
                color="#FDF7E3",
                style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
            )
        )
        self.login_to_signup.on_click = lambda e: self.controller.switch_view(page, "signup")

        login_view = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
                    margin=ft.margin.only(bottom=10)
                ),
                ft.Column(controls=[self.login_identifier, self.login_identifier_error], spacing=2),
                ft.Column(controls=[self.login_password, self.login_password_error], spacing=2),
                self.login_button,
                self.login_message_container,
                self.login_to_signup
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )

        login_view_container = ft.Container(
            content=login_view,
            alignment=ft.alignment.center_left,
            width=550,
            margin=ft.margin.only(left=150, top=150, bottom=150),
            bgcolor="#5F7755",
            border_radius=20,
            padding=ft.padding.all(20)
        )

        logo_image = ft.Image(
            src="images/eventlink.png",
            width=500,
            height=500,
            fit=ft.ImageFit.CONTAIN
        )
        logo_container = ft.Container(
            content=logo_image,
            alignment=ft.alignment.center_right,
            expand=True,
            margin=ft.margin.only(left=150, right=250, bottom=100)
        )

        row = ft.Row(
            controls=[login_view_container, logo_container],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        page.controls.clear()
        page.add(row)
        page.update()
