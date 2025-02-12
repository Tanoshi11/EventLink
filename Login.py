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

# Function to register a new user
def register_user(username, password):
    if not password:  # Ensure password is not empty
        return "Password is required!"
    if users_collection.find_one({"username": username}):
        return "Username already exists!"
    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  
    users_collection.insert_one({"username": username, "password": hashed_password.decode()})  # Store as string
    return "Success"

def main(page: ft.Page):
    page.title = "Login & Signup System"
    
    def show_login(e=None):
        page.controls.clear()
        page.add(login_view)
        page.update()

    def show_signup(e=None):
        page.controls.clear()
        page.add(signup_view)
        page.update()
    
    # Login Page
    login_username = ft.TextField(label="Username")
    login_password = ft.TextField(label="Password", password=True)
    login_message = ft.Text("", color="red")

    def login(e):
        if check_login(login_username.value, login_password.value):
            login_message.value = "Login Successful!"
            login_message.color = "green"
        else:
            login_message.value = "Invalid Username or Password!"
            login_message.color = "red"
        page.update()

    login_button = ft.ElevatedButton("Login", on_click=login)
    signup_redirect = ft.TextButton("Don't have an account? Sign up here", on_click=show_signup)

    login_view = ft.Column([
        ft.Text("Login", size=20, weight=ft.FontWeight.BOLD),
        login_username, login_password, login_button, login_message, signup_redirect
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    # Signup Page
    signup_username = ft.TextField(label="Username")
    signup_password = ft.TextField(label="Password", password=True)
    signup_message = ft.Text("", color="red")

    def signup(e):
        result = register_user(signup_username.value, signup_password.value)
        if result == "Success":
            signup_message.value = "Signup Successful! Please log in."
            signup_message.color = "green"
            page.update()
            ft.dialog.alert("Signup Successful! Redirecting to login page...")
            show_login()  # Redirect to login page after signup
        else:
            signup_message.value = result
            signup_message.color = "red"
        page.update()

    signup_button = ft.ElevatedButton("Sign Up", on_click=signup)
    login_redirect = ft.TextButton("Already have an account? Log in here", on_click=show_login)

    signup_view = ft.Column([
        ft.Text("Sign Up", size=20, weight=ft.FontWeight.BOLD),
        signup_username, signup_password, signup_button, signup_message, login_redirect
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Start with Login Page
    show_login()

ft.app(target=main)
