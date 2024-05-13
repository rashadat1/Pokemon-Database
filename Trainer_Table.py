# Notable Trainer Table
import psycopg2

gym_leaders_list = [
    # Kanto Gym Leaders
    {"Name": "Brock", "Region Name": "Kanto", "Type": "Rock", "Location": "Pewter City", "TrainerType": "Gym Leader"},
    {"Name": "Misty", "Region Name": "Kanto", "Type": "Water", "Location": "Cerulean City", "TrainerType": "Gym Leader"},
    {"Name": "Lt. Surge", "Region Name": "Kanto", "Type": "Electric", "Location": "Vermilion City", "TrainerType": "Gym Leader"},
    {"Name": "Erika", "Region Name": "Kanto", "Type": "Grass", "Location": "Celadon City", "TrainerType": "Gym Leader"},
    {"Name": "Koga", "Region Name": "Kanto", "Type": "Poison", "Location": "Fuchsia City", "TrainerType": "Gym Leader"},
    {"Name": "Sabrina", "Region Name": "Kanto", "Type": "Psychic", "Location": "Saffron City", "TrainerType": "Gym Leader"},
    {"Name": "Blaine", "Region Name": "Kanto", "Type": "Fire", "Location": "Cinnabar Island", "TrainerType": "Gym Leader"},
    {"Name": "Giovanni", "Region Name": "Kanto", "Type": "Ground", "Location": "Viridian City", "TrainerType": "Gym Leader"},
    # Johto Gym Leaders
    {"Name": "Falkner", "Region Name": "Johto", "Type": "Flying", "Location": "Violet City", "TrainerType": "Gym Leader"},
    {"Name": "Bugsy", "Region Name": "Johto", "Type": "Bug", "Location": "Azalea Town", "TrainerType": "Gym Leader"},
    {"Name": "Whitney", "Region Name": "Johto", "Type": "Normal", "Location": "Goldenrod City", "TrainerType": "Gym Leader"},
    {"Name": "Morty", "Region Name": "Johto", "Type": "Ghost", "Location": "Ecruteak City", "TrainerType": "Gym Leader"},
    {"Name": "Chuck", "Region Name": "Johto", "Type": "Fighting", "Location": "Cianwood City", "TrainerType": "Gym Leader"},
    {"Name": "Jasmine", "Region Name": "Johto", "Type": "Steel", "Location": "Olivine City", "TrainerType": "Gym Leader"},
    {"Name": "Pryce", "Region Name": "Johto", "Type": "Ice", "Location": "Mahogany Town", "TrainerType": "Gym Leader"},
    {"Name": "Clair", "Region Name": "Johto", "Type": "Dragon", "Location": "Blackthorn City", "TrainerType": "Gym Leader"},
    # Hoenn Gym Leaders
    {"Name": "Roxanne", "Region Name": "Hoenn", "Type": "Rock", "Location": "Rustboro City", "TrainerType": "Gym Leader"},
    {"Name": "Brawly", "Region Name": "Hoenn", "Type": "Fighting", "Location": "Dewford Town", "TrainerType": "Gym Leader"},
    {"Name": "Wattson", "Region Name": "Hoenn", "Type": "Electric", "Location": "Mauville City", "TrainerType": "Gym Leader"},
    {"Name": "Flannery", "Region Name": "Hoenn", "Type": "Fire", "Location": "Lavaridge Town", "TrainerType": "Gym Leader"},
    {"Name": "Norman", "Region Name": "Hoenn", "Type": "Normal", "Location": "Petalburg City", "TrainerType": "Gym Leader"},
    {"Name": "Winona", "Region Name": "Hoenn", "Type": "Flying", "Location": "Fortree City", "TrainerType": "Gym Leader"},
    {"Name": "Tate and Liza", "Region Name": "Hoenn", "Type": "Psychic", "Location": "Mossdeep City", "TrainerType": "Gym Leader"},
    {"Name": "Juan", "Region Name": "Hoenn", "Type": "Water", "Location": "Sootopolis City", "TrainerType": "Gym Leader"},
    # Unova Gym Leaders
    {"Name": "Cilan", "Region Name": "Unova", "Type": "Grass", "Location": "Striaton City", "TrainerType": "Gym Leader"},
    {"Name": "Chili", "Region Name": "Unova", "Type": "Fire", "Location": "Striaton City", "TrainerType": "Gym Leader"},
    {"Name": "Cress", "Region Name": "Unova", "Type": "Water", "Location": "Striaton City", "TrainerType": "Gym Leader"},
    {"Name": "Lenora", "Region Name": "Unova", "Type": "Normal", "Location": "Nacrene City", "TrainerType": "Gym Leader"},
    {"Name": "Burgh", "Region Name": "Unova", "Type": "Bug", "Location": "Castelia City", "TrainerType": "Gym Leader"},
    {"Name": "Elesa", "Region Name": "Unova", "Type": "Electric", "Location": "Nimbasa City", "TrainerType": "Gym Leader"},
    {"Name": "Clay", "Region Name": "Unova", "Type": "Ground", "Location": "Driftveil City", "TrainerType": "Gym Leader"},
    {"Name": "Skyla", "Region Name": "Unova", "Type": "Flying", "Location": "Mistralton City", "TrainerType": "Gym Leader"},
    {"Name": "Drayden", "Region Name": "Unova", "Type": "Dragon", "Location": "Opelucid City", "TrainerType": "Gym Leader"},
    {"Name": "Marlon", "Region Name": "Unova", "Type": "Water", "Location": "Humilau City", "TrainerType": "Gym Leader"},
    # Kalos Gym Leaders
    {"Name": "Viola", "Region Name": "Kalos", "Type": "Bug", "Location": "Santalune City", "TrainerType": "Gym Leader"},
    {"Name": "Grant", "Region Name": "Kalos", "Type": "Rock", "Location": "Cyllage City", "TrainerType": "Gym Leader"},
    {"Name": "Korrina", "Region Name": "Kalos", "Type": "Fighting", "Location": "Shalour City", "TrainerType": "Gym Leader"},
    {"Name": "Ramos", "Region Name": "Kalos", "Type": "Grass", "Location": "Coumarine City", "TrainerType": "Gym Leader"},
    {"Name": "Clemont", "Region Name": "Kalos", "Type": "Electric", "Location": "Lumiose City", "TrainerType": "Gym Leader"},
    {"Name": "Valerie", "Region Name": "Kalos", "Type": "Fairy", "Location": "Laverre City", "TrainerType": "Gym Leader"},
    {"Name": "Olympia", "Region Name": "Kalos", "Type": "Psychic", "Location": "Anistar City", "TrainerType": "Gym Leader"},
    {"Name": "Wulfric", "Region Name": "Kalos", "Type": "Ice", "Location": "Snowbelle City", "TrainerType": "Gym Leader"},
    # Galar Gym Leaders
    {"Name": "Milo", "Region Name": "Galar", "Type": "Grass", "Location": "Turffield", "TrainerType": "Gym Leader"},
    {"Name": "Nessa", "Region Name": "Galar", "Type": "Water", "Location": "Hulbury", "TrainerType": "Gym Leader"},
    {"Name": "Kabu", "Region Name": "Galar", "Type": "Fire", "Location": "Motostoke", "TrainerType": "Gym Leader"},
    {"Name": "Bea/Allister", "Region Name": "Galar", "Type": "Fighting/Ghost", "Location": "Stow-on-Side/Balnlea", "TrainerType": "Gym Leader"},
    {"Name": "Opal", "Region Name": "Galar", "Type": "Fairy", "Location": "Ballonlea", "TrainerType": "Gym Leader"},
    {"Name": "Gordie/Melony", "Region Name": "Galar", "Type": "Rock/Ice", "Location": "Circhester", "TrainerType": "Gym Leader"},
    {"Name": "Piers", "Region Name": "Galar", "Type": "Dark", "Location": "Spikemuth", "TrainerType": "Gym Leader"},
    {"Name": "Raihan", "Region Name": "Galar", "Type": "Dragon", "Location": "Hammerlocke", "TrainerType": "Gym Leader"},
    # Sinnoh Gym Leaders
    {"Name": "Roark", "Region Name": "Sinnoh", "Type": "Rock", "Location": "Oreburgh City", "TrainerType": "Gym Leader"},
    {"Name": "Gardenia", "Region Name": "Sinnoh", "Type": "Grass", "Location": "Eterna City", "TrainerType": "Gym Leader"},
    {"Name": "Maylene", "Region Name": "Sinnoh", "Type": "Fighting", "Location": "Veilstone City", "TrainerType": "Gym Leader"},
    {"Name": "Crasher Wake", "Region Name": "Sinnoh", "Type": "Water", "Location": "Pastoria City", "TrainerType": "Gym Leader"},
    {"Name": "Fantina", "Region Name": "Sinnoh", "Type": "Ghost", "Location": "Hearthome City", "TrainerType": "Gym Leader"},
    {"Name": "Byron", "Region Name": "Sinnoh", "Type": "Steel", "Location": "Canalave City", "TrainerType": "Gym Leader"},
    {"Name": "Candice", "Region Name": "Sinnoh", "Type": "Ice", "Location": "Snowpoint City", "TrainerType": "Gym Leader"},
    {"Name": "Volkner", "Region Name": "Sinnoh", "Type": "Electric", "Location": "Sunyshore City", "TrainerType": "Gym Leader"},
    # Paldea Gym Leaders
    {"Name": "Katy", "Region Name": "Paldea", "Type": "Bug", "Location": "Cortondo Town", "TrainerType": "Gym Leader"},
    {"Name": "Brassius", "Region Name": "Paldea", "Type": "Grass", "Location": "Artazon Town", "TrainerType": "Gym Leader"},
    {"Name": "Iono", "Region Name": "Paldea", "Type": "Electric", "Location": "Levincia City", "TrainerType": "Gym Leader"},
    {"Name": "Kofu", "Region Name": "Paldea", "Type": "Water", "Location": "Cascarrafa City", "TrainerType": "Gym Leader"},
    {"Name": "Larry", "Region Name": "Paldea", "Type": "Normal", "Location": "Medali Town", "TrainerType": "Gym Leader"},
    {"Name": "Ryme", "Region Name": "Paldea", "Type": "Ghost", "Location": "Montenevera Town", "TrainerType": "Gym Leader"},
    {"Name": "Tulip", "Region Name": "Paldea", "Type": "Psychic", "Location": "Alfornada Town", "TrainerType": "Gym Leader"},
    {"Name": "Grusha", "Region Name": "Paldea", "Type": "Ice", "Location": "Glaseado Mountain", "TrainerType": "Gym Leader"}
]

