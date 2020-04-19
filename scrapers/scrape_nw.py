#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc

print('NW')
xls = sc.xlsdownload('http://www.nw.ch/coronastatistik')
sc.timestamp()

rows = sc.parse_xls(xls, header_row=3)
if rows:
    last_row = rows[-1]
    print('Date and time:', last_row['A'].date().isoformat())
    print('Confirmed cases:', last_row['Positiv getestete Personen (kumuliert)'])
    print('Hospitalized:', last_row['Aktuell hospitalisierte Personen'])
    print('ICU:', last_row['Davon auf der Intensivstation'])
    print('Deaths:', last_row['Personen verstorben'])
