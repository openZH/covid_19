#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime
import sys
from bs4 import BeautifulSoup
import scrape_common as sc
d = sc.download('https://www.ge.ch/document/covid-19-situation-epidemiologique-geneve', silent=True)

soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(title=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.ge.ch{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0, skip_rows=2)
is_first = True
for i, row in enumerate(rows):
    if not isinstance(row['Date'], datetime.datetime):
        print(f"WARNING: {row['Date']} is not a valid date, skipping.", file=sys.stderr)
        continue

    if row['Nombre cas COVID-19'] is None:
        print(f"WARNING: 'Nombre cas COVID-19' is empty on {row['Date']}, skipping.", file=sys.stderr)
        continue

    if not is_first:
        print('-' * 10)
    is_first = False
    
    # TODO: remove when source is fixed
    # handle wrong value on 2020-04-09, see issue #819
    if row['Date'].date().isoformat() == '2020-04-09':
        row['Cumul COVID-19 sorties d\'hospitalisation'] = ''

    dd = sc.DayData(canton='GE', url=xls_url)
    dd.datetime = row['Date'].date().isoformat()
    dd.cases = row['Cumul cas COVID-19']
    dd.hospitalized = row['Total hospitalisations COVID-19 actifs ']
    dd.icu = row['Patients COVID-19 aux soins intensifs total']
    dd.icf = row['Patients COVID-19 aux soins intermédiaires']
    dd.vent = row['Patients COVID-19 aux soins intensifs intubés']
    dd.deaths = row['Cumul décès COVID-19 ']

    # Since 01.07.2020 new_hosp and recovered are no longer provided
    #dd.new_hosp = row['Nb nouveaux patients COVID-19 hospitalisés']
    #dd.recovered = row['Cumul COVID-19 sorties d\'hospitalisation']

    # TODO: check if Nombre tests is added again
    # on 2020-06-09 GE removed the `Nombre tests` column
    #dd.tested = sum(r['Nombre tests'] for r in rows[:i+1])
    print(dd)
