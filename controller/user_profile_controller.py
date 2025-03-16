import flet as ft
import re
from model.user_profile_model import UserProfileModel
from view.user_profile_view import UserProfileView
import httpx

class UserProfileController:
    def __init__(self, page, username):
        self.page = page
        self.username = username  # Store the username
        self.model = UserProfileModel()
        self.view = UserProfileView()
        self.popup = None

    def show_profile(self):
        username = self.username
        if not username:
            UserProfileView.show_alert(self.page, "Error", "User not logged in.")
            return

        try:
            user_data = self.model.fetch_user_data(username)
            print(f"✅ Fetched user data for {username}: {user_data}")  # Debugging

            if not user_data:  # Check if the response is empty
                print("❌ User data is empty!")
                UserProfileView.show_alert(self.page, "Error", "User profile data is missing.")
                return

            # Ensure all required fields exist in user_data
            required_fields = ["username", "email", "contact", "date_joined", "gender", "description", "backup_email", "backup_number", "address"]
            for field in required_fields:
                if field not in user_data:
                    user_data[field] = "N/A"  # Default to "N/A" if missing

            self.page.user_data = user_data
            UserProfileView.render_profile_popup(self.page, user_data, self)

        except Exception as e:
            print("❌ Error in show_profile:", e)
            UserProfileView.show_alert(self.page, "Error", str(e))



    def edit_profile(self):
        print("✅ edit_profile() was called!")  # Debugging line
        user_data = self.page.user_data if hasattr(self.page, "user_data") else {}
        missing_fields_controls = {}
        error_labels = {}

        # Define credentials (including Contact) with Gender first
        credentials = [
            ("Gender", "gender"),
            ("Email", "email"),
            ("Backup Email", "backup_email"),
            ("Contact", "contact"),
            ("Backup Number", "backup_number"),
            ("Address", "address")  # Ensure "address" is included
        ]

        for label, key in credentials:
            if user_data.get(key, "N/A") in ["N/A", "-"]:
                error_labels[key] = ft.Text("", color="red", size=12)
                if key == "contact":
                    missing_fields_controls[key] = ft.TextField(
                        label=label,
                        hint_text=f"Enter {label}",
                        width=350,
                        input_filter=ft.InputFilter(regex_string=r"\d", allow=True),
                        max_length=11,
                        text_style=ft.TextStyle(color="#FDF7E3"),
                        label_style=ft.TextStyle(color="#FDF7E3"),
                        border_color="#D4A937",
                        content_padding=ft.padding.all(10)
                    )
                elif key == "gender":  # Changed from else to elif to handle gender
                    missing_fields_controls[key] = ft.Dropdown(
                        label=label,
                        options=[
                            ft.dropdown.Option("Male"),
                            ft.dropdown.Option("Female"),
                            ft.dropdown.Option("Preferred not to say"),
                        ],
                        width=350,
                        text_style=ft.TextStyle(color="#FDF7E3"),
                        label_style=ft.TextStyle(color="#FDF7E3"),
                        content_padding=ft.padding.all(10),
                        border_color="#D4A937",  # Dark green border
                        bgcolor="#0C3B2E",  # Dark green background
                        color="white",  # White text
                    )
                else:
                    missing_fields_controls[key] = ft.TextField(
                        label=label,
                        hint_text=f"Enter {label}",
                        width=350,
                        text_style=ft.TextStyle(color="#FDF7E3"),
                        label_style=ft.TextStyle(color="#FDF7E3"),
                        border_color="#D4A937",
                        content_padding=ft.padding.all(10)
                    )
        
        # Ensure the popup is properly initialized
        self.popup = UserProfileView.render_edit_profile_popup(self.page, user_data, self)
        if self.popup:
            UserProfileView.show_profile_popup(self.page, self.popup)
            print(f"🔍 Popup Content: {self.popup}")
        else:
            print("Error: Popup is None")



    def full_edit_profile(self):
        user_data = self.page.user_data if hasattr(self.page, "user_data") else {}
        edit_fields_controls = {}
        error_labels = {}

        # Define credentials (including Contact) with Gender first
        credentials = [
            ("Gender", "gender"),
            ("Email", "email"),
            ("Backup Email", "backup_email"),
            ("Contact", "contact"),
            ("Backup Number", "backup_number"),
            ("Address", "address")  # Ensure "address" is included
        ]

        for label, key in credentials:
            error_labels[key] = ft.Text("", color="red", size=12)
            if key == "contact":
                edit_fields_controls[key] = ft.TextField(
                    label=label,
                    hint_text=f"Enter {label}",
                    value=user_data.get(key, ""),
                    width=350,
                    input_filter=ft.InputFilter(regex_string=r"\d", allow=True),
                    max_length=11,
                    text_style=ft.TextStyle(color="#FDF7E3"),
                    label_style=ft.TextStyle(color="#FDF7E3"),
                    border_color="#D4A937",
                    content_padding=ft.padding.all(10)
                )
            elif key == "gender":
                edit_fields_controls[key] = ft.Dropdown(
                    label=label,
                    options=[
                        ft.dropdown.Option("Male"),
                        ft.dropdown.Option("Female"),
                        ft.dropdown.Option("Preferred not to say"),
                    ],
                    value=user_data.get(key, ""),  # Set initial value
                    width=350,
                    text_style=ft.TextStyle(color="#FDF7E3"),
                    label_style=ft.TextStyle(color="#FDF7E3"),
                    content_padding=ft.padding.all(10),
                    border_color="#D4A937",  # Dark green border
                    bgcolor="#0C3B2E",  # Dark green background
                    color="white",  # White text
                )
            else:
                edit_fields_controls[key] = ft.TextField(
                    label=label,
                    hint_text=f"Enter {label}",
                    value=user_data.get(key, ""),
                    width=350,
                    text_style=ft.TextStyle(color="#FDF7E3"),
                    label_style=ft.TextStyle(color="#FDF7E3"),
                    border_color="#D4A937",
                    content_padding=ft.padding.all(10)
                )
        
        UserProfileView.render_full_edit_profile_popup(self.page, edit_fields_controls, error_labels, self)

    def handle_save_missing_fields(self, missing_fields_controls, error_labels, popup):
        """Handles saving of missing fields, updates UI, and closes the edit popup."""
        
        # Reset error messages
        for key in error_labels:
            error_labels[key].value = ""
            missing_fields_controls[key].border_color = "#FDF7E3"

        errors = False
        updated_values = {}

        # Validate and collect new values
        for key, field in missing_fields_controls.items():
            value = field.value.strip() if isinstance(field, ft.TextField) else field.value
            
            if key == "contact" and (not value.isdigit() or len(value) != 11):
                error_labels[key].value = "Contact number must be exactly 11 digits."
                missing_fields_controls[key].border_color = "red"
                errors = True

            if key == "backup_email" and value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                error_labels[key].value = "Invalid email format. Use user@example.com."
                missing_fields_controls[key].border_color = "red"
                errors = True

            if key == "backup_number" and (not value.isdigit() or len(value) != 11):
                error_labels[key].value = "Backup number must be exactly 11 digits."
                missing_fields_controls[key].border_color = "red"
                errors = True

            if key == "address" and not re.match(r"^.+,\s*.+,\s*.+$", value):
                error_labels[key].value = "Address format should be: Street, City, Province."
                missing_fields_controls[key].border_color = "red"
                errors = True

            # Only add non-empty valid values
            if value:
                updated_values[key] = value

        # ✅ Ensure the error messages appear
        self.page.update()

        if errors:
            print("Validation errors encountered.")
            return

        if not updated_values:
            print("No new updates provided.")
            return

        try:
            # Send the updated data to the database
            username = self.page.user_data.get("username")
            response = httpx.patch(
                f"http://127.0.0.1:8000/update_user?username={username}",
                json=updated_values,
                timeout=10.0
            )
            response.raise_for_status()

            # Update page data with new values
            for key, value in updated_values.items():
                self.page.user_data[key] = value

            print("✅ Profile updated successfully!")

            # Remove the edit popup from the overlay
            if popup in self.page.overlay:
                self.page.overlay.remove(popup)

            # Clear previous profile popups
            self.page.overlay.clear()

            # Re-render profile popup with updated data
            self.show_profile()

            UserProfileView.show_alert(self.page, "Success", "Profile updated successfully!")

        except Exception as ex:
            print("Error updating profile:", ex)
            UserProfileView.show_alert(self.page, "Error", f"Error updating profile: {ex}")




    def handle_save_full_edit_fields(self, edit_fields_controls, error_labels, popup):
        # Reset error messages and border colors
        for key in error_labels:
            error_labels[key].value = ""
            if key in edit_fields_controls:  # Check if the field exists
                edit_fields_controls[key].border_color = "#FDF7E3"

        errors = False

        # Validate Contact: must be exactly 11 digits.
        if "contact" in edit_fields_controls:
            contact_val = edit_fields_controls["contact"].value.strip()
            if contact_val and (not contact_val.isdigit() or len(contact_val) != 11):
                error_labels["contact"].value = "Contact number must be exactly 11 digits."
                edit_fields_controls["contact"].border_color = "red"
                errors = True

        # Validate Backup Email
        if "backup_email" in edit_fields_controls:
            backup_email_val = edit_fields_controls["backup_email"].value.strip()
            if backup_email_val and not re.match(r"[^@]+@[^@]+\.[^@]+", backup_email_val):
                error_labels["backup_email"].value = "Invalid backup email format. Use user@example.com."
                edit_fields_controls["backup_email"].border_color = "red"
                errors = True

        # Validate Backup Number
        if "backup_number" in edit_fields_controls:
            backup_number_val = edit_fields_controls["backup_number"].value.strip()
            if backup_number_val and (not backup_number_val.isdigit() or len(backup_number_val) != 11):
                error_labels["backup_number"].value = "Backup number must be exactly 11 digits."
                edit_fields_controls["backup_number"].border_color = "red"
                errors = True

        # Validate Address: expects "Street, City, Province"
        if "address" in edit_fields_controls:
            address_val = edit_fields_controls["address"].value.strip()
            if address_val and not re.match(r"^.+,\s*.+,\s*.+$", address_val):
                error_labels["address"].value = "Address must be in format: Street, City, Province."
                edit_fields_controls["address"].border_color = "red"
                errors = True

        self.page.update()

        if errors:
            print("Validation errors encountered.")
            return

        updated_values = {}
        for key, field in edit_fields_controls.items():
            val = field.value if isinstance(field, ft.TextField) else field.value
            if val:
                updated_values[key] = val

        if not updated_values:
            print("No updates provided")
            return

        try:
            username = self.page.user_data.get('username')
            response = httpx.patch(
                f"http://127.0.0.1:8000/update_user?username={username}",
                json=updated_values,
                timeout=10.0
            )
            response.raise_for_status()

            for key, value in updated_values.items():
                self.page.user_data[key] = value

            print("Profile updated successfully")
            self.close_edit_popup()
            UserProfileView.show_alert(self.page, "Success", "Profile updated successfully!")

        except Exception as ex:
            print("Error updating profile:", ex)
            UserProfileView.show_alert(self.page, "Error", f"Error updating profile: {ex}")
    
    def handle_edit_description(self, description_field, save_button, edit_description):
        print("handle_edit_description() was called!")  # Debugging line
        description_field.read_only = False
        save_button.visible = True
        edit_description.visible = False
        self.page.update()
    
    def handle_save_description(self, page, description_field, save_button, edit_description):
        username = page.data.get("username")
        new_description = description_field.value
        try:
            response = httpx.patch(
                f"http://127.0.0.1:8000/update_user?username={username}",
                json={"description": new_description},
                timeout=10.0
            )
            response.raise_for_status()
            page.user_data["description"] = new_description
            print("Description saved successfully")
            UserProfileView.show_alert(page, "Success", "Description saved successfully!")
        except Exception as ex:
            print("Error saving description:", ex)
            UserProfileView.show_alert(page, "Error", f"Error saving description: {ex}")
        
        # Reset the UI
        description_field.read_only = True
        save_button.visible = False
        edit_description.visible = True  # Restore "Edit Description" button
        page.update()


    def close_profile_popup(self):
        print("✅ close_profile_popup() was called!")  # Debugging line
        self.page.overlay.clear()
        self.page.update()

    def close_edit_popup(self):
        """Closes the edit profile popup."""
        if self.page.overlay:
            self.page.overlay.clear()
        self.page.update()
