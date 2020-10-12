#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.jura.ch/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')

soup = BeautifulSoup(d, 'html.parser')
is_first = True
box = soup.find(class_="ico-xlsx")
if box:
    xls_url = box.find('a').get('href')
    assert xls_url, "URL is empty"
    if not xls_url.startswith('http'):
        xls_url = f'https://www.jura.ch{xls_url}'

    xls = sc.xlsdownload(xls_url, silent=True)

    rows = sc.parse_xls(xls, header_row=0)
    for i, row in enumerate(rows):
        if not isinstance(row['Date'], datetime.datetime):
            continue

        if not is_first:
            print('-' * 10)
        is_first = False

        dd = sc.DayData(canton='JU', url=xls_url)
        dd.datetime = row['Date'].date().isoformat()
        dd.cases = row['Cumul des cas confimés']
        dd.hospitalized = row.get('Nb cas actuellement hospitalisés')
        dd.icu = row.get('Nb cas actuellement en SI')
        if sc.represents_int(row.get('Nombre de nouveaux décès')):
            dd.deaths = sum(r['Nombre de nouveaux décès'] for r in rows[:i+1])
        print(dd)

data_table = soup.find('caption', string=re.compile(r'Evolution du nombre de cas.*Jura')).find_parent('table')
if data_table:
    headers = [" ".join(cell.stripped_strings) for cell in data_table.find('tr').find_all(['td', 'th'])]
    assert len(headers) == 5, f"Number of headers changed: {len(headers)} != 5"
    rows = []
    for row in data_table.find_all('tr'):
        data = {}
        for col_num, cell in enumerate(row.find_all(['th', 'td'])):
            if cell.string:
                data[headers[col_num]] = cell.string.strip()
        rows.append(data)

    if rows:
        for i, row in enumerate(rows[1:]):
            if not is_first:
                print('-' * 10)
            is_first = False

            if not row.get('Date'):
                continue

            dd = sc.DayData(canton='JU', url=url)
            current_year = datetime.datetime.now().year
            if row.get('Date') and not re.match(f'{current_year}', row.get('Date')):
                dd.datetime = f"{row.get('Date')} {current_year}"
            else:
                dd.datetime = row.get('Date')
            dd.cases = row.get('Cumul des cas confirmés')
            dd.hospitalized = row.get('Nombre de cas actuellement hospitalisés')
            dd.icu = row.get('Nombre de cas actuellement en soins intensifs')
            dd.deaths = sum(int(r.get('Nombre de nouveaux décès', 0)) for r in rows[:i+1] if r.get('Nombre de nouveaux décès'))
            print(dd)
