# move scraper

# TBD for alternate forms find scrape their movesets on the page ----- TBD

# TBD for learned_by_tm make a check to see if the text that the pokemon
# cannot learn any tms is here. If so, we should stop searching
# also need to make sure we are not adding moves from non-tm lists by checking
# maybe the message at the header of the table ------ FIXED


# Next up make a regions table - 
# the elite 4 members and the champion
# the gym leaders
# the three starters
# ask gpt for other ideas

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import psycopg2

url = 'https://pokemondb.net/move/all'

request = Request(
    url,
    headers = {'User-Agent' : 'Mozilla/5.0'}
)

conn = psycopg2.connect(database = 'pokemondb',
                        user = 'tarikrashada')

cursor = conn.cursor()


movelistopen = urlopen(request)

movelist_bytes = movelistopen.read()

movelist_html = movelist_bytes.decode('utf-8')

movelist_soup = BeautifulSoup(movelist_html,'html.parser')

movelist = movelist_soup.find_all('body')[0].find_all('main',{'id' : 'main'})[0].find_all('div',{'class' : 'resp-scroll'})[0].find_all('table',{'id' : 'moves'})[0]

movelist_rows = movelist.find_all('tbody')[0].find_all('tr')

move_data = []

for move in movelist_rows:
    
    move_row_dict = {}
    
    name = move.find_all('td')[0].getText()
    element = move.find_all('td')[1].getText()
    category = move.find_all('td')[2]['data-sort-value'].capitalize()
    power = move.find_all('td')[3].getText()
    accuracy = move.find_all('td')[4].getText()
    pp = move.find_all('td')[5].getText()
    effect = move.find_all('td')[6].getText()
    
    # did some investigation and found accuracy has the non-int values of infinity or '-'
    # power and pp have non-int values of '-'
    try:
        accuracy = int(accuracy)
    except:
        accuracy = 100
        
    try:
        power = int(power)
    except:
        power = 0
        
    try:
        pp = int(pp)
    except:
        pp = 10

    move_row_dict['Name'] = name
    move_row_dict['Element'] = element
    move_row_dict['Category'] = category
    move_row_dict['Power'] = power
    move_row_dict['Accuracy'] = accuracy
    move_row_dict['PP'] = pp
    move_row_dict['Effect'] = effect
    
    move_data.append(move_row_dict)
    

create_table_query = '''
    CREATE TABLE IF NOT EXISTS MOVES(
        move_id SERIAL PRIMARY KEY,
        Name TEXT,
        Element TEXT,
        Category TEXT,
        Power INT,
        Accuracy INT,
        PP TEXT,
        Effect TEXT)'''


cursor.execute(create_table_query)

cursor.execute('''SELECT COUNT(*) FROM MOVES''')
length = cursor.fetchone()[0]

if length == 0:
    for i in range(len(move_data)):
        
        insert_query = '''INSERT INTO MOVES(Name, Element, Category, Power, Accuracy, PP, Effect)
            VALUES (%(Name)s, %(Element)s, %(Category)s, %(Power)s, %(Accuracy)s, %(PP)s, %(Effect)s)'''
            
        cursor.execute(insert_query,move_data[i])
        
else:
    print("The MOVES table already contains data.")
        
        
create_table_query = '''
    CREATE TABLE IF NOT EXISTS LEARNED_BY_LEVELING (
        pokemon_id INT,
        move_id INT,
        level_learned INT,
        FOREIGN KEY (pokemon_id) REFERENCES POKEDEX(id),
        FOREIGN KEY (move_id) REFERENCES MOVES (move_id)
    )
'''
cursor.execute(create_table_query)

# make a second reference to a TM/HM Table perhaps for TM/HM number
create_table_query = '''
    CREATE TABLE IF NOT EXISTS LEARNED_BY_TM (
        pokemon_id INT,
        move_id INT,
        FOREIGN KEY (pokemon_id) REFERENCES POKEDEX(id),
        FOREIGN KEY (move_id) REFERENCES MOVES (move_id)
        )
'''

cursor.execute(create_table_query)

cursor.execute("SELECT Details_URL FROM POKEDEX")

res = list(cursor.fetchall())

AllUrls = [v[0] for v in res]

AllUrls = list(set(AllUrls))

# url to pokemon database website
url = 'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers = {'User-Agent' : 'Mozilla/5.0'}
)

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


