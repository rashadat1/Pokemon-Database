# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Abilities(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    num_holders = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'abilities'
        verbose_name_plural = 'Abilities'

class LearnedByLeveling(models.Model):
    pokemon = models.OneToOneField('Pokedex', on_delete = models.DO_NOTHING, blank = True, primary_key = True)
    move = models.ForeignKey('Moves', models.DO_NOTHING, blank=True, null=True)
    level_learned = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'learned_by_leveling'
        verbose_name_plural = 'Learned By Leveling'


class LearnedByTm(models.Model):
    pokemon = models.OneToOneField('Pokedex', on_delete = models.DO_NOTHING, blank = True, primary_key = True)
    move = models.ForeignKey('Moves', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'learned_by_tm'
        verbose_name_plural = 'Learned By TM'


class Moves(models.Model):
    move_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    element = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)
    pp = models.TextField(blank=True, null=True)
    effect = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'moves'
        verbose_name_plural = 'Moves'


class NotableTrainers(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    region = models.ForeignKey('Regions', models.DO_NOTHING, db_column='region', blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    trainer_class = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'notable_trainers'
        verbose_name_plural = 'Notable Trainers'


class Pokedex(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.TextField(blank=True, null=True)
    details_url = models.TextField(blank=True, null=True)
    type = ArrayField(models.TextField(blank=True, null=True))
    total = models.IntegerField(blank=True, null=True)
    hp = models.IntegerField(blank=True, null=True)
    atk = models.IntegerField(blank=True, null=True)
    def_field = models.IntegerField(db_column='def_val', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    spatk = models.IntegerField(blank=True, null=True)
    spdef = models.IntegerField(blank=True, null=True)
    spd = models.IntegerField(blank=True, null=True)
    entry = models.TextField(blank=True, null=True)
    generation = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'pokedex'
        verbose_name_plural = 'Pokedex'


class PokemonAbilities(models.Model):
    pokemon = models.OneToOneField('Pokedex', on_delete = models.DO_NOTHING, blank = True, primary_key = True)
    ability = models.ForeignKey('Abilities', on_delete = models.DO_NOTHING, blank=True)

    class Meta:
        managed = False
        db_table = 'pokemon_abilities'
        verbose_name_plural = 'Pokemon Abilities'


class PokemonRegion(models.Model):
    pokemon = models.OneToOneField('Pokedex', on_delete = models.DO_NOTHING, blank = True, primary_key = True)
    region = models.ForeignKey('Regions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pokemon_region'
        verbose_name_plural = 'Pokemon Regions'


class Regions(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=20, blank=True, null=True)
    professor_name = models.CharField(max_length=20, blank=True, null=True)
    generations = ArrayField(models.TextField(blank=True, null=True))
    grass_starter = models.ForeignKey(Pokedex, models.DO_NOTHING, blank=True, null=True)
    water_starter = models.ForeignKey(Pokedex, models.DO_NOTHING, related_name='regions_water_starter_set', blank=True, null=True)
    fire_starter = models.ForeignKey(Pokedex, models.DO_NOTHING, related_name='regions_fire_starter_set', blank=True, null=True)

    def __str__(self):
        return self.region_name
    
    class Meta:
        managed = False
        db_table = 'regions'
        verbose_name_plural = 'Regions'