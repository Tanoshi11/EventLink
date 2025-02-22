import flet as ft
import httpx
import os

def show_profile(page: ft.Page):
    page.bgcolor = "#064735"  # Set background color
    
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

    profile_title = ft.Text("Profile Information", size=28, weight=ft.FontWeight.BOLD)  # Adjusted size
    
    profile_content = ft.Row([
        ft.Image(
            src="images/no_profile.png",  # Placeholder image
            width=100,
            height=100,
            border_radius=50,  # Make it circular
        ),
        ft.Column([
            ft.Text(user_data["username"], size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"User ID: {username}", size=16, color="gray"),
            ft.Text(f"Date Joined: {user_data['date_joined']}", size=16, color="gray"),
            ft.Text(f"Gender: {user_data['gender']}", size=16, color="gray")
        ], alignment=ft.MainAxisAlignment.START)
    ], spacing=10)

    credentials_section = ft.Column([
        ft.Row([ft.Icon(ft.icons.EMAIL, color="#B46617"), ft.Text(f"Email: {user_data['email']}", size=16)]),
        ft.Row([ft.Icon(ft.icons.EMAIL, color="#B46617"), ft.Text(f"Backup Email: {user_data['backup_email']}", size=16)]),
        ft.Row([ft.Icon(ft.icons.PHONE, color="#B46617"), ft.Text(f"Contact: {user_data['contact']}", size=16)]),
        ft.Row([ft.Icon(ft.icons.PHONE, color="#B46617"), ft.Text(f"Backup Number: {user_data['backup_number']}", size=16)]),
        ft.Row([ft.Icon(ft.icons.HOME, color="#B46617"), ft.Text(f"Address: {user_data['address']}", size=16)])
    ], spacing=8)

    transactions_section = ft.Column([
        ft.Row([ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET, color="#B46617"), ft.ElevatedButton("View My Wallet", on_click=lambda e: view_wallet(page), bgcolor="transparent", color="white")]),
        ft.Row([ft.Icon(ft.icons.RECEIPT_LONG, color="#B46617"), ft.ElevatedButton("My Transactions", on_click=lambda e: view_transactions(page), bgcolor="transparent", color="white")])
    ], spacing=8)

    incomplete_fields = any(value == "N/A" or value == "-------" for key, value in user_data.items() if key not in ["username", "date_joined"])
    note_text = ft.Text("Note: Some profile details are incomplete. Please update for better security.", size=12, color="yellow") if incomplete_fields else None

    edit_buttons_section = ft.Column([
        note_text if note_text else ft.Container(),
        ft.Row([
            ft.ElevatedButton("Edit Profile", icon=ft.icons.EDIT_NOTE_SHARP, icon_color="#B46617", on_click=lambda e: edit_profile(page), bgcolor="transparent", color="white"),
            ft.ElevatedButton("Back to Home", icon=ft.icons.EXIT_TO_APP, icon_color="#B46617", on_click=lambda e: back_to_home(page), bgcolor="transparent", color="white")
        ], spacing=20),
    ], spacing=20)

    vertical_divider = ft.VerticalDivider(color="white", thickness=2)

    history_log_title = ft.Text("History Log", size=24, weight=ft.FontWeight.BOLD, color="white")
    history_log_entries = ft.ListView(expand=True, auto_scroll=True)
    
    for entry in ["- Logged in at 10:00 AM", "- Updated profile information", "- Changed password"]:
        history_log_entries.controls.append(ft.Text(entry, color="white"))
    
    history_log_container = ft.Container(
        content=ft.Column([
            history_log_entries
        ], expand=True),
        bgcolor="#406157",
        padding=ft.padding.all(10),
        expand=True,
        border_radius=10
    )

    full_profile_container = ft.Container(
        content=ft.Row([
            ft.Column([
                profile_title,
                profile_content,
                ft.Divider(color="white"),
                credentials_section,
                ft.Divider(color="white"),
                transactions_section,
                ft.Divider(color="white"),
                edit_buttons_section
            ], spacing=15, expand=True),
            vertical_divider,
            ft.Column([
                history_log_title,
                ft.Divider(color="white"),
                history_log_container,               
            ], spacing=15, expand=True),
            vertical_divider,
            ft.Container(expand=True, bgcolor="#406157")
        ], alignment=ft.MainAxisAlignment.START, expand=True),
        bgcolor="#063628",
        padding=ft.padding.all(15),
        border_radius=10,
        border=ft.border.all(2, "white"),
        width=page.width * 0.9,
        height=page.height * 0.9,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(left=70,top=30)
    )
    
    page.controls.clear()
    page.add(ft.Row([full_profile_container], alignment=ft.MainAxisAlignment.START))
    page.update()

def edit_profile(page: ft.Page):
    print("Edit profile clicked")

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
