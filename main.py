import flet as ft
from controller.login_controller import LoginController

def main(page: ft.Page):
    page.title = "EventLink - Login"
    page.bgcolor = "#0C3B2E"

    controller = LoginController(page)
    controller.load_login_view()

if __name__ == "__main__":
    ft.app(target=main)
