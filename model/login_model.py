import httpx

class LoginModel:
    @staticmethod
    def authenticate(identifier, password):
        user_data = {
            "identifier": identifier,
            "password": password
        }
        try:
            response = httpx.post("http://127.0.0.1:8000/login", json=user_data, timeout=20.0)
            response.raise_for_status()
            return {"success": True, "username": identifier}
        except httpx.ConnectError:
            return {"success": False, "error": "Connection error: FastAPI server not available."}
        except httpx.HTTPStatusError as exc:
            return {"success": False, "error": f"Login failed: {exc.response.json()['detail']}"}
