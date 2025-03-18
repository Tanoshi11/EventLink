class CategoryListModel:
    def __init__(self):
        self.categories = [
            {"icon": "BRUSH", "label": "Arts"},
            {"icon": "BUSINESS_CENTER", "label": "Business"},
            {"icon": "FAVORITE", "label": "Charity"},
            {"icon": "LOCAL_LIBRARY", "label": "Community"},
            {"icon": "SCHOOL", "label": "Education"},
            {"icon": "THEATER_COMEDY", "label": "Entertainment"},
            {"icon": "ECO", "label": "Environment"},
            {"icon": "RESTAURANT", "label": "Food"},
            {"icon": "GAMES", "label": "Gaming"},
            {"icon": "HEALTH_AND_SAFETY", "label": "Health"},
            {"icon": "MUSIC_NOTE", "label": "Music"},
            {"icon": "GAVEL", "label": "Politics"},
            {"icon": "SPORTS_SOCCER", "label": "Sports"},
            {"icon": "DEVICES", "label": "Technology"},
            {"icon": "FLIGHT", "label": "Travel"},
        ]

    def get_categories(self):
        return self.categories