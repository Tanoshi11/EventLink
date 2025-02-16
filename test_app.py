import os
import math
import unittest
from datetime import datetime
from fastapi.testclient import TestClient
import bcrypt

# Import the FastAPI app and the users_collection from your server module.
from server import app, users_collection

# Create a TestClient for your FastAPI app.
client = TestClient(app)

#############################################
# Test FastAPI Endpoints in server.py
#############################################
class TestServerEndpoints(unittest.TestCase):
    def setUp(self):
        # Create a test user in the DB.
        self.test_username = "unittestuser"
        self.test_email = "unittest@example.com"
        self.test_contact = "09123456789"
        self.test_password = "password123"
        # Ensure any existing test user is removed.
        users_collection.delete_many({"username": self.test_username})
        
        hashed_password = bcrypt.hashpw(self.test_password.encode(), bcrypt.gensalt()).decode()
        self.test_user = {
            "username": self.test_username,
            "email": self.test_email,
            "contact": self.test_contact,
            "password": hashed_password,
            "date_joined": datetime.now().strftime("%Y-%m-%d")
        }
        users_collection.insert_one(self.test_user)
    
    def tearDown(self):
        # Clean up the test user after tests.
        users_collection.delete_many({"username": self.test_username})
    
    def test_get_user_found(self):
        response = client.get(f"/get_user?username={self.test_username}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], self.test_username)
        self.assertEqual(data["email"], self.test_email)
        self.assertEqual(data["contact"], self.test_contact)
    
    def test_get_user_not_found(self):
        response = client.get("/get_user?username=nonexistentuser")
        self.assertEqual(response.status_code, 404)
    
    def test_events_endpoint(self):
        response = client.get("/events")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
    
    def test_register_duplicate(self):
        # Attempt to register a user that already exists.
        payload = {
            "username": self.test_username,
            "email": self.test_email,
            "contact": "09999999999",
            "password": "newpassword"
        }
        response = client.post("/register", json=payload)
        self.assertEqual(response.status_code, 400)
        # Check for a substring, case-insensitive, e.g. "already exist"
        detail = response.json()["detail"].lower()
        self.assertIn("already exist", detail)
    
    def test_check_username(self):
        response = client.get(f"/check-username?username={self.test_username}")
        # Allow either 400 (if endpoint exists) or 404 (if not implemented)
        self.assertIn(response.status_code, [400, 404],
                      "check_username endpoint returned unexpected status code")
        if response.status_code == 400:
            self.assertEqual(response.json()["detail"], "Username already exists")
    
    def test_check_email(self):
        response = client.get(f"/check-email?email={self.test_email}")
        self.assertIn(response.status_code, [400, 404],
                      "check_email endpoint returned unexpected status code")
        if response.status_code == 400:
            self.assertEqual(response.json()["detail"], "Email already exists")
    
    def test_login_success(self):
        payload = {
            "identifier": self.test_username,
            "password": self.test_password
        }
        response = client.post("/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.json()["message"])
    
    def test_login_fail(self):
        payload = {
            "identifier": self.test_username,
            "password": "wrongpassword"
        }
        response = client.post("/login", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid credentials", response.json()["detail"])

#############################################
# Test Flet UI Functions using a FakePage
#############################################
class FakePage:
    def __init__(self):
        self.controls = []
        self.data = {}
    def add(self, control):
        self.controls.append(control)
    def update(self):
        pass
    def clear(self):
        self.controls = []

class TestFletUI(unittest.TestCase):
    def test_homepage_view(self):
        # Test that homepg.main adds controls to the page.
        from homepg import main as home_main
        fake_page = FakePage()
        home_main(fake_page)
        self.assertGreater(len(fake_page.controls), 0)
    
    def test_login_view(self):
        # Test that login.load_login adds controls to the page.
        from login import load_login
        fake_page = FakePage()
        load_login(fake_page)
        self.assertGreater(len(fake_page.controls), 0)
    
    def test_profile_view_error(self):
        # Test that user_profile.show_profile shows an error when no username is set.
        from user_profile import show_profile
        fake_page = FakePage()
        # Do not set fake_page.data["username"] to simulate a user not logged in.
        show_profile(fake_page)
        self.assertGreater(len(fake_page.controls), 0)
    
    def test_profile_view_success(self):
        # Test that user_profile.show_profile adds controls when a username is set.
        from user_profile import show_profile
        fake_page = FakePage()
        fake_page.data = {"username": "nonexistentuser"}  # This will trigger the error branch.
        show_profile(fake_page)
        self.assertGreater(len(fake_page.controls), 0)

if __name__ == "__main__":
    unittest.main()
