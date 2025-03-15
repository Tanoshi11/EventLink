import flet as ft
import re

class UserProfileView:
    @staticmethod
    def show_alert(page, title, content):
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[ft.TextButton("OK", on_click=lambda e: UserProfileView.close_dialog(page))]
        )
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    @staticmethod
    def close_dialog(page):
        page.dialog.open = False
        page.update()

    @staticmethod
    def render_profile_popup(page: ft.Page, user_data: dict, controller):
        """Renders the user profile popup."""

        # --- Local Helper Functions ---
        def on_edit_description(e):
            controller.handle_edit_description(description_field, save_button, edit_description)
        
        def on_save_description_clicked(e):
             controller.handle_save_description(page, description_field, save_button, edit_description)

        def close_profile(e):
            controller.close_profile_popup()

        profile_title = ft.Text("Profile Information", size=30, weight=ft.FontWeight.BOLD)
        profile_content = ft.Row([
            ft.Image(
                src="images/no_profile.png",
                width=120, height=120, border_radius=60,
            ),
            ft.Column([
                ft.Text(user_data["username"], size=22, weight=ft.FontWeight.BOLD),
                ft.Text(f"User ID: {user_data['username']}", size=18, color="gray"),
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
                on_click=lambda e: controller.edit_profile(),
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
                        on_click=lambda e: controller.close_profile_popup(),
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
            action_buttons = ft.Column(
                controls=[
                    ft.TextButton(
                        "Edit Profile",
                        icon=ft.icons.EDIT,
                        icon_color="#FFBA00",
                        on_click=lambda e: controller.edit_profile(),
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
                        on_click=lambda e: controller.close_profile_popup(),
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
            on_click=lambda e: controller.handle_save_description(page, description_field, save_button, edit_description),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                text_style=ft.TextStyle(size=18)
            )
        )
        
        edit_description = ft.TextButton(
            "Edit Description",
            icon=ft.icons.EDIT,
            icon_color="#FFBA00",
            on_click=lambda e: controller.handle_edit_description(description_field, save_button, edit_description),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                text_style=ft.TextStyle(size=18)
            )
        )
        
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
                ft.Container(
                    bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                    expand=True
                ),
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

    @staticmethod
    def show_profile_popup(page: ft.Page, popup):
        page.overlay.append(popup)
        page.update()


    @staticmethod
    def close_profile_popup(page: ft.Page):
        """Close the profile popup."""
        page.overlay.clear()
        page.update()

    @staticmethod
    def render_edit_profile_popup(page: ft.Page, user_data, controller):
        """Renders the edit profile popup with user credentials pre-filled."""

        def on_save_clicked(e):
            save_button.disabled = True  # Temporarily disable to prevent multiple clicks
            page.update()
            controller.handle_save_missing_fields(inputs, error_labels, popup)
            save_button.disabled = False  # Re-enable after saving
            page.update()

        def close_edit(e):
            page.overlay.remove(popup)  # Remove only the edit popup, not the whole profile view
            page.update()

        def enable_save_button(e):
            save_button.disabled = False  # Enable Save button when input changes
            page.update()

        # ✅ Input fields pre-filled with user data
        gender_input = ft.Dropdown(
            value=user_data.get("gender", ""),
            options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")],
            bgcolor="#2E443F",
            color="white",
            border=ft.border.all(1, "#E0C78F"),
            on_change=enable_save_button  # Enable Save on change
        )

        email_input = ft.TextField(
            value=user_data.get("email", ""),
            bgcolor="#2E443F",
            color="white",
            border=ft.border.all(1, "#E0C78F"),
            on_change=enable_save_button
        )

        backup_email_input = ft.TextField(
            value=user_data.get("backup_email", ""),
            bgcolor="#2E443F",
            color="white",
            border=ft.border.all(1, "#E0C78F"),
            on_change=enable_save_button
        )

        contact_input = ft.TextField(
            value=user_data.get("contact", ""),
            bgcolor="#2E443F",
            color="white",
            border=ft.border.all(1, "#E0C78F"),
            on_change=enable_save_button
        )

        backup_number_input = ft.TextField(
            value=user_data.get("backup_number", ""),
            bgcolor="#2E443F",
            color="white",
            border=ft.border.all(1, "#E0C78F"),
            on_change=enable_save_button
        )

        # Store inputs in dictionary for easier handling
        inputs = {
            "gender": gender_input,
            "email": email_input,
            "backup_email": backup_email_input,
            "contact": contact_input,
            "backup_number": backup_number_input
        }

        error_labels = {
            key: ft.Text("", color="red", size=12) for key in inputs
        }

        save_button = ft.ElevatedButton(
            "Save",
            on_click=on_save_clicked,
            bgcolor="#C77000",
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            disabled=False  # Initially disabled, will be enabled on input change
        )

        popup = ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor="rgba(0,0,0,0.5)",  # Semi-transparent overlay
            content=ft.Container(
                width=450,
                padding=20,
                border_radius=10,
                bgcolor="#406157",
                border=ft.border.all(2, "#E0C78F"),
                content=ft.Column(
                    controls=[
                        ft.Text("Edit Profile", size=22, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Column(controls=[
                            ft.Text("Gender", size=14, color="#E0C78F"), gender_input,
                            ft.Text("Email", size=14, color="#E0C78F"), email_input,
                            ft.Text("Backup Email", size=14, color="#E0C78F"), backup_email_input,
                            ft.Text("Contact", size=14, color="#E0C78F"), contact_input,
                            ft.Text("Backup Number", size=14, color="#E0C78F"), backup_number_input,
                        ], spacing=12),
                        ft.Row(
                            controls=[
                                save_button,
                                ft.ElevatedButton(
                                    "Close",
                                    on_click=close_edit,
                                    bgcolor="#C77000",
                                    color="white",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                        ),
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ),
        )

        page.overlay.append(popup)
        page.update()




    @staticmethod
    def render_full_edit_profile_popup(page: ft.Page, edit_fields_controls, error_labels, controller):
        """Renders the full edit profile popup."""
        # --- Local Helper Functions ---
        def on_save_clicked(e):
            controller.handle_save_full_edit_fields(edit_fields_controls, error_labels, popup)

        def close_edit(e):
            controller.close_edit_popup()

        columns = []
        for key in edit_fields_controls:
            columns.append(ft.Column(controls=[edit_fields_controls[key], error_labels[key]], spacing=2))

        if columns:
            form_content = ft.Column(controls=columns, spacing=15)
        else:
            form_content = ft.Text("No fields to edit.", size=18, color="#FDF7E3")

        popup = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Profile"),
            content=form_content,
            actions=[
                ft.TextButton("Save", on_click=on_save_clicked),
                ft.TextButton("Close", on_click=close_edit),
            ],
        )

        page.overlay.append(popup)
        page.update()

    @staticmethod
    def close_edit_popup(page: ft.Page):
        """Closes any edit popup."""
        if page.overlay:
            page.overlay.clear()  # Clear all overlays
        page.update()
