#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = "https://corona.so.ch/index.php?id=27979"
d = sc.download(url, silent=True)

soup = BeautifulSoup(d, 'html.parser')
data_table = soup.find('h2', text=re.compile("Situation Kanton Solothurn")).find_next("table")
headers = [cell.string for cell in data_table.find('tr').find_all('th')]
rows = []
for row in data_table.find_all('tr'):
    data = {}
    col_num = 0
    for cell in row.find_all(['td']):
        if headers[col_num] == 'Datum':
            data['Date'] = cell.string
        elif headers[col_num] == 'Zeit':
            data['Time'] = cell.string
        elif headers[col_num] == 'Bestätigte Fälle (kumuliert)':
            data['Cases'] = cell.string
        elif headers[col_num] == 'Todesfälle (kumuliert)':
            data['Deaths'] = cell.string
        elif headers[col_num] == 'Im Kanton Hospitalisierte Personen':
            data['Hospitalized'] = cell.string
        col_num += 1
    if data:
        rows.append(data)

is_first = True
# skip first row
for row in rows[1:]:
    if not is_first:
        print('-' * 10)
    is_first = False

    print('SO')
    sc.timestamp()
    print('Downloading:', url)

    print(f"Date and time: {row['Date']} {row['Time']}")
    print(f"Confirmed cases: {row['Cases']}")
    print(f"Hospitalized: {row['Hospitalized']}")
    print(f"Deaths: {row['Deaths']}")
