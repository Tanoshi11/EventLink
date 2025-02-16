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

def main(page: ft.Page):
    page.window_full_screen = False
    page.window_maximized = True
    page.theme_mode = ft.ThemeMode.DARK  # Start in dark mode
    load_login(page)

def load_login(page: ft.Page):
    page.title = "EventLink"

    # --------------------
    # Build Login View
    # --------------------
    login_identifier = ft.TextField(
        label="Username or Email",
        label_style=ft.TextStyle(color="white"),  # label always white
        text_style=ft.TextStyle(color="white"),   # typed text white
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
        style=ft.ButtonStyle(
            side=ft.BorderSide(color="white", width=0.5)
        )
    )
    login_button.width = 100
    login_button.color = "white"
    login_to_signup = ft.TextButton(
        content=ft.Text(
            "Don't have an account? Sign up here",
            color="white",
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        )
    )

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
    # Build Signup View
    # --------------------
    signup_username = ft.TextField(
        label="Username",
        label_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        width=500,
        border_color="white",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )

    signup_email = ft.TextField(
        label="Email",
        label_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        width=500,
        border_color="white",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )

    signup_contact = ft.TextField(
        label="Contact Number",
        label_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        width=500,
        border_color="white",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )

    signup_password = ft.TextField(
        label="Password",
        label_style=ft.TextStyle(color="white"),
        text_style=ft.TextStyle(color="white"),
        width=500,
        password=True,
        border_color="white",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )

    username_error = ft.Text("", color="red", size=12)
    email_error = ft.Text("", color="red", size=12)
    contact_error = ft.Text("", color="red", size=12)
    password_error = ft.Text("", color="red", size=12)
    
    signup_message_container = ft.Container(margin=ft.margin.only(top=5))
    
    def signup(e):
        username_error.value = ""
        email_error.value = ""
        contact_error.value = ""
        password_error.value = ""
        signup_username.border_color = "white"
        signup_email.border_color = "white"
        signup_contact.border_color = "white"
        signup_password.border_color = "white"
        
        errors = []
        if not signup_username.value.strip():
            username_error.value = "Username is required!"
            signup_username.border_color = "red"
            errors.append(username_error.value)
        if not signup_email.value.strip():
            email_error.value = "Email is required!"
            signup_email.border_color = "red"
            errors.append(email_error.value)
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", signup_email.value.strip()):
            email_error.value = "Invalid email format. Use user@example.com."
            signup_email.border_color = "red"
            errors.append(email_error.value)
        if not signup_contact.value.strip():
            contact_error.value = "Contact number is required!"
            signup_contact.border_color = "red"
            errors.append(contact_error.value)
        elif not signup_contact.value.strip().isdigit():
            contact_error.value = "Contact number must contain only digits. (Ex. 09XXXXXXXXX)"
            signup_contact.border_color = "red"
            errors.append(contact_error.value)
        if not signup_password.value.strip():
            password_error.value = "Password is required!"
            signup_password.border_color = "red"
            errors.append(password_error.value)
        
        if errors:
            page.update()
            return

        user_data = {
            "username": signup_username.value,
            "email": signup_email.value,
            "contact": signup_contact.value,
            "password": signup_password.value
        }
        try:
            response = httpx.post("http://127.0.0.1:8000/register", json=user_data, timeout=10.0)
            response.raise_for_status()
            signup_message_container.content = ft.Text("Signup Successful! Please log in.", color="green")
            page.update()
            show_alert(page, "Signup Successful!", "Redirecting to login page...")
            switch_view(login_view_container)
        except httpx.HTTPStatusError as exc:
            error_detail = exc.response.json()["detail"]
            # Reset any prior messages
            username_error.value = ""
            email_error.value = ""
            signup_message_container.content = None
            
            # If the error says BOTH are taken:
            if "Username and Email" in error_detail:
                username_error.value = "Username already exists"
                signup_username.border_color = "red"
                email_error.value = "Email already exists"
                signup_email.border_color = "red"
            else:
                # Check partial matches:
                if "Username" in error_detail:
                    username_error.value = "Username already exists"
                    signup_username.border_color = "red"
                if "Email" in error_detail:
                    email_error.value = "Email already exists"
                    signup_email.border_color = "red"

            # If there's any other error detail, show it in a general container:
            if not ("Username" in error_detail or "Email" in error_detail):
                signup_message_container.content = ft.Text(error_detail, color="red")

            page.update()

    
    signup_button = ft.ElevatedButton(
        "Sign Up",
        on_click=signup,
        style=ft.ButtonStyle(side=ft.BorderSide(color="white", width=0.5)),
        color="white"
    )
    signup_button.width = 100
    signup_to_login = ft.TextButton(
        content=ft.Text(
            "Already have an account? Log in here",
            color="white",
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        )
    )
    signup_to_login.on_click = lambda e: switch_view(login_view_container)
    
    signup_view = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Sign Up", size=24, weight=ft.FontWeight.BOLD, color="white"),
                margin=ft.margin.only(bottom=10)
            ),
            ft.Column(controls=[signup_username, username_error], spacing=2),
            ft.Column(controls=[signup_email, email_error], spacing=2),
            ft.Column(controls=[signup_contact, contact_error], spacing=2),
            ft.Column(controls=[signup_password, password_error], spacing=2),
            signup_button,
            signup_message_container,
            signup_to_login
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    )
    signup_view_container = ft.Container(
        content=signup_view,
        alignment=ft.alignment.center_left,
        width=550,
        margin=ft.margin.only(left=150)
    )
    
    # --------------------
    # Build Logo Container
    # --------------------
    logo = ft.Text("EventLink🎉", size=85, weight=ft.FontWeight.BOLD, color="blue")
    logo_container = ft.Container(
        content=logo,
        alignment=ft.alignment.center_right,
        expand=True,
        margin=ft.margin.only(right=170, bottom=100)
    )
    
    def switch_view(view_container):
        row = ft.Row(
            controls=[view_container, logo_container],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        page.controls.clear()
        page.add(row)
        page.update()
    
    login_to_signup.on_click = lambda e: switch_view(signup_view_container)
    
    switch_view(login_view_container)

if __name__ == "__main__":
    ft.app(target=main)
