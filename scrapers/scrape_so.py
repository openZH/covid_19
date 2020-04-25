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

# skip first row
for i, row in enumerate(rows[1:]):
    print('SO')
    sc.timestamp()
    print('Downloading:', url)

    print(f"Date and time: {row['Date']} {row['Time']}")
    print(f"Confirmed cases: {row['Cases']}")
    print(f"Hospitalized: {row['Hospitalized']}")
    print(f"Deaths: {row['Deaths']}")

    if len(rows[1:]) - 1 > i:
        print('-' * 10)
