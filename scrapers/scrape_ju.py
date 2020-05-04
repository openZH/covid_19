#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import scrape_common as sc

print('JU')
d = sc.download('https://www.jura.ch/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html', silent=True)
sc.timestamp()

soup = BeautifulSoup(d, 'html.parser')
box = soup.find('li', class_="ico-xlsx")
xls_url = box.find('a').get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.jura.ch{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
sc.timestamp()

rows = sc.parse_xls(xls, header_row=0)
is_first = True
for i, row in enumerate(rows):
    if not is_first:
        print('-' * 10)
    is_first = False

    print('JU')
    sc.timestamp()
    print('Downloading:', xls_url)
    print('Date and time:', row['Date'].date().isoformat())
    print('Confirmed cases:', row['Cumul des cas confimés'])
    print('Hospitalized:', row['Nb cas actuellement hospitalisés'])
    print('ICU:', row['Nb cas actuellement en SI'])
    print('Deaths:', sum(r['Nombre de nouveaux décès'] for r in rows[:i+1]))
