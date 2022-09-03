#!/usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc


base_url = 'https://www.ow.ch'
url = f'{base_url}/de/verwaltung/dienstleistungen/?dienst_id=5962'
"""
d = sc.download(url, silent=True, encoding='windows-1252')
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')

dd = sc.DayData(canton='OW', url=url)
date = sc.find(r'Stand (\d+\.\s+\w+\s+20\d{2})', d)
time = sc.find(r'Stand .*,\s?([\d\.:]+).*Uhr', d)
dd.datetime = f'{date}, {time} Uhr'
dd.isolated = soup.find(text=re.compile(r'In Isolation \(aktuell\)')).find_next('td').string
dd.quarantined = soup.find(text=re.compile(r'In Quarant.ne \(aktuell\)')).find_next('td').string
dd.quarantine_riskareatravel = soup.find(text=re.compile(r'Reiser.ckkehrer in Quarant.ne')).find_next('td').string

is_first = True
if dd:
    print(dd)
    is_first = False
"""

is_first = True


d = sc.download(f'{base_url}/de/kanton/publired/publikationen/?action=info&pubid=20318',
                encoding='windows-1252', silent=True)
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find('a', string=re.compile("Download")).get('href')
assert xls_url, "URL is empty"
xls_url = f'{base_url}{xls_url}'

for row in soup.find_all('dl'):
    cells = row.find_all('dd')
    if cells[0].string:
        file_date = cells[0].string

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=4)
for row in rows:
    if isinstance(row['A'], datetime.datetime):
        dd = sc.DayData(canton='OW', url=url)
        dd.datetime = row['A']
        data_found = False
        if isinstance(row['Infizierte Personen (kumuliert)'], int) and row['Infizierte Personen (kumuliert)'] > 0:
            dd.cases = row['Infizierte Personen (kumuliert)']
            data_found = True
        hosp_key = """Hospitalisierte Personen im KSOW /
Eintritte Covid-Station; Alle Einwohner OW alle Spitäler CH***"""
        if isinstance(row[hosp_key], int):
            dd.hospitalized = row[hosp_key]
        if isinstance(row['Gestorbene Personen (kumuliert)'], int):
            dd.deaths = row['Gestorbene Personen (kumuliert)']
        if isinstance(row['Isolation'], int):
            dd.isolated = row['Isolation']
        if isinstance(row['Quarantäne'], int):
            dd.quarantined = row['Quarantäne']
        if isinstance(row['Quarantäne Reiserückkehrer'], int):
            dd.quarantine_riskareatravel = row['Quarantäne Reiserückkehrer']
        if data_found:
            if not is_first:
                print('-' * 10)
            else:
                is_first = False
            print(dd)
