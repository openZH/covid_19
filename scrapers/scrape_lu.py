#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc


base_url = 'https://www.lustat.ch'
url = f'{base_url}/daten?id=28177'
d = sc.download(url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

xls_url = soup.find('a', href=re.compile(r'.*\.xlsx')).get('href')
if not xls_url.startswith('http'):
    xls_url = f'{base_url}{xls_url}'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=3)
total_cases = 0
total_deaths = 0
is_first = True
for row in rows:
    dd = sc.DayData(canton='LU', url=xls_url)
    dd.datetime = row['Datum']
    dd.cases = sc.int_or_word(row['Neue\xa0Fälle'])
    if dd.cases:
        total_cases += dd.cases
        dd.cases = total_cases
    dd.deaths = sc.int_or_word(row['Verstorbene'])
    if dd.deaths:
        total_deaths += dd.deaths
        dd.deaths = total_deaths
    dd.hospitalized = sc.int_or_word(row['Hospitalisierte'])
    dd.vent = sc.int_or_word(row['Beatmete'])
    dd.isolated = sc.int_or_word(row['In\xa0Isolation'])
    dd.quarantined = sc.int_or_word(row['In\xa0Quarantäne'])
    dd.quarantine_riskareatravel = sc.int_or_word(row['Reiserückkehrer\xa0in\xa0Quarantäne'])
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
