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

NATURE_CHOICES = [
    ('Hardy', 'Hardy'), ('Lonely', 'Lonely'), ('Brave', 'Brave'), ('Adamant', 'Adamant'), ('Naughty', 'Naughty'),
    ('Bold', 'Bold'), ('Docile', 'Docile'), ('Relaxed', 'Relaxed'), ('Impish', 'Impish'), ('Lax', 'Lax'),
    ('Timid', 'Timid'), ('Hasty', 'Hasty'), ('Serious', 'Serious'), ('Jolly', 'Jolly'), ('Naive', 'Naive'),
    ('Modest', 'Modest'), ('Mild', 'Mild'), ('Quiet', 'Quiet'), ('Bashful', 'Bashful'), ('Rash', 'Rash'),
    ('Calm', 'Calm'), ('Gentle', 'Gentle'), ('Sassy', 'Sassy'), ('Careful', 'Careful'), ('Quirky', 'Quirky'),
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
            

class StatCalculatorForm(forms.Form):
    pokemon_name = forms.CharField(required=True, label='Pokemon', widget=forms.TextInput(attrs={'class': 'autocomplete'}))
    level = forms.IntegerField(required=True, label='Level', min_value=1, max_value=100)
    nature = forms.ChoiceField(required=True, choices=NATURE_CHOICES, label='Nature')
    
    hp_iv = forms.IntegerField(required=True, label='HP IV', min_value=0, max_value=31)
    atk_iv = forms.IntegerField(required=True, label='ATK IV', min_value=0, max_value=31)
    def_iv = forms.IntegerField(required=True, label='DEF IV', min_value=0, max_value=31)
    spatk_iv = forms.IntegerField(required=True, label='SPATK IV', min_value=0, max_value=31)
    spdef_iv = forms.IntegerField(required=True, label='SPDEF IV', min_value=0, max_value=31)
    spd_iv = forms.IntegerField(required=True, label='SPD IV', min_value=0, max_value=31)
    
    hp_ev = forms.IntegerField(required=True, label='HP EV', min_value=0, max_value=252)
    atk_ev = forms.IntegerField(required=True, label='ATK EV', min_value=0, max_value=252)
    def_ev = forms.IntegerField(required=True, label='DEF EV', min_value=0, max_value=252)
    spatk_ev = forms.IntegerField(required=True, label='SPATK EV', min_value=0, max_value=252)
    spdef_ev = forms.IntegerField(required=True, label='SPDEF EV', min_value=0, max_value=252)
    spd_ev = forms.IntegerField(required=True, label='SPD EV', min_value=0, max_value=252)

    def clean_pokemon_name(self):
        pokemon_name = self.cleaned_data.get('pokemon_name')
        if pokemon_name:
            try:
                return Pokedex.objects.get(name=pokemon_name)
            except Pokedex.DoesNotExist:
                raise forms.ValidationError("Invalid Pokemon selected")
        return None
    
    def clean_EVs(self):
        cleaned_data = super().clean_EVs()
        
        hp_ev = self.cleaned_data.get('hp_ev')
        atk_ev = self.cleaned_data.get('atk_ev')
        def_ev = self.cleaned_data.get('def_ev')
        spatk_ev = self.cleaned_data.get('spatk_ev')
        spdef_ev = self.cleaned_data.get('spdef_ev')
        spd_ev = self.cleaned_data.get('spd_ev')
        
        total_EVs = hp_ev + atk_ev + def_ev + spatk_ev + spdef_ev + spd_ev
        if total_EVs > 510:
            raise forms.ValidationError(f"Invalid EV Spread. The sum of this pokemon's EVs is {total_EVs} which exceeds the limit of 510")
        return cleaned_data