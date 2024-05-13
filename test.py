from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = 'https://bulbapedia.bulbagarden.net/wiki/Gym_Leader'
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
gymleadersoup = BeautifulSoup(page_html, 'html.parser')

gymleaderInfo = gymleadersoup.find_all('table',{'class' : 'roundy'})

gymleaderlist = []
for i in range(len(gymleaderInfo)-4):
    
    gymleaderstr = {}
    regiongymleaderInfo = gymleadersoup.find_all('table',{'class' : 'roundy'})[i]
    gymleadertable = regiongymleaderInfo.find_all('tbody')[0]
    region = gymleadertable.find_all('tr')[1].find_all('th')[1].find_all('a')[1].getText()
    
    
    gymleadername = gymleadertable.find_all('tr')
