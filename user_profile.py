import flet as ft
import httpx
import re

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

# ----------------- Profile Page -----------------
def show_profile(page: ft.Page):
    page.bgcolor = "#d6aa54"

    username = page.data.get("username") if page.data else None
    if not username:
        error_view = ft.Column([
            ft.Text("User not logged in.", color="red", size=20),
            ft.ElevatedButton("Back to Login", on_click=lambda e: back_to_login(page), bgcolor="transparent", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.controls.clear()
        page.add(error_view)
        page.update()
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
            "date_joined": doc.get("date_joined", "N/A")
        }
    except Exception as e:
        error_view = ft.Column([
            ft.Text("Error retrieving user data.", color="red", size=20),
            ft.Text(str(e), color="red"),
            ft.ElevatedButton("Back to Login", on_click=lambda e: back_to_login(page), bgcolor="transparent", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.controls.clear()
        page.add(error_view)
        page.update()
        return

    # Store user_data on the page for use in the popups.
    page.user_data = user_data

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

    # transactions_section = ft.Column([
    #     ft.Row([
    #         ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET, color="#FFBA00"),
    #         ft.TextButton(
    #             "View My Wallet",
    #             on_click=lambda e: view_wallet(page),
    #             style=ft.ButtonStyle(
    #                 color=ft.colors.WHITE,
    #                 text_style=ft.TextStyle(size=18)
    #             )
    #         )
    #     ]),
    #     ft.Row([
    #         ft.Icon(ft.icons.RECEIPT_LONG, color="#FFBA00"),
    #         ft.TextButton(
    #             "My Transactions",
    #             on_click=lambda e: view_transactions(page),
    #             style=ft.ButtonStyle(
    #                 color=ft.colors.WHITE,
    #                 text_style=ft.TextStyle(size=18)
    #             )
    #         )
    #     ])
    # ], spacing=10)

    # Check for missing fields (incomplete details) excluding main email and contact
    incomplete_fields = any(value in ["N/A", "-"] for key, value in user_data.items() if key not in ["username", "date_joined", "email", "contact"])
    if incomplete_fields:
        note_text = ft.Text("Note: Some profile details are incomplete. Please update for better security.", size=14, color="yellow")
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
        edit_buttons_section = ft.Row(
            controls=[note_text, update_button],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
    else:
        edit_buttons_section = ft.TextButton(
            "Edit Profile",
            icon=ft.icons.EDIT,
            icon_color="#FFBA00",
            on_click=lambda e: full_edit_profile(page),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                text_style=ft.TextStyle(size=18)
            )
        )

    back_to_home_container = ft.Container(
        content=ft.TextButton(
            "Back to Home",
            icon=ft.icons.EXIT_TO_APP,
            icon_color="#FFBA00",
            on_click=lambda e: back_to_home(page),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                text_style=ft.TextStyle(size=18)
            )
        ),
        alignment=ft.alignment.bottom_left,
        expand=True,
    )

    vertical_divider = ft.VerticalDivider(color="white", thickness=2)

    # "About Me" Section
    about_me_title = ft.Text("About Me", size=26, weight=ft.FontWeight.BOLD, color="white")
    about_me = ft.Container(
        content=ft.Text("Describe Yourself!", color="white", size=18),
        bgcolor="#406157",
        padding=15,
        border_radius=10,
        width=420,
        height=160,
    )

    # "Activity Log" Section
    activity_log_title = ft.Text("Activity Log", size=26, weight=ft.FontWeight.BOLD, color="white")
    activity_log = ft.Container(
        content=ft.Text("Recent Activities", color="white", size=18),
        bgcolor="#406157",
        padding=15,
        border_radius=10,
        width=420,  
        height=380,  
    )

    side_column = ft.Column([
        about_me_title,
        about_me,
        ft.Divider(color="white", thickness=2),
        activity_log_title,
        activity_log,
    ], spacing=20, width=420) 

    full_profile_container = ft.Container(
        content=ft.Row([
            ft.Column([
                profile_title,
                profile_content,
                ft.Divider(color="white", thickness=2),
                credentials_section,
                # ft.Divider(color="white", thickness=2),
                # transactions_section,
                ft.Divider(color="white", thickness=2),
                edit_buttons_section,
                back_to_home_container
            ], spacing=20, expand=True),
            vertical_divider, 
            side_column  
        ], alignment=ft.MainAxisAlignment.START, expand=True),
        bgcolor="#063628",
        padding=ft.padding.all(20),
        border_radius=10,
        border=ft.border.all(2, "white"),
        width=page.width * 0.9,
        height=page.height * 0.9,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(left=70, top=30)
    )

    page.controls.clear()
    page.add(ft.Row([full_profile_container], alignment=ft.MainAxisAlignment.START))
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
            val = field.value.strip()
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
            show_profile(page)
        except Exception as ex:
            print("Error updating profile:", ex)
    
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
                                )
                            ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
    )
    page.overlay.append(popup)
    page.update()

# ----------------- Full Edit Popup (All Editable Fields) -----------------
def full_edit_profile(page: ft.Page):
    # This popup shows all editable fields (excluding date joined, main email, and main contact)
    user_data = page.user_data if hasattr(page, "user_data") else {}

    backup_email_field = ft.TextField(
        label="Backup Email",
        hint_text="Enter Backup Email",
        width=350,
        value=user_data.get("backup_email", "") if user_data.get("backup_email", "N/A") not in ["N/A", "-"] else "",
        text_style=ft.TextStyle(color="#FDF7E3"),
        label_style=ft.TextStyle(color="#FDF7E3"),
        border_color="#D4A937",
        content_padding=ft.padding.all(10)
    )
    backup_number_field = ft.TextField(
        label="Backup Number",
        hint_text="Enter Backup Number",
        width=350,
        value=user_data.get("backup_number", "") if user_data.get("backup_number", "N/A") not in ["N/A", "-"] else "",
        text_style=ft.TextStyle(color="#FDF7E3"),
        label_style=ft.TextStyle(color="#FDF7E3"),
        border_color="#D4A937",
        content_padding=ft.padding.all(10)
    )
    address_field = ft.TextField(
        label="Address",
        hint_text="Street, City, Province",
        width=350,
        value=user_data.get("address", "") if user_data.get("address", "N/A") not in ["N/A", "-"] else "",
        text_style=ft.TextStyle(color="#FDF7E3"),
        label_style=ft.TextStyle(color="#FDF7E3"),
        border_color="#D4A937",
        content_padding=ft.padding.all(10)
    )
    
    # Create error labels for each field
    backup_email_error = ft.Text("", color="red", size=12)
    backup_number_error = ft.Text("", color="red", size=12)
    address_error = ft.Text("", color="red", size=12)
    
    # Wrap each field with its error message for uniform spacing
    backup_email_column = ft.Column(controls=[backup_email_field, backup_email_error], spacing=2)
    backup_number_column = ft.Column(controls=[backup_number_field, backup_number_error], spacing=2)
    address_column = ft.Column(controls=[address_field, address_error], spacing=2)
    
    form_content = ft.Column(
        controls=[backup_email_column, backup_number_column, address_column],
        spacing=15
    )
    
    def on_save(e):
        # Reset error messages and border colors to default
        backup_email_error.value = ""
        backup_number_error.value = ""
        address_error.value = ""
        backup_email_field.border_color = "#FDF7E3"
        backup_number_field.border_color = "#FDF7E3"
        address_field.border_color = "#FDF7E3"
        
        errors = False
        
        backup_email = backup_email_field.value.strip()
        if backup_email and not re.match(r"[^@]+@[^@]+\.[^@]+", backup_email):
            backup_email_error.value = "Invalid backup email format. Use user@example.com."
            backup_email_field.border_color = "red"
            errors = True
        
        backup_number = backup_number_field.value.strip()
        if backup_number and not (backup_number.isdigit() and len(backup_number) == 11):
            backup_number_error.value = "Backup number must be exactly 11 digits."
            backup_number_field.border_color = "red"
            errors = True
        
        address = address_field.value.strip()
        if address and not re.match(r"^.+,\s*.+,\s*.+$", address):
            address_error.value = "Address must be in format: Street, City, Province."
            address_field.border_color = "red"
            errors = True
        
        page.update()  # Update the popup to reflect error messages
        
        if errors:
            print("Validation errors encountered.")
            return
        
        updated_values = {}
        if backup_email:
            updated_values["backup_email"] = backup_email
        if backup_number:
            updated_values["backup_number"] = backup_number
        if address:
            updated_values["address"] = address
        
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
            show_profile(page)
        except Exception as ex:
            print("Error updating profile:", ex)
    
    popup = ft.AnimatedSwitcher(
    duration=500,
    content=ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="rgba(0,0,0,0.5)",
        content=ft.Container(
            margin=ft.margin.only(left=500, right=500, top=250, bottom=250),
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
                                )
                            ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
    )

    page.overlay.append(popup)
    page.update()

def close_edit_popup(page: ft.Page, popup: ft.Control):
    if popup in page.overlay:
        page.overlay.remove(popup)
    page.update()

def view_wallet(page: ft.Page):
    print("View My Wallet clicked")

def view_transactions(page: ft.Page):
    print("My Transactions clicked")

def back_to_login(page: ft.Page):
    import login
    login.load_login(page)

def back_to_home(page: ft.Page):
    import homepg
    homepg.main(page)
