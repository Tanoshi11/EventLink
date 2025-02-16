import flet as ft
import httpx
import re  # For email validation

def show_alert(page, title, content):
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(page))]
    )
    page.dialog = dialog
    page.dialog.open = True
    page.update()

def close_dialog(page):
    page.dialog.open = False
    page.update()

def load_login(page: ft.Page):
    page.title = "EventLink - Login"

    # --------------------
    # Build Login View
    # --------------------
    login_identifier = ft.TextField(
        label="Username or Email",
        label_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        width=500,
        border_color="white",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )
    login_identifier_error = ft.Text("", color="red", size=12)

    login_password = ft.TextField(
        label="Password",
        label_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        width=500,
        password=True,
        border_color="white",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )
    login_password_error = ft.Text("", color="red", size=12)

    login_message = ft.Text("", color="red")
    login_message_container = ft.Container(content=login_message, margin=ft.margin.only(top=5))
    
    def login(e):
        # Reset border colors and error labels
        login_identifier.border_color = "white"
        login_password.border_color = "white"
        login_identifier_error.value = ""
        login_password_error.value = ""
        login_message.value = ""
        
        errors = False
        if not login_identifier.value.strip():
            login_identifier_error.value = "Username or Email is required!"
            login_identifier.border_color = "red"
            errors = True
        if not login_password.value.strip():
            login_password_error.value = "Password is required!"
            login_password.border_color = "red"
            errors = True
        
        if errors:
            page.update()
            return

        user_data = {
            "identifier": login_identifier.value,
            "password": login_password.value
        }
        try:
            response = httpx.post("http://127.0.0.1:8000/login", json=user_data, timeout=10.0)
            response.raise_for_status()
            # Store the username in page.data for later use (e.g. profile view)
            page.data = {"username": login_identifier.value}
            import homepg
            homepg.main(page)
        except httpx.ConnectError:
            login_message.value = "Connection error: FastAPI server not available."
            login_message.color = "red"
            page.update()
        except httpx.HTTPStatusError as exc:
            login_message.value = f"Login failed: {exc.response.json()['detail']}"
            login_message.color = "red"
            page.update()
    
    login_button = ft.ElevatedButton(
        "Login",
        on_click=login,
        style=ft.ButtonStyle(side=ft.BorderSide(color="white", width=0.5))
    )
    login_button.width = 100
    login_button.color = "white"

    # Button to navigate to the signup view.
    login_to_signup = ft.TextButton(
        content=ft.Text(
            "Don't have an account? Sign up here",
            color="white",
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        )
    )
    login_to_signup.on_click = lambda e: switch_view(page, "signup")
    
    login_view = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="white"),
                margin=ft.margin.only(bottom=10)
            ),
            ft.Column(controls=[login_identifier, login_identifier_error], spacing=2),
            ft.Column(controls=[login_password, login_password_error], spacing=2),
            login_button,
            login_message_container,
            login_to_signup
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    )
    login_view_container = ft.Container(
        content=login_view,
        alignment=ft.alignment.center_left,
        width=550,
        margin=ft.margin.only(left=150)
    )
    
    # --------------------
    # Build Logo Container
    # --------------------
    logo_image = ft.Image(
        src="exlogo.png",  # Ensure "exlogo.png" is in your project directory.
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN
    )
    logo_container = ft.Container(
        content=logo_image,
        alignment=ft.alignment.center_right,
        expand=True,
        margin=ft.margin.only(right=250, bottom=100)
    )
    
    def switch_view(page: ft.Page, view: str):
        if view == "login":
            load_login(page)
        elif view == "signup":
            import signup
            signup.load_signup(page)
    
    # Arrange the login view and the logo in a row.
    row = ft.Row(
        controls=[login_view_container, logo_container],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    page.controls.clear()
    page.add(row)
    page.update()

if __name__ == "__main__":
    ft.app(target=load_login)
