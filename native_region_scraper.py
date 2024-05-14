# pokemon native region scraper

import psycopg2
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


conn = psycopg2.connect(database = 'pokemondb',
                        user = 'tarikrashada')

cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS POKEMON_REGION (
        pokemon_id INT,
        region_id INT,
        FOREIGN KEY (pokemon_id) REFERENCES POKEDEX(id),
        FOREIGN KEY (region_id) REFERENCES REGIONS(region_id)
    )
'''

cursor.execute(create_table_query)
conn.commit()


game_titles = {
    'Kanto' : 'firered-leafgreen',
    'Johto' : 'heartgold-soulsilver',
    'Sinnoh' : 'platinum',
    'Unova' : 'black-white-2',
    'Kalos' : 'x-y',
    'Hoenn' : 'omega-ruby-alpha-sapphire',
    'Alola' : 'ultra-sun-ultra-moon',
    'Galar' : 'sword-shield',
    'Paldea' : 'scarlet-violet'
}

url_base = 'https://pokemondb.net/pokedex/game/'

for region in game_titles:
    pokemon_names = []
    
    urlpokemonlist = url_base + game_titles[region]
    
    request = Request(
        urlpokemonlist,
        headers = {'User-Agent' : 'Mozilla/5.0'}
    )
    
    urlpokemonlistopened = urlopen(request)
    
    pokemonlisthtml = urlpokemonlistopened.read().decode('utf-8')
    
    regionpokemonsoup = BeautifulSoup(pokemonlisthtml,'html.parser')
    
    pokemon = regionpokemonsoup.find_all('div',{'class' : 'infocard'})
    
    region_id_query = '''SELECT region_id FROM REGIONS WHERE region_name = %s'''
    
    cursor.execute(region_id_query,(region,))
    
    region_id = cursor.fetchone()[0]
    
    for i in range(len(pokemon)):
        name = pokemon[i].find_all('span',{'class' : 'infocard-lg-data text-muted'})[0].find_all('a',{'class' : 'ent-name'})[0].getText()
        pokemon_names.append(name)
        
        pokemon_names = list(set(pokemon_names))
    
    for i in range(len(pokemon_names)):
        
        name_id_query = '''SELECT id FROM POKEDEX WHERE name = %s'''
        
        try:
            cursor.execute(name_id_query,(pokemon_names[i],))
            name_id = cursor.fetchone()[0]
            
        except:
            continue
        
        insert_query = '''INSERT INTO POKEMON_REGION (pokemon_id,region_id) VALUES (%(name_id)s, %(region_id)s)'''
        cursor.execute(insert_query,{'name_id' : name_id,'region_id' : region_id})
        

conn.commit()
cursor.close()
conn.close()
        
        
    


