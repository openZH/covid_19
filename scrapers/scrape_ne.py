#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc

xls_url = 'https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Documents/Covid-19-Statistiques/COVID19_PublicationInternet.xlsx'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls)
for i, row in enumerate(rows):
    print('NE')
    sc.timestamp()
    print('Downloading:', xls_url)
    print('Date and time:', row['A'].date().isoformat())
    print('Confirmed cases:', row['Cumul'])
    print('Hospitalized:', row['Total des cas hospitalisés'])
    if row['Soins intensifs (intubés)'] and row['Soins intensifs (non intubés)']:
        print('ICU:', int(row['Soins intensifs (intubés)']) + int(row['Soins intensifs (non intubés)']))
    print('Vent:', row['Soins intensifs (intubés)'])
    print('Deaths:', row['Cumul des décès'])
    # do not print record delimiter for last record
    # this is an indicator for the next script to check
    # for expected values.
    if len(rows) - 1 > i:
        print('-' * 10)
