#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc

print('NE')

xls_url = 'https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Documents/Covid-19-Statistiques/COVID19_PublicationInternet.xlsx'
xls = sc.xlsdownload(xls_url)
sc.timestamp()
rows = sc.parse_xls(xls)
cases = None
if rows:
    last_row = rows[-1]
    print('Date and time:', last_row['A'].date().isoformat())
    cases = last_row['Cumul']
    if cases:
        print('Confirmed cases:', cases)
    print('Hospitalized:', last_row['Total des cas hospitalisés'])
    print('ICU:', int(last_row['Soins intensifs (intubés)']) + int(last_row['Soins intensifs (non intubés)']))
    print('Vent:', last_row['Soins intensifs (intubés)'])
    print('Deaths:', last_row['Cumul des décès'])

if not cases:
    d = sc.pdfdownload('https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Documents/Covid-19-Statistiques/COVID19_PublicationInternet.pdf')
    print('Confirmed cases:', sc.find(r'Au\s*total\s*:\s*(\d+)\s*cas\s*positif', d.replace('\n', '')))