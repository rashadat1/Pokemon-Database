# ability scraper

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import psycopg2
from typing import List, NamedTuple

# url to pokemon database website ability page
url = 'https://pokemondb.net/ability'
request = Request(
    url,
    headers = {'User-Agent' : 'Mozilla/5.0'}
)

abilitypage = urlopen(request)
page_content_bytes = abilitypage.read()

abilitypage_html = page_content_bytes.decode('utf-8')

ability_soup = BeautifulSoup(abilitypage_html,'html.parser')

ability_rows = ability_soup.find_all('main')[0].find_all('div',{'class' : 'resp-scroll'})[0].find_all('table',id='abilities')[0].find_all('tbody')[0]

ability_scraped = []

for i in range(len(ability_rows.find_all('tr'))):
    ability_row_table = {}
    ability_row_table['NAME'] = ability_rows.find_all('tr')[i].find_all('td')[0].find_all('a',{'class' : 'ent-name'})[0].getText()
    ability_row_table['DESCRIPTION'] = ability_rows.find_all('tr')[i].find_all('td',{'class' : 'cell-med-text'})[0].getText()
    ability_row_table['NUM_HOLDERS'] = ability_rows.find_all('tr')[i].find_all('td',{'class' : 'cell-num cell-total'})[0].getText()
    
    ability_scraped.append(ability_row_table)


conn = psycopg2.connect(database = 'pokemondb',
                        user = 'tarikrashada')

cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS ABILITIES (
        id SERIAL PRIMARY KEY,
        Name TEXT,
        Description TEXT,
        Num_Holders INT
        )'''
        
        
cursor.execute(create_table_query)

cursor.execute("SELECT COUNT(*) FROM ABILITIES")
count = cursor.fetchone()[0]

if count == 0:
    for ability in ability_scraped:
        print(ability)
        cursor.execute(
            '''
            INSERT INTO ABILITIES (Name, Description, Num_Holders)
            VALUES (%(NAME)s, %(DESCRIPTION)s, %(NUM_HOLDERS)s)
            ''',ability)
        
    conn.commit()
    
cursor.close()
conn.close()