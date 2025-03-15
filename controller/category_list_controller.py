import flet as ft
from model.category_list_model import CategoryListModel
from view.category_list_view import CategoryListView

class CategoryListController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = CategoryListModel()
        self.view = CategoryListView(self)

    def get_categories(self):
        return self.model.get_categories()

    def on_category_click(self, e, category_label: str):
        print(f"Category clicked: {category_label}")
        
        # Lazy import inside function to prevent circular import
        from controller.search_controller import load_search
        load_search(self.page, query=category_label, search_type="category")


    def build(self):
        return self.view.build(self.page)