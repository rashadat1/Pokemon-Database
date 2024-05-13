# web scraper

# The little name thing has to be fixed
# The solution is I think to join tables with pokedex based
# on pokedex number

# the problem is the following:
# when we go back to look at our pokedex table to find a pokemon in this table
# some pokemon will not exist like Hoopa. The name Hoopa does not exist or Zacian
# because of the little name issue

# the little names should be stored in a tuple maybe
# but then we would have to restructure so that there is a stat total
# for every form in the tuple

# better solution, append the little name to the big name
# unless the little name is an alolan, galacian, or hirsdasd whatever
# or mega form. In this case we do not append and instead replace

# the only issue is some pokemon will not be found if we lookup their name 



from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import psycopg2
from typing import List, NamedTuple

# url to pokemon database website
url = 'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers = {'User-Agent' : 'Mozilla/5.0'}
)
# header mimics a web browser for the purposes of retrieving
# the webpage
# send HTTP request to the web address
page = urlopen(request)
page_content_bytes = page.read()

# decode utf-8 encoding into html
page_html = page_content_bytes.decode('utf-8')

# parse the HTML content to create a Beautiful Soup
# object called soup
soup = BeautifulSoup(page_html, 'html.parser')

# go through entirety of the page html and return all the table elements
# with an id of pokedex which can be found in the page
pokemon_rows_ = soup.find_all('table',id='pokedex')

# if we go to the table in the html we see thead (formatting the header)
# and then one level deeper there is tbody which has individual lines for 
# each of the pokemon rows (tr)

pokemon_rows = soup.find_all('table', id = 'pokedex')[0].find_all('tbody')[0].find_all('tr')

# indexing through pokemon_rows gives us one pokemon's data for each index
#print(pokemon_rows)

# now within each tr there is a td for each attribute (the data in each row)
# one td for health, one for sp. def, one for sp. atk, etc
pokedex_data = []

conn = psycopg2.connect(database = 'pokemondb',
                        user = 'tarikrashada')

cursor = conn.cursor()


for i in range(len(pokemon_rows)):
    
    pokemon_row_dict = {}
    # The line `pokemon_data = pokemon_rows[i].find_all('td')` is extracting all the `<td>` elements
    # within a specific row (`<tr>`) of the Pokemon table. This line is used within a loop to iterate over
    # each row of the table and retrieve the data for each attribute of a Pokemon, such as ID, name, type,
    # total stats, HP, attack, defense, special attack, special defense, speed, and details URL.
    pokemon_data = pokemon_rows[i].find_all('td')
    
    id = pokemon_data[0]['data-sort-value']
    # url of the pokemon's sprite 
    avatar = pokemon_data[0].find_all('source')[0]['srcset']
    # pokemon name
    name = pokemon_data[0].find_all('img')[0]['alt']
    
    # pokemon type
    type_array = []
    # for every type we have an a tag 
    typing = pokemon_data[2].find_all('a')
    
    # append to path ('https://pokemondb.net') to obtain path to this pokemon's entry on website
    # in pokedex
    details_uri = pokemon_data[1].find_all('a')[0]['href']
    
    # some pokemon have a secondary small name in their entry to indicate that they have a Mega
    # form this is stored as a <small class = 'text-muted'>Mega Venusaur</small>
    # so we add
    
    if pokemon_data[1].find_all('small'):
        small_name = pokemon_data[1].find_all('small')[0].getText()
    
        if ('Mega' in small_name) or ('Hisuian' in small_name) or ('Alolan' in small_name) or ('Galarian' in small_name):
            
            pokemon_row_dict['NAME'] = small_name
        
        else:
            
            pokemon_row_dict['NAME'] = name
    
    else:
        pokemon_row_dict['NAME'] = name
        
    for pokemon_type in typing:
        # take text from the a tags
        type_array.append(pokemon_type.getText())
    
    pokemon_row_dict['TYPE'] = type_array
    
    total = pokemon_data[3].getText()
    hp = pokemon_data[4].getText()
    atk = pokemon_data[5].getText()
    def_ = pokemon_data[6].getText()
    sp_atk = pokemon_data[7].getText()
    sp_def = pokemon_data[8].getText()
    spd = pokemon_data[9].getText()
    
    pokemon_row_dict['TOTAL'] = total
    pokemon_row_dict['HP'] = hp
    pokemon_row_dict['ATK'] = atk
    pokemon_row_dict['DEF'] = def_
    pokemon_row_dict['SPATK'] = sp_atk
    pokemon_row_dict['SPDEF'] = sp_def
    pokemon_row_dict['SPD'] = spd
    
    # lastly we want the pokedex entry for the pokemon which can be found on the webpage
    # at the path obtained by appending details_uri to the main domain name
    
    entry_url = 'https://pokemondb.net' + details_uri
    
    pokemon_row_dict['DETAILS_URL'] = entry_url

    request = Request(
        entry_url,
        headers = {'User-Agent': 'Mozilla/5.0'}
    )
    entry_page_html = urlopen(request).read().decode('utf-8')
    
    # entry_soup is giving whole page for a particular pokemon
    entry_soup = BeautifulSoup(entry_page_html,'html.parser')
    
    print(pokemon_row_dict['NAME'])

    gen = entry_soup.find_all('p')[0].find_all('abbr')[0].getText()[-1]
    
    # one of the div tags with class = resp-scroll contains the pokedex descriptions for each pokemon
    # to find which one of the n divs contains it we loop through entry_text_search which has all divs with this class
    entry_text_search = entry_soup.find_all('main')[0].find_all('div',{'class' : 'resp-scroll'})
    
    pokemon_row_dict['GENERATION'] = gen
    try:
        entry_text_found_len = 0
        for i in range(len(entry_text_search)):
            try:
                # because the pokedex entry will be the longest string stored in one of these divs we look for the
                # div containing the longest text
                if len(entry_text_search[i].find_all('tr')[0].find_all('td')[0].getText()) > entry_text_found_len:
                    entry_text_found = entry_text_search[i]
                    entry_text_found_len = len(entry_text_search[i].find_all('tr')[0].find_all('td')[0].getText())
            except:
                continue
        
        entry_text = entry_text_found.find_all('tr')[0].find_all('td')[0].getText()
                
    except:
        entry_text = 'Pokedex entry not yet available for this Pokemon.'

    pokemon_row_dict['ENTRY_TEXT'] = entry_text
    pokedex_data.append(pokemon_row_dict)

    
