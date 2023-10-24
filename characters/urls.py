from django.urls import path

from characters import views

urlpatterns = [
    path(
        "characters/random/", views.get_random_character_view, name="character-random"
    ),
    path("characters/", views.CharacterListView.as_view(), name="character-list"),
]

app_name = "characters"
