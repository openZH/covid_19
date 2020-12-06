#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc


def sanitize_row(row):
    # sanitize data:
    # 2020-12-04 contains 'Non communiqué' entries, skip them for now
    if not sc.represents_int(row.get('Nombre de cas actuellement hospitalisés')):
        row['Nombre de cas actuellement hospitalisés'] = ''
    if not sc.represents_int(row.get('Nombre de cas actuellement en soins intensifs')):
        row['Nombre de cas actuellement en soins intensifs'] = ''
    if not sc.represents_int(row.get('Nombre de nouveaux décès')):
        row['Nombre de nouveaux décès'] = ''
    return row


url = 'https://www.jura.ch/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')

is_first = True
data_table = soup.find('caption', string=re.compile(r'Evolution du nombre de cas.*Jura')).find_parent('table')
if data_table:
    headers = [" ".join(cell.stripped_strings) for cell in data_table.find('tr').find_all(['td', 'th'])]
    assert len(headers) == 6, f"Number of headers changed: {len(headers)} != 6"
    rows = []
    for row in data_table.find_all('tr')[1:-1]:
        data = {}
        for col_num, cell in enumerate(row.find_all(['th', 'td'])):
            content = " ".join(cell.stripped_strings).strip()
            if content:
                data[headers[col_num]] = content
        rows.append(data)

    if rows:
        for row in rows[:-1]:
            row = sanitize_row(row)

        for i, row in enumerate(rows[:-1]):
            if not row.get('Date') or row.get('Date') == 'Date':
                continue

            if not is_first:
                print('-' * 10)
            is_first = False

            dd = sc.DayData(canton='JU', url=url)
            current_year = datetime.datetime.now().year
            if row.get('Date') and not re.search(f'{current_year}', row.get('Date')):
                dd.datetime = f"{row.get('Date', '')} {current_year}"
            else:
                dd.datetime = row.get('Date', '')
            dd.datetime = dd.datetime.replace('1 er', '1')

            dd.cases = row.get('Cumul des cas confirmés')
            dd.hospitalized = row.get('Nombre de cas actuellement hospitalisés')
            dd.icu = row.get('Nombre de cas actuellement en soins intensifs')
            dd.deaths = sum(int(str(r.get('Nombre de nouveaux décès', 0)).replace('*', '')) for r in rows[i:] if r.get('Nombre de nouveaux décès'))
            print(dd)
