from django import forms
from .models import Pokedex, Regions, Abilities, Moves
from .models import LearnedByLeveling, LearnedByTm, PokemonAbilities, PokemonRegion


GENERATION_CHOICES = [(i,str(i)) for i in range(1,10)]
TYPE_CHOICES = [
    ('Normal', 'Normal'),
    ('Fire', 'Fire'),
    ('Water', 'Water'),
    ('Grass', 'Grass'),
    ('Electric', 'Electric'),
    ('Ice', 'Ice'),
    ('Fighting', 'Fighting'),
    ('Poison', 'Poison'),
    ('Ground', 'Ground'),
    ('Flying', 'Flying'),
    ('Psychic', 'Psychic'),
    ('Bug', 'Bug'),
    ('Rock', 'Rock'),
    ('Ghost', 'Ghost'),
    ('Dragon', 'Dragon'),
    ('Dark', 'Dark'),
    ('Steel', 'Steel'),
    ('Fairy', 'Fairy'),
]

class PokemonFilterForm(forms.Form):
    min_stat_total = forms.IntegerField(required=False, label='Min Stat Total')
    max_stat_total = forms.IntegerField(required=False, label='Max Stat Total')
    min_atk = forms.IntegerField(required=False, label='Min Attack')
    min_hp = forms.IntegerField(required=False, label='Min HP')
    min_def = forms.IntegerField(required=False, label='Min Defense')
    min_spatk = forms.IntegerField(required=False, label='Min Special Attack')
    min_spdef = forms.IntegerField(required=False, label='Min Special Defense')
    min_spd = forms.IntegerField(required=False, label='Min Speed')
    type = forms.ChoiceField(choices=[('','Any')] + TYPE_CHOICES, required=False, label='Type')
    ability = forms.CharField(required=False, label='Ability', widget=forms.TextInput(attrs={'class': 'autocomplete'}))
    region = forms.ModelChoiceField(queryset=Regions.objects.all(), required=False, label='Region')
    
    def clean_ability(self):
        ability_name = self.cleaned_data.get('ability')
        if ability_name:
            try:
                return Abilities.objects.get(name=ability_name)
            except Abilities.DoesNotExist:
                raise forms.ValidationError("Invalid ability selected")
        return None
            