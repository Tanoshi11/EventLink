import flet as ft
from controller.login_controller import main as login_main

def main(page: ft.Page):
    """Initialize the application with the login page."""
    login_main(page)

if __name__ == "__main__":
    ft.app(target=main)
