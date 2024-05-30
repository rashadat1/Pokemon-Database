from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name = 'index'),
    path("pokemon_list/", views.all_pokemon, name = 'pokemon_list'),
    path("abilities_list/", views.all_abilities, name = 'ability_list'),
    path("move_list/", views.all_moves, name = 'move_list'),
    path("filter_list/", views.filter_pokemon, name = 'filter_list'),
    path('autocomplete/ability/', views.autocomplete_ability, name = 'autocomplete_ability'),
    path('stat_calculator/', views.StatCalculatorTool, name = 'statcalculator'),
    path('autocomplete/pokemon/', views.autocomplete_pokemon, name = 'autocomplete_pokemon')
]

# first argument is a URL path - in this case it matches the root URL
# e,g, http://example.com/

# second argument refers to the view function that will handle requests to this URL
# pattern - the index function in the views.py module

# third argument is an optional name for the pattern