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

def load_signup(page: ft.Page):
    page.title = "EventLink - Sign Up"
    page.bgcolor = "#0C3B2E"  
    
    # --------------------
    # Build Sign Up Form Fields
    # --------------------
    signup_username = ft.TextField(
        label="Username",
        label_style=ft.TextStyle(color="#EAE3D2"),
        text_style=ft.TextStyle(color="#F5E7C4"),
        width=500,
        border_color="#D4A937",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )
    signup_email = ft.TextField(
        label="Email",
        label_style=ft.TextStyle(color="#EAE3D2"),
        text_style=ft.TextStyle(color="#F5E7C4"),
        width=500,
        border_color="#D4A937",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )
    signup_contact = ft.TextField(
        label="Contact Number",
        label_style=ft.TextStyle(color="#EAE3D2"),
        text_style=ft.TextStyle(color="#F5E7C4"),
        width=500,
        border_color="#D4A937",
        border_radius=10,
        content_padding=ft.padding.all(10),
        input_filter=ft.InputFilter(
            regex_string=r"\d",  # Allow only digits
            allow=True
        ),
        max_length=11  # Limit input to 11 characters
    )
    signup_password = ft.TextField(
        label="Password",
        label_style=ft.TextStyle(color="#EAE3D2"),
        text_style=ft.TextStyle(color="#F5E7C4"),
        width=500,
        password=True,
        border_color="#D4A937",
        border_radius=10,
        content_padding=ft.padding.all(10)
    )
    
    # Error messages for each field
    username_error = ft.Text("", color="red", size=12)
    email_error = ft.Text("", color="red", size=12)
    contact_error = ft.Text("", color="red", size=12)
    password_error = ft.Text("", color="red", size=12)
    
    signup_message_container = ft.Container(margin=ft.margin.only(top=5))
    
    def signup(e):
        # Reset errors and borders
        username_error.value = ""
        email_error.value = ""
        contact_error.value = ""
        password_error.value = ""
        signup_username.border_color = "#FFBA00"
        signup_email.border_color = "#FFBA00"
        signup_contact.border_color = "#FFBA00"
        signup_password.border_color = "#FFBA00"
        
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
        elif len(signup_contact.value.strip()) != 11:
            contact_error.value = "Contact number must be exactly 11 digits."
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
            switch_view(page, "login")
        except httpx.HTTPStatusError as exc:
            error_detail = exc.response.json()["detail"]
            # Reset any prior messages
            username_error.value = ""
            email_error.value = ""
            signup_message_container.content = None
            if "Username and Email" in error_detail:
                username_error.value = "Username already exists"
                signup_username.border_color = "red"
                email_error.value = "Email already exists"
                signup_email.border_color = "red"
            else:
                if "Username" in error_detail:
                    username_error.value = "Username already exists"
                    signup_username.border_color = "red"
                if "Email" in error_detail:
                    email_error.value = "Email already exists"
                    signup_email.border_color = "red"
            if not ("Username" in error_detail or "Email" in error_detail):
                signup_message_container.content = ft.Text(error_detail, color="red")
            page.update()
    
    signup_button = ft.ElevatedButton(
        "Sign Up",
        on_click=signup,
        bgcolor="#C77000",   # Button background
        color="white",       # Button text color
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    signup_button.width = 100
    
    signup_to_login = ft.TextButton(
        content=ft.Text(
            "Already have an account? Log in here",
            color="#F5E7C4",  # Accent color for links
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        )
    )
    signup_to_login.on_click = lambda e: switch_view(page, "login")
    
    signup_view = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Sign Up", size=24, weight=ft.FontWeight.BOLD, color="#F5E7C4"),
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
        margin=ft.margin.only(left=150, top=80, bottom=80),
        bgcolor="#6D9773",   # Form container background
        border_radius=20,
        padding=ft.padding.all(20)
    )
    
    # --------------------
    # Build Logo Container (similar to login page)
    # --------------------
    logo_image = ft.Image(
        src="eventlink.png",  # Ensure your logo file is in the project directory.
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
    
    def switch_view(page: ft.Page, view: str):
        if view == "login":
            import login
            login.load_login(page)
        elif view == "signup":
            load_signup(page)
    
    # --------------------
    # Arrange the Sign Up Form and Logo
    # --------------------
    page.controls.clear()
    row = ft.Row(
        controls=[signup_view_container, logo_container],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    page.add(row)
    page.update()

if __name__ == "__main__":
    ft.app(target=load_signup)