elite_four_list = [
    # Kanto E4
    {"Name": "Lorelei", "Region Name": "Kanto", "Type": "Ice", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    {"Name": "Bruno", "Region Name": "Kanto", "Type": "Fighting", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    {"Name": "Agatha", "Region Name": "Kanto", "Type": "Ghost", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    {"Name": "Lance", "Region Name": "Kanto", "Type": "Dragon", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    # Johto E4
    {"Name": "Will", "Region Name": "Johto", "Type": "Psychic", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    {"Name": "Koga", "Region Name": "Johto", "Type": "Poison", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    {"Name": "Bruno", "Region Name": "Johto", "Type": "Fighting", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    {"Name": "Karen", "Region Name": "Johto", "Type": "Dark", "Location": "Indigo Plateau", "TrainerType": "Elite Four"},
    # Hoenn E4
    {"Name": "Sidney", "Region Name": "Hoenn", "Type": "Dark", "Location": "Ever Grande City", "TrainerType": "Elite Four"},
    {"Name": "Phoebe", "Region Name": "Hoenn", "Type": "Ghost", "Location": "Ever Grande City", "TrainerType": "Elite Four"},
    {"Name": "Glacia", "Region Name": "Hoenn", "Type": "Ice", "Location": "Ever Grande City", "TrainerType": "Elite Four"},
    {"Name": "Drake", "Region Name": "Hoenn", "Type": "Dragon", "Location": "Ever Grande City", "TrainerType": "Elite Four"},
    # Sinnoh E4
    {"Name": "Aaron", "Region Name": "Sinnoh", "Type": "Bug", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Bertha", "Region Name": "Sinnoh", "Type": "Ground", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Flint", "Region Name": "Sinnoh", "Type": "Fire", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Lucian", "Region Name": "Sinnoh", "Type": "Psychic", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    # Unova E4
    {"Name": "Shauntal", "Region Name": "Unova", "Type": "Ghost", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Marshal", "Region Name": "Unova", "Type": "Fighting", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Grimsley", "Region Name": "Unova", "Type": "Dark", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Caitlin", "Region Name": "Unova", "Type": "Psychic", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    # Kalos E4
    {"Name": "Malva", "Region Name": "Kalos", "Type": "Fire", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Wikstrom", "Region Name": "Kalos", "Type": "Steel", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Drasna", "Region Name": "Kalos", "Type": "Dragon", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    {"Name": "Siebold", "Region Name": "Kalos", "Type": "Water", "Location": "Pokémon League", "TrainerType": "Elite Four"},
    # Galar E4
    {"Name": "Bede", "Region Name": "Galar", "Type": "Fairy", "Location": "Wyndon", "TrainerType": "Champion Cup"},
    {"Name": "Marnie", "Region Name": "Galar", "Type": "Dark", "Location": "Wyndon", "TrainerType": "Champion Cup"},
    {"Name": "Hop", "Region Name": "Galar", "Type": "Mixed", "Location": "Wyndon", "TrainerType": "Champion Cup"},
    #Paldea E4
    {"Name": "Rika", "Region Name": "Paldea", "Type": "Ground", "Location": "Pokemon League", "TrainerType": "Elite Four"},
    {"Name": "Poppy", "Region Name": "Paldea", "Type": "Steel", "Location": "Pokemon League", "TrainerType": "Elite Four"},
    {"Name": "Larry", "Region Name": "Paldea", "Type": "Flying", "Location": "Pokemon League", "TrainerType": "Elite Four"},
    {"Name": "Hassel", "Region Name": "Paldea", "Type": "Dragon", "Location": "Pokemon League", "TrainerType": "Elite Four"}
]

champion_list = [
    # Kanto
    {"Name": "Blue", "Region Name": "Kanto", "Location": "Indigo Plateau", "TrainerType": "Champion", "Type": "Mixed"},
    # Johto
    {"Name": "Lance", "Region Name": "Johto", "Location": "Indigo Plateau", "TrainerType": "Champion", "Type": "Dragon"},
    # Hoenn
    {"Name": "Steven Stone", "Region Name": "Hoenn", "Location": "Ever Grande City", "TrainerType": "Champion", "Type": "Steel"},
    # Sinnoh
    {"Name": "Cynthia", "Region Name": "Sinnoh", "Location": "Pokémon League", "TrainerType": "Champion", "Type": "Mixed"},
    # Unova
    {"Name": "Alder", "Region Name": "Unova", "Location": "Pokémon League", "TrainerType": "Champion", "Type": "Mixed"},
    # Kalos
    {"Name": "Diantha", "Region Name": "Kalos", "Location": "Pokémon League", "TrainerType": "Champion", "Type": "Fairy"},
    # Alola
    {"Name": "Hau", "Region Name": "Alola", "Location": "Indigo Plateau", "TrainerType": "Champion", "Type": "Mixed"},
    # Galar
    {"Name": "Leon", "Region Name": "Galar", "Location": "Wyndon", "TrainerType": "Champion", "Type": "Normal"},
    # Paldea
    {"Name": "Geeta", "Region Name": "Paldea", "Location": "Pokemon League", "TrainerType": "Champion", "Type": "Mixed"}
]

notable_trainers = []
notable_trainers.extend(gym_leaders_list)
notable_trainers.extend(elite_four_list)
notable_trainers.extend(champion_list)

create_table_query = '''
    CREATE TABLE IF NOT EXISTS NOTABLE_TRAINERS (
        trainer_id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        region INT,
        Location VARCHAR(50),
        Trainer_Class VARCHAR(50),
        Type VARCHAR(20),
        FOREIGN KEY (region) REFERENCES REGIONS(region_id)
    )
'''

conn = psycopg2.connect(database = 'pokemondb',
                        user = 'tarikrashada')

cursor = conn.cursor()

cursor.execute(create_table_query)

for trainer in notable_trainers:
    
    region_name = trainer['Region Name']
    
    region_id_query = '''SELECT region_id FROM REGIONS WHERE region_name = %s'''
    
    cursor.execute(region_id_query,(region_name,))
    
    region_id = cursor.fetchone()[0]
    
    trainer['Region ID'] = region_id
    
    insert_query = '''INSERT INTO NOTABLE_TRAINERS (name, region, Location, Trainer_Class, Type)
        VALUES (%(Name)s, %(Region ID)s, %(Location)s, %(TrainerType)s, %(Type)s)'''
        
    cursor.execute(insert_query,trainer)
    

conn.commit()
cursor.close()
conn.close()