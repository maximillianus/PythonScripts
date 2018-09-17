"""
Script to scrape KPU website entirel to gain ~ 150M NIK
Functionality:
1. login to the target KPU website which contains data and scrape the table
    a. find table name 'table table-striped table-bordered display select dataTable no-footer'
    b. scrape table
    c. find paginate button 'next'
    d. repeat a & b
    e. repeat c - a - b until no more next button
2. go to the regional page and scrape the link
3. Need to add features to easily continue after broken download

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import csv
import os
import random
import platform
from datetime import datetime
import argparse
import re

# initialize working directory and webdriver path
webdriver_execpath = '/Users/adityap/Codes/webdriver/geckodriver'
if platform.system() == 'Darwin':
    os.chdir('/Users/adityap/Work/Xendit')
    webdriver_execpath = '/Users/adityap/Codes/webdriver/geckodriver'
elif platform.system() == 'Windows':
    os.chdir('D:\\Downloads\\koko')
    webdriver_execpath = 'D:\\Downloads\\koko\\webdriver\\geckodriver.exe'

# Create function to scrape javascript table
writeToFileToggle = 0
def scrape_table(province, kabupaten, kecamatan, kelurahan, tps):
    # alert may appear here, try to catch alert
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to_alert()
        alert.accept()
        print('alert accepted')
    except TimeoutException:
        print('no alert')
    show_entry_select = Select(wait.until(EC.presence_of_element_located((By.NAME, 'listDps_length'))))
    show_entry_select.select_by_value('100')
    while True:
        region = [province, kabupaten, kecamatan, kelurahan, tps]
        no_more_next = 'paginate_button next disabled'
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table_id = 'listDps'
        table = soup.find('table', id=table_id)
        rows = table.find_all('tr')
        #refresh once if no data available
        if rows[1].text == 'No data available in table':
            driver.refresh()
            show_entry_select = Select(wait.until(EC.presence_of_element_located((By.NAME, 'listDps_length'))))
            show_entry_select.select_by_value('100')
            soup = BeautifulSoup(driver.page_source, 'lxml')
            rows = soup.find('table', id=table_id).find_all('tr')
        for row in rows[1:]:
            cols = [ele.text for ele in row.find_all('td')]
            # print(cols + region)
            if writeToFileToggle == 1 and platform.system() =='Windows':
                with open('dataset/KTP_scrapes/'+outputname, 'a', encoding='utf8', newline='') as resFile:
                    writer = csv.writer(resFile)
                    writer.writerow(cols + region)
            if writeToFileToggle == 1 and platform.system() =='Darwin':
                with open('dataset/KTP_scrapes/'+outputname, 'a', encoding='utf8') as resFile:
                    writer = csv.writer(resFile)
                    writer.writerow(cols + region)
        print('\t  ',cols[0])
        time.sleep(0.7)
        next_button = driver.find_element_by_id('listDps_next')
        if next_button.get_attribute('class') == no_more_next:
            return int(cols[0])
            break
        else:
            next_button.click()
            time.sleep(1.3)

def fetch_links_and_go(linktext):
    try:
        url_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, linktext)))
    except TimeoutException:
        print('waiting too long')
        driver.refresh()
    region = url_link.text
    url_link.click()
    # wait for page to load
    time.sleep(1)
    # print data table info
    datatable_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.dataTables_info'))).text
    max_entry_len = int(re.findall(r'\d+', datatable_info)[2])
    if max_entry_len > 50:
        print(datatable_info)
        print('max length of entries:', max_entry_len)
        show_entry_select = Select(wait.until(EC.presence_of_element_located((By.TAG_NAME, 'select'))))
        show_entry_select.select_by_value('100')


#start time
start_time = time.time()
print('Time:', datetime.now())

# Parsing argument if any
# parser = argparse.ArgumentParser(description='Process province name.')
# parser.add_argument('province', metavar='N', type=str, help='a string showing province')
# args = parser.parse_args()
# province_name = args.province.upper()



# wait until 'table tbody a' links appear
url = 'https://infopemilu.kpu.go.id/pilkada2018/pemilih/dpt/1/nasional'
driver = webdriver.Firefox(executable_path=webdriver_execpath)
driver.get(url)
wait = WebDriverWait(driver, 10)
province_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody a')))

# find province
province_name = 'kalimantan barat'.upper()
province_link = driver.find_element(By.LINK_TEXT, province_name)

# These are to decide the index which scraping should start or continue
# kabupaten
ii = 0
# kecamatan
jj = 0
# kelurahan
kk = 0
# tps
ll = 0

# sample region that has more than > 50 TPS per page
# 1. Banten > Tangerang > Curug > Binong
# 2. Kalimantan Barat > Kota Pontianak > Pontianak Barat > Sungai Beliung

# click on province
province_link.click()

kabupaten_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody a')))
kabupaten_links_text = [a.text for a in kabupaten_links]
time.sleep(2)

# Select kabupaten starting from the first one
# for i in range(0, len(kabupaten_links)):
for kabupaten_text in kabupaten_links_text[ii:]:
    # go into each link and go back
    region_chained = province_name + '>' + kabupaten_text
    print(region_chained)
    fetch_links_and_go(kabupaten_text)
    kecamatan_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody a')))
    kecamatan_links_text = [a.text for a in kecamatan_links]
    for kecamatan_text in kecamatan_links_text[jj:]:
        region_chained = province_name + '>' + kabupaten_text + '>' + kecamatan_text
        print(region_chained)
        fetch_links_and_go(kecamatan_text)
        kelurahan_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody a')))
        kelurahan_links_text = [a.text for a in kelurahan_links]
        for kelurahan_text in kelurahan_links_text[kk:]:
            region_chained = province_name + '>' + kabupaten_text + '>' + kecamatan_text + '>' + kelurahan_text
            print(region_chained)
            fetch_links_and_go(kelurahan_text)
            total_scraped = 0
            while True:
                no_more_next = 'paginate_button next disabled'
                if ll > 100:
                    next_button = driver.find_element_by_id('listKelurahan_next')
                    next_button.click()
                    time.sleep(1.0)
                tps_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody a')))
                tps_links_text = [a.text for a in tps_links]
                for tps_text in tps_links_text[ll:]:
                    region_chained = province_name + '>' + kabupaten_text + '>' + kecamatan_text + '>' + kelurahan_text + '>' + tps_text
                    print(region_chained)
                    tps_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, tps_text)))
                    tps_link.click()
                    time.sleep(1.0)
                    ## SCRAPE DATA ##
                    # tps_scraped = scrape_table(province_name, kabupaten_text, kecamatan_text, kelurahan_text, tps_text)
                    # total_scraped += tps_scraped
                    driver.back()
                    time.sleep(0.5)
                ll=0
                next_button = driver.find_element_by_id('listKelurahan_next')
                if next_button.get_attribute('class') == no_more_next:
                    break
                else:
                    next_button.click()
                    time.sleep(1.0)
            print(province_name + '>' + kabupaten_text + '>' + kecamatan_text + '>' + kelurahan_text, '\nTotal scraped', total_scraped)
            driver.back()
            time.sleep(0.5)
        driver.back()
        time.sleep(0.5)
        kk=0
    # Go back
    driver.back()
    time.sleep(0.5)
    jj=0



print('Time:', datetime.now())
total_time = (time.time() - start_time) / 60
print('Total time (mins):', total_time)
time.sleep(1)
driver.quit()
exit()
