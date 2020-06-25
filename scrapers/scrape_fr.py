#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime
import sys
from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.fr.ch/sante/covid-19/coronavirus-statistiques-evolution-de-la-situation-dans-le-canton', silent=True)

soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.fr.ch{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0, sheet_name='Données sites internet')
is_first = True
for row in rows:
    if row['Date'] is None:
        continue
    if not isinstance(row['Date'], datetime.datetime):
        print(f"WARNING: {row['Date']} is not a valid date, skipping.", file=sys.stderr)
        continue

    if not is_first:
        print('-' * 10)
    is_first = False

    print('FR')
    sc.timestamp()
    print('Downloading:', xls_url)
    print('Date and time:', row['Date'].date().isoformat())
    print('Confirmed cases:', row['Total cas avérés'])
    print('Hospitalized:', row['Personnes hospitalisées'])
    print('ICU:', row['dont soins intensifs'])
    print('Deaths:', row['Total décès'])
    print('Recovered:', row['Total Sortis de l\'hôpital'])
