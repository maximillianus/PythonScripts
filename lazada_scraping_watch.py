import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import os

url = 'https://pages.lazada.sg/wow/i/sg/SGCampaign/match-your-watch-9-to-5-look-watches?spm=a2o42.11498105.icms-' \
'5018142-1526288547130.1.52155f86ELEwY8&hybrid=1&scm=1003.4.icms-zebra-5018141-2738295.OTHER_5278278882_2396089'

proxies = {'http': 'http://10.62.36.14:80',
            'https': 'http://10.62.36.14:80'}

page = requests.get(url, proxies=proxies, verify=False)

soup = BeautifulSoup(page.text, 'html.parser')
s = soup.find('script', type='text/data')

# get data as json format
jsondata = json.loads(s.text)

# convert json to dataframe
df = pd.DataFrame.from_dict(jsondata)

# print(df.head())

# clean data
df.itemTitle = df.itemTitle.str.capitalize()
df.itemDiscountPrice = df.itemDiscountPrice.str.replace(',','')
df['itemDiscountPrice'] = df.itemDiscountPrice.astype(float)
df.itemPrice = df.itemPrice.str.replace(',','')
df['itemPrice'] = df.itemPrice.astype(float)
df['itemModel'] = df.itemTitle.str.extract('([A-Za-z]{1,5}[0-9]+[-0-9a-zA-Z]+)')
df['itemBrand'] = df.itemTitle.str.extract('([sS]eiko|[cC]itizen|[oO]rient|[tT]issot)')
df['japanMade'] = df.itemTitle.str.extract('([jJ]apan|JAPAN)')

# set dir
os.chdir('C:\\NotBackedUp\\codes\\Pyscript')

# write to file
df.to_csv('lazada_watch_sale.csv')

print('script done')