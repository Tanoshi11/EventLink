import flet as ft
import time
import threading

# Global variable to store the notification popup overlay
notif_popup = None

def main(page: ft.Page):
    page.title = "Home"
    page.bgcolor = "#5F7755"
    page.padding = 0  # Ensure no extra padding at the edges

    def logout(e):
        def delayed_logout():
            time.sleep(0.6)
            if page.data is not None:
                page.data.clear()
            import login
            login.load_login(page)
        threading.Thread(target=delayed_logout).start()

    def show_profile_page(e):
        def delayed_profile():
            time.sleep(2)
            import user_profile
            user_profile.show_profile(page)
        threading.Thread(target=delayed_profile).start()

    def open_notifications(e):
        global notif_popup
        if notif_popup:
            close_notifications(e)
        else:
            show_notifications(e)

    def show_notifications(e):
        global notif_popup
        notifications = [f"Notification {i}: Event Update" for i in range(1, 101)]

        def on_click_event(event_text):
            print(f"Event clicked: {event_text}")

        notif_controls = []
        for notif in notifications:
            notif_controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[ft.Text(notif, size=18, color="white", weight=ft.FontWeight.BOLD)],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=15),
                    bgcolor="#4C7043",
                    border_radius=10,
                    margin=ft.margin.only(bottom=10),
                    on_click=lambda e, notif_text=notif: on_click_event(notif_text),
                )
            )

        close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            on_click=close_notifications,
            icon_color="white",
            icon_size=30,
            tooltip=None,
            width=30,
            height=30,
            alignment=ft.alignment.top_right,
            style=ft.ButtonStyle(overlay_color=ft.colors.TRANSPARENT)
        )

        list_view = ft.ListView(
            controls=notif_controls,
            height=300,
            expand=True,
        )

        inner_popup_height = 400

        inner_popup = ft.Container(
            content=ft.Column(
                controls=[close_button, list_view],
                spacing=20,
            ),
            bgcolor="#6D9773",
            padding=10,
            border_radius=10,
            width=400,
            height=inner_popup_height,
            shadow=ft.BoxShadow(blur_radius=10, color="gray", offset=ft.Offset(2, 2)),
            on_click=lambda e: e.stop_propagation() if hasattr(e, "stop_propagation") else None,
        )

        notif_popup = ft.AnimatedSwitcher(
            duration=500,  # Duration in milliseconds
            content=ft.Container(
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=100, bottom=300, right=15),
                content=inner_popup,
            ),
        )

        page.overlay.append(notif_popup)
        page.update()

    def close_notifications(e):
        global notif_popup
        if notif_popup in page.overlay:
            page.overlay.remove(notif_popup)
        notif_popup = None
        page.update()

    def handle_click_outside(e):
        if notif_popup and notif_popup in page.overlay:
            close_notifications(e)

    # ----------------- Taskbar (Header) -----------------
    header = ft.Row(
        controls=[
            ft.Container(width=15),
            ft.Container(
                content=ft.Image(src="images/eventlink.png", width=200, height=80, fit=ft.ImageFit.CONTAIN),
                margin=ft.margin.only(right=10)
            ),
            # Search and Location Fields
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SEARCH, color="white", size=30),
                        ft.TextField(
                            hint_text="Search events",
                            border=None,
                            expand=True,
                            text_style=ft.TextStyle(size=18, color="white"),
                            border_radius=20,
                            border_color="#B46617"
                        ),
                        ft.VerticalDivider(width=1, color="white"),
                        ft.Icon(name=ft.Icons.LOCATION_ON, color="white", size=30),
                        ft.TextField(
                            hint_text="Select Location",
                            border=None,
                            expand=True,
                            text_style=ft.TextStyle(size=18, color="white"),
                            border_radius=20,
                            border_color="#B46617"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                border_radius=15,
                border=ft.border.all(1, "#B46617"),
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                expand=True,
                bgcolor="#105743",
                margin=ft.margin.only(top=16, bottom=16, right=30)
            ),
            ft.VerticalDivider(width=1, color="white", leading_indent=30, trailing_indent=30),
            # Shop Button
            ft.Container(
                tooltip=None,
                content=ft.TextButton(
                    text="Shop",
                    on_click=lambda e: print("Shop clicked"),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TRANSPARENT,
                        overlay_color=ft.Colors.TRANSPARENT,
                        elevation=0,
                        color="white",
                        text_style=ft.TextStyle(
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            letter_spacing=2
                        )
                    )
                ),
                margin=ft.margin.only(left=30, right=30)
            ),
            ft.VerticalDivider(width=1, color="white", leading_indent=30, trailing_indent=30),
            # Events Popup Menu
            ft.Container(
                content=ft.PopupMenuButton(
                    tooltip="",
                    content=ft.Container(
                        content=ft.Text(
                            "Events",
                            style=ft.TextStyle(
                                size=20,
                                color="white",
                                weight=ft.FontWeight.BOLD,
                                letter_spacing=1.5
                            )
                        ),
                        alignment=ft.alignment.center
                    ),
                    height=55,
                    width=175,
                    bgcolor="#B46617",
                    menu_position=ft.PopupMenuPosition.UNDER,
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.CALENDAR_TODAY, color="white", size=15),
                                    ft.Text("My Events", style=ft.TextStyle(color="white", size=15))
                                ],
                                spacing=5
                            ),
                            on_click=lambda e: print("My Events clicked")
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.EVENT_NOTE, color="white", size=15),
                                    ft.Text("Create Event", style=ft.TextStyle(color="white", size=15))
                                ],
                                spacing=5
                            ),
                            on_click=lambda e: print("Create Event clicked")
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.SENTIMENT_SATISFIED, color="white", size=15),
                                    ft.Text("Volunteer", style=ft.TextStyle(color="white", size=15))
                                ],
                                spacing=5
                            ),
                            on_click=lambda e: print("Volunteer clicked")
                        )
                    ]
                ),
                margin=ft.margin.only(left=3, right=3)
            ),
            ft.VerticalDivider(width=1, color="white", leading_indent=30, trailing_indent=30),
            # Notifications Icon Container with a border overlay
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.NOTIFICATIONS,
                    on_click=open_notifications,
                    icon_color="#FFBA00",
                    icon_size=40,
                    tooltip="Notifications",
                    width=60
                ),
                margin=ft.margin.only(left=40, right=10),
                border=ft.border.all(2, "#105743"),
                border_radius=30
            ),
            # Profile Popup Menu Container with a border overlay
            ft.Container(
                content=ft.PopupMenuButton(
                    tooltip="Profile",
                    content=ft.Container(
                        content=ft.Icon(name=ft.Icons.PERSON_ROUNDED, color="#FFBA00", size=40),
                        alignment=ft.alignment.center
                    ),
                    height=55,
                    width=60,
                    bgcolor="#B46617",
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.PERSON_ROUNDED, color="white", size=15),
                                    ft.Text("Profile", style=ft.TextStyle(color="white", size=15))
                                ],
                                spacing=5
                            ),
                            on_click=show_profile_page
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.EXIT_TO_APP, color="white", size=15),
                                    ft.Text("Logout", style=ft.TextStyle(color="white", size=15))
                                ],
                                spacing=5
                            ),
                            on_click=logout
                        )
                    ]
                ),
                margin=ft.margin.only(left=50, right=20),
                border=ft.border.all(2, "#105743"),
                border_radius=30
            )
        ]
    )

    # The taskbar container sits at the very top.
    taskbar = ft.Container(
        content=header,
        height=100,  # Adjust height as needed
        bgcolor="#0C3B2E",
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=10)
    )

    # ----------------- Other Main Content -----------------
    top_left_text = ft.Container(
        content=ft.Text(
            "Upcoming Events 🎉",
            size=30,
            weight=ft.FontWeight.BOLD,
            color="white",
            text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.top_left,
        margin=ft.margin.only(top=110, left=150),
        padding=20
    )

    # ======== FLOATING DISCOVER & SLIDER ========

    # 1) "Discover" text remains unchanged (you can also adjust its font size if desired)
    discover_text = ft.Text(
        "Discover New Events!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.CENTER
    )

    # 2) Slider images
    slider_images = [
        "images/eventsample_img1.jpg",
        "images/eventsample_img2.png",
        "images/eventsample_img3.jpg",
    ]

    animated_slider = ft.AnimatedSwitcher(
        duration=500,  # Duration in milliseconds
        content=ft.Image(src=slider_images[0], width=400, fit=ft.ImageFit.FIT_WIDTH)
    )

    def slider_loop():
        current_index = 0
        while True:
            time.sleep(8)
            current_index = (current_index + 1) % len(slider_images)
            animated_slider.content = ft.Image(
                src=slider_images[current_index],
                width=600,
                height=300,
                fit=ft.ImageFit.FIT_WIDTH
            )
            page.update()

    threading.Thread(target=slider_loop, daemon=True).start()

    # slider_image_container = ft.Container(
    #     content=animated_slider,
    #     width=420,  # Reduced width
    #     border=ft.border.all(5, "#FFBA00"),
    #     border_radius=10,
    #     margin=ft.margin.only(top=20)
    # )

    # 3) Floating container content (text + slider)
    floating_slider_content = ft.Container(
        width=420,                # Reduced overall width
        bgcolor="#1D572C",        # Example background color
        border_radius=20,
        padding=15,
        content=ft.Column(
            controls=[
                discover_text,
                animated_slider
            ],
            spacing=15,
            alignment=ft.alignment.top_center
        )
    )


    # 4) Outer container to position on the right
    floating_slider_container = ft.Container(
        content=floating_slider_content,
        alignment=ft.alignment.center_right,
        margin=ft.margin.only(right=20, top=110,bottom=10)
    )

    # ======== END FLOATING DISCOVER & SLIDER ========

    # 5) Minimal "homepage_view" with only top_left_text
    homepage_view = ft.Container(
        content=top_left_text,
        expand=True
    )

    # ----------------- Category Icons Section -----------------
    category_buttons = ft.Column(
        controls=[
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.MUSIC_NOTE,
                    icon_color="white",
                    on_click=lambda e: print("Music clicked"),
                    icon_size=23
                ),
                border=ft.border.all(1, "white"),
                border_radius=ft.border_radius.all(20),
                padding=8,
                margin=ft.margin.symmetric(vertical=4),
                scale=0.9
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.LOCAL_BAR,
                    icon_color="white",
                    on_click=lambda e: print("Nightlife clicked"),
                    icon_size=23
                ),
                border=ft.border.all(1, "white"),
                border_radius=ft.border_radius.all(20),
                padding=8,
                margin=ft.margin.symmetric(vertical=4),
                scale=0.9
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.THEATER_COMEDY,
                    icon_color="white",
                    on_click=lambda e: print("Performing & Visual Arts clicked"),
                    icon_size=23
                ),
                border=ft.border.all(1, "white"),
                border_radius=ft.border_radius.all(20),
                padding=8,
                margin=ft.margin.symmetric(vertical=4),
                scale=0.9
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.BEACH_ACCESS,
                    icon_color="white",
                    on_click=lambda e: print("Holidays clicked"),
                    icon_size=23
                ),
                border=ft.border.all(1, "white"),
                border_radius=ft.border_radius.all(20),
                padding=8,
                margin=ft.margin.symmetric(vertical=4),
                scale=0.9
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.PALETTE,
                    icon_color="white",
                    on_click=lambda e: print("Hobbies clicked"),
                    icon_size=23
                ),
                border=ft.border.all(1, "white"),
                border_radius=ft.border_radius.all(20),
                padding=8,
                margin=ft.margin.symmetric(vertical=4),
                scale=0.9
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.BUSINESS_CENTER,
                    icon_color="white",
                    on_click=lambda e: print("Business clicked"),
                    icon_size=23
                ),
                border=ft.border.all(1, "white"),
                border_radius=ft.border_radius.all(20),
                padding=8,
                margin=ft.margin.symmetric(vertical=4),
                scale=0.9
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.RESTAURANT,
                    icon_color="white",
                    on_click=lambda e: print("Food & Drink clicked"),
                    icon_size=23
                ),
                border=ft.border.all(1, "white"),
                border_radius=ft.border_radius.all(20),
                padding=8,
                margin=ft.margin.symmetric(vertical=4),
                scale=0.9
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30
    )

    side_taskbar = ft.Container(
        content=ft.Container(
            content=category_buttons,
            width=95,
            height=page.height * 1,
            bgcolor="#5a7051",
            alignment=ft.alignment.center_left,
            padding=20,
            border_radius=50
        ),
        expand=True,
        alignment=ft.alignment.center_left,
        margin=ft.margin.only(left=30,top=100)
    )
    event1_highlight = ft.Container(
        content=ft.Container(
            width=450,
            height=320,
            bgcolor="#a63b0a",
            alignment=ft.alignment.top_center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=190, right=770)
    )

    event2_highlight = ft.Container(
        content=ft.Container(
            width=450,
            height=320,
            bgcolor="#a6750a",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=190, right= -150)
    )

    event3_highlight = ft.Container(
        content=ft.Container(
            width=450,
            height=320,
            bgcolor="#0a9135",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=520, right=770)
    )

    event4_highlight = ft.Container(
        content=ft.Container(
            width=450,
            height=320,
            bgcolor="#b6dbf2",
            alignment=ft.alignment.center,
            padding=20,
            border_radius=20
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=520, right=-150)
    )

    # Place the floating slider LAST so it appears on top
    main_stack = ft.Stack(
        controls=[
            homepage_view,
            event1_highlight,
            event2_highlight,
            event3_highlight,
            event4_highlight,
            floating_slider_container,  # floats above the homepage content
            side_taskbar,
            # Add the taskbar as the last element with absolute positioning:
            ft.Container(
                content=taskbar,
                alignment=ft.alignment.top_center,
                expand=True,
                padding=ft.padding.only(top=0)  # adjust if needed
            )
        ],
        expand=True,
    )

    page.controls.clear()
    page.add(main_stack)
    page.update()


def load_homepage(page):
    page.controls.clear()
    main(page)

def load_login(page):
    page.floating_action_button = None
    pass

def load_profile(page):
    page.floating_action_button = None
    pass

if __name__ == "__main__":
    ft.app(target=main)
