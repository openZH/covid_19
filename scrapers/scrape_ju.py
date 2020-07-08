#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.jura.ch/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html', silent=True)

soup = BeautifulSoup(d, 'html.parser')
box = soup.find('li', class_="ico-xlsx")
xls_url = box.find('a').get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.jura.ch{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)

rows = sc.parse_xls(xls, header_row=0)
is_first = True
for i, row in enumerate(rows):
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='JU', url=xls_url)
    dd.datetime = row['Date'].date().isoformat()
    dd.cases = row['Cumul des cas confimés']
    dd.hospitalized = row.get('Nb cas actuellement hospitalisés')
    dd.icu = row.get('Nb cas actuellement en SI')
    dd.deaths = sum(r['Nombre de nouveaux décès'] for r in rows[:i+1])
    print(dd)
