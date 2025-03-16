import httpx

class UserProfileModel:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def fetch_user_data(self, username):
        try:
            response = httpx.get(f"{self.base_url}/get_user?username={username}", timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP Error retrieving user data: {e}")
        except Exception as e:
            raise Exception(f"Error retrieving user data: {e}")

    def update_user_data(self, username, data):
        try:
            response = httpx.patch(f"{self.base_url}/update_user?username={username}", json=data, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as ex:
            raise Exception(f"Error updating profile: {ex}")
        except Exception as ex:
            raise Exception(f"Error updating profile: {ex}")
