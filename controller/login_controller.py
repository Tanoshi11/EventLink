import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import flet as ft
from model.login_model import LoginModel
from view.login_view import LoginView

class LoginController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = LoginModel()
        self.view = LoginView(self)

    def login(self, e):
        identifier = self.view.login_identifier.value.strip()
        password = self.view.login_password.value.strip()

        self.view.login_identifier.border_color = "#FFBA00"
        self.view.login_password.border_color = "#F5E7C4"
        self.view.login_identifier_error.value = ""
        self.view.login_password_error.value = ""
        self.view.login_message.value = ""

        errors = False
        if not identifier:
            self.view.login_identifier_error.value = "Username or Email is required!"
            self.view.login_identifier.border_color = "red"
            errors = True
        if not password:
            self.view.login_password_error.value = "Password is required!"
            self.view.login_password.border_color = "red"
            errors = True

        if errors:
            self.page.update()
            return

        response = self.model.authenticate(identifier, password)
        if response["success"]:
            self.page.data = {"username": identifier}
            import controller.homepg_controller as homepg
            homepg.main(self.page)
        else:
            self.view.login_message.value = response["error"]
            self.view.login_message.color = "red"
            self.page.update()

    def switch_view(self, page: ft.Page, view: str):
        if view == "login":
            self.view.build(page)
        elif view == "signup":
            from controller.signup_controller import main as signup_main
            signup_main(page)


def handle_logout(page: ft.Page):
        """Clears session data and redirects to the login page."""
        page.data.clear()  # Clears user session
        page.controls.clear()  # Clears the UI
        main(page)  # Redirects to login

def main(page: ft.Page):
    controller = LoginController(page)
    controller.view.build(page)

if __name__ == "__main__":
    ft.app(target=main)
