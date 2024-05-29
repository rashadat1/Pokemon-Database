from django.shortcuts import render
from django.http import HttpResponse
from .models import Pokedex, Abilities, Moves
from .forms import PokemonFilterForm
from django.http import JsonResponse

# contains Python functions called view functions that handle HTTP requests and return
# HTTP responses

# Create your views here.
def index(request):
    return HttpResponse('Welcome to the Pokemon Database!')

# to call the view we need to map it to a URL which requires a URLconf
# to do this we create a urls.py file in our app directory

# process incoming HTTP requests and generate appropriate HTTP responses
# each view corresponds to a particular URL pattern

# based on the request data the view function can perform tasks such as querying a database,
# processing form submissions etc.

# after processing the HTTP request, the view function returns an HTTP response to be provided
# to the client - HTML page, JSON data, file download or whatever

# in urls.py we do the crucial step of URL routing - URL patterns that map to specific view
# functions

# first we create a view function to display all of the pokemon

def all_pokemon(request):
    pokemon_list = Pokedex.objects.all()
    return render(request, 'query/all_pokemon.html',{'pokemon_list' : pokemon_list})
    
    
def all_abilities(request):
    ability_list = Abilities.objects.all()
    return render(request, 'query/all_abilities.html',{'ability_list' : ability_list})
    

def all_moves(request):
    move_list = Moves.objects.all()
    return render(request, 'query/all_moves.html', {'move_list' : move_list})

# request is an http request

# 
def filter_pokemon(request):
    pokemon_list = Pokedex.objects.none()
    errors = None
    if request.method == 'GET':
        # when a user submits a form using the GET method the form data is appended to the URL as query
        # parameters. E.g. 
        form = PokemonFilterForm(request.GET)
        if form.is_valid():
            # if true, this means that all of the required fields were correctly filled out by default
            # that each filled out field was supplied a value of the correct data type by default
            pokemon_list = Pokedex.objects.all()
            
            if form.cleaned_data['min_stat_total']:
                pokemon_list = pokemon_list.filter(total__gte = form.cleaned_data['min_stat_total'])
            
            if form.cleaned_data['max_stat_total']:
                pokemon_list = pokemon_list.filter(total__lte = form.cleaned_data['max_stat_total'])
                
            if form.cleaned_data['min_atk']:
                pokemon_list = pokemon_list.filter(atk__gte = form.cleaned_data['min_atk'])

            if form.cleaned_data['min_hp']:
                pokemon_list = pokemon_list.filter(hp__gte = form.cleaned_data['min_hp'])

            if form.cleaned_data['min_def']:
                pokemon_list = pokemon_list.filter(def_field__gte = form.cleaned_data['min_def'])

            if form.cleaned_data['min_spatk']:
                pokemon_list = pokemon_list.filter(spatk__gte = form.cleaned_data['min_spatk'])

            if form.cleaned_data['min_spdef']:
                pokemon_list = pokemon_list.filter(spdef__gte = form.cleaned_data['min_spdef'])

            if form.cleaned_data['min_spd']:
                pokemon_list = pokemon_list.filter(spd__gte = form.cleaned_data['min_spd'])
                
            if form.cleaned_data['type']:
                pokemon_type = form.cleaned_data['type']
                pokemon_list = pokemon_list.filter(type__contains = [pokemon_type])
                
            if form.cleaned_data['ability']:
                pokemon_list = pokemon_list.filter(pokemonabilities__ability = form.cleaned_data['ability'])
                
            if form.cleaned_data['region']:
                pokemon_list = pokemon_list.filter(pokemonregion__region = form.cleaned_data['region'])
                
            pokemon_list = pokemon_list.order_by('id')
            
        else:
            errors = form.errors
        #if form.errors['ability']:
        #    form.errors['ability'] = ['Invalid ability choice.']

    else:
        form = PokemonFilterForm()
        pokemon_list = Pokedex.objects.all().order_by('id')
        
        
        
    return render(request, 'query/filter_pokemon.html', {'form' : form, 'pokemon_list' : pokemon_list, 'errors' : errors})
        
            
def autocomplete_ability(request):
    if 'term' in request.GET:
        # checks if there is a user typed word 'term' in the GET request
        qs = Abilities.objects.filter(name__icontains = request.GET.get('term'))
        # finds the abilities containing the typed phrase[]
        names = list(qs.values_list('name',flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


        
    
            
            
        
    

    