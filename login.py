import flet as ft
import httpx

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
    page.theme_mode = "dark"  # Enable dark mode
    
    load_login(page)  # Ensure this function is defined
    page.update()  # Apply the changes

def load_login(page: ft.Page):
    page.title = "EventLink"

    # --- Build Login View ---
    login_username = ft.TextField(
        label="Username",
        width=500,
        content_padding=ft.padding.only(left=20, top=8, bottom=8, right=8),
        border_color="white"
    )
    login_password = ft.TextField(
        label="Password",
        width=500,
        password=True,
        content_padding=ft.padding.only(left=20, top=8, bottom=8, right=8),
        border_color="white"
    )
    login_message = ft.Text("", color="red")
    login_message_container = ft.Container(content=login_message, margin=ft.margin.only(left=10))
    
    def login(e):
        user_data = {
            "username": login_username.value,
            "password": login_password.value
        }
        try:
            response = httpx.post("http://127.0.0.1:8000/login", json=user_data, timeout=10.0)
            response.raise_for_status()
            # On successful login, store the username for later use.
            page.data = {"username": login_username.value}
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
    
    login_button = ft.ElevatedButton("Login", on_click=login)
    login_button.width = 90
    login_button_container = ft.Container(content=login_button, margin=ft.margin.only(left=5))
    signup_redirect = ft.TextButton("Don't have an account? Sign up here")
    
    login_view = ft.Column([
        ft.Text("Login", size=20, weight=ft.FontWeight.BOLD),
        login_username,
        login_password,
        login_button_container,
        login_message_container,
        signup_redirect
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    login_view_container = ft.Container(
        content=login_view,
        alignment=ft.alignment.center_left,
        expand=False,
        width=520,
        margin=ft.margin.only(left=150)
    )
    
    # --- Build Signup View ---
    signup_username = ft.TextField(
        label="Username",
        width=500,
        content_padding=ft.padding.only(left=20, top=8, bottom=8, right=8),
        border_color="white"
    )
    signup_password = ft.TextField(
        label="Password",
        width=500,
        password=True,
        content_padding=ft.padding.only(left=20, top=8, bottom=8, right=8),
        border_color="white"
    )
    signup_message = ft.Text("", color="red")
    signup_message.width = 500
    signup_message_container = ft.Container(content=signup_message, margin=ft.margin.only(left=10))
    
    def signup(e):
        # Local validation for empty fields.
        if not signup_username.value.strip() and not signup_password.value.strip():
            signup_message.value = "Username and Password are required!"
            signup_message.color = "red"
            page.update()
            return
        elif not signup_username.value.strip():
            signup_message.value = "Username is required!"
            signup_message.color = "red"
            page.update()
            return
        elif not signup_password.value.strip():
            signup_message.value = "Password is required!"
            signup_message.color = "red"
            page.update()
            return

        user_data = {
            "username": signup_username.value,
            "password": signup_password.value
        }
        try:
            response = httpx.post("http://127.0.0.1:8000/register", json=user_data, timeout=10.0)
            response.raise_for_status()
            signup_message.value = "Signup Successful! Please log in."
            signup_message.color = "green"
            page.update()
            show_alert(page, "Signup Successful!", "Redirecting to login page...")
            switch_view(login_view_container)  # Redirect to login view after signup
        except httpx.HTTPStatusError as exc:
            signup_message.value = exc.response.json()["detail"]
            signup_message.color = "red"
        page.update()
    
    signup_button = ft.ElevatedButton("Sign Up", on_click=signup)
    signup_button.width = 90
    signup_button_container = ft.Container(content=signup_button, margin=ft.margin.only(left=5))
    login_redirect_signup = ft.TextButton("Already have an account? Log in here")
    
    signup_view = ft.Column([
        ft.Text("Sign Up", size=20, weight=ft.FontWeight.BOLD),
        signup_username,
        signup_password,
        signup_button_container,
        signup_message_container,
        login_redirect_signup
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    signup_view_container = ft.Container(
        content=signup_view,
        alignment=ft.alignment.center_left,
        expand=False,
        width=520,
        margin=ft.margin.only(left=150)
    )
    
    # --- Build Logo Container ---
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
    
    signup_redirect.on_click = lambda e: switch_view(signup_view_container)
    login_redirect_signup.on_click = lambda e: switch_view(login_view_container)
    
    switch_view(login_view_container)

if __name__ == "__main__":
    ft.app(target=main)
