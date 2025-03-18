import flet as ft

def clear_overlay(page):
    """Safely clear overlays before navigating to a new page."""
    if hasattr(page, "overlay") and page.overlay:
        page.overlay.clear()
        page.update()
