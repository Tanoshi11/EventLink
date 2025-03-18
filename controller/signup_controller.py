import flet as ft
from model.signup_model import SignupModel
from view.signup_view import SignupView

class SignupController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = SignupModel()
        self.view = SignupView(self)

    def signup(self, e):
        username = self.view.signup_username.value.strip()
        email = self.view.signup_email.value.strip()
        contact = self.view.signup_contact.value.strip()
        password = self.view.signup_password.value.strip()

        self.view.username_error.value = ""
        self.view.email_error.value = ""
        self.view.contact_error.value = ""
        self.view.password_error.value = ""
        self.view.signup_message_container.content = None

        errors = self.model.validate_inputs(username, email, contact, password)
        if errors:
            for error in errors:
                if "Username" in error:
                    self.view.username_error.value = error
                if "Email" in error:
                    self.view.email_error.value = error
                if "Contact" in error:
                    self.view.contact_error.value = error
                if "Password" in error:
                    self.view.password_error.value = error
            self.page.update()
            return

        response = self.model.register_user(username, email, contact, password)
        if response["success"]:
            self.view.signup_message_container.content = ft.Text("Signup Successful! Please log in.", color="green")
            self.page.update()
            self.switch_to_login(None)
        else:
            self.view.signup_message_container.content = ft.Text(response["error"], color="red")
            self.page.update()

    def switch_to_login(self, e):
        from controller.login_controller import main as login_main
        login_main(self.page)

def main(page: ft.Page):
    controller = SignupController(page)
    controller.view.build(page)

if __name__ == "__main__":
    ft.app(target=main)
