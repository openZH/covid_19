#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

print('JU')
d = sc.download('https://www.jura.ch/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html')
sc.timestamp()

soup = BeautifulSoup(d, 'html.parser')
box = soup.find('li', class_="ico-xlsx")
xls_url = box.find('a').get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.jura.ch{xls_url}'

xls = sc.xlsdownload(xls_url)
sc.timestamp()

rows = sc.parse_xls(xls, header_row=0)
if rows:
    last_row = rows[-1]
    print('Date and time:', last_row['Date'].date().isoformat())
    print('Confirmed cases:', last_row['Cumul des cas confimés'])
    print('Hospitalized:', last_row['Nb cas actuellement hospitalisés'])
    print('ICU:', last_row['Nb cas actuellement en SI'])
    print('Deaths:', sum(r['Nombre de nouveaux décès'] for r in rows))
