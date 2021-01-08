#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import scrape_common as sc
import scrape_ge_common as sgc

is_first = True

# parse tested from PDF
pdf_url = sgc.get_latest_ge_weekly_pdf_url()
pdf = sc.pdfdownload(pdf_url, silent=True)

week_number = sc.find(r'Situation semaine (\d+)', pdf)
if week_number:
    week_end_date = datetime.datetime.strptime('2021-W' + week_number + '-7', '%G-W%V-%u').date()
    number_of_tests = sc.find(r'Au total, (\d+\'\d+) tests PCR ont', pdf)

    if number_of_tests is not None:
        number_of_tests = number_of_tests.replace('\'', '')

        dd_test = sc.DayData(canton='GE', url=pdf_url)
        dd_test.datetime = week_end_date.isoformat()
        dd_test.tested = number_of_tests
        print(dd_test)
        is_first = False


# get hospitalized number
hosp_url = 'https://www.hug.ch/coronavirus-maladie-covid-19/situation-aux-hug'
d = sc.download(hosp_url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')
content = soup.find(string=re.compile("Evolution du nombre de malades.*")).find_previous('p').text

dd_hosp = sc.DayData(canton='GE', url=hosp_url)
hosp_date = sc.find(r'^Au (\d+\s*(:?\w+)?\s+\w+)\s+à\s+\d+h', content, flags=re.I|re.UNICODE)
dd_hosp.datetime = f'{hosp_date} 2021'
dd_hosp.hospitalized = sc.find(r'(\d+) malades Covid actif', content)
dd_hosp.icu = sc.find(r'(\d+) aux soins intensifs', content)
dd_hosp.icf = sc.find(r'(\d+) aux soins intermédiaires', content)
if dd_hosp:
    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd_hosp)


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

url = 'https://infocovid.smc.unige.ch/'
driver.get(url)
elem = driver.find_element_by_link_text('Tables')
elem.click()

# get quarantine xls
elem = driver.find_element_by_partial_link_text('cas et quarantaines')
elem.click()
# needs delay, that the link is present
time.sleep(1)
elem = driver.find_element_by_id('download_table_cas')
quarantine_xls_url = elem.get_attribute('href')

xls = sc.xlsdownload(quarantine_xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    dd = sc.DayData(canton='GE', url=url)
    dd.datetime = row['date']
    dd.isolated = row['isolement déjà en cours']
    dd.quarantined = row['Quarantaines en cours suite\nà un contact étroit']
    dd.quarantine_riskareatravel = row['Quarantaines en cours au retour de zone à risque']

    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)


# get cases xls
elem = driver.find_element_by_partial_link_text('Indicateurs principaux')
elem.click()
# needs delay, that the link is present
time.sleep(1)
elem = driver.find_element_by_id('download_table_incidence')
case_xls_url = elem.get_attribute('href')

xls = sc.xlsdownload(case_xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    dd = sc.DayData(canton='GE', url=url)
    dd.datetime = row['Date']
    dd.cases = row['Cumul cas COVID-19']
    dd.hospitalized = row['Total hospitalisations COVID-19 actifs (en cours) canton (HUG-cliniques)']
    dd.icu = row['Patients COVID-19 actifs aux soins intensifs HUG']
    dd.icf = row['Patients COVID-19 actifs aux soins intermédiaires HUG']
    dd.deaths = row['Cumul décès COVID-19 ']
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
