from django.shortcuts import render
from django.http import HttpResponse
from .models import Pokedex, Abilities, Moves
from .forms import PokemonFilterForm, StatCalculatorForm
from django.http import JsonResponse
from math import floor

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


def nature_modifier(nature, stat):
    nature_increase = {
        'Lonely': 'atk', 'Brave': 'atk', 'Adamant': 'atk', 'Naughty': 'atk',
        'Bold': 'def', 'Relaxed': 'def', 'Impish': 'def', 'Lax': 'def',
        'Modest': 'spatk', 'Mild': 'spatk', 'Quiet': 'spatk', 'Rash': 'spatk',
        'Calm': 'spdef', 'Gentle': 'spdef', 'Sassy': 'spdef', 'Careful': 'spdef',
        'Timid': 'spd', 'Hasty': 'spd', 'Jolly': 'spd', 'Naive': 'spd'
    }
    
    nature_decrease = {
        'Lonely': 'def', 'Brave': 'spd', 'Adamant': 'spatk', 'Naughty': 'spdef',
        'Bold': 'atk', 'Relaxed': 'spd', 'Impish': 'spatk', 'Lax': 'spdef',
        'Modest': 'atk', 'Mild': 'def', 'Quiet': 'spd', 'Rash': 'spdef',
        'Calm': 'atk', 'Gentle': 'def', 'Sassy': 'spd', 'Careful': 'spatk',
        'Timid': 'atk', 'Hasty': 'def', 'Jolly': 'spatk', 'Naive': 'spdef'
    }
    
    if nature_increase.get(nature) == stat:
        return 1.1
    
    elif nature_decrease.get(nature) == stat:
        return 0.9
    
    else:
        return 1.0   

def calculate_hp(base, iv, ev, level):
    return int((((2 * base + iv + (ev // 4)) * level) // 100) + level + 10)
    
def calculate_otherstats(base, iv, ev, level, nature_mod):
    return int(((((2 * base + iv + (ev // 4)) * level) // 100) + 5) * nature_mod)
    

def StatCalculatorTool(request):
    if request.method == 'POST':
        form = StatCalculatorForm(request.POST)
        if form.is_valid():
            pokemon = form.cleaned_data['pokemon_name']
            level = form.cleaned_data['level']
            nature = form.cleaned_data['nature']
            ivs = {
                'hp' : form.cleaned_data['hp_iv'],
                'atk' : form.cleaned_data['atk_iv'], 
                'def' : form.cleaned_data['def_iv'],
                'spatk' : form.cleaned_data['spatk_iv'],
                'spdef' : form.cleaned_data['spdef_iv'],
                'spd' : form.cleaned_data['spd_iv']}
            
            evs = {
                'hp' : form.cleaned_data['hp_ev'],
                'atk' : form.cleaned_data['atk_ev'], 
                'def' : form.cleaned_data['def_ev'],
                'spatk' : form.cleaned_data['spatk_ev'],
                'spdef' : form.cleaned_data['spdef_ev'],
                'spd' : form.cleaned_data['spd_ev']}
            
            stats = {
                'hp' : calculate_hp(pokemon.hp, ivs['hp'], evs['hp'], level),
                'atk' : calculate_otherstats(pokemon.atk, ivs['atk'], evs['atk'], level, nature_modifier(nature,'atk')),
                'def' : calculate_otherstats(pokemon.def_field, ivs['def'], evs['def'], level, nature_modifier(nature,'def')),
                'spatk' : calculate_otherstats(pokemon.spatk, ivs['spatk'], evs['spatk'], level, nature_modifier(nature,'spatk')),
                'spdef' : calculate_otherstats(pokemon.spdef, ivs['spdef'], evs['spdef'], level, nature_modifier(nature,'spdef')),
                'spd' : calculate_otherstats(pokemon.spd, ivs['spd'], evs['spd'], level, nature_modifier(nature,'spd'))
            }
            
            return render(request, 'query/stat_calculation_tool.html', {'stats' : stats, 'pokemon' : pokemon})        
    else:
        form = StatCalculatorForm()
    return render(request, 'query/stat_calculation_tool.html', {'form' : form})
    
    
def autocomplete_ability(request):
    if 'term' in request.GET:
        # checks if there is a user typed word 'term' in the GET request
        qs = Abilities.objects.filter(name__icontains = request.GET.get('term'))
        # finds the abilities containing the typed phrase[]
        names = list(qs.values_list('name',flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def autocomplete_pokemon(request):
    if 'term' in request.POST:
        qs = Pokedex.objects.filter(name__icontains = request.POST.get('term'))
        names = list(qs.values_list('name',flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)



        
    
            
            
        
    

    