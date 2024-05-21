from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name = 'index'),
    path("pokemon_list/", views.all_pokemon, name = 'pokemon_list'),
    path("abilities_list/", views.all_abilities, name = 'ability_list'),
    path("move_list/", views.all_moves, name = 'move_list'),
]

# first argument is a URL path - in this case it matches the root URL
# e,g, http://example.com/

# second argument refers to the view function that will handle requests to this URL
# pattern - the index function in the views.py module

# third argument is an optional name for the pattern