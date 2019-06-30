import time
import re
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

webpage = os.getenv('MANGASEE_MANGALIST')
# manga = 'Tekken-Chinmi-Legends'
manga = 'Shingeki-No-Kyojin'
# manga = 'Nanatsu-No-Taizai'
# manga = 'Hunter-X-Hunter'
# manga = 'One-Piece'
# manga = 'Boruto'

site = webpage + manga
print(site)

starttime = time.time()

response = requests.get(site)
if response.status_code != 200:
    print("Error during connection. Status code:", response.status_code)
    quit()
soup = BeautifulSoup(response.text, 'html.parser')
latest_chapters = soup.findAll('span',{'class':'chapterLabel'})

for t in latest_chapters[:8]:
    print(t.text)

endtime = time.time()

print('Total Time:', endtime-starttime)
print('** script done **')
