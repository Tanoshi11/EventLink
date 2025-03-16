import flet as ft

class SignupView:
    def __init__(self, controller):
        self.controller = controller

    def build(self, page: ft.Page):
        page.title = "EventLink - Sign Up"
        page.bgcolor = "#0C3B2E"

        self.signup_username = ft.TextField(
            label="Username",
            label_style=ft.TextStyle(color="#EAE3D2"),
            text_style=ft.TextStyle(color="#F5E7C4"),
            width=500,
            border_color="#D4A937",
            border_radius=10,
            content_padding=ft.padding.all(10)
        )
        self.signup_email = ft.TextField(
            label="Email",
            label_style=ft.TextStyle(color="#EAE3D2"),
            text_style=ft.TextStyle(color="#F5E7C4"),
            width=500,
            border_color="#D4A937",
            border_radius=10,
            content_padding=ft.padding.all(10)
        )
        self.signup_contact = ft.TextField(
            label="Contact Number",
            label_style=ft.TextStyle(color="#EAE3D2"),
            text_style=ft.TextStyle(color="#F5E7C4"),
            width=500,
            border_color="#D4A937",
            border_radius=10,
            content_padding=ft.padding.all(10),
            input_filter=ft.InputFilter(
                regex_string=r"\d", allow=True
            ),
            max_length=11
        )
        self.signup_password = ft.TextField(
            label="Password",
            label_style=ft.TextStyle(color="#EAE3D2"),
            text_style=ft.TextStyle(color="#F5E7C4"),
            width=500,
            password=True,
            border_color="#D4A937",
            border_radius=10,
            content_padding=ft.padding.all(10)
        )

        self.username_error = ft.Text("", color="red", size=12)
        self.email_error = ft.Text("", color="red", size=12)
        self.contact_error = ft.Text("", color="red", size=12)
        self.password_error = ft.Text("", color="red", size=12)

        self.signup_message_container = ft.Container(margin=ft.margin.only(top=5))

        self.signup_button = ft.ElevatedButton(
            "Sign Up",
            on_click=self.controller.signup,
            bgcolor="#C77000",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        self.signup_button.width = 100

        self.signup_to_login = ft.TextButton(
            content=ft.Text(
                "Already have an account? Log in here",
                color="#FDF7E3",
                style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
            )
        )
        self.signup_to_login.on_click = self.controller.switch_to_login

        signup_view = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Sign Up", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
                    margin=ft.margin.only(bottom=10)
                ),
                ft.Column(controls=[self.signup_username, self.username_error], spacing=2),
                ft.Column(controls=[self.signup_email, self.email_error], spacing=2),
                ft.Column(controls=[self.signup_contact, self.contact_error], spacing=2),
                ft.Column(controls=[self.signup_password, self.password_error], spacing=2),
                self.signup_button,
                self.signup_message_container,
                self.signup_to_login
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )

        signup_view_container = ft.Container(
            content=signup_view,
            alignment=ft.alignment.center_left,
            width=550,
            margin=ft.margin.only(left=150, top=80, bottom=80),
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
            controls=[signup_view_container, logo_container],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        page.controls.clear()
        page.add(row)
        page.update()
