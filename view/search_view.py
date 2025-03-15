import flet as ft
from controller.sidebar_controller import SidebarController

def clear_overlay(page: ft.Page):
    if page.overlay:
        page.overlay.clear()
        page.update()

def load_event_details(page, event):
    import event_details
    search_context = {
        "query": page.data.get("query", "All"),
        "search_type": page.data.get("search_type", "global"),
        "location": page.data.get("location", None)
    }
    event_details.load_event_details(page, event, search_context)

def create_category_row(icon_name: str, label: str, on_click):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(name=icon_name, color="white", size=20),
                ft.Text(label, color="white", size=16),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=ft.padding.all(5),
        on_click=on_click,
        ink=True,
        border_radius=ft.border_radius.all(5),
    )

def create_results_view(heading_text):
    results_title = ft.Text(
        heading_text,
        size=30,
        weight=ft.FontWeight.BOLD,
        color="#faf9f7"
    )

    heading_divider = ft.Divider(color="white", thickness=1)

    results_list = ft.ListView(expand=True, spacing=10)
    results_list.controls.append(ft.Text("Loading Results...", size=20, color="white"))

    return results_title, heading_divider, results_list

def create_main_stack(taskbar, side_taskbar, sidebar, results_title, heading_divider, results_list):
    return ft.Stack(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[results_title, heading_divider, results_list],
                    spacing=20,
                    expand=True
                ),
                margin=ft.margin.only(left=270, top=120, right=40),
                expand=True
            ),
            taskbar,
            # side_taskbar,
            sidebar
        ],
        expand=True
    )