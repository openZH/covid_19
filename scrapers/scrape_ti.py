#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import scrape_common as sc

# get xlsx URL from covid19 page of TI
main_url = 'https://www4.ti.ch/dss/dsp/covid19/home/'
d = sc.download(main_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"

if not xls_url.startswith('http'):
    xls_url = f'https://www4.ti.ch/{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
is_first = True
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='TI', url=xls_url)
    dd.datetime = f"{row['Data'].date().isoformat()}"
    if row['Ora']:
        dd.datetime += f"T{row['Ora'].time().isoformat()}"
    dd.cases = row['Totale casi confermati']
    dd.hospitalized = row['Pazienti ricoverati attualmente']
    dd.icu = row['Pazienti in cure intense']
    dd.vent = row['Pazienti ventilati']
    dd.recovered = row['Totale pazienti dimessi da ospedali']
    dd.deaths = row['Totale decessi']
    print(dd)
