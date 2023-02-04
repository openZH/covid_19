#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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

dd = sc.DayData(canton='GE', url=url)

# get data from front page
dd.datetime = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.ID,"datedump").text)
dd.datetime = sc.find(r'(\d{4}-\d{2}-\d{2}\s+\d+:\d+:\d+)', dd.datetime)

elem = driver.find_element(By.ID, 'keyvalue_ns-cas_cum_pub')
elem = elem.find_element(By.TAG_NAME, 'h3')
dd.cases = elem.text

elem = driver.find_element(By.ID, 'keyvalue_ns-deces_cum_pub')
elem = elem.find_element(By.TAG_NAME, 'h3')
dd.deaths = elem.text
if dd:
    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd)


elem = driver.find_element(By.LINK_TEXT, 'Tables')
elem.click()

# get hospitalized xls
elem = driver.find_element(By.LINK_TEXT, 'Hospitalisations')
elem.click()
elem = driver.find_elements(By.ID, 'dropdown_download_table')
elem = elem[-1]
elem.click()
xls_url = sgc.get_link_from_element(driver, 'download_table_hospit_xlsx')
assert xls_url, "Couldn't find XLS url"

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    date = row['Date']
    if date < datetime.datetime(2020, 1, 1):
        # skip entries from before 2020
        continue

    dd = sc.DayData(canton='GE', url=url)
    dd.datetime = date.isoformat()
    current_hosp = row['Patients hospitalisés COVID-19 actifs HUG']
    if sc.represents_int(current_hosp) and int(current_hosp) >= 0:
        dd.hospitalized = current_hosp
    dd.icu = row['Patients COVID-19 hospitalisés aux soins intensifs']
    dd.icf = row['Patients COVID-19 hospitalisés aux soins intermédiaires']

    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)


# get cases xls
"""
elem = driver.find_element(By.LINK_TEXT, 'Cas')
elem.click()
elem = driver.find_elements(By.ID, 'dropdown_download_table')
elem = elem[0]
elem.click()
xls_url = sgc.get_link_from_element(driver, 'download_table_cas_deces_xlsx')
assert xls_url, "Couldn't find XLS url"

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    date = row['Date']
    if date < datetime.datetime(2020, 1, 1):
        # skip entries from before 2020
        continue

    dd = sc.DayData(canton='GE', url=url)
    dd.datetime = date.isoformat()
    dd.cases = row['Cumul cas COVID-19 (GE)']
    # death values seem to be sorted in the wrong order
    # dd.deaths = row['Cumul décès COVID-19 ']
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
"""
