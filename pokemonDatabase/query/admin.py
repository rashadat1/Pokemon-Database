from django.contrib import admin
from .models import Abilities, LearnedByLeveling, LearnedByTm, Moves
from .models import NotableTrainers, Pokedex, PokemonAbilities, PokemonRegion
from .models import Regions

# Register your models here.

admin.site.register(Abilities)
admin.site.register(LearnedByLeveling)
admin.site.register(LearnedByTm)
admin.site.register(Moves)
admin.site.register(NotableTrainers)
admin.site.register(Pokedex)
admin.site.register(PokemonAbilities)
admin.site.register(PokemonRegion)
admin.site.register(Regions)