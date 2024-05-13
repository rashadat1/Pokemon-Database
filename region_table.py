# Region Table
import psycopg2


create_table_query = '''
    CREATE TABLE IF NOT EXISTS REGIONS (
        region_id SERIAL PRIMARY KEY,
        region_name VARCHAR(10),
        professor_name VARCHAR(20),
        generations VARCHAR[],
        grass_starter_id INT,
        water_starter_id INT,
        fire_starter_id INT,
        FOREIGN KEY (grass_starter_id) REFERENCES POKEDEX(id),
        FOREIGN KEY (water_starter_id) REFERENCES POKEDEX(id),
        FOREIGN KEY (fire_starter_id) REFERENCES POKEDEX(id))'''
        

conn = psycopg2.connect(database = 'pokemondb',
                        user = 'tarikrashada')

cursor = conn.cursor()

cursor.execute(create_table_query)

starter_list = {
    'Kanto': ['Bulbasaur', 'Squirtle', 'Charmander'],
    'Johto': ['Chikorita', 'Totodile', 'Cyndaquil'],
    'Hoenn': ['Treecko', 'Mudkip', 'Torchic'],
    'Sinnoh': ['Turtwig', 'Piplup', 'Chimchar'],
    'Unova': ['Snivy', 'Oshawott', 'Tepig'],
    'Kalos': ['Chespin', 'Froakie', 'Fennekin'],
    'Alola': ['Rowlet', 'Popplio', 'Litten'],
    'Galar': ['Grookey', 'Sobble', 'Scorbunny'],
    'Paldea': ['Sprigatito', 'Fuecoco', 'Quaxly']
}

professor_list = {
    'Kanto': 'Oak',
    'Johto': 'Elm',
    'Hoenn': 'Birch',
    'Sinnoh': 'Rowan',
    'Unova': 'Juniper',
    'Kalos': 'Sycamore',
    'Alola': 'Kukui',
    'Galar': 'Magnolia',
    'Paldea': 'Sada,Turo'
}

generation_list = {
    'Kanto': [1,2,3,4,7],
    'Johto': [2,4],
    'Hoenn': [3,6],
    'Sinnoh': [4,8],
    'Unova': [5,9],
    'Kalos': [6,9],
    'Alola': [7],
    'Galar': [8],
    'Paldea': [9]
}

regionInfoStr = []
for region in starter_list.keys():
    
    regionInfo = {}
    
    region_name = region
    professor = professor_list[region]
    generations = generation_list[region]
    
    [grass,water,fire] = starter_list[region]
    
    pokemon_id_query = 'SELECT id FROM POKEDEX WHERE name = %s'
    
    grass_pokemon_query = cursor.execute(pokemon_id_query,(grass,))
    grass_pokemon_id = cursor.fetchone()[0]
    
    water_pokemon_query = cursor.execute(pokemon_id_query,(water,))
    water_pokemon_id = cursor.fetchone()[0]

    
    fire_pokemon_query = cursor.execute(pokemon_id_query,(fire,))
    fire_pokemon_id = cursor.fetchone()[0]
    
    regionInfo['Name'] = region_name
    regionInfo['Professor'] = professor
    regionInfo['Grass_Starter'] = grass_pokemon_id
    regionInfo['Water_Starter'] = water_pokemon_id
    regionInfo['Fire_Starter'] = fire_pokemon_id
    regionInfo['Generations'] = generations
    
    regionInfoStr.append(regionInfo)
    
    
for i in range(len(starter_list.keys())):
    
    insert_query = '''
        INSERT INTO REGIONS (region_name, professor_name, generations, grass_starter_id, water_starter_id, fire_starter_id)
        VALUES (%(Name)s, %(Professor)s, %(Generations)s, %(Grass_Starter)s, %(Water_Starter)s, %(Fire_Starter)s)'''
        
    cursor.execute(insert_query,regionInfoStr[i])
    

    
    

conn.commit()
cursor.close()
conn.close()