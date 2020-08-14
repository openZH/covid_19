#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc

xls_url = 'http://www.nw.ch/coronastatistik'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=3)
is_first = True
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False

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
    print(dd)
