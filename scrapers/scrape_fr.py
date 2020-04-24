#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

print('FR')

d = sc.download('https://www.fr.ch/covid19/sante/covid-19/coronavirus-statistiques-evolution-de-la-situation-dans-le-canton')
sc.timestamp()

soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.fr.ch{xls_url}'

xls = sc.xlsdownload(xls_url)
sc.timestamp()

rows = sc.parse_xls(xls, header_row=0, sheet_name='Données sites internet')
for row in rows:
    print('FR')
    sc.timestamp()
    print('Downloading:', xls_url)
    print('Date and time:', row['Date'].date().isoformat())
    print('Confirmed cases:', row['Total cas avérés'])
    print('Hospitalized:', row['Personnes hospitalisées'])
    print('ICU:', row['dont soins intensifs'])
    print('Deaths:', row['Total décès'])
    print('Recovered:', row['Total Sortis de l\'hôpital'])
    print('-' * 10)
