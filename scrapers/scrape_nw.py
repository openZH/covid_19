#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc

xls_url = 'http://www.nw.ch/coronastatistik'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=3)
for i, row in enumerate(rows):
    print('NW')
    sc.timestamp()
    print('Downloading:', xls_url)
    print('Date and time:', row['A'].date().isoformat())
    print('Confirmed cases:', row['Positiv getestete Personen (kumuliert)'])
    print('Hospitalized:', row['Aktuell hospitalisierte Personen'])
    print('ICU:', row['Davon auf der Intensivstation'])
    print('Deaths:', row['Personen verstorben'])
    # do not print record delimiter for last record
    # this is an indicator for the next script to check
    # for expected values.
    if len(rows) - 1 > i:
        print('-' * 10)