# there are 13 div with class resp-scroll and if we check we see the third corresponds to
# the pokedex entries table
#print(entry_text) # = 13


create_table_query = '''
    CREATE TABLE IF NOT EXISTS POKEDEX (
        id SERIAL PRIMARY KEY,
        Name TEXT,
        Details_URL TEXT,
        Type TEXT[],
        Total INT,
        HP INT,
        Atk INT,
        Def INT,
        SPAtk INT,
        SPDef INT,
        Spd INT,
        Entry TEXT,
        Generation INT
        )'''


cursor.execute(create_table_query)
conn.commit()

cursor.execute("SELECT COUNT(*) FROM POKEDEX")
count = cursor.fetchone()[0]

if count == 0:
    for pokemon in pokedex_data:

        cursor.execute('''
            INSERT INTO POKEDEX (Name, Details_URL, Type, Total, HP, Atk, Def, SPAtk, SPDef, Spd, Entry, Generation)
            VALUES (%(NAME)s, %(DETAILS_URL)s, %(TYPE)s, %(TOTAL)s, %(HP)s, %(ATK)s, %(DEF)s, %(SPATK)s, %(SPDEF)s, %(SPD)s, %(ENTRY_TEXT)s, %(GENERATION)s)
            ''', pokemon)

    conn.commit()
else:
    print('POKEDEX table already exists.')

create_table_query = '''
    CREATE TABLE IF NOT EXISTS POKEMON_ABILITIES (
        pokemon_id INT,
        ability_id INT,
        FOREIGN KEY (pokemon_id) REFERENCES POKEDEX(id),
        FOREIGN KEY (ability_id) REFERENCES ABILITIES(id)
        )'''
        
cursor.execute(create_table_query)
conn.commit()


for i in range(len(pokemon_rows)):
    
    pokemon_data = pokemon_rows[i].find_all('td')
    
    details_uri = pokemon_data[1].find_all('a')[0]['href']
    entry_url = 'https://pokemondb.net' + details_uri
    
    Name = pokemon_data[0].find_all('img')[0]['alt']

    if pokemon_data[1].find_all('small'):
        small_name = pokemon_data[1].find_all('small')[0].getText()
    
        if ('Mega' in small_name) or ('Hisuian' in small_name) or ('Alolan' in small_name) or ('Galarian' in small_name):
            
            name = small_name
        
        else:
            
            name = Name
            
    else:
        
        name = Name
            
    request = Request(
        entry_url,
        headers = {'User-Agent': 'Mozilla/5.0'}
    )
    entry_page_html = urlopen(request).read().decode('utf-8')
    
    # entry_soup is giving whole page for a particular pokemon
    entry_soup = BeautifulSoup(entry_page_html,'html.parser')
    ability_list_search = entry_soup.find_all('main')[0].find_all('div',{'class' : 'grid-col span-md-6 span-lg-4'})[0]

    for ability in ability_list_search.find_all('table',{'class' : 'vitals-table'})[0].find_all('tbody')[0].find_all('tr')[5].find_all('td')[0].find_all('span'):
        
        print(name)
        query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
        cursor.execute(query, (name,))
        PokemonID = cursor.fetchone()
        
        ability_name = ability.getText().replace('1. ','').replace('2. ','')
        query2 = 'SELECT id FROM ABILITIES WHERE NAME = %s'
        cursor.execute(query2, (ability_name,))
        AbilityID = cursor.fetchone()
        
        query3 = 'INSERT INTO POKEMON_ABILITIES (pokemon_id, ability_id) VALUES (%s, %s)'
        cursor.execute(query3, (PokemonID[0], AbilityID[0]))
        conn.commit()
        


conn.commit()
cursor.close()
conn.close()
'''
select name from POKEDEX where id in (select pokemon_id from pokemon_abilities where ability_id = (select id from ABILITIES where NAME = 'Arena Trap'))


select p.name, a."name"  from pokedex p, pokemon_abilities pa, abilities a where p.id = pa.pokemon_id and pa.ability_id = a.id and a."name" = 'Arena Trap';
'''