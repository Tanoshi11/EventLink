import flet as ft
from pymongo import MongoClient
import bcrypt

# Connect to MongoDB
client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/")
db = client["EventLink"]  # Replace with your database name
users_collection = db["users"]  # Collection to store users

# Function to check login credentials
def check_login(username, password):
    user = users_collection.find_one({"username": username})
    if user:
        stored_password = user["password"].encode()  # Convert string back to bytes
        if bcrypt.checkpw(password.encode(), stored_password):
            return True
    return False

<<<<<<< HEAD
# Function to register a new user with validations for empty fields.
def register_user(username, password):
    if not username and not password:
        return "Username and Password are required!"
    if not username:
        return "Username is required!"
    if not password:
=======
# Function to register a new user
def register_user(username, password):
    if not password:  # Ensure password is not empty
>>>>>>> 3645e807539396092d5f12af37a36706249e03df
        return "Password is required!"
    if users_collection.find_one({"username": username}):
        return "Username already exists!"
    
<<<<<<< HEAD
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed_password.decode()})
    return "Success"

# This function builds the login/signup views and loads them into the page.
def load_login(page: ft.Page):
=======
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  
    users_collection.insert_one({"username": username, "password": hashed_password.decode()})  # Store as string
    return "Success"

def main(page: ft.Page):
>>>>>>> 3645e807539396092d5f12af37a36706249e03df
    page.title = "Login & Signup System"

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
        if check_login(login_username.value, login_password.value):
            import homepg
            homepg.main(page)
        else:
            login_message.value = "Invalid Username or Password!"
            login_message.color = "red"
            page.update()

    login_button = ft.ElevatedButton("Login", on_click=login)
    login_button.width = 90
    login_button_container = ft.Container(content=login_button, margin=ft.margin.only(left=5))
    # Placeholder; on_click will be set later
    signup_redirect = ft.TextButton("Don't have an account? Sign up here")
    
    login_view = ft.Column([
        ft.Text("Login", size=20, weight=ft.FontWeight.BOLD),
        login_username,
        login_password,
        login_button_container,
        login_message_container,
        signup_redirect
    ], alignment=ft.MainAxisAlignment.CENTER)

    # The container expands to fill the page and aligns its content vertically centered and to the left.
    # Increased margin to move the interface further to the right.
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
    signup_message_container = ft.Container(content=signup_message, margin=ft.margin.only(left=5))
    
    def signup(e):
        result = register_user(signup_username.value, signup_password.value)
        if result == "Success":
            signup_message.value = "Signup Successful! Please log in."
            signup_message.color = "green"
            page.update()
            ft.dialog.alert("Signup Successful! Redirecting to login page...")
<<<<<<< HEAD
            switch_view(login_view_container)  # Redirect to login view after signup
=======
            show_login()  # Redirect to login page after signup
>>>>>>> 3645e807539396092d5f12af37a36706249e03df
        else:
            signup_message.value = result
            signup_message.color = "red"
        page.update()

    signup_button = ft.ElevatedButton("Sign Up", on_click=signup)
    signup_button.width = 90
    signup_button_container = ft.Container(content=signup_button, margin=ft.margin.only(left=5))
    # Placeholder; on_click will be set later
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
    logo = ft.Text("EventLink 🎉", size=85, weight=ft.FontWeight.BOLD, color="blue")
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
    
    # Set the on_click handlers for switching views in the text buttons.
    signup_redirect.on_click = lambda e: switch_view(signup_view_container)
    login_redirect_signup.on_click = lambda e: switch_view(login_view_container)
    
    # Start with the login view.
    switch_view(login_view_container)

def main(page: ft.Page):
    load_login(page)

if __name__ == "__main__":
    ft.app(target=main)
