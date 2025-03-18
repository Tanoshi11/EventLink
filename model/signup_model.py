import httpx
import re

class SignupModel:
    @staticmethod
    def validate_inputs(username, email, contact, password):
        errors = []
        if not username.strip():
            errors.append("Username is required!")
        if not email.strip():
            errors.append("Email is required!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
            errors.append("Invalid email format. Use user@example.com.")
        if not contact.strip():
            errors.append("Contact number is required!")
        elif len(contact.strip()) != 11:
            errors.append("Contact number must be exactly 11 digits.")
        if not password.strip():
            errors.append("Password is required!")
        return errors

    @staticmethod
    def register_user(username, email, contact, password):
        user_data = {
            "username": username,
            "email": email,
            "contact": contact,
            "password": password
        }
        try:
            response = httpx.post("http://127.0.0.1:8000/register", json=user_data, timeout=10.0)
            response.raise_for_status()
            return {"success": True}
        except httpx.HTTPStatusError as exc:
            return {"success": False, "error": exc.response.json()["detail"]}
