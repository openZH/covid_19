#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import datetime
import scrape_common as sc

# get pdf and xlsx URL from covid19 page of TI
main_url = 'https://www4.ti.ch/dss/dsp/covid19/home/'
d = sc.download(main_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

is_first = True

"""
container = soup.find('h2', string=re.compile(r'Isolamento e quarantena')).find_next('div')
for item in container.find_all('div'):
    divs = item.find_all('div')
    if len(divs) == 3:
        dd = sc.DayData(canton='TI', url=main_url)
        dd.datetime = sc.find(r'.*?(\d+\.\d+\.\d{2})', divs[2].string)
        if sc.find(r'.*(quarantena)', divs[1].string):
            dd.quarantined = divs[0].string
        if sc.find(r'.*(isolamento)', divs[1].string):
            dd.isolated = divs[0].string
        if dd:
            if not is_first:
                print('-' * 10)
            is_first = False
            print(dd)
"""

xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"

if not xls_url.startswith('http'):
    xls_url = f'https://www4.ti.ch/{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='TI', url=xls_url)
    dd.datetime = f"{row['Data'].date().isoformat()}"
    if row.get('Ora'):
        dd.datetime += f"T{row['Ora'].time().isoformat()}"
    dd.cases = row['Totale casi confermati']
    dd.hospitalized = row['Totale giornaliero pazienti ricoverati']
    dd.icu = row['Totale giornaliero pazienti cure intense']
    dd.vent = row['Totale giornaliero pazienti ventilati']
    dd.recovered = row['Totale pazienti dimessi da ospedali']
    dd.deaths = row['Totale decessi']
    print(dd)
