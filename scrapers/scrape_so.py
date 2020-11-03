#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

base_url = 'https://corona.so.ch'
url = f'{base_url}/bevoelkerung/daten/woechentlicher-situationsbericht/'
d = sc.download(url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
pdf_url = soup.find(href=re.compile(r'\.pdf$')).get('href')
pdf_url = f'{base_url}{pdf_url}'

content = sc.pdfdownload(pdf_url, layout=True, silent=True)

"""
Hospitalisationen im Kanton  Anzahl Personen in Isolation  davon Kontakte in Quarantäne  Anzahl zusätzlicher Personen in Quarantäne nach Rückkehr aus Risikoland  Re- Wert***
6 (6)                        120 (71)                      280 (189)                     388 (280)                                                                1.46 (1.1)
"""

rows = []

date = sc.find(r'S\s?tand: (\d+\.\d+\.20\d{2})', content)
number_of_tests = sc.find(r'PCR-Tes\s?ts\sTotal\s+(\d+\'?\d+)\s', content).replace('\'', '')
res = re.search(r'Hospitalisationen im Kanton.*\d+ \(\d+\)\s+(\d+) \(\d+\)\s+(\d+) \(\d+\)\s+(\d+) \(\d+\)\s+\d\.\d+ \(\d\.\d+\)', content, re.DOTALL)
if res is not None:
    data = sc.DayData(canton='SO', url=pdf_url)
    data.datetime = date
    data.tested = number_of_tests
    data.isolated = res[1]
    data.quarantined = res[2]
    data.quarantine_riskareatravel = res[3]
    rows.append(data)


url = f"{base_url}/index.php?id=27979"
d = sc.download(url, silent=True)
d = d.replace("&nbsp;", " ")

soup = BeautifulSoup(d, 'html.parser')
data_table = soup.find('h2', text=re.compile("Situation Kanton Solothurn")).find_next("table")
# not updated anymore after 2020-10-30
if data_table and False:
    headers = [cell.string for cell in data_table.find('tr').find_all('th')]
    for row in data_table.find_all('tr'):
        data = sc.DayData(canton='SO', url=url)
        col_num = 0
        tmp_date = None
        tmp_time = None
        for cell in row.find_all(['td']):
            if headers[col_num] == 'Datum':
                tmp_date = cell.string.strip()
            elif headers[col_num] == 'Zeit':
                tmp_time = cell.string.strip()
            elif headers[col_num] == 'Bestätigte Fälle (kumuliert)':
                data.cases = cell.string.strip()
            elif headers[col_num] == 'Todesfälle (kumuliert)':
                data.deaths = cell.string.strip()
            elif headers[col_num] == 'Im Kanton Hospitalisierte Personen':
                data.hospitalized = cell.string.strip()
            col_num += 1
        if data and tmp_date and tmp_time and not tmp_date.startswith('bis '):
            data.datetime = f"{tmp_date} {tmp_time}".strip()
            rows.append(data)
else:
    # if the table is not there (it vanished on 2020-05-20) fallback to main page
    url = "https://corona.so.ch/"
    d = sc.download(url, silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    title = soup.find('h3', text=re.compile("Situation Kanton Solothurn"))
    data_list = title.find_parent("div").find_all('li')
    date_str = sc.find('Stand\s*(.+)\s*Uhr', title.string)
    data = sc.DayData(canton='SO', url=url)
    for item in data_list:
        content = "".join([str(s) for s in item.contents])
        if not item:
            continue
        value = sc.find(r'.*:.*?(\d+)\s*.*', content).strip()
        if 'Laborbestätigte Infektionen (kumuliert)' in content:
            data.cases = value
            continue
        if 'Verstorbene Personen' in content:
            data.deaths = value
            continue
        if 'hospitalisierte Personen' in content and not 'weniger als' in content:
            data.hospitalized = value
            continue
        if 'Davon befinden sich auf intensivmedizinischen Abteilungen' in content and not 'weniger als' in content:
            data.icu = value
            continue
    rows.append(data)


is_first = True
# skip first row
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False
    print(row)

