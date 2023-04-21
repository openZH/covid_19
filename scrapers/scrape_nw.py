#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_nw_common as snc

is_first = True
xls_url = 'http://www.nw.ch/coronastatistik'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=2)
for row in rows:
    dd = sc.DayData(canton='NW', url=xls_url)
    dd.datetime = row['A'].date().isoformat()
    dd.cases = row['Positiv getestete Personen (kumuliert)']
    dd.icu = row['Davon auf der Intensivstation']

    try:
        dd.hospitalized = row['Aktuell hospitalisierte Personen']
    except KeyError:
        dd.hospitalized = row['Hospitalisierte Personen']

    try:
        dd.deaths = row['Personen verstorben']
    except KeyError:
        dd.deaths = row['Verstorbene Personen']

    # skip empty rows
    if dd.cases is None and dd.icu is None and dd.hospitalized is None and dd.deaths is None:
        continue

    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd)