for i in range(len(pokemon_rows)):
    
    pokemon_data = pokemon_rows[i].find_all('td')
    
    details_url = pokemon_data[1].find_all('a')[0]['href']
    
    entry_url = 'https://pokemondb.net' + details_url
    

    
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
        headers = {'User-Agent' : 'Mozilla/5.0'}
    )
    
    # when we do this need to check if the pokemon name contains Galarian,
    # Hisuian or Alolan. In this case we need to change the tab for the move
    # set

    pokemon_page_html = urlopen(request).read().decode('utf-8')
    
    pokemon_soup = BeautifulSoup(pokemon_page_html, 'html.parser')
    
    print(name)
    
    learnset_tables = pokemon_soup.find_all('div',{'class' : 'sv-tabs-panel-list'})
    
    
    i = 0
    while i < len(learnset_tables) - 1:
        if learnset_tables[i].find_all('h3'):
            while (learnset_tables[i].find_all('h3')[0].getText() != 'Moves learnt by level up'):
                i += 1
                
            if learnset_tables[i].find_all('h3')[0].getText() == 'Moves learnt by level up':
                break
        else:
            i += 1
            
    
    
    level_up_learnset = learnset_tables[i].find_all('div',{'class' : 'resp-scroll'})[0].find_all('tbody')[0].find_all('tr')
    
    # let's make a junction table for pokemon and learned moves
    # let's also make a separate junction table for pokemon and learned moves by tm/hm

    for i in range(len(level_up_learnset)):
        level_learned = level_up_learnset[i].find_all('td')[0].getText()
        move_name = level_up_learnset[i].find_all('td')[1].getText()
        print(level_learned)
        print(move_name)
        
        query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
        cursor.execute(query, (name,))
        PokemonID = cursor.fetchone()
        
        query2 = 'SELECT move_id FROM MOVES WHERE NAME = %s'
        cursor.execute(query2, (move_name,))
        MoveID = cursor.fetchone()
        
        query3 = 'INSERT INTO LEARNED_BY_LEVELING (pokemon_id, move_id, level_learned) VALUES (%s, %s, %s)'
        cursor.execute(query3, (PokemonID[0], MoveID[0], level_learned))
        conn.commit()
    
    j = 0   
    while j < len(learnset_tables):
        if learnset_tables[j].find_all('h3'):
            for k in range(len(learnset_tables[j].find_all('h3'))):
                if learnset_tables[j].find_all('h3')[k].getText() == 'Moves learnt by TM':
                    print('found')
                    print(j)
                    val = j
                    break
                
            while (j < len(learnset_tables)):
                j += 1
        else:
            j += 1
    
    try:
        tm_table = learnset_tables[val].find_all('div',{'class' : 'resp-scroll'})[2]
        #print(tm_table)
        
        first_col_key = tm_table.find_all('table',{'class' : 'data-table'})[0].find_all('thead')[0].find_all('tr')[0].find_all('th',{'class' : 'sorting'})[0].find_all('div',{'class' : 'sortwrap'})[0].getText()
        print(first_col_key)
        if first_col_key == 'TM':
            #print('found the table')
            tm_learnset = tm_table.find_all('tbody')[0].find_all('tr')
            for i in range(len(tm_learnset)):
                move_name = tm_learnset[i].find_all('td')[1].getText()
                print(move_name)
                
                query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
                cursor.execute(query, (name,))
                PokemonID = cursor.fetchone()
                
                query2 = 'SELECT move_id FROM MOVES WHERE NAME = %s'
                cursor.execute(query2, (move_name,))
                MoveID = cursor.fetchone()
                print(PokemonID)
                print(MoveID)
                query3 = 'INSERT INTO LEARNED_BY_TM (pokemon_id, move_id) VALUES (%s, %s)'
                cursor.execute(query3, (PokemonID[0], MoveID[0]))
                conn.commit()
        else:
            raise Exception
    except:
        
        try:
            tm_table = learnset_tables[val].find_all('div',{'class' : 'resp-scroll'})[1]
            #print(tm_table)
            first_col_key = tm_table.find_all('table',{'class' : 'data-table'})[0].find_all('thead')[0].find_all('tr')[0].find_all('th',{'class' : 'sorting'})[0].find_all('div',{'class' : 'sortwrap'})[0].getText()
            print(first_col_key)
            if first_col_key == 'TM':
                tm_learnset = tm_table.find_all('tbody')[0].find_all('tr')
                for i in range(len(tm_learnset)):
                    move_name = tm_learnset[i].find_all('td')[1].getText()
                    print(move_name)
                    
                    query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
                    cursor.execute(query, (name,))
                    PokemonID = cursor.fetchone()
                    
                    query2 = 'SELECT move_id FROM MOVES WHERE NAME = %s'
                    cursor.execute(query2, (move_name,))
                    MoveID = cursor.fetchone()
                    print(PokemonID)
                    print(MoveID)
                    query3 = 'INSERT INTO LEARNED_BY_TM (pokemon_id, move_id) VALUES (%s, %s)'
                    cursor.execute(query3, (PokemonID[0], MoveID[0]))
                    conn.commit()
            else:
                raise Exception
        except:
            
            try:
                
                tm_table = learnset_tables[val].find_all('div',{'class' : 'resp-scroll'})[3]
                first_col_key = tm_table.find_all('table',{'class' : 'data-table'})[0].find_all('thead')[0].find_all('tr')[0].find_all('th',{'class' : 'sorting'})[0].find_all('div',{'class' : 'sortwrap'})[0].getText()
                print(first_col_key)
                if first_col_key == 'TM':
                    tm_learnset = tm_table.find_all('tbody')[0].find_all('tr')
                    for i in range(len(tm_learnset)):
                        move_name = tm_learnset[i].find_all('td')[1].getText()
                        print(move_name)
                        
                        query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
                        cursor.execute(query, (name,))
                        PokemonID = cursor.fetchone()
                        
                        query2 = 'SELECT move_id FROM MOVES WHERE NAME = %s'
                        cursor.execute(query2, (move_name,))
                        MoveID = cursor.fetchone()
                        print(PokemonID)
                        print(MoveID)
                        query3 = 'INSERT INTO LEARNED_BY_TM (pokemon_id, move_id) VALUES (%s, %s)'
                        cursor.execute(query3, (PokemonID[0], MoveID[0]))
                        conn.commit()
                else:
                    raise Exception
            except:
                
                try:
                    
                    tm_table = learnset_tables[val].find_all('div',{'class' : 'resp-scroll'})[4]
                    first_col_key = tm_table.find_all('table',{'class' : 'data-table'})[0].find_all('thead')[0].find_all('tr')[0].find_all('th',{'class' : 'sorting'})[0].find_all('div',{'class' : 'sortwrap'})[0].getText()
                    print(first_col_key)
                    if first_col_key == 'TM':
                        tm_learnset = tm_table.find_all('tbody')[0].find_all('tr')
                        for i in range(len(tm_learnset)):
                            move_name = tm_learnset[i].find_all('td')[1].getText()
                            print(move_name)
                            
                            query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
                            cursor.execute(query, (name,))
                            PokemonID = cursor.fetchone()
                            
                            query2 = 'SELECT move_id FROM MOVES WHERE NAME = %s'
                            cursor.execute(query2, (move_name,))
                            MoveID = cursor.fetchone()
                            print(PokemonID)
                            print(MoveID)
                            query3 = 'INSERT INTO LEARNED_BY_TM (pokemon_id, move_id) VALUES (%s, %s)'
                            cursor.execute(query3, (PokemonID[0], MoveID[0]))
                            conn.commit()
                    else:
                        raise Exception
                except:
                    
                    try:
                        tm_table = learnset_tables[val].find_all('div',{'class' : 'resp-scroll'})[5]
                        first_col_key = tm_table.find_all('table',{'class' : 'data-table'})[0].find_all('thead')[0].find_all('tr')[0].find_all('th',{'class' : 'sorting'})[0].find_all('div',{'class' : 'sortwrap'})[0].getText()
                        print(first_col_key)
                        if first_col_key == 'TM':
                            tm_learnset = tm_table.find_all('tbody')[0].find_all('tr')
                            for i in range(len(tm_learnset)):
                                move_name = tm_learnset[i].find_all('td')[1].getText()
                                print(move_name)
                                
                                query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
                                cursor.execute(query, (name,))
                                PokemonID = cursor.fetchone()
                                
                                query2 = 'SELECT move_id FROM MOVES WHERE NAME = %s'
                                cursor.execute(query2, (move_name,))
                                MoveID = cursor.fetchone()
                                print(PokemonID)
                                print(MoveID)
                                query3 = 'INSERT INTO LEARNED_BY_TM (pokemon_id, move_id) VALUES (%s, %s)'
                                cursor.execute(query3, (PokemonID[0], MoveID[0]))
                                conn.commit()
                        else:
                            raise Exception                                
                    except:
                        
                        try:
                            tm_table = learnset_tables[val].find_all('div',{'class' : 'resp-scroll'})[6]
                            first_col_key = tm_table.find_all('table',{'class' : 'data-table'})[0].find_all('thead')[0].find_all('tr')[0].find_all('th',{'class' : 'sorting'})[0].find_all('div',{'class' : 'sortwrap'})[0].getText()
                            print(first_col_key)
                            if first_col_key == 'TM':
                                tm_learnset = tm_table.find_all('tbody')[0].find_all('tr')
                                for i in range(len(tm_learnset)):
                                    move_name = tm_learnset[i].find_all('td')[1].getText()
                                    print(move_name)
                                    
                                    query = 'SELECT id FROM POKEDEX WHERE NAME = %s'
                                    cursor.execute(query, (name,))
                                    PokemonID = cursor.fetchone()
                                    
                                    query2 = 'SELECT move_id FROM MOVES WHERE NAME = %s'
                                    cursor.execute(query2, (move_name,))
                                    MoveID = cursor.fetchone()
                                    print(PokemonID)
                                    print(MoveID)
                                    query3 = 'INSERT INTO LEARNED_BY_TM (pokemon_id, move_id) VALUES (%s, %s)'
                                    cursor.execute(query3, (PokemonID[0], MoveID[0]))
                                    conn.commit()
                            else:
                                raise Exception
                        except:
                            continue
conn.commit()
cursor.close()
conn.close()