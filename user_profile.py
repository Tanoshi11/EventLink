import flet as ft
import httpx
import re
from homepg import load_homepage
from login import load_login

# --- Alert Dialog Helpers ---
def show_alert(page, title, content):
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(page))]
    )
    page.dialog = dialog
    page.dialog.open = True
    page.update()

def close_dialog(page):
    page.dialog.open = False
    page.update()

# ----------------- Profile Popup -----------------
def show_profile_popup(page: ft.Page):
    """Show the profile as a popup with a blurred background."""

    # Create a semi-transparent overlay to simulate the blur effect
    overlay = ft.Container(
        bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),  # Semi-transparent black
        expand=True,  # Cover the entire page
    )

    # Fetch user data
    username = page.data.get("username") if page.data else None
    if not username:
        show_alert(page, "Error", "User not logged in.")
        return

    try:
        response = httpx.get(f"http://127.0.0.1:8000/get_user?username={username}", timeout=10.0)
        response.raise_for_status()
        doc = response.json()
        user_data = {
            "username": doc.get("username", "N/A"),
            "email": doc.get("email", "N/A"),
            "backup_email": doc.get("backup_email", "N/A"),
            "contact": doc.get("contact", "N/A"),
            "backup_number": doc.get("backup_number", "N/A"),
            "address": doc.get("address", "N/A"),
            "gender": doc.get("gender", "-"),
            "date_joined": doc.get("date_joined", "N/A"),
            "description": doc.get("description", "Describe Yourself!")  # Add description field
        }
    except httpx.HTTPStatusError as e:
        show_alert(page, "Error", f"HTTP Error retrieving user data: {e}")
        return
    except Exception as e:
        show_alert(page, "Error", f"Error retrieving user data: {e}")
        return

    # Store user_data on the page for use in the popups.
    page.user_data = user_data

    # Profile content
    profile_title = ft.Text("Profile Information", size=30, weight=ft.FontWeight.BOLD)
    profile_content = ft.Row([
        ft.Image(
            src="images/no_profile.png",
            width=120, height=120, border_radius=60,
        ),
        ft.Column([
            ft.Text(user_data["username"], size=22, weight=ft.FontWeight.BOLD),
            ft.Text(f"User ID: {username}", size=18, color="gray"),
            ft.Text(f"Date Joined: {user_data['date_joined']}", size=18, color="gray"),
            ft.Text(f"Gender: {user_data['gender']}", size=18, color="gray")
        ], spacing=5, alignment=ft.MainAxisAlignment.START)
    ], spacing=15)

    credentials_section = ft.Column([
        ft.Row([ft.Icon(ft.icons.EMAIL, color="#FFBA00"), ft.Text(f"Email: {user_data['email']}", size=18)]),
        ft.Row([ft.Icon(ft.icons.EMAIL, color="#FFBA00"), ft.Text(f"Backup Email: {user_data['backup_email']}", size=18)]),
        ft.Row([ft.Icon(ft.icons.PHONE, color="#FFBA00"), ft.Text(f"Contact: {user_data['contact']}", size=18)]),
        ft.Row([ft.Icon(ft.icons.PHONE, color="#FFBA00"), ft.Text(f"Backup Number: {user_data['backup_number']}", size=18)]),
        ft.Row([ft.Icon(ft.icons.HOME, color="#FFBA00"), ft.Text(f"Address: {user_data['address']}", size=18)])
    ], spacing=10)

    # Check for incomplete fields
    incomplete_fields = any(value in ["N/A", "-"] for key, value in user_data.items() if key not in ["username", "date_joined", "email", "contact"])

    if incomplete_fields:
        note_text = ft.Text(
            "Note: Some profile details are incomplete. Please update for better security.",
            size=14,
            color="yellow",
            text_align=ft.TextAlign.CENTER,
        )

        update_button = ft.TextButton(
            "Update Profile",
            icon=ft.icons.EDIT_NOTE_SHARP,
            icon_color="#FFBA00",
            on_click=lambda e: edit_profile(page),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                text_style=ft.TextStyle(size=18)
            )
        )

        action_buttons = ft.Column(
            controls=[
                note_text,  # Message about profile completeness
                update_button,  # Update Profile button
                ft.TextButton(
                    "Back",
                    icon=ft.icons.ARROW_BACK,
                    icon_color="#FFBA00",
                    on_click=lambda e: close_profile_popup(page),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        text_style=ft.TextStyle(size=18)
                    )
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    else:
        # After updating, reposition the Edit Profile button
        action_buttons = ft.Column(
            controls=[
                ft.TextButton(
                    "Edit Profile",
                    icon=ft.icons.EDIT,
                    icon_color="#FFBA00",
                    on_click=lambda e: full_edit_profile(page),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        text_style=ft.TextStyle(size=18)
                    )
                ),
                ft.Container(height=20),  # Blank space
                ft.TextButton(
                    "Back",
                    icon=ft.icons.ARROW_BACK,
                    icon_color="#FFBA00",
                    on_click=lambda e: close_profile_popup(page),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        text_style=ft.TextStyle(size=18)
                    )
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    vertical_divider = ft.VerticalDivider(color="white", thickness=2)
    about_me_title = ft.Text("About Me", size=26, weight=ft.FontWeight.BOLD, color="white")

    # Add a TextField for the description
    description_field = ft.TextField(
        value=user_data["description"],
        multiline=True,
        max_length=465,  # Increase to 1000 or whatever limit you prefer
        text_style=ft.TextStyle(color="white", size=18),
        border=ft.InputBorder.NONE,
        read_only=True,  # Turn this off when editing
        content_padding=ft.padding.all(10),
        width=420,
        height=450,
    )


    about_me = ft.Container(
        content=description_field,
        bgcolor="#406157",
        padding=15,
        border_radius=10,
        width=420,
        height=450,
    )

    # Save button (initially hidden)
    save_button = ft.TextButton(
        "Save",
        icon=ft.icons.SAVE,
        icon_color="#FFBA00",
        visible=False,  # Initially hidden
        on_click=lambda e: on_save_description(page, description_field, save_button, edit_description),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            text_style=ft.TextStyle(size=18)
        )
    )

    def on_edit_description(e):
        description_field.read_only = False
        save_button.visible = True
        edit_description.visible = False
        page.update()

    edit_description = ft.TextButton(
        "Edit Description",
        icon=ft.icons.EDIT,
        icon_color="#FFBA00",
        on_click=on_edit_description,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            text_style=ft.TextStyle(size=18)
        )
    )

    def on_save_description(page, description_field, save_button, edit_description):
        # Save the description to the backend
        username = page.data.get("username")
        new_description = description_field.value
        try:
            response = httpx.patch(
                f"http://127.0.0.1:8000/update_user?username={username}",
                json={"description": new_description},
                timeout=10.0
            )
            response.raise_for_status()
            # Update the user_data on the page
            page.user_data["description"] = new_description
            print("Description saved successfully")
            show_alert(page, "Success", "Description saved successfully!")
        except httpx.HTTPStatusError as ex:
            print("Error saving description:", ex)
            show_alert(page, "Error", f"Error saving description: {ex}") # Show error to user
        except Exception as ex:
            print("Error saving description:", ex)
            show_alert(page, "Error", f"Error saving description: {ex}") # Show error to user

        # Reset the UI
        description_field.read_only = True
        save_button.visible = False
        edit_description.visible = True
        page.update()

    # Row for Edit and Save buttons
    button_row = ft.Row(
        controls=[
            edit_description,
            save_button,
        ],
        spacing=10,
    )

    side_column = ft.Column([
        about_me_title,
        about_me,
        button_row  # Use the button row here
    ], spacing=20, width=420)

    full_profile_container = ft.Container(
        content=ft.Row([
            ft.Column([
                profile_title,
                profile_content,
                ft.Divider(color="white", thickness=2),
                credentials_section,
                ft.Divider(color="white", thickness=2),
                action_buttons,  # Use the organized action buttons here
            ], spacing=20, expand=True),
            vertical_divider,
            side_column
        ], alignment=ft.MainAxisAlignment.START, expand=True),
        bgcolor="#063628",
        padding=ft.padding.all(20),
        border_radius=10,
        border=ft.border.all(2, "white"),
        width=page.width * 0.7,
        height=page.height * 0.7,
        alignment=ft.alignment.center,
    )

    # Stack the overlay and the profile container
    stack = ft.Stack(
        controls=[
            overlay,  # Semi-transparent overlay
            ft.Container(
                content=full_profile_container,
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        expand=True,
    )

    # Add the stack to the page overlay
    page.overlay.append(stack)
    page.update()

def close_profile_popup(page: ft.Page):
    """Close the profile popup."""
    page.overlay.clear()
    page.update()

# ----------------- Update Popup (Missing Fields Only) -----------------
def edit_profile(page: ft.Page):
    # This popup shows only missing fields (for updating incomplete profile info)
    user_data = page.user_data if hasattr(page, "user_data") else {}
    missing_fields_controls = {}
    error_labels = {}

    # Define credentials (including Contact) with Gender first
    credentials = [
        ("Gender", "gender"),
        ("Email", "email"),
        ("Backup Email", "backup_email"),
        ("Contact", "contact"),
        ("Backup Number", "backup_number"),
        ("Address", "address")
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

    columns = []
    for key in missing_fields_controls:
        columns.append(ft.Column(controls=[missing_fields_controls[key], error_labels[key]], spacing=2))

    if columns:
        form_content = ft.Column(controls=columns, spacing=15)
    else:
        form_content = ft.Text("All profile details are complete.", size=18, color="#FDF7E3")

    def on_save(e):
        # Reset error messages and border colors
        for key in error_labels:
            error_labels[key].value = ""
            missing_fields_controls[key].border_color = "#FDF7E3"

        errors = False

        # Validate Contact: must be exactly 11 digits.
        if "contact" in missing_fields_controls:
            contact_val = missing_fields_controls["contact"].value.strip()
            if contact_val and (not contact_val.isdigit() or len(contact_val) != 11):
                error_labels["contact"].value = "Contact number must be exactly 11 digits."
                missing_fields_controls["contact"].border_color = "red"
                errors = True

        # Validate Backup Email
        if "backup_email" in missing_fields_controls:
            backup_email_val = missing_fields_controls["backup_email"].value.strip()
            if backup_email_val and not re.match(r"[^@]+@[^@]+\.[^@]+", backup_email_val):
                error_labels["backup_email"].value = "Invalid backup email format. Use user@example.com."
                missing_fields_controls["backup_email"].border_color = "red"
                errors = True

        # Validate Backup Number
        if "backup_number" in missing_fields_controls:
            backup_number_val = missing_fields_controls["backup_number"].value.strip()
            if backup_number_val and (not backup_number_val.isdigit() or len(backup_number_val) != 11):
                error_labels["backup_number"].value = "Backup number must be exactly 11 digits."
                missing_fields_controls["backup_number"].border_color = "red"
                errors = True

        # Validate Address: expects "Street, City, Province"
        if "address" in missing_fields_controls:
            address_val = missing_fields_controls["address"].value.strip()
            if address_val and not re.match(r"^.+,\s*.+,\s*.+$", address_val):
                error_labels["address"].value = "Address must be in format: Street, City, Province."
                missing_fields_controls["address"].border_color = "red"
                errors = True

        page.update()

        if errors:
            print("Validation errors encountered.")
            return

        updated_values = {}
        for key, field in missing_fields_controls.items():
            # Access value differently for TextField vs. Dropdown
            val = field.value if isinstance(field, ft.TextField) else field.value
            if val:
                updated_values[key] = val

        if not updated_values:
            print("No updates provided")
            return

        try:
            response = httpx.patch(
                f"http://127.0.0.1:8000/update_user?username={user_data.get('username')}",
                json=updated_values,
                timeout=10.0
            )
            response.raise_for_status()

            for key, value in updated_values.items():
                page.user_data[key] = value

            print("Profile updated successfully")
            close_edit_popup(page, popup)
            show_alert(page, "Success", "Profile updated successfully!")

        except httpx.HTTPStatusError as ex:
            print("Error updating profile:", ex)
            show_alert(page, "Error", f"Error updating profile: {ex}")
        except Exception as ex:
            print("Error updating profile:", ex)
            show_alert(page, "Error", f"Error updating profile: {ex}")

    popup = ft.AnimatedSwitcher(
        duration=500,
        content=ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor="rgba(0,0,0,0.5)",
            content=ft.Container(
                margin=ft.margin.only(left=500, right=500, top=200, bottom=200),
                padding=20,
                border_radius=10,
                bgcolor="#406157",
                border=ft.border.all(3, "white"),
                content=ft.Column(
                    controls=[
                        ft.Text("Update Profile", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
                        form_content,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Save",
                                    on_click=on_save,
                                    bgcolor="#C77000",
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                                ft.ElevatedButton(
                                    "Close",
                                    on_click=lambda e: close_edit_popup(page, popup),
                                    bgcolor="#C77000",
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ),
        ),
    )

    page.overlay.append(popup)
    page.update()
    popup.content.opacity = 1
    popup.update()

def close_edit_popup(page, popup):
    popup.content.opacity = 0
    popup.update()
    page.overlay.remove(popup)
    page.update()

# ----------------- Full Edit Popup -----------------
def full_edit_profile(page: ft.Page):
    user_data = page.user_data if hasattr(page, "user_data") else {}
    edit_fields_controls = {}
    error_labels = {}

    # Define credentials (including Contact) with Gender first
    credentials = [
        ("Gender", "gender"),
        ("Email", "email"),
        ("Backup Email", "backup_email"),
        ("Contact", "contact"),
        ("Backup Number", "backup_number"),
        ("Address", "address")
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

    columns = []
    for key in edit_fields_controls:
        columns.append(ft.Column(controls=[edit_fields_controls[key], error_labels[key]], spacing=2))

    form_content = ft.Column(controls=columns, spacing=15)

    def on_save(e):
        # Reset error messages and border colors
        for key in error_labels:
            error_labels[key].value = ""
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

        page.update()

        if errors:
            print("Validation errors encountered.")
            return

        updated_values = {}
        for key, field in edit_fields_controls.items():
            # Access value differently for TextField vs. Dropdown
            val = field.value if isinstance(field, ft.TextField) else field.value
            if val:
                updated_values[key] = val

        if not updated_values:
            print("No updates provided")
            return

        try:
            response = httpx.patch(
                f"http://127.0.0.1:8000/update_user?username={user_data.get('username')}",
                json=updated_values,
                timeout=10.0
            )
            response.raise_for_status()

            for key, value in updated_values.items():
                page.user_data[key] = value

            print("Profile updated successfully")
            close_edit_popup(page, popup)
            show_alert(page, "Success", "Profile updated successfully!")

        except httpx.HTTPStatusError as ex:
            print("Error updating profile:", ex)
            show_alert(page, "Error", f"Error updating profile: {ex}")
        except Exception as ex:
            print("Error updating profile:", ex)
            show_alert(page, "Error", f"Error updating profile: {ex}")

    popup = ft.AnimatedSwitcher(
        duration=500,
        content=ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor="rgba(0,0,0,0.5)",
            content=ft.Container(
                margin=ft.margin.only(left=500, right=500, top=200, bottom=200),
                padding=20,
                border_radius=10,
                bgcolor="#406157",
                border=ft.border.all(3, "white"),
                content=ft.Column(
                    controls=[
                        ft.Text("Edit Profile", size=24, weight=ft.FontWeight.BOLD, color="#FDF7E3"),
                        form_content,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Save",
                                    on_click=on_save,
                                    bgcolor="#C77000",
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                                ft.ElevatedButton(
                                    "Close",
                                    on_click=lambda e: close_edit_popup(page, popup),
                                    bgcolor="#C77000",
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ),
        ),
    )

    page.overlay.append(popup)
    page.update()
    popup.content.opacity = 1
    popup.update()


# ----------------- Navigation Functions -----------------
def back_to_home(page: ft.Page):
    load_homepage(page)  # Directly load the homepage

def back_to_login(page: ft.Page):
    load_login(page)
