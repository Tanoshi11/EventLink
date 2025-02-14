import flet as ft
import httpx

def main(page: ft.Page):
    page.window_full_screen = False
    page.window_maximized = True
    load_login(page)

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
            # If login is successful, switch to the homepage.
            import homepg
            homepg.main(page)
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
            ft.dialog.alert("Signup Successful! Redirecting to login page...")
            switch_view(login_view_container)
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
    # Replace this Text with an Image widget if you have a logo file.
    logo = ft.Text("EventLink🎉", size=85, weight=ft.FontWeight.BOLD, color="blue")
    logo_container = ft.Container(
        content=logo,
        alignment=ft.alignment.center_right,
        expand=True,
        margin=ft.margin.only(right=170, bottom=100)
    )
    
    # --- Define a helper function to switch views.
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
    
    # Start with the login view.
    switch_view(login_view_container)

if __name__ == "__main__":
    ft.app(target=main)
